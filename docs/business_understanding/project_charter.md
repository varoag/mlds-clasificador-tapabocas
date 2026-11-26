# Marco del proyecto · Clasificación de fotografías según el uso visible de tapabocas

## Nombre del proyecto
Clasificador de imágenes con y sin tapabocas. Proyecto aplicado del curso Metodologías Ágiles para el Desarrollo de Proyectos de Machine Learning.

## Objetivo del proyecto
Un equipo que revisa un lote de fotografías debe abrirlas una por una para distinguir aquellas en las que aparece una persona sin tapabocas. Proponemos un prototipo que priorice esas fotografías para revisión humana. El escenario de uso es académico y la reducción de tiempo es una hipótesis que se evaluará en una prueba con usuarios.

La unidad de decisión es una fotografía con un rostro principal visible. Dada esa entrada, el prototipo estimará la clase «con tapabocas» o «sin tapabocas». Para el revisor, el error más costoso es que una foto sin tapabocas quede fuera de la cola prioritaria. Priorizar demasiadas fotos con tapabocas también tiene un costo, porque aumenta el tiempo de revisión.

## Alcance del proyecto
### Incluye
- Adquirir y verificar el conjunto público de Hugging Face, documentar sus campos y conservar el origen de cada fila.
- Comparar una línea base de clase mayoritaria y un clasificador de imágenes. Evaluar por clase y revisar ejemplos de ambos tipos de error.
- Proponer una interfaz de carga individual que muestre la clase estimada y permita al revisor corregirla. Una entrada grupal, ambigua o sin rostro queda fuera del protocolo de prueba.

### Criterios de éxito propuestos
| Decisión | Indicador y protocolo | Meta |
| --- | --- | --- |
| Aceptar la carga | Releer todas las filas de la versión fijada, decodificar cada imagen y conciliar frecuencias con el total | 11 792 imágenes válidas y dos clases reconocidas |
| Priorizar fotos sin tapabocas | Sensibilidad de WithoutMask = VP/(VP+FN) sobre prueba reservada | ≥ 0,90 |
| Mantener útil la cola | Precisión de WithoutMask = VP/(VP+FP) sobre la misma prueba | ≥ 0,85 |
| Verificar desempeño en ambas clases | Media de F1 de ambas clases frente a la línea base en la misma partición | F1 macro ≥ 0,85 y superior a la línea base |
| Evaluar utilidad operativa | Comparar revisión manual y revisión asistida en lotes equivalentes, alternando el orden entre revisores. Medir minutos por 100 fotos y omisiones finales | Reducción propuesta ≥ 20 % sin aumentar omisiones |

Las metas orientan la aceptación del prototipo. Se elegirá el umbral con validación y se congelará antes de evaluar prueba. Se reportarán denominadores y matriz de confusión junto con las métricas.

### Excluye
Reconocimiento de identidad, evaluación del ajuste o certificación del tapabocas, clasificación por persona en grupos, análisis de video y decisiones automáticas de acceso. Las etiquetas disponibles describen la imagen completa.

## Metodología
Seguiremos TDSP con incrementos semanales. En la primera iteración, el equipo traduce la decisión del revisor a una tarea binaria y comprueba que puede leer ambos tipos de ejemplo. En la segunda, audita etiquetas, resolución, duplicados y derivados de aumentación. Antes de dividir, agrupará copias exactas por hash y revisará similitudes visuales y nombres que sugieran un mismo original. Un grupo quedará íntegro en una sola partición. Las discrepancias de etiqueta se revisarán antes del entrenamiento. Se propone 70/15/15 con representación de ambas clases, semilla 42 y registro de los índices asignados. La ausencia de identificadores personales impide garantizar independencia por sujeto.

En las iteraciones siguientes se comparará la línea base con una red preentrenada de tamaño reducido. El redimensionamiento y la normalización se documentarán. La aumentación se aplicará únicamente a entrenamiento. Se revisarán errores por iluminación, ángulo y oclusión cuando existan ejemplos suficientes. Para el piloto se usarán fotos autorizadas, se registrará la corrección del revisor y se comprobarán las condiciones de uso antes de distribuir imágenes o publicar un servicio.

## Cronograma propuesto
| Periodo relativo al inicio | Trabajo | Evidencia para cerrar la iteración |
| --- | --- | --- |
| Semana 1 | Entendimiento y adquisición | Marco, diccionario, comando reproducible e inventario conciliado |
| Semana 2 | Calidad, exploración y partición | Informe de duplicados y grupos, índices congelados y distribución por clase |
| Semana 3 | Línea base y entrenamiento | Comparación reproducible en validación y registro de experimentos |
| Semana 4 | Evaluación y prototipo | Resultados sobre prueba reservada, interfaz y casos de error |
| Semana 5 | Aceptación y entrega | Prueba con revisores, contraste con metas y documentación final |

Cada semana el equipo integrará el incremento en un commit identificable. Las fechas calendario se ajustarán a la programación oficial del curso.

## Equipo del proyecto
Asignación propuesta para un equipo de tres. Víctor Alfonso Roa Gómez coordina el alcance, integra el repositorio y verifica la entrega. Un segundo integrante se encarga de adquisición, calidad y particiones. Un tercer integrante se encarga de modelamiento, evaluación y prototipo. Los nombres de los otros dos integrantes y la distribución definitiva deben confirmarse al registrar el equipo.

## Presupuesto
Estimación de planificación: tres integrantes × 3 horas semanales × 5 semanas = 45 horas-persona. Se proyectan COP 0 de desembolso incremental usando equipos existentes, herramientas de código abierto y cómputo gratuito. La estimación excluye la valorización de horas y depende de la disponibilidad de cómputo.

## Stakeholders
| Actor | Decisión o responsabilidad | Expectativa |
| --- | --- | --- |
| Revisor de fotografías (usuario propuesto) | Verificar y corregir los resultados | Encontrar primero las fotos sin tapabocas y conservar control sobre la clasificación final |
| Equipo del proyecto | Desarrollar, documentar y reproducir el flujo | Trazabilidad entre fuente, datos y experimentos |
| Docente o evaluador | Evaluar la entrega frente a la rúbrica | Documentos completos y carga ejecutable desde el repositorio |

## Aprobaciones
Se propone que el equipo valide alcance y asignación antes de registrar la entrega. La evaluación académica corresponde al docente. Estado al elaborar esta versión: pendiente de revisión del equipo y de evaluación docente. No se han recibido firmas ni fechas de aprobación.
