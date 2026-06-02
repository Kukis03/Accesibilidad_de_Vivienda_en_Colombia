# Fase 4 — Modelado
## Notebook: `notebooks/03_modelado.ipynb`
**Responsable:** Steve · **Apoyo:** Kukis  
**Insumo:** `data/processed/vivienda_colombia_limpio.csv`  
**Entregables:** `models/modelo_random_forest.pkl`, `models/kmeans_segmentacion.pkl`  
**Semanas:** 7 – 8

---

## Sección 1: Setup y Carga del Dataset
**Celdas 1–5: Importaciones y configuración**
- [ ] Importar pandas, numpy, matplotlib, seaborn, plotly, joblib
- [ ] Importar desde scikit-learn: `train_test_split`, `ColumnTransformer`, `StandardScaler`, `OneHotEncoder`, `Pipeline`
- [ ] Importar modelos: `Ridge`, `RandomForestRegressor`, `KMeans`, `DBSCAN`
- [ ] Importar métricas: `mean_absolute_error`, `mean_squared_error`, `r2_score`, `silhouette_score`
- [ ] Importar `PCA`, `cross_val_score`, `GridSearchCV`
- [ ] Crear carpeta `models/` si no existe (`os.makedirs("models", exist_ok=True)`)

**Celdas 6–8: Carga y verificación del dataset**
- [ ] Cargar `data/processed/vivienda_colombia_limpio.csv`
- [ ] Verificar shape, tipos de datos y ausencia de nulos
- [ ] Imprimir distribución de `year` y `city` para confirmar cobertura 2019–2024

---

## Sección 2: Preparación de Features
**Celdas 9–14: Definición de variables**
- [ ] Definir `FEATURES_NUM`: `['area', 'rooms', 'bathrooms', 'estrato', 'year', 'ipc_var_anual', 'tasa_hipotecaria_anual', 'tasa_desempleo', 'ipvu_variacion_anual']`
- [ ] Definir `FEATURES_CAT`: `['city', 'property_type']`
- [ ] Definir `TARGET`: `'price'`
- [ ] Crear `X = df[FEATURES_NUM + FEATURES_CAT]` y `y = df[TARGET]`

**Celdas 15–18: Análisis de multicolinealidad (VIF)**
- [ ] Calcular VIF para cada variable numérica usando `statsmodels.stats.outliers_influence.variance_inflation_factor`
- [ ] Imprimir tabla VIF por variable
- [ ] Documentar si alguna variable supera VIF > 10 (no eliminar, solo documentar — Ridge maneja colinealidad)
- [ ] Crear heatmap de correlación entre variables numéricas

**Celdas 19–21: División train / test**
- [ ] Dividir con `train_test_split(X, y, test_size=0.20, random_state=42)`
- [ ] Imprimir shape de X_train, X_test, y_train, y_test
- [ ] Verificar que la distribución de `city` es similar en train y test

**Celdas 22–24: Pipeline de preprocesamiento**
- [ ] Definir `preprocessor = ColumnTransformer` con `StandardScaler` para numéricas y `OneHotEncoder(handle_unknown='ignore')` para categóricas
- [ ] Confirmar que el pipeline no genera fugas de información (fit solo en train)

---

## Sección 3: Modelo Baseline — Ridge Regression
**Celdas 25–32: Entrenamiento y evaluación de Ridge**
- [ ] Construir `pipeline_ridge = Pipeline([('preprocessor', preprocessor), ('regressor', Ridge(alpha=1.0))])`
- [ ] Entrenar con `pipeline_ridge.fit(X_train, y_train)`
- [ ] Predecir sobre X_test
- [ ] Calcular R², MAE, RMSE y RMSE relativo (RMSE / precio mediano × 100)
- [ ] Calcular `cross_val_score(pipeline_ridge, X_train, y_train, cv=5, scoring='r2')`; imprimir media y desviación estándar
- [ ] Crear gráfico `y_test vs y_pred` (scatter de predicciones)
- [ ] Crear gráfico de residuos (residuos vs valores predichos)
- [ ] Imprimir tabla de métricas Ridge vs umbrales de Fase 1

---

## Sección 4: Modelo Principal — Random Forest Regressor
**Celdas 33–42: Entrenamiento inicial de Random Forest**
- [ ] Construir `pipeline_rf = Pipeline([('preprocessor', preprocessor), ('regressor', RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1))])`
- [ ] Entrenar con `pipeline_rf.fit(X_train, y_train)`
- [ ] Predecir sobre X_test
- [ ] Calcular R², MAE, RMSE y RMSE relativo
- [ ] Calcular validación cruzada 5-fold en R² sobre X_train
- [ ] Comparar métricas RF vs Ridge en una tabla resumen
- [ ] Confirmar si RF supera Ridge en R² por más de 10 puntos porcentuales (criterio de selección)

**Celdas 43–50: Importancia de variables y diagnóstico**
- [ ] Extraer `feature_importances_` del Random Forest
- [ ] Recuperar nombres de features tras OneHotEncoder
- [ ] Crear gráfico de barras horizontal de las 15 variables más importantes
- [ ] Crear gráfico `y_test vs y_pred` para Random Forest
- [ ] Crear gráfico de residuos del Random Forest
- [ ] Crear histograma de residuos — verificar aproximación a distribución normal
- [ ] Calcular residuos por ciudad — identificar si hay sesgo sistemático en alguna ciudad

**Celdas 51–57: Optimización de hiperparámetros**
- [ ] Definir `param_grid`: `{'regressor__n_estimators': [100, 200], 'regressor__max_depth': [10, 20, None], 'regressor__min_samples_split': [2, 5]}`
- [ ] Ejecutar `GridSearchCV(pipeline_rf, param_grid, cv=5, scoring='r2', n_jobs=-1)`
- [ ] Imprimir mejores parámetros (`best_params_`) y mejor R² (`best_score_`)
- [ ] Reentrenar pipeline con los mejores hiperparámetros
- [ ] Evaluar modelo optimizado en X_test
- [ ] Actualizar tabla de métricas finales

---

## Sección 5: Exportación del Modelo de Regresión
**Celdas 58–62: Serialización**
- [ ] Guardar pipeline optimizado: `joblib.dump(pipeline_rf_opt, 'models/modelo_random_forest.pkl')`
- [ ] Guardar lista de features en orden: `json.dump(FEATURES_NUM + FEATURES_CAT, open('models/features_order.json', 'w'))`
- [ ] Verificar que el modelo se puede cargar y predice correctamente con un registro de prueba
- [ ] Imprimir: confirmación de archivo guardado y predicción de prueba

---

## Sección 6: Preparación de Features para Clustering
**Celdas 63–68: Construcción del dataset de clustering**
- [ ] Calcular mediana de `IAH`, `precio_m2`, `ratio_cuota_salario` y `tasa_desempleo` por `(city, year)`
- [ ] Crear `df_cluster`: una fila por ciudad-año con esas 4 variables
- [ ] Escalar las 4 variables con `StandardScaler`
- [ ] Confirmar que `df_cluster` tiene `12 ciudades × 6 años = 72 filas` (o las disponibles)

---

## Sección 7: KMeans — Segmentación de Mercados
**Celdas 69–78: Determinación del K óptimo**
- [ ] Calcular inercia (método del codo) para K = 2 a 10
- [ ] Calcular coeficiente de silueta para K = 2 a 10
- [ ] Calcular índice Davies-Bouldin para K = 2 a 10
- [ ] Crear gráfico del codo (inercia vs K)
- [ ] Crear gráfico de silueta vs K
- [ ] Seleccionar K óptimo (esperado K = 4 según criterio de negocio: ≥ 3 clusters diferenciables)

**Celdas 79–86: Entrenamiento y análisis de KMeans**
- [ ] Entrenar `KMeans(n_clusters=K_optimo, init='k-means++', n_init=20, random_state=42)`
- [ ] Asignar etiqueta de cluster a cada fila de `df_cluster`
- [ ] Calcular coeficiente de silueta final — verificar que supera umbral de 0.45 (Fase 1)
- [ ] Calcular media de cada variable por cluster (tabla de perfiles de cluster)
- [ ] Nombrar cualitativamente cada cluster según su perfil (ej. "Inaccesible Alto Costo", "Mercado Moderado")
- [ ] Crear scatter plot IAH vs precio_m2 con puntos coloreados por cluster y etiquetados por ciudad
- [ ] Crear gráfico de líneas: evolución de asignación de cluster por ciudad a lo largo del tiempo (2019–2024)
- [ ] Crear heatmap: ciudad × año con color de cluster asignado

---

## Sección 8: Validación con DBSCAN
**Celdas 87–93: DBSCAN como contraste**
- [ ] Entrenar `DBSCAN` con `eps` calibrado (probar 0.5, 0.8, 1.0) y `min_samples=3`
- [ ] Identificar ciudades marcadas como ruido (label = -1) — son mercados atípicos
- [ ] Comparar asignaciones DBSCAN vs KMeans — ¿coinciden los outliers detectados?
- [ ] Documentar ciudades con comportamiento atípico (esperado: Cartagena por mercado turístico)

---

## Sección 9: Análisis PCA
**Celdas 94–99: Reducción de dimensionalidad para visualización**
- [ ] Aplicar PCA con 2 componentes sobre el dataset de clustering escalado
- [ ] Calcular varianza explicada por cada componente
- [ ] Crear scatter plot PC1 vs PC2 con puntos coloreados por cluster KMeans y etiquetados por ciudad-año
- [ ] Interpretar qué variables cargan más en cada componente principal (biplot)
- [ ] Documentar si los 4 clusters son visualmente separables en el espacio PCA

---

## Sección 10: Exportación del Modelo de Clustering
**Celdas 100–104: Serialización y outputs**
- [ ] Guardar `KMeans`: `joblib.dump(kmeans, 'models/kmeans_segmentacion.pkl')`
- [ ] Guardar `StandardScaler` del clustering: `joblib.dump(scaler_cluster, 'models/scaler_cluster.pkl')`
- [ ] Exportar `df_cluster` con etiquetas asignadas a `data/processed/ciudades_clusters.csv`
- [ ] Guardar tabla de perfiles de clusters a `data/processed/perfiles_clusters.csv`

---

## Sección 11: Resumen Comparativo de Modelos
**Celdas 105–108: Tabla final de resultados**
- [ ] Crear tabla comparativa: Ridge vs Random Forest (R², MAE, RMSE relativo, CV R² std)
- [ ] Crear tabla de criterios de éxito de Fase 1 vs valores obtenidos en Fase 4
- [ ] Redactar celda Markdown con decisión justificada del modelo seleccionado para producción
- [ ] Documentar hiperparámetros finales del modelo elegido

---

## Sección 12: Preparación para GitHub
**Celdas 109–114: Verificación y commit**
- [ ] Ejecutar todas las celdas en kernel limpio (Restart & Run All) sin errores
- [ ] Verificar que NO hay rutas absolutas en el notebook
- [ ] Confirmar que `models/modelo_random_forest.pkl` existe y se puede cargar
- [ ] Confirmar que `models/kmeans_segmentacion.pkl` existe
- [ ] Confirmar que `data/processed/ciudades_clusters.csv` existe
- [ ] `git add notebooks/03_modelado.ipynb models/ data/processed/ciudades_clusters.csv data/processed/perfiles_clusters.csv`
- [ ] Commit: `"feat: Fase 4 - modelos RF y KMeans entrenados y exportados"`
- [ ] Push a rama `development`
- [ ] Actualizar `README.md`: marcar Fase 4 como completada
- [ ] Crear `docs/FASE_4_COMPLETA.md` con hallazgos y métricas finales

---

## Entregables de Fase 4

| Archivo | Ruta | Descripción |
|---|---|---|
| Notebook de modelado | `notebooks/03_modelado.ipynb` | Pipeline completo de entrenamiento supervisado y no supervisado |
| Modelo Random Forest | `models/modelo_random_forest.pkl` | Pipeline serializado para predicción de precios |
| Modelo KMeans | `models/kmeans_segmentacion.pkl` | Modelo de segmentación de mercados |
| Scaler clustering | `models/scaler_cluster.pkl` | StandardScaler ajustado para las 4 features del clustering |
| Features order | `models/features_order.json` | Orden de features para alimentar el modelo en producción |
| Clusters por ciudad-año | `data/processed/ciudades_clusters.csv` | Asignación de cluster a cada combinación ciudad-año |
| Perfiles de clusters | `data/processed/perfiles_clusters.csv` | Estadísticas descriptivas por cluster |
| Documento de fase | `docs/FASE_4_COMPLETA.md` | Reporte con métricas, gráficas y justificación de decisiones |
