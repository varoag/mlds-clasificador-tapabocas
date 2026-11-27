# Arquitectura y modelo de datos

Este documento describe la arquitectura actual del proyecto clasificador de tapabocas y el modelo lógico de los datos usados por el proceso de adquisición e inventario.

## Diagrama de arquitectura

El flujo implementado descarga una revisión fija del conjunto Face-Mask-Detection, conserva una copia local en formato Parquet y genera un inventario tabular en CSV.

```mermaid
flowchart LR
    HF["Hugging Face Dataset<br/>Face-Mask-Detection"]
    ACQ["scripts/data_acquisition/main.py"]
    DB["tapabocas/database/acquisition.py"]
    RAW[("data/raw/train.parquet")]
    INTERIM[("data/interim/inventory.csv")]
    PIL["Pillow"]
    PYARROW["PyArrow"]

    HF -->|"Descarga HTTPS de la revisión fija"| DB
    ACQ -->|"Invoca acquire() e inventory()"| DB
    DB -->|"Verifica SHA-256"| RAW
    DB -->|"Lee batches y metadatos"| PYARROW
    PYARROW -->|"Entrega imágenes y etiquetas"| DB
    DB -->|"Extrae dimensiones y hash"| PIL
    PIL -->|"Devuelve propiedades de la imagen"| DB
    DB -->|"Genera el inventario"| INTERIM

    subgraph "Capas previstas"
        PRE["src/tapabocas/preprocessing"]
        MODEL["src/tapabocas/models"]
        TRAIN["src/tapabocas/training"]
        EVAL["src/tapabocas/evaluation"]
        VIS["src/tapabocas/visualization"]
    end

    INTERIM -.-> PRE
    PRE -.-> TRAIN
    TRAIN -.-> MODEL
    MODEL -.-> EVAL
    EVAL -.-> VIS
```

### Responsabilidades

- **Fuente externa:** aloja el archivo Parquet de la revisión documentada.
- **Script de adquisición:** establece la raíz del proyecto y coordina descarga e inventario.
- **Módulo de adquisición:** valida la revisión y el SHA-256, verifica las clases y transforma cada registro del conjunto en una fila del inventario.
- **Almacenamiento local:** separa el archivo fuente original en `data/raw` y el resumen procesado en `data/interim`.
- **Preprocesamiento, entrenamiento y evaluación:** cuentan con módulos previstos en `src/tapabocas`; su integración debe partir del inventario generado.

## Diagrama de entidad relacion

El modelo representa conceptualmente el conjunto adquirido y el contenido de `inventory.csv`. La entidad `Dataset` corresponde a una revisión fija, `InventoryRow` corresponde a cada fila del CSV y `Image` identifica imágenes por su SHA-256.

```mermaid
erDiagram
    DATASET ||--o{ IMAGE_DATA : contiene
    CLASS_DATA ||--o{ INVENTORY_ROW : clasifica
    IMAGE_DATA ||--o{ INVENTORY_ROW : representa
    DATASET ||--o{ INVENTORY_ROW : registra

    DATASET {
        string revision PK "Commit de la revisión en Hugging Face"
        string sha256 UK "Hash del archivo Parquet"
        string format "Formato de origen"
        int row_count "Cantidad esperada de filas"
    }

    INVENTORY_ROW {
        int row_id PK "Identificador consecutivo"
        string image_path "Ruta original dentro del dataset"
        int label FK "Código 0 o 1"
        string class_name "Nombre de la clase"
        string image_sha256 FK "Hash SHA-256 del contenido"
        int width_px "Ancho en píxeles"
        int height_px "Alto en píxeles"
        string mode "Modo de color de Pillow"
    }

    IMAGE_DATA {
        string image_sha256 PK "SHA-256 del contenido"
        string image_path "Ruta reportada en el registro"
        int width_px "Ancho en píxeles"
        int height_px "Alto en píxeles"
        string mode "Modo de color de Pillow"
    }

    CLASS_DATA {
        int label PK "Código 0 o 1"
        string class_name UK "WithMask o WithoutMask"
    }
```

### Reglas del modelo

- El conjunto tiene exactamente 11.792 filas para la revisión configurada.
- `WithMask` corresponde a la etiqueta `0`; `WithoutMask` corresponde a la etiqueta `1`.
- `row_id` identifica cada observación del inventario y comienza en cero.
- `image_sha256` permite detectar imágenes repetidas.
- Una imagen puede aparecer en varias filas si el conjunto contiene duplicados; un conjunto de hashes conflictivos indica que una misma imagen tiene etiquetas distintas.
- El modelo no almacena los bytes de la imagen en una base de datos relacional: estos permanecen dentro de `data/raw/train.parquet`.

## Diagrama UML del proyecto

La siguiente vista UML representa los módulos actuales y los módulos previstos por la estructura del paquete `tapabocas`.

```mermaid
classDiagram
    direction LR

    class data_acquisition_main {
        <<script>>
        +main() void
    }

    class acquisition {
        <<module>>
        +REVISION string
        +URL string
        +SHA256 string
        +CLASSES list
        +FIELDS list
        +checksum(path) string
        +acquire(root) Path
        +inventory(raw, output) dict
    }

    class preprocessing {
        <<package>>
    }

    class training {
        <<package>>
    }

    class models {
        <<package>>
    }

    class evaluation {
        <<package>>
    }

    class visualization {
        <<package>>
    }

    class train_parquet {
        <<artifact>>
        +train.parquet
    }

    class inventory_csv {
        <<artifact>>
        +inventory.csv
    }

    data_acquisition_main ..> acquisition : usa
    acquisition ..> train_parquet : lee o crea
    acquisition ..> inventory_csv : genera
    inventory_csv ..> preprocessing : alimenta
    preprocessing ..> training : entrega datos preparados
    training ..> models : produce
    models ..> evaluation : es evaluado por
    evaluation ..> visualization : registra resultados para
```
