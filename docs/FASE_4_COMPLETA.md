# Fase 4 — Modelado
## Proyecto: Accesibilidad de Vivienda en Colombia · CRISP-DM 2025-I
**Responsable principal:** Steve · **Apoyo:** Kukis  
**Estado:** ⏳ Pendiente — requiere dataset corregido de Fase 3 (8 bugs sin corregir)  
**Notebook asociado:** `notebooks/03_modelado.ipynb` *(por ejecutar)*  
**Semanas:** 7 – 8

> ⚠️ **Aviso de auditoría:** Esta fase **no ha sido ejecutada**. El documento describe el diseño metodológico planificado y el código a implementar. Todos los bloques de resultados, métricas, tablas comparativas y hallazgos están marcados como `[PENDIENTE]` y deberán completarse tras la ejecución real. No contiene datos inventados.

---

## Introducción

La Fase 4 de la metodología CRISP-DM corresponde al Modelado. En esta etapa se utilizará el dataset limpio y unificado de la Fase 3 (`vivienda_colombia_limpio.csv` — versión corregida) para diseñar y entrenar modelos que respondan a los objetivos de negocio y preguntas de investigación.

El trabajo se divide en dos enfoques metodológicos:
1. **Modelado Supervisado (Regresión):** Predecir el precio nominal de venta de un inmueble en función de sus características estructurales y del entorno macroeconómico. Se entrenarán y compararán Ridge Regression y Random Forest.
2. **Modelado No Supervisado (Clustering):** Segmentar los mercados inmobiliarios de las 12 ciudades a lo largo del tiempo en función de sus condiciones de accesibilidad y costo. Se empleará KMeans validado con DBSCAN y PCA.

**Prerrequisito bloqueante:** Aplicar los 8 bugs documentados en FASE_3_COMPLETA.md (sección 8 y 15) y re-ejecutar el pipeline de preparación de datos antes de iniciar esta fase.

---

## 1. Justificación de la Selección de Modelos

### 1.1 Modelos de Regresión Evaluados

| Algoritmo | Justificación de Selección | Ventajas Clave | Limitaciones | Parámetros a Optimizar |
|---|---|---|---|---|
| **Ridge Regression** | Baseline lineal. Verifica si las relaciones del mercado son predominantemente lineales. | Alta interpretabilidad, bajo costo computacional, maneja multicolinealidad mediante regularización L2. | No captura interacciones no lineales complejas. | `alpha` (fuerza de regularización). |
| **Random Forest** | Modelo no paramétrico basado en ensambles de árboles (Bagging). | Manejo nativo de variables categóricas, robusto a outliers, calcula `feature_importances_`. | Consumo de memoria elevado, tiende a sobreajustar sin limitación de árboles. | `n_estimators`, `max_depth`, `min_samples_split`. |

### 1.2 Modelos de Clustering Evaluados

| Algoritmo | Justificación de Selección | Ventajas Clave | Limitaciones | Parámetros a Optimizar |
|---|---|---|---|---|
| **KMeans** | Particionamiento espacial por centroides. | Simplicidad, reproducibilidad (semilla fija), fácil asignación de nuevas observaciones. | Asume clústeres esféricos de similar tamaño, sensible a escala. | `n_clusters` (K), `init`, `n_init`. |
| **DBSCAN** | Clustering por densidad para validar estructura y detectar anomalías. | Encuentra clústeres de formas arbitrarias, detecta outliers automáticamente. | Sensible a epsilon y densidad mínima. | `eps`, `min_samples`. |
| **Clustering Jerárquico** | Enfoque aglomerativo para exploración preliminar mediante dendrogramas. | Visualización de subgrupos y jerarquía. | Escalamiento computacional $O(N^2)$ prohibitivo en datasets grandes. | `n_clusters`, `linkage`. |

### 1.3 Criterio de Selección para Producción
Se utilizará **Random Forest** para el predictor de precios si supera al baseline Ridge por más de 10 puntos de R² en validación cruzada. Para la segmentación, se seleccionará **KMeans** como algoritmo principal validado por **DBSCAN** para identificar mercados anómalos.

---

## 2. Preparación de Features para Modelado

### 2.1 Definición de Variables

```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

# Cargar dataset preparado (versión corregida de Fase 3)
df = pd.read_csv("data/processed/vivienda_colombia_limpio.csv")

FEATURES_NUM = ['area', 'rooms', 'bathrooms', 'estrato', 'year', 'ipc_var_anual',
                'tasa_hipotecaria_anual', 'tasa_desempleo', 'ipvu_variacion_anual']
FEATURES_CAT = ['city', 'property_type']
TARGET = 'price'

X = df[FEATURES_NUM + FEATURES_CAT]
y = df[TARGET]
```

### 2.2 Análisis de Multicolinealidad (VIF)

```python
X_vif = sm.add_constant(df[FEATURES_NUM].dropna())
vif_data = pd.DataFrame()
vif_data["feature"] = X_vif.columns
vif_data["VIF"] = [variance_inflation_factor(X_vif.values, i) for i in range(len(X_vif.columns))]
print(vif_data.round(2))
```

**Resultados VIF:** `[PENDIENTE — completar tras ejecutar con dataset corregido]`

> **Criterio de decisión:** Variables con VIF > 10 serán candidatas a eliminación. Variables entre 5–10 se analizarán caso a caso según relevancia de dominio.

### 2.3 Preprocesador con ColumnTransformer

```python
num_transformer = Pipeline(steps=[('scaler', StandardScaler())])
cat_transformer = Pipeline(steps=[('onehot', OneHotEncoder(drop='first', handle_unknown='ignore'))])

preprocessor = ColumnTransformer(transformers=[
    ('num', num_transformer, FEATURES_NUM),
    ('cat', cat_transformer, FEATURES_CAT)
])
```

### 2.4 División Train / Test (80% / 20%)

```python
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
print(f"Set de Entrenamiento: {X_train.shape[0]:,} registros")
print(f"Set de Prueba:        {X_test.shape[0]:,} registros")
```

**Tamaño del set de entrenamiento:** `[PENDIENTE]`  
**Tamaño del set de prueba:** `[PENDIENTE]`

> **Control de data leakage:** La división se realizará a nivel de registro (*row-level shuffle*). La deduplicación de Fase 3 (clave: ciudad + precio + área + tipo + año) minimiza el riesgo de duplicados entre conjuntos. Se validará con la desviación estándar de validación cruzada.

---

## 3. Modelo 1 — Regresión: Predicción de Precio

### 3.1 Entrenamiento y Comparación de Modelos

```python
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import time

modelos = {
    'Ridge': Ridge(alpha=10.0),
    'RandomForest': RandomForestRegressor(n_estimators=100, max_depth=12, random_state=42, n_jobs=-1)
}

resultados = []
for nombre, model in modelos.items():
    pipeline_model = Pipeline(steps=[('preprocessor', preprocessor), ('regressor', model)])
    t0 = time.time()
    pipeline_model.fit(X_train, y_train)
    t_train = time.time() - t0
    y_pred = pipeline_model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100
    rmse_relativo = (rmse / y_test.mean()) * 100
    resultados.append({'Modelo': nombre, 'RMSE (COP)': rmse, 'MAE (COP)': mae,
                       'R²': r2, 'MAPE (%)': mape, 'RMSE Relativo (%)': rmse_relativo,
                       'Tiempo (s)': t_train})
df_res_reg = pd.DataFrame(resultados)
print(df_res_reg.round(3))
```

### 3.2 Tabla Comparativa de Métricas de Regresión

| Modelo Candidato | R² | MAE (COP) | RMSE (COP) | MAPE (%) | RMSE Relativo (%) | Tiempo (s) |
|---|---|---|---|---|---|---|
| **Ridge Regression** | `[PENDIENTE]` | `[PENDIENTE]` | `[PENDIENTE]` | `[PENDIENTE]` | `[PENDIENTE]` | `[PENDIENTE]` |
| **Random Forest** | `[PENDIENTE]` | `[PENDIENTE]` | `[PENDIENTE]` | `[PENDIENTE]` | `[PENDIENTE]` | `[PENDIENTE]` |

> **Criterio de selección:** Random Forest se seleccionará como modelo final si supera a Ridge en más de 10 puntos de R². De lo contrario, se evaluarán modelos adicionales.

**Modelo ganador:** `[PENDIENTE]`

### 3.3 Ajuste de Hiperparámetros (RandomizedSearchCV)

```python
from sklearn.model_selection import RandomizedSearchCV

param_dist = {
    'regressor__n_estimators': [100, 200, 300, 400],
    'regressor__max_depth': [8, 12, 16, 20],
    'regressor__min_samples_split': [5, 10, 20],
    'regressor__min_samples_leaf': [2, 4, 6],
    'regressor__max_features': ['sqrt', 'log2']
}

pipeline_rf = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(random_state=42, n_jobs=-1))
])

search_rf = RandomizedSearchCV(
    pipeline_rf, param_distributions=param_dist, n_iter=10,
    cv=3, scoring='r2', random_state=42, n_jobs=-1, verbose=1
)
search_rf.fit(X_train, y_train)
best_model_rf = search_rf.best_estimator_
print(f"Mejores parámetros: {search_rf.best_params_}")
```

**Mejores parámetros encontrados:** `[PENDIENTE]`  
**R² optimizado en test set:** `[PENDIENTE]` | **MAPE optimizado:** `[PENDIENTE]`%

### 3.4 Análisis de Importancia de Variables

```python
rf_step = best_model_rf.named_steps['regressor']
prep_step = best_model_rf.named_steps['preprocessor']
cat_encoder = prep_step.named_transformers_['cat'].named_steps['onehot']
cat_cols = list(cat_encoder.get_feature_names_out(FEATURES_CAT))
all_features_trans = FEATURES_NUM + cat_cols
importances = rf_step.feature_importances_
indices = np.argsort(importances)[::-1]
for i in range(len(all_features_trans)):
    print(f"{i+1}. {all_features_trans[indices[i]]}: {importances[indices[i]]:.3f}")
```

**Ranking de importancia de variables:** `[PENDIENTE — completar tras ejecutar modelo]`

**Figura generada:** `docs/figures/07_feature_importance.png` `[PENDIENTE]`

### 3.5 Análisis de Errores por Segmento

```python
df_eval = X_test.copy()
df_eval['real'] = y_test
df_eval['pred'] = best_model_rf.predict(X_test)
df_eval['error_abs_pct'] = (np.abs(df_eval['real'] - df_eval['pred']) / df_eval['real']) * 100
print("MAPE por Ciudad:")
print(df_eval.groupby('city')['error_abs_pct'].mean().sort_values().round(2))
```

**MAPE por ciudad:** `[PENDIENTE — completar tras ejecutar modelo]`

### 3.6 Guardado del Modelo

```python
import joblib
joblib.dump(best_model_rf, "models/modelo_random_forest.pkl")
print("Modelo guardado en models/modelo_random_forest.pkl")
```

**Estado del archivo `models/modelo_random_forest.pkl`:** `[PENDIENTE — generar tras ejecución exitosa]`

---

## 4. Modelo 2 — Clustering: Segmentación de Mercados

### 4.1 Construcción del Dataset de Submercados (Ciudad-Año)

```python
df_submercados = df.groupby(['city', 'year']).agg(
    precio_mediano=('price', 'median'),
    IAH_promedio=('IAH', 'mean'),
    ratio_cuota_promedio=('ratio_cuota_salario', 'mean'),
    precio_m2_mediano=('precio_m2', 'median'),
    tasa_desempleo=('tasa_desempleo', 'mean'),
    n_propiedades=('price', 'count')
).reset_index()

df_submercados = df_submercados[df_submercados['n_propiedades'] >= 30].copy()
print(f"Submercados válidos (ciudad-año): {len(df_submercados)}")
```

**Número de submercados ciudad-año válidos:** `[PENDIENTE]`

### 4.2 Escalado de Variables

```python
from sklearn.preprocessing import StandardScaler

VARS_CLUSTER = ['precio_mediano', 'IAH_promedio', 'ratio_cuota_promedio',
                'precio_m2_mediano', 'tasa_desempleo']
scaler_clus = StandardScaler()
X_clus = scaler_clus.fit_transform(df_submercados[VARS_CLUSTER])
```

### 4.3 Selección del Número de Clústeres (K)

```python
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score

inercia, silueta, db_index = [], [], []
rango_k = range(2, 9)

for k in rango_k:
    km = KMeans(n_clusters=k, random_state=42, n_init=15)
    labels = km.fit_predict(X_clus)
    inercia.append(km.inertia_)
    silueta.append(silhouette_score(X_clus, labels))
    db_index.append(davies_bouldin_score(X_clus, labels))
```

**Tabla de métricas por K:**

| K | Inercia | Coef. Silueta | Índice Davies-Bouldin |
|---|---------|--------------|----------------------|
| 2 | `[PENDIENTE]` | `[PENDIENTE]` | `[PENDIENTE]` |
| 3 | `[PENDIENTE]` | `[PENDIENTE]` | `[PENDIENTE]` |
| 4 | `[PENDIENTE]` | `[PENDIENTE]` | `[PENDIENTE]` |
| 5 | `[PENDIENTE]` | `[PENDIENTE]` | `[PENDIENTE]` |
| 6 | `[PENDIENTE]` | `[PENDIENTE]` | `[PENDIENTE]` |

**K óptimo seleccionado:** `[PENDIENTE — determinar tras maximizar Silueta y minimizar Davies-Bouldin]`

### 4.4 Modelo Final KMeans

```python
K_OPTIMO = None  # [PENDIENTE — reemplazar con el valor óptimo determinado]

kmeans_final = KMeans(n_clusters=K_OPTIMO, random_state=42, n_init=20)
df_submercados['cluster'] = kmeans_final.fit_predict(X_clus)

# Ordenar clústeres por IAH promedio y asignar etiquetas cualitativas
centroides = df_submercados.groupby('cluster')[VARS_CLUSTER].mean().reset_index()
centroides_ordenados = centroides.sort_values(by='IAH_promedio').reset_index(drop=True)
# Mapear etiquetas según posición en el ranking de IAH (menor = más accesible)
```

### 4.5 Caracterización de Segmentos Inmobiliarios

> ⚠️ Esta tabla se completa **después de ejecutar el clustering**. No completar con datos estimados.

| Segmento | Precio Mediano (COP) | IAH Promedio (Años) | Ratio Cuota/Salario | Precio m² (COP) | Tasa Desempleo (%) | Ciudades Típicas |
|---|---|---|---|---|---|---|
| **Accesible** | `[PENDIENTE]` | `[PENDIENTE]` | `[PENDIENTE]` | `[PENDIENTE]` | `[PENDIENTE]` | `[PENDIENTE]` |
| **Moderado** | `[PENDIENTE]` | `[PENDIENTE]` | `[PENDIENTE]` | `[PENDIENTE]` | `[PENDIENTE]` | `[PENDIENTE]` |
| **Elevado** | `[PENDIENTE]` | `[PENDIENTE]` | `[PENDIENTE]` | `[PENDIENTE]` | `[PENDIENTE]` | `[PENDIENTE]` |
| **Crítico** | `[PENDIENTE]` | `[PENDIENTE]` | `[PENDIENTE]` | `[PENDIENTE]` | `[PENDIENTE]` | `[PENDIENTE]` |

### 4.6 Validación con DBSCAN

```python
from sklearn.cluster import DBSCAN

dbscan = DBSCAN(eps=0.8, min_samples=3)
dbscan_labels = dbscan.fit_predict(X_clus)
df_submercados['dbscan_label'] = dbscan_labels

outliers = df_submercados[df_submercados['dbscan_label'] == -1][['city', 'year', 'IAH_promedio']]
print("Anomalías identificadas por DBSCAN:")
print(outliers)
```

**Anomalías detectadas:** `[PENDIENTE — completar tras ejecutar]`

### 4.7 Análisis de Transición Temporal de Segmentos

```python
df_submercados.to_csv("data/processed/segmentos_mercado.csv", index=False)

pivot_transicion = df_submercados.pivot(index='city', columns='year', values='segmento')
print(pivot_transicion.fillna('-'))
```

**Tabla de transición histórica por ciudad:** `[PENDIENTE — completar tras ejecutar clustering]`

---

## 5. Modelo 3 — PCA (Análisis de Componentes Principales)

```python
from sklearn.decomposition import PCA

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_clus)
df_submercados['pca1'] = X_pca[:, 0]
df_submercados['pca2'] = X_pca[:, 1]
print(f"Varianza explicada por PC1: {pca.explained_variance_ratio_[0]*100:.2f}%")
print(f"Varianza explicada por PC2: {pca.explained_variance_ratio_[1]*100:.2f}%")
print(f"Varianza acumulada (2 componentes): {np.sum(pca.explained_variance_ratio_)*100:.2f}%")
```

**Varianza explicada por PC1:** `[PENDIENTE]`  
**Varianza explicada por PC2:** `[PENDIENTE]`  
**Varianza acumulada (2 componentes):** `[PENDIENTE]`  
**Interpretación de componentes:** `[PENDIENTE — completar tras ejecutar PCA]`

---

## 6. Hallazgos de la Fase 4

> ⚠️ Esta sección se completa **únicamente después de ejecutar la fase**. No completar con datos estimados o supuestos.

| ID | Hallazgo Clave | Evidencia Numérica | Relevancia para Fase 5 |
|---|---|---|---|
| **H4.1** | Dimensionalidad final tras One-Hot Encoding | `[PENDIENTE]` variables | `[PENDIENTE]` |
| **H4.2** | Rendimiento modelo ganador de regresión | R² = `[PENDIENTE]`, MAPE = `[PENDIENTE]`% | `[PENDIENTE]` |
| **H4.3** | Variable con mayor importancia predictiva | `[PENDIENTE]` | `[PENDIENTE]` |
| **H4.4** | Ciudad con mayor error de predicción | `[PENDIENTE]` (MAPE `[PENDIENTE]`%) | `[PENDIENTE]` |
| **H4.5** | K óptimo de clustering | K = `[PENDIENTE]`, Silueta = `[PENDIENTE]` | `[PENDIENTE]` |
| **H4.6** | Diferencia precio/m² entre segmentos extremos | `[PENDIENTE]` | `[PENDIENTE]` |
| **H4.7** | Anomalías detectadas por DBSCAN | `[PENDIENTE]` | `[PENDIENTE]` |
| **H4.8** | Tendencia temporal de accesibilidad | `[PENDIENTE]` | `[PENDIENTE]` |

---

## 7. Entregables de la Fase 4

| Archivo | Ruta | Estado |
|---------|------|--------|
| Notebook | `notebooks/03_modelado.ipynb` | ⏳ Pendiente de ejecución |
| Pipeline regresión | `models/modelo_random_forest.pkl` | ⏳ Pendiente de generación |
| Dataset de segmentos | `data/processed/segmentos_mercado.csv` | ⏳ Pendiente de generación |
| Figura importancia variables | `docs/figures/07_feature_importance.png` | ⏳ Pendiente |
| Figura diagnósticos regresión | `docs/figures/08_diagnosticos_regresion.png` | ⏳ Pendiente |
| Figura clústeres | `docs/figures/09_clusters_plot.png` | ⏳ Pendiente |

---

## 8. Checklist — Fase 4

- [ ] Aplicar correcciones de Fase 3 y verificar dataset de entrada
- [ ] Construcción de ColumnTransformer para preprocesamiento
- [ ] Análisis VIF y documentar resultados reales obtenidos
- [ ] Entrenamiento y comparación de Ridge y Random Forest
- [ ] Ajuste de hiperparámetros con RandomizedSearchCV
- [ ] Análisis de importancia de variables
- [ ] Exportación del pipeline a pickle
- [ ] Agrupación por ciudad-año y escalado para clustering
- [ ] Selección de K óptimo con Codo, Silueta y Davies-Bouldin
- [ ] Clasificación e interpretación de segmentos de mercado
- [ ] Validación con DBSCAN
- [ ] Análisis de transición temporal
- [ ] Completar sección de hallazgos con datos reales obtenidos
- [ ] Actualizar estado del documento de "Pendiente" a "Completa"

---

## 9. Notas para el Equipo

- **Prerrequisito (Kukis):** No ejecutar esta fase hasta que los 8 bugs de Fase 3 estén corregidos y el dataset final tenga las características esperadas (cobertura multi-fuente, tildes preservadas, lat/lon sin nulos).
- **Para Sofía (Fase 5):** Esta fase alimenta directamente la evaluación. Completar los hallazgos reales de esta fase antes de iniciar Fase 5.
- **Para Kukis (Fase 6):** El predictor del dashboard cargará `models/modelo_random_forest.pkl`. Esperar a que este archivo exista antes de integrar el módulo del predictor.

---

*Documento de Fase 4 · CRISP-DM 2025-I · Proyecto Accesibilidad Habitacional Colombia*  
*Estado: PLANTILLA — completar con datos reales tras ejecutar la fase*
