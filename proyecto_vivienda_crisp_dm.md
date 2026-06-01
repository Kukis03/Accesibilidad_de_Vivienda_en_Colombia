# Proyecto Final — Accesibilidad de Vivienda en Colombia
## Metodología CRISP-DM · Paso a Paso Completo

---

## Pregunta central

> **¿Cuántos salarios mínimos cuesta una vivienda en Colombia y cómo ha cambiado esa relación en el tiempo?**

Variables del proyecto:
- Precio de vivienda (por propiedad, ciudad, barrio)
- Salario mínimo mensual histórico
- Índice de Precios al Consumidor (IPC / inflación)
- Tasa de interés hipotecaria
- Tasa de desempleo

---

## Herramientas del proyecto

| Propósito | Herramienta |
|---|---|
| Exploración y limpieza | Python · pandas · numpy |
| Visualización análisis | matplotlib · seaborn · plotly |
| Modelado | scikit-learn · xgboost |
| Dashboard | Power BI · Tableau · **o Streamlit** |
| Entorno de trabajo | Jupyter Notebook / Google Colab |
| Control de versiones | GitHub |
| Datos | Kaggle · datos.gov.co · DANE · Banco de la República |

---

## Fase 1 — Comprensión del negocio

### Objetivo

Definir con claridad qué se quiere responder antes de tocar un solo dato. Esta fase es estratégica, no técnica.

### Preguntas que guían el proyecto

1. ¿Cuántos salarios mínimos anuales equivale el precio promedio de una vivienda en las principales ciudades de Colombia?
2. ¿Ha aumentado o disminuido la accesibilidad a la vivienda en los últimos 10 años?
3. ¿Qué variable explica mejor la variación en precios: el área, la ciudad, la inflación o la tasa de interés?
4. ¿Existen zonas o ciudades donde la vivienda es prácticamente inalcanzable para un hogar de ingreso mínimo?

### Criterios de éxito del proyecto

- El modelo de regresión predice precios con un error (RMSE) menor al 15% del precio promedio.
- El clustering identifica al menos 3 segmentos diferenciables de accesibilidad.
- El dashboard permite filtrar por ciudad, año y tipo de inmueble de forma interactiva.
- La presentación final responde con datos las 4 preguntas planteadas.

### Entregable de esta fase

Documento de una página (puede ser este mismo .md) con:
- Enunciado del problema
- Preguntas de negocio
- Criterios de éxito
- Stakeholders (en este caso: el jurado / profesor)

---

## Fase 2 — Comprensión de los datos

### Fuentes de datos

#### Dataset principal — Precios de vivienda

| Dataset | Fuente | URL | Descripción |
|---|---|---|---|
| Colombia Housing Properties Price | Kaggle | `kaggle.com/datasets/julianusugaortiz/colombia-housing-properties-price` | Precios reales, área, cuartos, ciudad, coordenadas |
| Colombian Properties | Kaggle | `kaggle.com/datasets/lauramartinezortiz/colombian-properties` | Dataset 2023, más reciente |
| Real Estate Bogotá | Kaggle | `kaggle.com/datasets/pablobravo73/real-estate-bogota` | Foco en Bogotá con barrios |
| Properati Latinoamérica | Kaggle | `kaggle.com/datasets/properati-data/properties` | 1.5M propiedades, incluye Colombia |

#### Variables macroeconómicas

| Variable | Fuente | URL | Notas |
|---|---|---|---|
| Salario mínimo histórico | DANE | `dane.gov.co` | Serie desde 1984, actualización anual |
| IPC / Inflación | DANE | `dane.gov.co/ipc` | Base mensual y anual |
| Tasa hipotecaria | Banco de la República | `banrep.gov.co` | Tasas de crédito hipotecario |
| Tasa de desempleo | DANE — GEIH | `dane.gov.co/geih` | Trimestral por ciudad |
| IPVU (vivienda usada) | datos.gov.co | `datos.gov.co/d/msis-zzf8` | Índice oficial de precios |
| Precios vivienda nueva Bogotá | datosabiertos.bogota.gov.co | Portal Hábitat Bogotá | Desagregado por UPZ |

### Exploración inicial (EDA)

Ejecutar en Jupyter Notebook o Google Colab:

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar el dataset principal
df = pd.read_csv('colombia_housing.csv')

# Vista general
print(df.shape)
print(df.dtypes)
print(df.isnull().sum())
print(df.describe())

# Distribución de precios
plt.figure(figsize=(10, 4))
sns.histplot(df['price'].dropna(), bins=60, kde=True)
plt.title('Distribución de precios de vivienda')
plt.xlabel('Precio (COP)')
plt.show()

# Precio promedio por ciudad
df.groupby('city')['price'].median().sort_values().plot(kind='barh', figsize=(8, 5))
plt.title('Precio mediano por ciudad')
plt.show()

# Mapa de calor de nulos
sns.heatmap(df.isnull(), cbar=False, yticklabels=False)
plt.title('Valores nulos por columna')
plt.show()

# Correlaciones
sns.heatmap(df.select_dtypes(include='number').corr(), annot=True, fmt='.2f', cmap='coolwarm')
plt.title('Matriz de correlación')
plt.show()
```

### Entregable de esta fase

- Notebook de EDA con mínimo 8 gráficas comentadas
- Reporte de calidad de datos: % de nulos por columna, rango de valores, inconsistencias detectadas
- Tabla resumen de las fuentes consolidadas

---

## Fase 3 — Preparación de los datos

### 3.1 Limpieza del dataset de vivienda

```python
import pandas as pd
import numpy as np

df = pd.read_csv('colombia_housing.csv')

# 1. Eliminar registros con precio inválido
df = df[df['price'] > 0]
df = df[df['price'].notna()]

# 2. Estandarizar nombres de ciudades
df['city'] = df['city'].str.lower().str.strip()
mapeo_ciudades = {
    'bogota': 'Bogotá',
    'bogotá': 'Bogotá',
    'medellin': 'Medellín',
    'medellín': 'Medellín',
    'cali': 'Cali',
    'barranquilla': 'Barranquilla',
    'bucaramanga': 'Bucaramanga'
}
df['city'] = df['city'].map(mapeo_ciudades).fillna(df['city'])

# 3. Eliminar outliers de precio usando IQR por ciudad
def remove_price_outliers(group):
    Q1 = group['price'].quantile(0.05)
    Q3 = group['price'].quantile(0.95)
    return group[(group['price'] >= Q1) & (group['price'] <= Q3)]

df = df.groupby('city', group_keys=False).apply(remove_price_outliers)

# 4. Imputar nulos en área por mediana de la ciudad
df['area'] = df.groupby('city')['area'].transform(
    lambda x: x.fillna(x.median())
)

# 5. Extraer año de la columna de fecha
df['year'] = pd.to_datetime(df['created_on'], errors='coerce').dt.year

print(f"Registros después de limpieza: {len(df)}")
```

### 3.2 Cargar y preparar variables macroeconómicas

```python
# Salario mínimo histórico
salario = pd.read_csv('salario_minimo_colombia.csv')
# Columnas esperadas: year, salario_mensual

# IPC anual
ipc = pd.read_csv('ipc_colombia.csv')
# Columnas esperadas: year, ipc_base2018

# Tasa hipotecaria
tasa = pd.read_csv('tasa_hipotecaria.csv')
# Columnas esperadas: year, tasa_anual_pct

# Desempleo
desempleo = pd.read_csv('desempleo_colombia.csv')
# Columnas esperadas: year, city, tasa_desempleo

# Merge de macroeconómicos por año
macro = salario.merge(ipc, on='year').merge(tasa, on='year')
```

### 3.3 Merge final y creación de variables derivadas

```python
# Unir vivienda con macroeconómicos
df_full = df.merge(macro, on='year', how='left')

# También unir desempleo por ciudad y año
df_full = df_full.merge(desempleo, on=['year', 'city'], how='left')

# --- Variables derivadas (las más importantes del proyecto) ---

# Salario anual
df_full['salario_anual'] = df_full['salario_mensual'] * 12

# Índice de accesibilidad: cuántos años de salario cuesta la vivienda
df_full['años_salario'] = df_full['price'] / df_full['salario_anual']

# Precio real (ajustado por inflación, en pesos constantes base 2018)
df_full['precio_real'] = df_full['price'] / (df_full['ipc_base2018'] / 100)

# Cuota mensual hipotecaria estimada (crédito a 15 años, 70% del valor)
def cuota_mensual(precio, tasa_anual):
    monto = precio * 0.70
    r = (tasa_anual / 100) / 12
    n = 15 * 12
    if r == 0:
        return monto / n
    return monto * (r * (1 + r)**n) / ((1 + r)**n - 1)

df_full['cuota_mensual'] = df_full.apply(
    lambda row: cuota_mensual(row['price'], row['tasa_anual_pct']), axis=1
)

# Ratio cuota / salario mínimo (> 0.30 = esfuerzo excesivo)
df_full['ratio_cuota_salario'] = df_full['cuota_mensual'] / df_full['salario_mensual']

# Precio por metro cuadrado
df_full['precio_m2'] = df_full['price'] / df_full['area']

print(df_full[['city', 'year', 'price', 'años_salario', 'ratio_cuota_salario']].describe())
```

### Entregable de esta fase

- Dataset limpio y unificado: `vivienda_colombia_limpio.csv`
- Notebook documentado con cada paso de limpieza y sus justificaciones
- Tabla de variables derivadas con su definición y fórmula

---

## Fase 4 — Modelado

### Modelo 1 — Regresión: predecir precio de vivienda

```python
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

# Variables de entrada y salida
features = ['area', 'rooms', 'bathrooms', 'city', 'year',
            'ipc_base2018', 'tasa_anual_pct', 'tasa_desempleo']
target = 'price'

df_model = df_full[features + [target]].dropna()

X = df_model[features]
y = df_model[target]

# Preprocesamiento
numeric_features = ['area', 'rooms', 'bathrooms', 'year',
                    'ipc_base2018', 'tasa_anual_pct', 'tasa_desempleo']
categorical_features = ['city']

preprocessor = ColumnTransformer([
    ('num', StandardScaler(), numeric_features),
    ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
])

# División train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Entrenar y comparar modelos
modelos = {
    'Regresión Lineal': LinearRegression(),
    'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
    'XGBoost': XGBRegressor(n_estimators=100, random_state=42, verbosity=0)
}

resultados = {}
for nombre, modelo in modelos.items():
    pipe = Pipeline([('prep', preprocessor), ('model', modelo)])
    pipe.fit(X_train, y_train)
    y_pred = pipe.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    resultados[nombre] = {'RMSE': rmse, 'R²': r2}
    print(f"{nombre}: RMSE={rmse:,.0f} | R²={r2:.3f}")
```

### Modelo 2 — Clustering: segmentar zonas por accesibilidad

```python
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# Agrupar por ciudad y año para el clustering
resumen = df_full.groupby(['city', 'year']).agg(
    precio_mediano=('price', 'median'),
    años_salario_promedio=('años_salario', 'mean'),
    ratio_cuota_promedio=('ratio_cuota_salario', 'mean'),
    precio_m2_mediano=('precio_m2', 'median')
).reset_index()

# Escalar variables
X_cluster = resumen[['precio_mediano', 'años_salario_promedio',
                      'ratio_cuota_promedio', 'precio_m2_mediano']]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_cluster)

# Método del codo para elegir k
inertias = []
for k in range(2, 8):
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X_scaled)
    inertias.append(km.inertia_)

plt.plot(range(2, 8), inertias, marker='o')
plt.title('Método del codo — número óptimo de clusters')
plt.xlabel('Número de clusters (k)')
plt.ylabel('Inercia')
plt.show()

# Modelo final con k=3 (bajo, medio, alto acceso)
km_final = KMeans(n_clusters=3, random_state=42, n_init=10)
resumen['cluster'] = km_final.fit_predict(X_scaled)

# Etiquetar clusters
medias = resumen.groupby('cluster')['años_salario_promedio'].mean()
orden = medias.sort_values().index
etiquetas = {orden[0]: 'Accesible', orden[1]: 'Moderado', orden[2]: 'Crítico'}
resumen['accesibilidad'] = resumen['cluster'].map(etiquetas)

print(resumen.groupby('accesibilidad')[
    ['precio_mediano', 'años_salario_promedio', 'ratio_cuota_promedio']
].mean().round(2))
```

### Entregable de esta fase

- Modelos entrenados y guardados con `joblib`
- Tabla comparativa de métricas (RMSE, MAE, R²) para los 3 modelos
- Gráfica de importancia de variables (Random Forest / XGBoost)
- Tabla de clusters con etiquetas interpretables

---

## Fase 5 — Evaluación

### Métricas para regresión

```python
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

# Con el mejor modelo (ejemplo: XGBoost)
y_pred = mejor_modelo.predict(X_test)

mae  = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2   = r2_score(y_test, y_pred)
mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100

print(f"MAE  (error absoluto medio):    ${mae:,.0f} COP")
print(f"RMSE (raíz error cuadrático):   ${rmse:,.0f} COP")
print(f"R²   (varianza explicada):       {r2:.3f}")
print(f"MAPE (error porcentual medio):   {mape:.1f}%")

# Validación cruzada (5-fold)
from sklearn.model_selection import cross_val_score
scores = cross_val_score(mejor_pipeline, X, y,
                         cv=5, scoring='r2')
print(f"\nR² promedio (5-fold CV): {scores.mean():.3f} ± {scores.std():.3f}")
```

### Métricas para clustering

```python
from sklearn.metrics import silhouette_score

score = silhouette_score(X_scaled, resumen['cluster'])
print(f"Coeficiente de silueta: {score:.3f}")
# Valores > 0.5 indican clusters bien definidos
```

### Interpretación en lenguaje de negocio

Al presentar resultados, traducir las métricas a conclusiones concretas. Ejemplos:

- "El modelo explica el **78% de la variación** en precios de vivienda."
- "El **área** es la variable más importante, seguida por la **ciudad** y la **tasa de interés**."
- "En Bogotá, el precio mediano equivale a **18 años de salario mínimo**, mientras que en Bucaramanga son **11 años**."
- "El **32% de los barrios analizados** caen en la categoría 'Crítico': su cuota hipotecaria supera el 50% del salario mínimo."

### Entregable de esta fase

- Tabla de métricas comparativa (todos los modelos)
- Gráfica de residuos (valores reales vs predichos)
- Interpretación en lenguaje de negocio (mínimo 5 conclusiones)
- Validación de que el modelo no está sobreajustado (CV score)

---

## Fase 6 — Despliegue

### Opción A — Power BI o Tableau

Importar el dataset limpio (`vivienda_colombia_limpio.csv`) y construir 4 vistas:

1. **Vista principal**: mapa de Colombia con colores por índice de accesibilidad (años de salario) por ciudad/departamento.
2. **Evolución histórica**: línea de tiempo del índice accesibilidad 2015–2024, con línea del salario mínimo real superpuesta.
3. **Comparador de ciudades**: gráfica de barras comparando años_salario y ratio_cuota_salario por ciudad, con filtro por año.
4. **Resultado del clustering**: mapa de calor o scatter plot de los 3 segmentos (Accesible / Moderado / Crítico) con filtro interactivo.

### Opción B — Streamlit (recomendada para mayor impacto)

Crear `app.py`:

```python
import streamlit as st
import pandas as pd
import plotly.express as px
import joblib

st.set_page_config(page_title="Accesibilidad de Vivienda en Colombia",
                   layout="wide")

st.title("Accesibilidad de Vivienda en Colombia")
st.markdown("¿Cuántos salarios mínimos cuesta una vivienda?")

# Cargar datos
df = pd.read_csv('vivienda_colombia_limpio.csv')

# Filtros en sidebar
ciudad = st.sidebar.selectbox("Ciudad", df['city'].unique())
año    = st.sidebar.slider("Año", int(df['year'].min()), int(df['year'].max()), 2022)

df_filtrado = df[(df['city'] == ciudad) & (df['year'] == año)]

# KPIs principales
col1, col2, col3, col4 = st.columns(4)
col1.metric("Precio mediano",
            f"${df_filtrado['price'].median():,.0f}")
col2.metric("Años de salario",
            f"{df_filtrado['años_salario'].mean():.1f}")
col3.metric("Ratio cuota/salario",
            f"{df_filtrado['ratio_cuota_salario'].mean():.1%}")
col4.metric("Precio por m²",
            f"${df_filtrado['precio_m2'].median():,.0f}")

# Gráfica de evolución histórica
evolucion = df[df['city'] == ciudad].groupby('year')['años_salario'].mean().reset_index()
fig = px.line(evolucion, x='year', y='años_salario',
              title=f'Años de salario mínimo para comprar vivienda — {ciudad}',
              labels={'años_salario': 'Años de salario', 'year': 'Año'})
st.plotly_chart(fig, use_container_width=True)

# Predictor de precio
st.subheader("Estimar precio de una propiedad")
area_input    = st.number_input("Área (m²)", 20, 500, 80)
cuartos_input = st.selectbox("Cuartos", [1, 2, 3, 4, 5])

modelo = joblib.load('modelo_xgboost.pkl')
# (ajustar según las variables del modelo entrenado)
# precio_pred = modelo.predict(...)
# st.success(f"Precio estimado: ${precio_pred[0]:,.0f} COP")
```

Desplegar gratis en **Streamlit Community Cloud** (streamlit.io/cloud) — la app queda con URL pública.

### Entregable de esta fase

- Dashboard funcional (Power BI, Tableau o Streamlit)
- URL pública si se usa Streamlit Cloud
- Repositorio en GitHub con todo el código, notebooks y datos

---

## Estructura del repositorio GitHub

```
proyecto-vivienda-colombia/
│
├── data/
│   ├── raw/                    # Datos originales sin modificar
│   │   ├── colombia_housing.csv
│   │   ├── salario_minimo.csv
│   │   ├── ipc_colombia.csv
│   │   └── tasa_hipotecaria.csv
│   └── processed/
│       └── vivienda_colombia_limpio.csv
│
├── notebooks/
│   ├── 01_EDA.ipynb            # Exploración inicial
│   ├── 02_limpieza.ipynb       # Preparación de datos
│   ├── 03_modelado.ipynb       # Modelos y métricas
│   └── 04_visualizaciones.ipynb
│
├── models/
│   └── modelo_xgboost.pkl      # Modelo guardado
│
├── app/
│   └── app.py                  # Dashboard Streamlit
│
├── docs/
│   └── proyecto_vivienda_crisp_dm.md   # Este documento
│
├── requirements.txt
└── README.md
```

---

## Estructura de la presentación final

| Sección | Contenido | Tiempo sugerido |
|---|---|---|
| 1. Problema | Por qué importa la accesibilidad a la vivienda en Colombia | 2 min |
| 2. Datos y fuentes | Qué datasets se usaron y cómo se combinaron | 3 min |
| 3. Hallazgos del EDA | Distribución de precios, evolución histórica, ciudades más caras | 5 min |
| 4. Variables derivadas | Qué es el índice de accesibilidad y cómo se calculó | 3 min |
| 5. Modelo y métricas | R², RMSE, importancia de variables, clusters | 5 min |
| 6. Dashboard en vivo | Demostración interactiva con filtros | 5 min |
| 7. Conclusiones | ¿Se está volviendo más difícil comprar vivienda en Colombia? | 3 min |
| 8. Preguntas | — | 4 min |

---

## Conclusiones esperadas del análisis

Al finalizar el proyecto, el análisis debería poder responder:

- **¿Cuánto cuesta una vivienda en salarios?** En Bogotá, el precio mediano de un apartamento equivale a entre 15 y 20 años de salario mínimo.
- **¿La brecha creció?** Si el precio real de la vivienda creció más rápido que el salario real, la accesibilidad empeoró.
- **¿Qué ciudad es más accesible?** El clustering permite clasificarlo de forma objetiva y visualizarlo.
- **¿Qué variable importa más?** Con la importancia de variables del modelo se puede responder con datos concretos.

---

*Documento generado para proyecto final de semestre · Metodología CRISP-DM · Universidad · 2024*
