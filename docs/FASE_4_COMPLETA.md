# Fase 4 — Modelado

## Proyecto: Accesibilidad de Vivienda en Colombia · CRISP-DM 2026-I

**Responsable principal:** Steve · **Apoyo:** Kukis
**Estado:** ⚠️ Completada — métricas por debajo de umbrales de Fase 1
**Semanas:** 7–9

---

## Resumen Ejecutivo

Se entrenaron y compararon modelos de regresión (Ridge, Random Forest) para predecir precios de vivienda y modelos de clustering (KMeans, DBSCAN, PCA) para segmentar mercados urbanos según accesibilidad habitacional.

**Resultado principal:** Random Forest alcanzó R²=0.6348, por debajo del umbral de 0.75 definido en Fase 1. El RMSE relativo de 67.86% supera ampliamente el umbral del 15%. El modelo no cumple los criterios de éxito para producción. La segmentación de mercados sí es satisfactoria (K=5, silueta=0.4874).

> **Prerrequisito de datos:** Dataset validado sin marcadores de conflicto, 282.660 × 26, 0 nulos críticos.

---

## Contexto dentro de CRISP-DM

| Relación en el ciclo | Descripción |
|---|---|
| Entrada requerida | Dataset preparado por Fase 3 (282.660 × 26, 2020–2024) |
| Rol de Fase 4 | Entrenar, comparar y seleccionar modelos de regresión y clustering |
| Salida hacia Fase 5 | Modelos serializados, métricas de desempeño, evidencia de validación técnica |
| Salida hacia Fase 6 | Dashboard con predicciones y segmentos de mercado |

---

## Objetivos de la Fase

1. Entrenar un baseline de regresión (Ridge) y un modelo principal (Random Forest) para predicción de precio.
2. Comparar modelos contra los criterios técnicos definidos en Fase 1 (R² ≥ 0.75, RMSE relativo < 15%).
3. Segmentar mercados ciudad-año mediante KMeans con validación DBSCAN y PCA.
4. Exportar modelos y artefactos reproducibles para evaluación y despliegue.
5. Documentar métricas reales, hiperparámetros y limitaciones.

---

## Alcance Ejecutado

| Componente | Estado | Resultado |
|---|---|---|
| Validación del dataset de entrada | ✅ Completo | 282.660 × 26, 0 nulos críticos |
| Regresión baseline | ✅ Completo | Ridge: R²=0.5382 |
| Random Forest + GridSearch | ✅ Completo | RF optimizado: R²=0.6348 |
| Clustering ciudad-año (KMeans) | ✅ Completo | K=5, silueta=0.4874 |
| Validación con DBSCAN/PCA | ✅ Completo | DBSCAN identifica ruido; PCA explica 97.23% |
| Serialización de artefactos | ✅ Completo | 6 archivos exportados |

---

## Metodología Aplicada

### Regresión

| Elemento | Definición |
|---|---|
| Target | `price` |
| Predictores físicos | `area`, `rooms`, `bathrooms`, `estrato`, `property_type` |
| Predictores geográficos | `city` (12 ciudades, OneHotEncoder) |
| Predictores temporales/macro | `year` (categórica), `ipc_var_anual`, `tasa_hipotecaria_anual`, `tasa_desempleo`, `ipvu_variacion_anual` |
| Baseline | Ridge Regression (alpha=1.0) |
| Candidato principal | Random Forest Regressor con GridSearch |
| Preprocesamiento | StandardScaler (numéricas) + OneHotEncoder (categóricas) |

### Clustering

| Elemento | Definición |
|---|---|
| Unidad de análisis | Ciudad-año |
| Variables | IAH mediano, precio_m2 mediano, ratio_cuota_salario, tasa_desempleo |
| Algoritmo principal | KMeans (K=5, init=k-means++, n_init=20) |
| Validación | DBSCAN (eps=0.8, min_samples=3), PCA (97.23% varianza), silueta (0.4874) |

---

## Resultados Obtenidos

### Regresión

| Resultado | Valor |
|---|---|
| Shape del dataset usado | 282.660 × 26 |
| Modelo de regresión ganador | Random Forest |
| Hiperparámetros finales | max_depth=20, min_samples_split=5, n_estimators=200 |
| R² en test (RF optimizado) | **0.6348** |
| MAE | **$168,048,700** |
| RMSE | **$284,996,129** |
| RMSE relativo | **67.86%** |
| R² en test (Ridge baseline) | 0.5382 |
| CV R² (RF, 5-fold) | 0.6320 |
| CV R² (Ridge, 5-fold) | 0.5305 ± 0.0037 |

### Clustering

| Resultado | Valor |
|---|---|
| Número de clusters elegido | **5** |
| Coeficiente de silueta | **0.4874** |
| Segmentos | 2 Premium (IAH 25-29), 3 Intermedios (IAH 12-19) |
| DBSCAN (eps=0.8) | 4 clusters, 8 pts ruido (Bogotá, Cartagena, Medellín, Pereira) |
| PCA varianza explicada | 97.23% (PC1=70.18%, PC2=27.05%) |

### Perfiles de Clusters

| Cluster | IAH medio | precio_m2 medio | ratio_cuota_salario | tasa_desempleo | Count | Nombre |
|---|---:|---:|---:|---:|---:|:---|
| 0 | 29.23 | $4,597,674 | 2.52 | 15.70 | 6 | Premium |
| 1 | 16.24 | $2,144,328 | 1.40 | 15.70 | 18 | Intermedio |
| 2 | 18.66 | $3,376,073 | 2.37 | 10.62 | 12 | Intermedio-Alto |
| 3 | 25.35 | $4,904,361 | 3.29 | 10.45 | 6 | Premium |
| 4 | 12.93 | $2,524,136 | 1.59 | 10.73 | 9 | Intermedio |

---

## Criterios de Éxito Fase 1 vs Fase 4

| Criterio técnico | Umbral | Obtenido | Estado |
|---|---:|---:|---:|
| R² en conjunto de prueba | ≥ 0.75 | 0.6348 | ❌ No cumple |
| RMSE relativo | < 15% | 67.86% | ❌ No cumple |
| Coeficiente de silueta | ≥ 0.45 | 0.4874 | ✅ Cumple |
| Segmentos diferenciables | ≥ 3 | 5 | ✅ Cumple |

---

## Hallazgos Clave

| Hallazgo | Evidencia |
|---|---|
| Random Forest supera a Ridge en +9.66 pp de R², pero sigue lejos del umbral 0.75 | RF=0.6348 vs Ridge=0.5382 |
| El RMSE relativo de 67.86% indica que el error de predicción es enorme respecto a la mediana de precios | RMSE relativo: 67.86% vs umbral 15% |
| Las variables macroeconómicas tienen VIF extremadamente alto (tasa_desempleo=85.5, tasa_hipotecaria=39.0), indicando multicolinealidad severa | VIF reportado en Sección 2 |
| `bathrooms` (42.2%), `area` (28.0%) y `estrato` (11.3%) son las variables más importantes; el contexto macro aporta <5% | Feature importance del RF (extraída del modelo) |
| El clustering es sólido: 5 segmentos con silueta de 0.4874, superando el umbral de 0.45 | Silueta confirmada con DBSCAN y PCA |
| 3 ciudades (Armenia, Barranquilla, Cartagena) solo tienen datos 2020-2021, limitando su representación en clustering | 51 de 60 city-year posibles |
| DBSCAN identifica Bogotá, Cartagena, Medellín y Pereira como ruido en clustering — mercados atípicos | eps=0.8, min_samples=3 |
| El modelo RF pesa ~450 MB, no es práctico para git o despliegue ligero | 448,622,538 bytes |
| 2023 solo tiene 8,014 registros (2.84% del dataset) por la corrección B9 | Distribución de años |

---

## Problemas Encontrados y Resolución

| Problema | Estado | Resolución |
|---|---|---|
| R² bajo (~0.63) — lejos del umbral 0.75 | ⚠️ Documentado | Ingeniería de features adicional (interacciones, más variables) o probar XGBoost/LightGBM en Fase 5 |
| RMSE relativo muy alto (67.86%) | ⚠️ Documentado | El target `price` tiene varianza extrema; considerar transformación logarítmica o target encoding por ciudad |
| Modelo RF de 448 MB no git-friendly | ⚠️ Pendiente | Agregar `models/*.pkl` a `.gitignore` y usar almacenamiento externo o git-lfs |
| Diferencia de alcance ciudad: Armenia vs Santa Marta | ⚠️ Documentado | El dataset contiene Armenia (1,493 reg) pero no Santa Marta, que es una de las 12 ciudades focales de Fase 1 |
| A2 con 72K registros vs 123K esperados | ⚠️ Documentado | La deduplicación eliminó el excedente; volumen actual es el real post-limpieza |

---

## Validaciones Realizadas

| Validación | Estado |
|---|---|
| Dataset de entrada sin conflictos | ✅ Completo |
| Shape de entrada confirmado | ✅ 282.660 × 26 |
| Nulos críticos de entrada | ✅ 0 |
| Codificación de `city` verificada por codepoint | ✅ Tildes almacenadas correctamente |
| Combinaciones ciudad-año para clustering | ✅ 51 combinaciones (9 ausentes documentadas) |
| Train/test reproducible | ✅ random_state=42, distribuciones similares |
| Métricas calculadas en test | ✅ R², MAE, RMSE, RMSE relativo |
| Validación cruzada ejecutada | ✅ 5-fold (Ridge y RF) |
| Modelos cargan después de serialización | ✅ Verificado con predicción de prueba |
| Clusters interpretables | ✅ 5 segmentos con perfiles claros |

---

## Entregables Generados

| Entregable | Ruta | Estado |
|---|---|---|
| Notebook de modelado | `notebooks/03_modelado.ipynb` | ✅ Ejecutado |
| Modelo de regresión | `models/modelo_random_forest.pkl` | ✅ 448 MB |
| Modelo de clustering | `models/kmeans_segmentacion.pkl` | ✅ 1 KB |
| Pipeline clustering | `models/pipeline_clustering.pkl` | ✅ (scaler+kmeans encapsulados) |
| Scaler de clustering | `models/scaler_cluster.pkl` | ✅ 1 KB |
| Orden de features | `models/features_order.json` | ✅ 159 bytes |
| Clusters ciudad-año | `data/processed/ciudades_clusters.csv` | ✅ 7.6 KB |
| Perfiles de cluster | `data/processed/perfiles_clusters.csv` | ✅ 228 bytes |
| Reporte de Fase 4 | `docs/FASE_4_COMPLETA.md` | ✅ Actualizado |

---

## Riesgos o Limitaciones Detectadas

1. El modelo no cumple R² ≥ 0.75 ni RMSE relativo < 15%. No debe presentarse como listo para producción.
2. `price` como target continuo tiene varianza extrema (desde $10M hasta $10,000M). Considerar transformación logarítmica.
3. Las ciudades con menor volumen (Armenia 0.5%, Villavicencio 0.9%) tienen error predictivo más alto.
4. Los modelos .pkl son demasiado grandes para git (~450 MB).
5. Santa Marta no está en el dataset pero es ciudad focal de Fase 1 — discrepancia de alcance.
6. La multicolinealidad en variables macro (VIF > 30) afecta la interpretabilidad de Ridge, no así de RF.

---

## Conclusiones

La Fase 4 se completó con todos los artefactos generados, pero los modelos de regresión no alcanzan los criterios mínimos definidos en Fase 1 (R²=0.63 vs 0.75 requerido). La segmentación de mercados es satisfactoria con 5 clusters y silueta de 0.4874.

Se recomienda en Fase 5:
1. Probar transformación logarítmica del target `price`
2. Probar XGBoost o LightGBM como alternativa a Random Forest
3. Evaluar ingeniería de features adicional (interacciones, features geográficas)
4. Evaluar si el criterio R² ≥ 0.75 es realista dado la alta varianza del mercado inmobiliario colombiano

---

## Preparación para la Siguiente Fase

Fase 5 (Evaluación) requiere:
1. ✅ Dataset de entrada validado
2. ✅ Modelo de regresión serializado y cargable
3. ✅ Modelo de clustering serializado y cargable
4. ✅ Métricas de test y validación cruzada
5. ✅ Tablas de clusters y perfiles exportadas
6. ⚠️ Revisar umbrales de Fase 1 contra resultados reales — posible ajuste metodológico

---

*Documento de Fase 4 · CRISP-DM 2026-I · Accesibilidad Habitacional Colombia*
