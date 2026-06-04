# Fase 4 — Modelado
## Notebook: `notebooks/03_modelado.ipynb`
**Responsable:** Steve · **Apoyo:** Kukis  
**Insumo:** `data/processed/vivienda_colombia_limpio.csv`  
**Estado:** ✅ Completada — commit `e1d8867`  
**Semanas:** 7–8

---

## Resumen de Resultados

### Regresión

| Modelo | R² | MAE | RMSE | RMSE rel |
|--------|----|-----|------|----------|
| **Ridge** | 0.5382 | $204M | $320M | 76.30% |
| **RF base** (100 trees) | 0.6261 | $169M | $288M | 68.65% |
| **RF optimizado** (200, d=20, s=5) | **0.6348** | $168M | $285M | 67.86% |

### Clustering

| K | Silueta | Davies-Bouldin | ¿Cumple ≥ 0.45? |
|---|---|---|---|
| **5** | **0.4874** | — | ✅ |
| DBSCAN (eps=0.8): 4 clusters, ruido en Bogotá/Cartagena/Medellín/Pereira | | | |
| PCA: 97.23% varianza (PC1=70.18%, PC2=27.05%) | | | |

### Criterios Fase 1

| Criterio | Umbral | Obtenido | ¿Cumple? |
|---|---|---|---|
| R² en test | ≥ 0.75 | 0.6348 | ❌ |
| RMSE relativo | < 15% | 67.86% | ❌ |
| Coef. silueta | ≥ 0.45 | 0.4874 | ✅ |
| Clusters | ≥ 3 | 5 | ✅ |

---

## Desviaciones del Plan Original

| Aspecto | Plan original | Ejecutado |
|---|---|---|
| `year` | Numérica en FEATURES_NUM | **Categórica** en FEATURES_CAT (decisión del proyecto) |
| FEATURES_NUM | 9 variables (incluía year) | **8 variables** (sin year) |
| FEATURES_CAT | 2 variables (city, property_type) | **3 variables** (city, property_type, year) |
| Clustering rows | 60 esperadas (12×5) | **51 reales** (Armenia/Barranquilla/Cartagena solo 2020–2021) |
| K esperado | 4 (según criterio de negocio) | **5** (mejor silueta: 0.4874) |
| GridSearch combos | 12 (2×3×2) | 12 ejecutados sin problemas de RAM |
| Modelo .pkl | Tamaño esperado ~100–200 MB | **448 MB** — excluido de git vía .gitignore |
| Santa Marta | Ciudad focal según Fase 1 (12) | No está en dataset — Armenia la reemplazó |

---

## Sección 1: Setup y Carga del Dataset
**Celdas 1–5: Importaciones y configuración**
- [x] pandas, numpy, matplotlib, seaborn, plotly, joblib
- [x] `train_test_split`, `ColumnTransformer`, `StandardScaler`, `OneHotEncoder`, `Pipeline`
- [x] `Ridge`, `RandomForestRegressor`, `KMeans`, `DBSCAN`
- [x] `mean_absolute_error`, `mean_squared_error`, `r2_score`, `silhouette_score`
- [x] `PCA`, `cross_val_score`, `GridSearchCV`
- [x] `os.makedirs("models", exist_ok=True)` + `os.chdir` a ruta absoluta

**Celdas 6–8: Carga y verificación del dataset**
- [x] Cargado `vivienda_colombia_limpio.csv` → **282.660 × 26**, 0 nulos críticos
- [x] Años: {2020: 60.399, 2021: 75.535, 2022: 69.993, 2023: 8.014, 2024: 68.719}
- [x] Ciudades: 12, con tildes correctas en UTF-8 (confirmado por codepoint)

---

## Sección 2: Preparación de Features
**Celdas 9–14: Definición de variables**
- [x] `FEATURES_NUM`: `['area', 'rooms', 'bathrooms', 'estrato', 'ipc_var_anual', 'tasa_hipotecaria_anual', 'tasa_desempleo', 'ipvu_variacion_anual']`
- [x] `FEATURES_CAT`: `['city', 'property_type', 'year']` ← **year como categórica**
- [x] `TARGET`: `'price'`
- [x] `X` (282.660 × 11), `y` (282.660)

**Celdas 15–18: VIF y correlación**
- [x] VIF reportado: `tasa_desempleo`=**85.5**, `tasa_hipotecaria_anual`=**39.0**, `ipvu_variacion_anual`=**18.5** (multicolinealidad severa)
- [x] Documentado: Ridge maneja colinealidad, no se eliminan variables
- [x] Heatmap de correlación guardado en `models/heatmap_correlacion.png`

**Celdas 19–21: División train/test**
- [x] `train_test_split(X, y, test_size=0.20, random_state=42)`
- [x] Train: **226.128**, Test: **56.532**
- [x] Distribución de `city` consistente entre train y test

**Celdas 22–24: Pipeline de preprocesamiento**
- [x] `ColumnTransformer`: `StandardScaler` (num) + `OneHotEncoder` (cat)
- [x] 27 features transformadas (8 num + 19 one-hot)
- [x] Sin fugas de información

---

## Sección 3: Modelo Baseline — Ridge Regression
**Celdas 25–32**
- [x] `Ridge(alpha=1.0)` entrenado ✅
- [x] **R²=0.5382**, MAE=$204M, RMSE=$320M, RMSE rel=76.30%
- [x] CV 5-fold: **0.5305 ± 0.0037**
- [x] Scatter plot: `models/scatter_ridge.png`
- [x] Residuos: `models/residuos_ridge.png`

---

## Sección 4: Modelo Principal — Random Forest Regressor
**Celdas 33–42: Entrenamiento inicial**
- [x] `RandomForestRegressor(n_estimators=100)` entrenado ✅
- [x] **R²=0.6261**, MAE=$169M, RMSE=$288M, RMSE rel=68.65%
- [x] CV 3-fold (RAM limitante): scores individuales
- [x] **RF supera a Ridge en +8.79 pp** de R²

**Celdas 43–50: Importancia y diagnóstico**
- [x] Top 15 features: `tasa_desempleo` y `ipc_var_anual` lideran (~12% c/u)
- [x] Scatter y residuos: `models/diagnostico_rf.png`
- [x] Error por ciudad: `models/error_por_ciudad.png`
- [x] Ciudades con menor volumen (Armenia, Villavicencio) tienen mayor error absoluto

**Celdas 51–57: GridSearch (12 combos × 5 folds)**
- [x] `param_grid`: `n_estimators=[100,200]`, `max_depth=[10,20,None]`, `min_samples_split=[2,5]`
- [x] Mejores params: **max_depth=20, min_samples_split=5, n_estimators=200**
- [x] Mejor CV R²: **0.6320**
- [x] RF optimizado en test: **R²=0.6348** (+0.86 pp vs RF base)

---

## Sección 5: Exportación del Modelo de Regresión
**Celdas 58–62**
- [x] `joblib.dump(pipeline_rf_opt, 'models/modelo_random_forest.pkl')` → **448 MB** ⚠️
- [x] `json.dump(FEATURES_NUM + FEATURES_CAT, open('models/features_order.json', 'w'))`
- [x] Verificación: modelo carga y predice correctamente
- [x] ⚠️ **.pkl excluido de git** por tamaño (~450 MB). Solo `features_order.json` y PNGs en el repo.

---

## Sección 6: Preparación de Features para Clustering
**Celdas 63–68**
- [x] Medianas de `IAH`, `precio_m2`, `ratio_cuota_salario`, `tasa_desempleo` por `(city, year)`
- [x] **51 filas** (no 60). Faltan: Armenia (2022–2024), Barranquilla (2022–2024), Cartagena (2022–2024)
- [x] `StandardScaler` ajustado, `X_cluster` de 51×4

---

## Sección 7: KMeans — Segmentación de Mercados
**Celdas 69–78: Determinación de K**
- [x] Codo, silueta y Davies-Bouldin para K=2..10
- [x] **K=5** seleccionado (silueta=0.4874, mejor equilibrio)

**Celdas 79–86: Entrenamiento y análisis**
- [x] KMeans final con K=5 ✅
- [x] **Silueta=0.4874** — cumple umbral ≥ 0.45
- [x] Perfiles:

| Cluster | IAH | precio_m2 | ratio_cuota | tasa_desemp | Count | Nombre |
|---|---:|---:|---:|---:|---:|:---|
| 0 | 29.23 | $4.6M | 2.52 | 15.70 | 6 | Elevado |
| 1 | 16.24 | $2.1M | 1.40 | 15.70 | 18 | Moderado |
| 2 | 18.66 | $3.4M | 2.37 | 10.62 | 12 | Moderado |
| 3 | 25.43 | — | — | — | — | Elevado |
| 4 | 12.87 | — | — | — | — | Moderado |

- [x] Scatter, evolución temporal y heatmap guardados en `models/`

---

## Sección 8: Validación con DBSCAN
**Celdas 87–93**
- [x] eps=0.5: 6 clusters, 22 pts ruido
- [x] eps=0.8: **4 clusters, 8 pts ruido** (Bogotá, Cartagena, Medellín, Pereira)
- [x] eps=1.0: 3 clusters, 0 pts ruido
- [x] DBSCAN confirma que Bogotá, Cartagena, Medellín y Pereira son mercados atípicos

---

## Sección 9: Análisis PCA
**Celdas 94–99**
- [x] PCA 2 componentes: **97.23% varianza explicada**
- [x] PC1 (70.18%): precio_m2 y ratio_cuota_salario dominan
- [x] PC2 (27.05%): tasa_desempleo domina (loading 0.883)
- [x] Scatter PC1 vs PC2: `models/pca_clusters.png`

---

## Sección 10: Exportación del Modelo de Clustering
**Celdas 100–104**
- [x] `models/kmeans_segmentacion.pkl` ✅
- [x] `models/scaler_cluster.pkl` ✅
- [x] `data/processed/ciudades_clusters.csv` ✅ (7.6 KB)
- [x] `data/processed/perfiles_clusters.csv` ✅ (228 bytes)
- [x] ⚠️ `*.pkl` excluido de git (añadido a `.gitignore`)

---

## Sección 11: Resumen Comparativo
**Celdas 105–108**

| Modelo | R² | MAE | RMSE | RMSE rel | CV R² (media) |
|---|---|---|---|---|---|
| Ridge | 0.5382 | $204M | $320M | 76.30% | 0.5305 |
| RF optimizado | **0.6348** | $168M | $285M | 67.86% | 0.6320 |

**Decisión:** Ningún modelo cumple R² ≥ 0.75. RF es el mejor candidato pero requiere mejoras en Fase 5 (transformación log, XGBoost, features adicionales).

---

## Sección 12: Preparación para GitHub
**Celdas 109–114**
- [x] Notebook ejecutado sin errores ✅
- [x] Rutas: absoluta via `os.chdir` + `os.makedirs` (portable)
- [x] `models/*.pkl` en `.gitignore` (448 MB)
- [x] `git commit "feat: Fase 4 - modelos RF y KMeans entrenados y exportados"` ✅
- [x] `docs/FASE_4_COMPLETA.md` actualizado con métricas reales

---

## Entregables Generados

| Archivo | Ruta | Estado | Git |
|---|---|---|---|
| Notebook de modelado | `notebooks/03_modelado.ipynb` | ✅ Ejecutado | Sí |
| Modelo Random Forest | `models/modelo_random_forest.pkl` | ✅ 448 MB | ❌ .gitignore |
| Modelo KMeans | `models/kmeans_segmentacion.pkl` | ✅ 1 KB | ❌ .gitignore |
| Scaler clustering | `models/scaler_cluster.pkl` | ✅ 1 KB | ❌ .gitignore |
| Features order | `models/features_order.json` | ✅ 159 B | Sí |
| Clusters por ciudad-año | `data/processed/ciudades_clusters.csv` | ✅ 7.6 KB | Sí |
| Perfiles de clusters | `data/processed/perfiles_clusters.csv` | ✅ 228 B | Sí |
| Documento de fase | `docs/FASE_4_COMPLETA.md` | ✅ Actualizado | Sí |
| PNGs diagnóstico | `models/*.png` (14 archivos) | ✅ ~800 KB total | Sí |

---

## Recomendaciones para Fase 5

1. **Transformar target**: probar `log(price)` como target para reducir RMSE relativo
2. **Probar otros modelos**: XGBoost, LightGBM (más rápidos, menor huella de RAM)
3. **Feature engineering**: interacciones `city × year`, features geográficas (distancia a CBD), antigüedad del inmueble
4. **Revisar umbrales**: el R² ≥ 0.75 puede no ser realista para datos inmobiliarios con varianza extrema
5. **Santa Marta**: resolver discrepancia con Fase 1 (12 focal cities la incluyen, dataset tiene Armenia)
