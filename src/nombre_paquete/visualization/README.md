# Capa de despliegue: visualización

Este paquete documenta la capa de despliegue del clasificador de tapabocas: un servicio web pequeño formado por un frontend y un backend que se comunicará con el desarrollo de machine learning del proyecto.

> Estado: esta carpeta contiene documentación base, no código de la aplicación. Los módulos Python siguen vacíos.

## Propósito

- **Frontend:** permitir cargar una fotografía individual, mostrar el resultado y dejar que el revisor lo corrija.
- **Backend:** recibir la imagen, validarla, invocar la capa de ML y devolver el resultado.
- **ML (fuera de esta carpeta):** preprocesamiento, modelo y entrenamiento en `src/nombre_paquete/preprocessing`, `src/nombre_paquete/models` y `src/nombre_paquete/training`, aún por implementar.

El plan completo del servicio está en `docs/deployment/deploymentdoc.md`.

## Contrato de comunicación previsto

| Elemento | Definición prevista |
| --- | --- |
| Entrada | Una imagen individual con un rostro principal visible, enviada desde el frontend al backend. |
| Salida | Clase estimada («con tapabocas» / «sin tapabocas») y valor de confianza, más un identificador de la solicitud para trazabilidad. |
| Errores | Imagen inválida, ausencia de rostro detectable y fallo del modelo; cada caso debe devolver un mensaje legible para el revisor. |
| Corrección | El revisor puede cambiar la clase estimada; la corrección se registra sin alterar la predicción original. |

El contrato es una propuesta: se formalizará cuando se implementen las capas.

## Organización de la documentación

- `README.md`: este índice y el contrato común.
- `frontend.md`: responsabilidades, flujo de pantalla y criterios de la interfaz.
- `backend.md`: responsabilidades, contrato de la API y relación con el módulo de ML.

## Flujo de trabajo previsto

1. Mantener este contrato y el documento de despliegue sincronizados.
2. Definir los formatos concretos de entrada y salida antes de escribir código.
3. Implementar primero el backend contra una predicción simulada y luego conectar el modelo real.
4. Implementar el frontend consumiendo el contrato acordado.
5. Probar el recorrido completo: cargar imagen → predecir → mostrar → corregir.
6. Actualizar esta documentación con las decisiones tomadas.

## Checklist de la capa de despliegue

- [ ] Contrato de entrada/salida acordado.
- [ ] Manejo de errores definido.
- [ ] Variables de entorno documentadas.
- [ ] Backend implementado y probado.
- [ ] Frontend implementado y probado.
- [ ] Integración con el modelo verificada.
- [ ] Documentación de despliegue actualizada con la implementación real.
