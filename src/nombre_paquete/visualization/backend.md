# Backend de la capa de despliegue (diseño previsto)

> Estado: documento de diseño. Todavía no hay API ni servidor implementado en esta rama.

## Responsabilidades

- Exponer un punto de entrada para recibir una imagen desde el frontend.
- Validar el tipo, el tamaño y el contenido básico de la imagen antes de invocar al modelo.
- Llamar a la capa de machine learning prevista en `src/nombre_paquete/preprocessing` y `src/nombre_paquete/models`.
- Devolver la clase estimada, la confianza y un identificador de solicitud.
- Registrar la corrección del revisor sin sobrescribir la predicción original.
- Registrar logs de solicitudes, errores y latencia, sin almacenar las imágenes.

## Contrato previsto

| Elemento | Definición prevista |
| --- | --- |
| Solicitud | Imagen individual enviada por el frontend. |
| Respuesta | Clase «con tapabocas» / «sin tapabocas», confianza e identificador de solicitud. |
| Errores | Imagen inválida, imagen sin rostro detectable, modelo no disponible; respuesta con mensaje legible y código que el frontend pueda interpretar. |
| Corrección | Registro explícito de la clase elegida por el revisor, conservando la predicción original. |

El contrato es una propuesta; la ruta, el formato y el esquema exactos se definirán junto con la implementación del servicio.

## Variables de entorno previstas

- `APP_HOST`: interfaz de escucha del servicio.
- `APP_PORT`: puerto de escucha del servicio.
- `MODEL_PATH`: ruta al artefacto del modelo entrenado.

No tienen valores asignados en esta rama.

## Relación con machine learning

- El backend no entrena ni reentrena modelos: solo consume la capa de predicción.
- `preprocessing` preparará la imagen en el formato que el modelo requiera.
- `models` cargará el artefacto indicado por `MODEL_PATH` y producirá la clase y la confianza.
- Si el artefacto no existe o no es compatible, el backend debe responder con un error controlado en lugar de fallar sin respuesta.

## Criterios de revisión

- [ ] La validación de entrada está definida.
- [ ] La respuesta incluye clase, confianza e identificador de solicitud.
- [ ] Los errores están documentados y son manejables desde el frontend.
- [ ] La corrección humana se registra sin alterar la predicción.
- [ ] Los logs no contienen imágenes ni datos personales.

## Pendientes

- Definir ruta y esquema concretos de la API.
- Definir el formato de imagen que aceptará el servicio.
- Conectar primero con una predicción simulada y después con el modelo real.
