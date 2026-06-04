# Proyecto Final — Accesibilidad de Vivienda en Colombia

## Metodología CRISP-DM · Estado documental actualizado

**Proyecto:** Accesibilidad de Vivienda en Colombia  
**Período objetivo:** 2020-2024  
**Equipo:** Steve · Sofía · Kukis  
**Última actualización documental:** 2026-06-03

---

## Resumen Ejecutivo

Este proyecto analiza la accesibilidad económica a la vivienda urbana en Colombia mediante la construcción del **Indice de Accesibilidad Habitacional (IAH)**, una adaptación del Price-to-Income Ratio (PIR) al contexto colombiano usando el salario mínimo legal mensual vigente como proxy de ingreso.

La Fase 1 definió el problema de negocio, el alcance, las 12 ciudades focales, los criterios de éxito y el inventario de 16 fuentes de datos. Las Fases 2 y 3 documentan comprensión y preparación de datos. Las Fases 4, 5 y 6 **no han sido ejecutadas**; por tanto, este documento no reporta métricas de modelos, clusters finales, conclusiones de evaluación ni URL de dashboard.

> **Estado actual de datos:** `data/processed/vivienda_colombia_limpio.csv` fue validado sin marcadores de conflicto, con 282.660 registros × 26 columnas. Queda pendiente documentar la decisión sobre Armenia vs Santa Marta frente al alcance original de Fase 1.

---

## Pregunta Central de Investigación

> ¿Cómo ha evolucionado la accesibilidad económica a la vivienda en Colombia entre 2020 y 2024, y qué variables estructurales explican mejor las diferencias entre ciudades?

### Preguntas Derivadas

1. ¿Cuántos años de salario mínimo equivale el precio mediano de vivienda en las principales ciudades colombianas, y cómo cambió esa relación en 2020-2024?
2. ¿Qué variables tienen mayor poder predictivo sobre el precio de una propiedad?
3. ¿Es posible clasificar objetivamente los mercados urbanos en segmentos diferenciables de accesibilidad?
4. ¿Cuál es el ratio cuota/salario en cada ciudad frente al umbral financiero del 30%?

---

## Estado General por Fase

| Fase | Nombre | Responsable | Estado | Documento |
|---|---|---:|---|---|
| 1 | Comprensión del negocio | Steve | ✅ Completa | `docs/FASE_1_COMPLETA.md` |
| 2 | Comprensión de los datos | Sofía | ✅ Completa | `docs/FASE_2_COMPLETA.md` |
| 3 | Preparación de los datos | Kukis | ✅ Completa; caveat de alcance ciudad | `docs/FASE_3_COMPLETA.md` |
| 4 | Modelado | Steve | ⏳ Pendiente | `docs/FASE_4_COMPLETA.md` |
| 5 | Evaluación | Sofía | ⏳ Pendiente | `docs/FASE_5_COMPLETA.md` |
| 6 | Despliegue | Kukis | ⏳ Pendiente | `docs/FASE_6_COMPLETA.md` |

---

## Herramientas del Proyecto

| Propósito | Herramientas |
|---|---|
| Procesamiento | Python, pandas, numpy |
| EDA | Jupyter notebooks, matplotlib, seaborn, plotly |
| Modelado planificado | scikit-learn |
| Despliegue planificado | Streamlit |
| Versionamiento | Git, GitHub |
| Documentación | Markdown, metodología CRISP-DM |

---

## Distribución de Responsabilidades

| Integrante | Fases principales | Rol |
|---|---|---|
| Steve | 1 y 4 | Negocio, criterios de éxito, modelado. |
| Sofía | 2 y 5 | Comprensión de datos, evaluación y repositorio. |
| Kukis | 3 y 6 | Preparación de datos, integración técnica y dashboard. |

---

## Fase 1 — Comprensión del Negocio

**Estado:** ✅ Completa  
**Documento fuente:** `docs/FASE_1_COMPLETA.md`

### Resultado principal

La Fase 1 convirtió el problema de accesibilidad habitacional en un proyecto de ciencia de datos con objetivos, alcance, criterios de éxito, riesgos, cronograma y entregables.

### Alcance definido

| Dimensión | Definición |
|---|---|
| Período | 2020-2024 |
| Geografía | Análisis nacional + 12 ciudades focales |
| Indicador principal | IAH = precio mediano vivienda / salario mínimo anual |
| Fuentes | 16 archivos: A1-A8 y B1-B8 |

### Ciudades focales

Bogotá D.C., Medellín, Cali, Barranquilla, Bucaramanga, Cartagena, Pereira, Cúcuta, Manizales, Ibagué, Santa Marta y Villavicencio.

### Criterios de éxito técnico

| Criterio | Umbral |
|---|---:|
| R2 en test | >= 0,75 |
| RMSE relativo | < 15% |
| Silueta clustering | >= 0,45 |
| Segmentos diferenciables | >= 3 |

Estos criterios aún no han sido evaluados porque Fase 4 no se ha ejecutado.

---

## Fase 2 — Comprensión de los Datos

**Estado:** ✅ Completa  
**Documento fuente:** `docs/FASE_2_COMPLETA.md`  
**Hallazgos:** `docs/HALLAZGOS_FASE_2.md`

### Resultado principal

La Fase 2 verificó las 16 fuentes de datos, documentó calidad, esquemas, nulos, duplicados y problemas de integración. También dejó artefactos para Fase 3 en `data/processed/`.

### Inventario verificado

| Grupo | Fuentes | Filas crudas documentadas | Uso |
|---|---:|---:|---|
| A — Precios de vivienda | 8 | 3.005.876 | Base inmobiliaria del proyecto. |
| B — Macro/geografía | 8 | 3.435 | Contexto económico y validación. |
| Total | 16 | 3.009.311 | Inventario físico post-descarga. |

### Hallazgos documentales clave

1. Las fuentes existen, pero no comparten esquema.
2. A1 requiere filtrado colombiano.
3. A3 y A4 tienen duplicados relevantes.
4. A8 es referencia, no fuente de entrenamiento.
5. El IAH de EDA es preliminar y no debe usarse como conclusión final.

---

## Fase 3 — Preparación de los Datos

**Estado:** ⚠️ Ejecutada con observación crítica  
**Documento fuente:** `docs/FASE_3_COMPLETA.md`  
**Hallazgos:** `docs/HALLAZGOS_FASE_3.md`

### Resultado documentado

`data/processed/reporte_limpieza.csv` documenta un pipeline que reduce 880.714 registros consolidados a una salida esperada de 282.660 registros y 26 columnas.

| Paso | Operación | Entrada | Salida |
|---:|---|---:|---:|
| 0 | Consolidación inicial | 0 | 880.714 |
| 1 | Limpieza precios e invalidez | 880.714 | 876.104 |
| 2 | Estandarización / filtro ciudades | 876.104 | 666.156 |
| 3 | Restricción temporal | 666.156 | 652.047 |
| 4 | Tipo de inmueble | 652.047 | 598.353 |
| 5 | Filtro IQR outliers por grupo | 598.353 | 565.470 |
| 6 | Deduplicación inter-dataset v2 | 565.470 | 282.660 |

### Variables finales esperadas

El dataset final esperado incluye:

- Variables del inmueble: precio, área, habitaciones, baños, tipo, ciudad, estrato.
- Variables macro: salario, IPC, tasa hipotecaria, desempleo, IPVU/IPVN.
- Variables derivadas: salario anual, IAH, precio real, precio/m2, cuota mensual, ratio cuota/salario y nivel de accesibilidad.

### Observación actual

El archivo `data/processed/vivienda_colombia_limpio.csv` fue validado con 282.660 registros × 26 columnas, sin marcadores de conflicto y con período 2020-2024. La observación pendiente es de alcance: el CSV incluye Armenia y no incluye Santa Marta, aunque Fase 1 había definido Santa Marta entre las 12 ciudades focales.

---

## Fase 4 — Modelado

**Estado:** ⏳ Pendiente  
**Documento plantilla:** `docs/FASE_4_COMPLETA.md`  
**Guía:** `docs/GUIA_FASE_4.md`

### Objetivo planificado

Entrenar modelos de regresión para predicción de precio y modelos de clustering para segmentación de mercados.

### Entregables esperados

| Entregable | Ruta esperada | Estado |
|---|---|---|
| Notebook de modelado | `notebooks/03_modelado.ipynb` | `[PENDIENTE]` |
| Modelo de regresión | `models/modelo_random_forest.pkl` o nombre justificado | `[PENDIENTE]` |
| Modelo de clustering | `models/kmeans_segmentacion.pkl` | `[PENDIENTE]` |
| Scaler clustering | `models/scaler_cluster.pkl` | `[PENDIENTE]` |
| Tabla clusters ciudad-año | `data/processed/ciudades_clusters.csv` | `[PENDIENTE]` |

### Métricas pendientes

| Métrica | Estado |
|---|---|
| R2 | `[PENDIENTE]` |
| RMSE relativo | `[PENDIENTE]` |
| MAPE | `[PENDIENTE]` |
| Silueta | `[PENDIENTE]` |
| Davies-Bouldin | `[PENDIENTE]` |

---

## Fase 5 — Evaluación

**Estado:** ⏳ Pendiente  
**Documento plantilla:** `docs/FASE_5_COMPLETA.md`  
**Guía:** `docs/GUIA_FASE_5.md`

### Objetivo planificado

Validar si los modelos y hallazgos cumplen los criterios de éxito de Fase 1 y responder las cuatro preguntas de investigación con evidencia cuantitativa.

### Entregables esperados

| Entregable | Ruta esperada | Estado |
|---|---|---|
| Notebook de evaluación | `notebooks/04_evaluacion.ipynb` | `[PENDIENTE]` |
| Tabla de métricas finales | `docs/tabla_metricas_finales.csv` | `[PENDIENTE]` |
| Tabla de criterios de éxito | `docs/tabla_criterios_exito.csv` | `[PENDIENTE]` |
| Respuestas a preguntas | `docs/respuestas_preguntas.csv` | `[PENDIENTE]` |

### Decisión de despliegue

`[PENDIENTE — solo puede tomarse después de evaluar Fase 4]`

---

## Fase 6 — Despliegue

**Estado:** ⏳ Pendiente  
**Documento plantilla:** `docs/FASE_6_COMPLETA.md`  
**Guía:** `docs/GUIA_FASE_6.md`

### Estado actual

Existe una base de aplicación Streamlit en `app/`, pero no está validada como entrega final porque faltan modelos, clusters, evaluación y despliegue.

### Entregables esperados

| Entregable | Ruta/URL esperada | Estado |
|---|---|---|
| App principal | `app/app.py` | Base existente, no cierre de Fase 6 |
| Páginas de app | `app/pages/` | Base existente, no cierre de Fase 6 |
| URL pública | `[PENDIENTE]` | `[PENDIENTE]` |
| Pruebas locales | `[PENDIENTE]` | `[PENDIENTE]` |
| Pruebas cloud | `[PENDIENTE]` | `[PENDIENTE]` |

---

## Cronograma General

| Semana | Actividad | Responsable | Estado |
|---:|---|---:|---|
| 1-2 | Fase 1 — Comprensión del negocio | Steve | ✅ Completa |
| 3-4 | Fase 2 — Comprensión de los datos | Sofía | ✅ Completa |
| 5-6 | Fase 3 — Preparación de datos | Kukis | ✅ Completa; caveat de alcance ciudad |
| 7-9 | Fase 4 — Modelado | Steve | ⏳ Pendiente |
| 10 | Fase 5 — Evaluación | Sofía | ⏳ Pendiente |
| 11-12 | Fase 6 — Despliegue | Kukis | ⏳ Pendiente |
| 13-14 | Presentación final | Todos | ⏳ Pendiente |

---

## Riesgos Actuales

| Riesgo | Severidad | Acción |
|---|---|---|
| Diferencia Armenia/Santa Marta frente al alcance de Fase 1 | Media | Documentar cambio formal o regenerar dataset. |
| Modelos no existentes | Alta | No reportar métricas ni habilitar predictor. |
| App parcialmente construida antes de evaluación | Media | Tratarla como base, no como despliegue final. |
| Ciudades inconsistentes entre app y Fase 1 | Media | Alinear lista a las 12 focales. |
| Documentos con métricas inventadas | Alta | Mantener `[PENDIENTE]` hasta ejecución real. |

---

## Criterio de Integridad Documental

Toda métrica o resultado debe cumplir una de estas condiciones:

1. Estar respaldado por un archivo del proyecto.
2. Estar marcado como `[PENDIENTE]`.
3. Estar descrito como plan o plantilla, no como resultado.

Este criterio aplica especialmente a Fases 4, 5 y 6.

---

## Próximos Pasos

1. Decidir y documentar el tratamiento de Armenia vs Santa Marta frente al alcance de Fase 1.
2. Ejecutar Fase 4 y generar modelos reales.
3. Actualizar `docs/FASE_4_COMPLETA.md` solo con métricas obtenidas.
4. Ejecutar Fase 5 y decidir si los criterios de éxito se cumplen.
5. Completar Fase 6 solo con modelos, clusters y evaluación aprobados.

---

*Documento maestro · CRISP-DM 2026-I · Accesibilidad Habitacional Colombia*
