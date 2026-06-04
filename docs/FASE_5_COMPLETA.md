# Fase 5 — Evaluación

## Proyecto: Accesibilidad de Vivienda en Colombia · CRISP-DM 2026-I

**Responsable principal:** Sofía · **Apoyo:** Steve  
**Estado:** ⏳ Pendiente — requiere Fase 4 ejecutada y modelos validados  
**Semana planificada:** 10

---

## Resumen Ejecutivo

Esta fase **no ha sido ejecutada**. El presente documento es una plantilla para evaluar los modelos y responder las preguntas de investigación cuando existan resultados reales de Fase 4.

No se reportan métricas, conclusiones, rankings de variables, clusters ni respuestas de negocio porque aún no hay modelos entrenados ni evaluación reproducible.

---

## Contexto dentro de CRISP-DM

| Relación en el ciclo | Descripción |
|---|---|
| Entrada requerida | Modelos, métricas y clusters generados en Fase 4. |
| Rol de Fase 5 | Verificar si el proyecto cumple criterios de éxito técnicos y de negocio. |
| Salida hacia Fase 6 | Decisión de despliegue, conclusiones validadas y restricciones para el dashboard. |

---

## Objetivos de la Fase

1. Evaluar el desempeño real del modelo de regresión.
2. Evaluar la calidad e interpretabilidad de los clusters.
3. Verificar los criterios de éxito definidos en Fase 1.
4. Responder las cuatro preguntas de investigación con evidencia cuantitativa.
5. Definir si el proyecto está listo para despliegue o requiere iteración.

---

## Alcance Planificado

| Componente | Estado | Resultado esperado |
|---|---|---|
| Evaluación de regresión | `[PENDIENTE]` | R2, MAE, RMSE, RMSE relativo, MAPE. |
| Evaluación de clustering | `[PENDIENTE]` | Silueta, Davies-Bouldin, perfiles de clusters. |
| Validación de criterios Fase 1 | `[PENDIENTE]` | Tabla umbral vs valor obtenido. |
| Respuesta a P1-P4 | `[PENDIENTE]` | Respuestas con tablas y figuras reales. |
| Recomendación de despliegue | `[PENDIENTE]` | Aprobado, condicionado o rechazado. |

---

## Actividades por Realizar

1. Cargar dataset saneado y artefactos de Fase 4.
2. Reproducir la evaluación sobre el mismo conjunto de prueba.
3. Calcular métricas finales de regresión.
4. Analizar residuos y sesgos por ciudad.
5. Evaluar estabilidad del modelo.
6. Revisar importancia de variables.
7. Evaluar separación e interpretabilidad de clusters.
8. Verificar cada criterio de éxito de Fase 1.
9. Responder P1-P4 con evidencia cuantitativa.
10. Documentar limitaciones y decisión de despliegue.

---

## Correspondencia con GUIA_FASE_5.md

| Actividad planificada | Estado | Evidencia requerida |
|---|---|---|
| Carga de recursos | ⏳ Pendiente | Dataset y modelos cargados sin errores. |
| Verificación de criterios de éxito | ⏳ Pendiente | Tabla con valores reales. |
| Evaluación del modelo de regresión | ⏳ Pendiente | Métricas y análisis de residuos. |
| Evaluación del clustering | ⏳ Pendiente | Métricas de separación y perfiles. |
| Respuesta a preguntas de investigación | ⏳ Pendiente | Respuestas con tablas/figuras reales. |
| Análisis complementario del IAH | ⏳ Pendiente | Distribuciones por ciudad/año. |
| Validación final del proyecto | ⏳ Pendiente | Decisión de pasar o no a despliegue. |
| Guardado de outputs | ⏳ Pendiente | CSVs y figuras finales. |

---

## Metodología a Aplicar

### Evaluación técnica

| Criterio | Fuente | Umbral |
|---|---|---:|
| R2 en test | Fase 1 | >= 0,75 |
| RMSE relativo | Fase 1 | < 15% |
| Coeficiente de silueta | Fase 1 | >= 0,45 |
| Segmentos diferenciables | Fase 1 | >= 3 |
| Cobertura geográfica | Fase 1 | >= 8 ciudades con análisis completo |

### Evaluación de negocio

La evaluación debe responder con evidencia las cuatro preguntas definidas en Fase 1:

| Pregunta | Estado |
|---|---|
| P1 — Evolución del IAH por ciudad y año | `[PENDIENTE]` |
| P2 — Variables con mayor poder predictivo sobre precio | `[PENDIENTE]` |
| P3 — Segmentación objetiva de mercados urbanos | `[PENDIENTE]` |
| P4 — Ratio cuota/salario frente al umbral del 30% | `[PENDIENTE]` |

---

## Resultados Obtenidos

| Resultado | Valor |
|---|---|
| Modelo evaluado | `[PENDIENTE]` |
| Dataset de test usado | `[PENDIENTE]` |
| R2 | `[PENDIENTE]` |
| MAE | `[PENDIENTE]` |
| RMSE | `[PENDIENTE]` |
| RMSE relativo | `[PENDIENTE]` |
| MAPE | `[PENDIENTE]` |
| Silueta clustering | `[PENDIENTE]` |
| Davies-Bouldin | `[PENDIENTE]` |
| Preguntas respondidas | `[PENDIENTE]` |

---

## Métricas y Estadísticas Relevantes

| Criterio de éxito | Umbral | Valor obtenido | Cumple |
|---|---:|---:|---|
| R2 regresión | >= 0,75 | `[PENDIENTE]` | `[PENDIENTE]` |
| RMSE relativo | < 15% | `[PENDIENTE]` | `[PENDIENTE]` |
| Silueta clustering | >= 0,45 | `[PENDIENTE]` | `[PENDIENTE]` |
| Segmentos diferenciables | >= 3 | `[PENDIENTE]` | `[PENDIENTE]` |
| Ciudades con análisis completo | >= 8 | `[PENDIENTE]` | `[PENDIENTE]` |
| Preguntas respondidas | 4 de 4 | `[PENDIENTE]` | `[PENDIENTE]` |

---

## Plantilla de Respuesta a Preguntas de Investigación

### P1 — Evolución del IAH

**Respuesta:** `[PENDIENTE — calcular IAH mediano nacional y por ciudad para 2020-2024]`

| Ciudad | IAH inicial | IAH final | Cambio | Interpretación |
|---|---:|---:|---:|---|
| Bogotá | `[PENDIENTE]` | `[PENDIENTE]` | `[PENDIENTE]` | `[PENDIENTE]` |
| Medellín | `[PENDIENTE]` | `[PENDIENTE]` | `[PENDIENTE]` | `[PENDIENTE]` |
| Cali | `[PENDIENTE]` | `[PENDIENTE]` | `[PENDIENTE]` | `[PENDIENTE]` |
| Demás ciudades focales | `[PENDIENTE]` | `[PENDIENTE]` | `[PENDIENTE]` | `[PENDIENTE]` |

### P2 — Variables con mayor poder predictivo

**Respuesta:** `[PENDIENTE — extraer importancia de variables del modelo final]`

| Variable | Importancia | Interpretación |
|---|---:|---|
| `[PENDIENTE]` | `[PENDIENTE]` | `[PENDIENTE]` |

### P3 — Segmentación de mercados

**Respuesta:** `[PENDIENTE — completar con clusters reales y métricas de separación]`

| Segmento | Ciudades/años | Perfil | Evidencia |
|---|---|---|---|
| `[PENDIENTE]` | `[PENDIENTE]` | `[PENDIENTE]` | `[PENDIENTE]` |

### P4 — Ratio cuota/salario

**Respuesta:** `[PENDIENTE — calcular ratio mediano y porcentaje de registros sobre 30%]`

| Ciudad | Ratio cuota/salario | Estado frente a 30% | Interpretación |
|---|---:|---|---|
| `[PENDIENTE]` | `[PENDIENTE]` | `[PENDIENTE]` | `[PENDIENTE]` |

---

## Hallazgos Clave

| Hallazgo | Evidencia |
|---|---|
| `[PENDIENTE]` | `[PENDIENTE — completar solo con resultados reales]` |

---

## Problemas Encontrados y Resolución

| Problema | Estado | Resolución esperada |
|---|---|---|
| No existen modelos entrenados | ⏳ Pendiente | Ejecutar Fase 4. |
| No existen métricas finales | ⏳ Pendiente | Calcular en Fase 5. |
| No existe decisión de despliegue | ⏳ Pendiente | Tomar decisión tras verificar criterios de Fase 1. |

---

## Validaciones Realizadas

| Validación | Estado |
|---|---|
| Carga del modelo de regresión | `[PENDIENTE]` |
| Carga del modelo de clustering | `[PENDIENTE]` |
| Reproducción de partición test | `[PENDIENTE]` |
| Métricas finales calculadas | `[PENDIENTE]` |
| Preguntas de investigación respondidas | `[PENDIENTE]` |
| Recomendación de despliegue documentada | `[PENDIENTE]` |

---

## Entregables Esperados

| Entregable | Ruta esperada | Estado |
|---|---|---|
| Notebook de evaluación | `notebooks/04_evaluacion.ipynb` | ⏳ Pendiente |
| Tabla de métricas finales | `docs/tabla_metricas_finales.csv` | ⏳ Pendiente |
| Tabla de criterios de éxito | `docs/tabla_criterios_exito.csv` | ⏳ Pendiente |
| Tabla de respuestas | `docs/respuestas_preguntas.csv` | ⏳ Pendiente |
| Figuras finales | `docs/figures/` | ⏳ Pendiente |
| Reporte de Fase 5 completado | `docs/FASE_5_COMPLETA.md` | ⏳ Pendiente |

---

## Riesgos o Limitaciones Detectadas

1. Si Fase 4 no cumple criterios técnicos, Fase 6 no debe presentar el predictor como producción.
2. Si alguna pregunta de investigación no puede responderse con evidencia, debe marcarse explícitamente como no resuelta.
3. Las recomendaciones de política pública deben derivarse de resultados reales, no de hipótesis previas.

---

## Conclusiones

`[PENDIENTE — redactar únicamente después de ejecutar la evaluación y responder P1-P4 con evidencia]`

---

## Preparación para la Siguiente Fase

Fase 6 solo puede iniciar si Fase 5 determina que:

1. Los modelos cumplen o documentan adecuadamente sus desviaciones frente a los criterios de Fase 1.
2. Las cuatro preguntas de investigación tienen respuesta cuantitativa o limitación explícita.
3. Los artefactos de modelo y tablas requeridos por la app existen y son cargables.
4. Las limitaciones del predictor y del dashboard están documentadas.

---

*Plantilla de Fase 5 · CRISP-DM 2026-I · Accesibilidad Habitacional Colombia*
