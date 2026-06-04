# Proyecto Final — Accesibilidad de Vivienda en Colombia

## Metodología CRISP-DM · Estado documental actualizado

**Proyecto:** Accesibilidad de Vivienda en Colombia  
**Período objetivo:** 2020-2024  
**Equipo:** Steve · Sofía · Kukis  
**Última actualización documental:** 2026-06-04

---

## Resumen Ejecutivo

Este proyecto analiza la accesibilidad económica a la vivienda urbana en Colombia mediante la construcción del **Indice de Accesibilidad Habitacional (IAH)**, una adaptación del Price-to-Income Ratio (PIR) al contexto colombiano usando el salario mínimo legal mensual vigente como proxy de ingreso.

La Fase 1 definió el problema de negocio, el alcance, las 12 ciudades focales, los criterios de éxito y el inventario de 16 fuentes de datos. Las Fases 2 y 3 documentan comprensión y preparación de datos. Las **Fases 4, 5 y 6 están completadas**:

- **Fase 4 (Modelado):** Random Forest (R²=0.6348) + KMeans (5 clusters). Modelos exportados a `models/`.
- **Fase 5 (Evaluación):** 4/6 criterios de éxito cumplidos. Dashboard responde a las 4 preguntas de investigación.
- **Fase 6 (Despliegue):** Dashboard Streamlit con 5 páginas (Análisis Nacional, Comparador, Predictor, Segmentos, Homepage). Modelo Random Forest cargado vía Git LFS.

> **Estado actual de datos:** `data/processed/vivienda_colombia_limpio.csv` fue validado sin marcadores de conflicto, con 282.660 registros × 26 columnas. Armenia se incorporó al alcance (datos 2020-2021); Santa Marta se excluyó por falta de datos.

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
| 4 | Modelado | Steve | ✅ Completada | `docs/FASE_4_COMPLETA.md` |
| 5 | Evaluación | Sofía | ✅ Completada | `docs/FASE_5_COMPLETA.md` |
| 6 | Despliegue | Kukis | ✅ Completada | `docs/GUIA_FASE_6.md` |

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

Estos criterios fueron evaluados en Fase 5 (ver `docs/FASE_5_COMPLETA.md`). Resultado: 4/6 criterios cuantitativos cumplidos. R²=0.6348 (umbral ≥0.75), RMSE rel=67.86% (umbral <15%), silueta=0.4874 (umbral ≥0.45).

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

El archivo `data/processed/vivienda_colombia_limpio.csv` fue validado con 282.660 registros × 26 columnas, sin marcadores de conflicto y con período 2020-2024. Decisión de alcance: Armenia se incorporó (datos 2020-2021); Santa Marta se excluyó por falta de datos en las fuentes disponibles.

---

## Fase 4 — Modelado

**Estado:** ✅ Completada  
**Documento:** `docs/FASE_4_COMPLETA.md`  
**Guía:** `docs/GUIA_FASE_4.md`

### Objetivo cumplido

Modelos de regresión (Random Forest, XGBoost v2) y clustering (KMeans, 5 clusters) entrenados y exportados.

### Entregables

| Entregable | Ruta | Estado |
|---|---|---|
| Notebook de modelado v1 | `notebooks/03_modelado.ipynb` | ✅ Ejecutado (RF, R²=0.6348) |
| Notebook de modelado v2 | `notebooks/03_modelado_v2.ipynb` | ✅ Ejecutado (XGBoost log, R²~0.72) |
| Modelo de regresión | `models/modelo_random_forest.pkl` | ✅ 448 MB (vía Git LFS) |
| Modelo XGBoost v2 | `models/modelo_xgboost_v2.pkl` | ✅ (vía Git LFS) |
| Modelo de clustering | `models/kmeans_segmentacion.pkl` | ✅ 1 KB |
| Scaler clustering | `models/scaler_cluster.pkl` | ✅ 1 KB |
| Feature order v1 | `models/features_order.json` | ✅ |
| Feature order v2 | `models/features_order_v2.json` | ✅ |
| Feature importances | `models/feature_importances.json` | ✅ |
| Tabla clusters ciudad-año | `data/processed/ciudades_clusters.csv` | ✅ |

### Métricas

| Métrica | Random Forest | XGBoost v2 |
|---|---|---|
| R² | 0.6348 | ~0.72 |
| RMSE relativo | 67.86% | ~55% |
| MAE | $168M COP | — |
| Silueta (KMeans) | 0.4874 | 0.4874 |
| Davies-Bouldin | — | — |

---

## Fase 5 — Evaluación

**Estado:** ✅ Completada  
**Documento:** `docs/FASE_5_COMPLETA.md`  
**Guía:** `docs/GUIA_FASE_5.md`

### Objetivo cumplido

Validación de modelos frente a criterios de éxito de Fase 1. Respuesta a las 4 preguntas de investigación con evidencia cuantitativa.

### Entregables

| Entregable | Ruta | Estado |
|---|---|---|
| Informe de evaluación | `docs/FASE_5_COMPLETA.md` | ✅ Completo (4/6 criterios cumplidos) |
| Respuestas a preguntas | `docs/FASE_5_COMPLETA.md` | ✅ 4/4 respondidas |

---

## Fase 6 — Despliegue

**Estado:** ✅ Completada (pendiente despliegue público)  
**Documento:** `docs/GUIA_FASE_6.md`

### Estado actual

Dashboard Streamlit con 5 páginas funcionales, cargando modelo Random Forest vía Git LFS.

### Entregables

| Página | Archivo | Estado |
|---|---|---|
| Homepage | `app/app.py` | ✅ Mapa IAH, resumen ejecutivo |
| Análisis Nacional | `app/pages/01_analisis_nacional.py` | ✅ Evolución IAH, feature importances |
| Comparador | `app/pages/02_comparador_ciudades.py` | ✅ Comparación ciudades, heatmap cuota/salario |
| Predictor | `app/pages/03_predictor_precios.py` | ✅ Predicción precios con RF |
| Segmentos | `app/pages/04_segmentos_mercado.py` | ✅ KMeans 5 clusters, radar |
| URL pública | Pendiente | Requiere Streamlit Cloud con Git LFS |
| Pruebas locales | `streamlit run app/app.py` | ✅ Verificado |

---

## Cronograma General

| Semana | Actividad | Responsable | Estado |
|---:|---|---:|---|
| 1-2 | Fase 1 — Comprensión del negocio | Steve | ✅ Completa |
| 3-4 | Fase 2 — Comprensión de los datos | Sofía | ✅ Completa |
| 5-6 | Fase 3 — Preparación de datos | Kukis | ✅ Completa; caveat de alcance ciudad |
| 7-9 | Fase 4 — Modelado | Steve | ✅ Completada |
| 10 | Fase 5 — Evaluación | Sofía | ✅ Completada |
| 11-12 | Fase 6 — Despliegue | Kukis | ✅ Completada (pendiente Streamlit Cloud) |
| 13-14 | Presentación final | Todos | ⏳ Pendiente |

---

## Riesgos Actuales

| Riesgo | Severidad | Acción |
|---|---|---|
| Diferencia Armenia/Santa Marta frente al alcance de Fase 1 | Media | Resuelto — Armenia incorporada (2020-2021) y Santa Marta excluida por falta de datos. |
| Modelos no existentes | Alta | Resuelto — modelos disponibles vía Git LFS. |
| App parcialmente construida antes de evaluación | Media | Resuelto — dashboard completo con 5 páginas funcionales. |
| Ciudades inconsistentes entre app y Fase 1 | Media | Resuelto — documentación y dataset final declaran 12 ciudades con Armenia y sin Santa Marta. |
| Documentos con métricas inventadas | Alta | Ahora actualizado con métricas reales de Fases 4-6. |

---

## Criterio de Integridad Documental

Toda métrica o resultado debe cumplir una de estas condiciones:

1. Estar respaldado por un archivo del proyecto.
2. Estar marcado como `[PENDIENTE]` (hoy actualizado con valores reales).
3. Estar descrito como plan o plantilla, no como resultado.

Este criterio aplica especialmente a Fases 4, 5 y 6.

---

## Próximos Pasos

1. Publicar el dashboard en Streamlit Cloud y registrar la URL pública en `README.md`.
2. Verificar carga de modelos y archivos grandes en el entorno público.
3. Preparar la presentación final con métricas reales de Fases 4-6.

---

*Documento maestro · CRISP-DM 2026-I · Accesibilidad Habitacional Colombia*
