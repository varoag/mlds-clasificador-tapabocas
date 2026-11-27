# Frontend de la capa de despliegue (diseño previsto)

> Estado: documento de diseño. Todavía no hay interfaz implementada en esta rama.

## Responsabilidades

- Cargar una fotografía individual desde el navegador.
- Enviarla al backend respetando el contrato descrito en `README.md`.
- Mostrar la clase estimada y su confianza de manera comprensible para un revisor.
- Permitir corregir la clase estimada y registrar la corrección.
- Informar errores de carga, imagen inválida o fallo del servicio sin revelar detalles técnicos al usuario.
- Evitar entradas fuera del protocolo: fotos grupales, ambiguas o sin rostro principal.

## Flujo de pantalla previsto

1. Selección de una imagen.
2. Estado de envío / espera de la predicción.
3. Resultado: clase, confianza e identificador de la solicitud.
4. Acción del revisor: aceptar o corregir la clase.
5. Confirmación del registro de la corrección.

## Convenciones previstas

- Una sola imagen por solicitud; la unidad de decisión es la fotografía.
- Las etiquetas visibles son «con tapabocas» y «sin tapabocas», sin exponer códigos internos del modelo.
- La interfaz no decide la clase: solo presenta el resultado del backend y recoge la corrección humana.
- La tecnología concreta y la organización de archivos se definirán al implementar; este documento no fija un framework.

## Criterios de revisión

- [ ] La carga de la imagen es sencilla y funciona desde el navegador.
- [ ] El resultado y la confianza se muestran con claridad.
- [ ] La corrección humana es posible y queda registrada.
- [ ] Los estados de error son comprensibles.
- [ ] No se muestran códigos internos ni detalles de implementación.

## Pendientes

- Definir el formato exacto de envío de la imagen.
- Definir el diseño visual y los textos de error.
- Probar la interfaz con el backend y, posteriormente, con el modelo real.
