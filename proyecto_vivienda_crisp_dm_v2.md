# Proyecto Final — Accesibilidad de Vivienda en Colombia
## Metodología CRISP-DM · Análisis Predictivo y Descriptivo

**Asignatura:** Minería de Datos / Ciencia de Datos  
**Semestre:** 2025-I  
**Integrantes:** Steve · Sofía · Kukis  
**Repositorio:** `github.com/[usuario]/proyecto-vivienda-colombia`

---

## Resumen Ejecutivo

Este proyecto analiza la accesibilidad a la vivienda en Colombia entre 2015 y 2024, integrando datos de precios inmobiliarios con variables macroeconómicas (salario mínimo, inflación, tasas hipotecarias y desempleo). Se construye un índice propio de accesibilidad habitacional, se entrena un modelo predictivo de precios y se segmentan los mercados urbanos según su nivel de acceso real para hogares de ingreso mínimo. El resultado es un dashboard interactivo que permite explorar la evolución temporal de la brecha entre ingresos y precios de vivienda en las principales ciudades del país.

---

## Pregunta Central de Investigación

> **¿Cómo ha evolucionado la accesibilidad económica a la vivienda en Colombia entre 2015 y 2024, y qué variables estructurales explican mejor las diferencias entre ciudades?**

### Preguntas Derivadas

1. ¿Cuántos años de salario mínimo equivale el precio mediano de vivienda en las principales ciudades colombianas, y cómo ha cambiado esa relación en los últimos 10 años?
2. ¿Qué variables (área, ciudad, inflación, tasa hipotecaria, desempleo) tienen mayor poder predictivo sobre el precio de una propiedad?
3. ¿Es posible clasificar objetivamente los mercados de vivienda urbana en segmentos diferenciables de accesibilidad mediante técnicas de clustering?
4. ¿En qué ciudades o zonas la cuota hipotecaria supera el umbral del 30% del ingreso mensual, comprometiendo la viabilidad financiera de los hogares?

---

## Herramientas del Proyecto

| Propósito | Herramienta |
|---|---|
| Exploración y limpieza | Python · pandas · numpy |
| Visualización exploratoria | matplotlib · seaborn · plotly |
| Modelado supervisado | scikit-learn · xgboost · shap |
| Modelado no supervisado | scikit-learn (KMeans, DBSCAN) |
| Dashboard interactivo | Streamlit |
| Entorno de trabajo | Jupyter Notebook / Google Colab |
| Control de versiones | GitHub (rama por fase CRISP-DM) |
| Fuentes de datos | Kaggle · datos.gov.co · DANE · Banco de la República · Geoportal IGAC |

---

## Distribución de Responsabilidades

| Fase CRISP-DM | Responsable principal | Apoyo |
|---|---|---|
| Fase 1 — Comprensión del negocio | **Sofía** | Todos |
| Fase 2 — Comprensión de los datos | **Steve** | Sofía |
| Fase 3 — Preparación de los datos | **Kukis** | Steve |
| Fase 4 — Modelado | **Steve** | Kukis |
| Fase 5 — Evaluación | **Sofía** | Steve |
| Fase 6 — Despliegue (dashboard) | **Kukis** | Sofía |
| Presentación final | **Todos** (rotación de secciones) | — |

> La distribución garantiza que cada integrante lidera dos fases contiguas del ciclo y apoya la fase del compañero siguiente, promoviendo transferencia de conocimiento y revisión cruzada.

---

## Fase 1 — Comprensión del Negocio

**Responsable principal: Sofía**

### 1.1 Contexto y Justificación

La vivienda es el activo más costoso que adquiere un hogar a lo largo de su vida. En Colombia, el déficit habitacional cuantitativo supera el millón de unidades, y el precio de la vivienda ha crecido sostenidamente por encima del salario mínimo real durante la última década. Comprender esta brecha no es solo un ejercicio académico: es insumo directo para políticas públicas, decisiones de inversión y planificación urbana.

El indicador internacional más utilizado para medir accesibilidad habitacional es el **Price-to-Income Ratio (PIR)**: la razón entre el precio mediano de una vivienda y el ingreso anual mediano del hogar. Un PIR superior a 5 se considera crítico por organismos como la OCDE y ONU-Hábitat. Este proyecto construye una versión del PIR adaptada al contexto colombiano, incorporando el salario mínimo como proxy del ingreso de referencia.

### 1.2 Objetivos del Proyecto

**Objetivo general:**  
Desarrollar un sistema de análisis y predicción de accesibilidad habitacional en Colombia, basado en la integración de datos inmobiliarios y macroeconómicos, que permita identificar patrones espaciales y temporales de inequidad en el acceso a la vivienda.

**Objetivos específicos:**
1. Construir y validar un índice compuesto de accesibilidad habitacional (IAH) para las principales ciudades colombianas entre 2015 y 2024.
2. Entrenar y comparar modelos de regresión para predecir el precio de una propiedad con base en sus características y el contexto macroeconómico.
3. Segmentar los mercados de vivienda urbana mediante clustering no supervisado para identificar grupos de ciudades con comportamientos similares.
4. Desplegar los resultados en un dashboard interactivo de acceso público que permita exploración por ciudad, año y tipo de inmueble.

### 1.3 Criterios de Éxito

| Criterio | Métrica | Umbral mínimo aceptable |
|---|---|---|
| Precisión del modelo de regresión | RMSE relativo | < 15% del precio mediano |
| Bondad de ajuste del modelo | R² en conjunto de prueba | ≥ 0.75 |
| Calidad del clustering | Coeficiente de silueta | ≥ 0.45 |
| Separabilidad de clusters | Número de segmentos diferenciables | ≥ 3 |
| Cobertura geográfica | Ciudades representadas | ≥ 8 ciudades principales |
| Cobertura temporal | Años cubiertos | 2015 – 2024 |
| Funcionalidad del dashboard | Filtros operativos | Ciudad, año, tipo de inmueble |
| Respuesta a preguntas de investigación | Conclusiones con evidencia cuantitativa | 4 de 4 preguntas respondidas |

### 1.4 Stakeholders y Audiencia

| Stakeholder | Interés |
|---|---|
| Jurado / Profesor | Rigor metodológico, calidad del análisis, claridad en la presentación |
| Potencial comprador de vivienda | ¿Puedo costear una vivienda en mi ciudad con mi ingreso actual? |
| Investigador de política pública | ¿En qué ciudades se requiere intervención prioritaria? |
| Entidad financiera | ¿Cuál es el riesgo de impago hipotecario por ciudad? |

### 1.5 Supuestos y Restricciones

**Supuestos:**
- Los precios de los datasets de Kaggle y fuentes oficiales son representativos del mercado real, aunque pueden excluir transacciones informales.
- El salario mínimo legal se usa como proxy del ingreso de referencia para hogares de bajos ingresos.
- Las propiedades listadas en plataformas digitales representan mayoritariamente vivienda formal.

**Restricciones:**
- No se dispone de datos catastrales georreferenciados a nivel de predio para todas las ciudades.
- La disponibilidad de datos históricos puede variar por fuente y ciudad.
- El análisis se limita a vivienda urbana; la vivienda rural queda fuera del alcance.

### Entregable de Fase 1

Documento de planificación aprobado (este archivo) que incluye: enunciado del problema, preguntas de investigación, objetivos, criterios de éxito, stakeholders, supuestos y restricciones. Extensión: 2–3 páginas. Formato: Markdown en repositorio GitHub.

**Fecha de entrega:** Semana 2 del proyecto.

---

## Fase 2 — Comprensión de los Datos

**Responsable principal: Steve | Apoyo: Sofía**

### 2.1 Inventario de Fuentes de Datos

#### Dataset A — Precios de vivienda (fuente principal)

| # | Dataset | Fuente | URL | Registros aprox. | Período |
|---|---|---|---|---|---|
| A1 | Colombia Housing Properties Price | Kaggle | `kaggle.com/datasets/julianusugaortiz/colombia-housing-properties-price` | ~120.000 | 2018–2022 |
| A2 | Colombian Properties 2023 | Kaggle | `kaggle.com/datasets/lauramartinezortiz/colombian-properties` | ~50.000 | 2023 |
| A3 | Real Estate Bogotá (por barrio) | Kaggle | `kaggle.com/datasets/pablobravo73/real-estate-bogota` | ~30.000 | 2019–2022 |
| A4 | Properati Latinoamérica | Kaggle | `kaggle.com/datasets/properati-data/properties` | ~1.500.000 (filtrar Colombia) | 2015–2021 |

**Estrategia de integración de los datasets A:** Se priorizará A4 (Properati) como fuente histórica por su cobertura temporal amplia. A1 y A2 se usarán para actualización y validación cruzada. A3 enriquecerá el análisis a nivel de barrio para Bogotá. La columna `l3` (ciudad) permitirá el filtrado por mercado.

#### Dataset B — Variables macroeconómicas

| # | Variable | Fuente | URL / Tabla | Frecuencia | Período disponible |
|---|---|---|---|---|---|
| B1 | Salario mínimo legal mensual | DANE | `dane.gov.co → Series estadísticas` | Anual | 1984 – 2025 |
| B2 | IPC (Índice de Precios al Consumidor) | DANE | `dane.gov.co/ipc` | Mensual | 2000 – presente |
| B3 | Tasa de interés crédito hipotecario | Banco de la República | `banrep.gov.co → Series de datos` | Mensual | 2000 – presente |
| B4 | Tasa de desempleo por ciudad | DANE – GEIH | `dane.gov.co/geih` | Trimestral | 2006 – presente |
| B5 | IPVU (vivienda usada) | datos.gov.co | `datos.gov.co/d/msis-zzf8` | Trimestral | 2010 – presente |
| B6 | PIB per cápita departamental | DANE – Cuentas nacionales | `dane.gov.co` | Anual | 2010 – presente |

#### Dataset C — Datos geoespaciales y contextuales (enriquecimiento)

| # | Variable | Fuente | Descripción |
|---|---|---|---|
| C1 | Coordenadas y estratos socioeconómicos | Geoportal IGAC / Secretarías distritales | Estrato 1–6 por barrio en ciudades principales |
| C2 | Precios vivienda nueva Bogotá | datosabiertos.bogota.gov.co | Desagregado por UPZ (Unidad de Planeamiento Zonal) |
| C3 | Déficit habitacional por municipio | DANE – Censo 2018 | Déficit cuantitativo y cualitativo |

### 2.2 Esquema Esperado de las Variables Principales

#### Dataset A (vivienda) — columnas clave:

| Columna | Tipo | Descripción | Valores esperados |
|---|---|---|---|
| `price` | float | Precio en pesos colombianos | 50.000.000 – 5.000.000.000 |
| `area` | float | Área en metros cuadrados | 20 – 1.000 |
| `rooms` | int | Número de habitaciones | 1 – 10 |
| `bathrooms` | int | Número de baños | 1 – 8 |
| `property_type` | str | Apartamento / Casa / Lote | Categórica |
| `city` | str | Ciudad | Bogotá, Medellín, Cali, etc. |
| `lat` / `lon` | float | Coordenadas geográficas | Colombia: lat 1°–12°N |
| `created_on` | date | Fecha del anuncio | 2015 – 2024 |

#### Dataset B (macroeconómico) — estructura objetivo tras integración:

| Columna | Tipo | Descripción |
|---|---|---|
| `year` | int | Año de referencia |
| `month` | int | Mes (1–12) |
| `salario_mensual` | float | Salario mínimo mensual vigente (COP) |
| `ipc_var_anual` | float | Variación anual del IPC (%) |
| `tasa_hipotecaria` | float | Tasa de interés crédito hipotecario (% anual) |
| `tasa_desempleo_ciudad` | float | Desempleo trimestral por ciudad (%) |
| `ipvu_variacion` | float | Variación del índice de precios vivienda usada (%) |

### 2.3 Exploración Inicial (EDA) — Notebook 01

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# ----- 2.3.1 Carga y vista general -----
df = pd.read_csv('data/raw/properati_colombia.csv')

print(f"Dimensiones: {df.shape}")
print(f"\nTipos de datos:\n{df.dtypes}")
print(f"\nNulos por columna (%):\n{(df.isnull().mean() * 100).round(1)}")
print(f"\nEstadísticas descriptivas:\n{df.describe()}")

# ----- 2.3.2 Distribución de precios (escala log) -----
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].set_title('Distribución de precios (escala original)')
sns.histplot(df['price'].dropna(), bins=80, kde=True, ax=axes[0])
axes[0].set_xlabel('Precio (COP)')

axes[1].set_title('Distribución de precios (escala logarítmica)')
sns.histplot(df['price'].dropna().apply(lambda x: x if x > 0 else None),
             bins=80, kde=True, log_scale=True, ax=axes[1])
axes[1].set_xlabel('Precio (COP, log)')
plt.tight_layout()
plt.savefig('docs/figures/02_distribucion_precios.png', dpi=150)
plt.show()

# ----- 2.3.3 Precio mediano por ciudad -----
precio_ciudad = (
    df.groupby('city')['price']
    .median()
    .sort_values(ascending=False)
    .head(15)
)
fig = px.bar(precio_ciudad.reset_index(),
             x='price', y='city', orientation='h',
             title='Precio mediano por ciudad (Top 15)',
             labels={'price': 'Precio mediano (COP)', 'city': 'Ciudad'})
fig.write_html('docs/figures/03_precio_ciudad.html')
fig.show()

# ----- 2.3.4 Evolución del precio promedio anual -----
df['year'] = pd.to_datetime(df['created_on'], errors='coerce').dt.year
evolucion = df.groupby('year')['price'].median().reset_index()
fig = px.line(evolucion, x='year', y='price',
              title='Evolución del precio mediano anual (todas las ciudades)',
              markers=True)
fig.show()

# ----- 2.3.5 Relación área-precio -----
muestra = df.sample(min(5000, len(df)), random_state=42)
fig = px.scatter(muestra, x='area', y='price', color='city',
                 title='Relación Área vs Precio por ciudad',
                 opacity=0.4, log_y=True,
                 labels={'area': 'Área (m²)', 'price': 'Precio (COP, log)'})
fig.show()

# ----- 2.3.6 Mapa de calor de nulos -----
plt.figure(figsize=(10, 4))
sns.heatmap(df.isnull(), cbar=False, yticklabels=False, cmap='viridis')
plt.title('Mapa de valores nulos por columna')
plt.savefig('docs/figures/04_nulos.png', dpi=150)
plt.show()

# ----- 2.3.7 Correlación entre variables numéricas -----
num_cols = df.select_dtypes(include='number').columns
plt.figure(figsize=(10, 8))
sns.heatmap(df[num_cols].corr(), annot=True, fmt='.2f', cmap='coolwarm',
            center=0, square=True)
plt.title('Matriz de correlación')
plt.savefig('docs/figures/05_correlacion.png', dpi=150)
plt.show()

# ----- 2.3.8 Volumen de registros por fuente y año -----
print(df.groupby(['year', 'property_type']).size().unstack(fill_value=0))
```

### 2.4 Requerimientos de Calidad de Datos

Para que un registro sea apto para el análisis debe cumplir:

| Requerimiento | Criterio de inclusión |
|---|---|
| Precio válido | `price > 0` y no nulo |
| Área válida | `area > 0` y no nula |
| Ciudad identificable | `city` en el listado de ciudades del proyecto |
| Fecha presente | `created_on` parseable a año entre 2015 y 2024 |
| Tipo de propiedad | Apartamento o Casa (excluir lotes en modelo principal) |
| Precio razonable | Entre percentil 2 y 98 por ciudad (eliminar outliers extremos) |

### 2.5 Entregable de Fase 2

**Responsable:** Steve  
**Fecha:** Semana 3–4 del proyecto

- Notebook `01_EDA.ipynb` con mínimo 10 visualizaciones comentadas (una por hallazgo clave).
- Reporte de calidad de datos: porcentaje de nulos por columna, rango de valores, inconsistencias detectadas, decisiones tomadas.
- Tabla resumen de fuentes consolidadas con volumen de registros por fuente, ciudad y año.
- Archivo `data/raw/README.md` que documenta el origen, descarga y estructura de cada dataset.

---

## Fase 3 — Preparación de los Datos

**Responsable principal: Kukis | Apoyo: Steve**

### 3.1 Requerimientos del Dataset Final

El dataset limpio (`vivienda_colombia_limpio.csv`) debe cumplir los siguientes requerimientos antes de avanzar al modelado:

| Requerimiento | Verificación |
|---|---|
| Sin valores nulos en variables de modelado | `df[features].isnull().sum() == 0` |
| Precios en escala consistente (COP corriente) | Documentación de conversión si aplica |
| Ciudades estandarizadas | Nombre único por ciudad, sin variantes tipográficas |
| Variables macroeconómicas integradas por año | `df.merge(macro, on='year')` sin pérdida > 5% |
| Variables derivadas calculadas y validadas | Ver sección 3.3 |
| Dataset guardado en `data/processed/` | `vivienda_colombia_limpio.csv` |
| Notebook documentado con cada decisión | Justificación de cada paso de limpieza |

### 3.2 Limpieza del Dataset de Vivienda

```python
import pandas as pd
import numpy as np

# ----- Cargar fuentes y unificar -----
df_a4 = pd.read_csv('data/raw/properati_colombia.csv')        # Fuente histórica
df_a1 = pd.read_csv('data/raw/colombia_housing.csv')          # Actualización
df_a2 = pd.read_csv('data/raw/colombian_properties_2023.csv') # 2023

# Estandarizar columnas mínimas antes de concatenar
COLS_COMUNES = ['price', 'area', 'rooms', 'bathrooms',
                'property_type', 'city', 'lat', 'lon', 'created_on']

def normalizar_columnas(df, mapa):
    """Renombra columnas según el mapa {nombre_original: nombre_estandar}."""
    return df.rename(columns=mapa)

# Aplicar mapeos según la estructura de cada fuente (ajustar según inspección real)
df_a4 = normalizar_columnas(df_a4, {'l3': 'city', 'surface_total': 'area'})
df = pd.concat([df_a4[COLS_COMUNES],
                df_a1[COLS_COMUNES],
                df_a2[COLS_COMUNES]], ignore_index=True)

print(f"Registros totales antes de limpieza: {len(df):,}")

# ----- 3.2.1 Filtrar precios inválidos -----
df = df[(df['price'] > 0) & df['price'].notna()]

# ----- 3.2.2 Estandarizar ciudades -----
df['city'] = df['city'].str.lower().str.strip()
MAPA_CIUDADES = {
    'bogota': 'Bogotá', 'bogotá': 'Bogotá', 'santa fe de bogota': 'Bogotá',
    'medellin': 'Medellín', 'medellín': 'Medellín',
    'cali': 'Cali', 'santiago de cali': 'Cali',
    'barranquilla': 'Barranquilla',
    'bucaramanga': 'Bucaramanga',
    'cartagena': 'Cartagena',
    'pereira': 'Pereira',
    'manizales': 'Manizales',
    'cucuta': 'Cúcuta', 'cúcuta': 'Cúcuta'
}
CIUDADES_VALIDAS = set(MAPA_CIUDADES.values())
df['city'] = df['city'].map(MAPA_CIUDADES)
df = df[df['city'].isin(CIUDADES_VALIDAS)]

# ----- 3.2.3 Extraer año de la fecha -----
df['year'] = pd.to_datetime(df['created_on'], errors='coerce').dt.year
df = df[(df['year'] >= 2015) & (df['year'] <= 2024)]

# ----- 3.2.4 Filtrar tipo de propiedad -----
df['property_type'] = df['property_type'].str.lower()
df = df[df['property_type'].isin(['apartamento', 'casa', 'apartment', 'house'])]
df['property_type'] = df['property_type'].replace(
    {'apartment': 'Apartamento', 'house': 'Casa',
     'apartamento': 'Apartamento', 'casa': 'Casa'}
)

# ----- 3.2.5 Eliminar outliers de precio por ciudad y año (IQR 5-95) -----
def remover_outliers_precio(grupo):
    q_low  = grupo['price'].quantile(0.05)
    q_high = grupo['price'].quantile(0.95)
    return grupo[(grupo['price'] >= q_low) & (grupo['price'] <= q_high)]

df = df.groupby(['city', 'year'], group_keys=False).apply(remover_outliers_precio)

# ----- 3.2.6 Imputar nulos en área por mediana ciudad-año -----
df['area'] = df.groupby(['city', 'year'])['area'].transform(
    lambda x: x.fillna(x.median())
)

# ----- 3.2.7 Imputar nulos en habitaciones y baños -----
df['rooms'] = df.groupby(['city', 'property_type'])['rooms'].transform(
    lambda x: x.fillna(x.median())
).fillna(3)  # fallback global

df['bathrooms'] = df.groupby(['city', 'property_type'])['bathrooms'].transform(
    lambda x: x.fillna(x.median())
).fillna(2)

print(f"Registros después de limpieza: {len(df):,}")
print(f"Registros descartados: {len(df) - len(df):,}")
print(f"\nDistribución por ciudad:\n{df['city'].value_counts()}")
```

### 3.3 Preparación de Variables Macroeconómicas

```python
# ----- Cargar fuentes macroeconómicas -----
salario = pd.read_csv('data/raw/salario_minimo_colombia.csv')
# Columnas: year, salario_mensual (COP corriente)

ipc = pd.read_csv('data/raw/ipc_colombia_anual.csv')
# Columnas: year, ipc_var_anual (%), ipc_base2018 (índice)

tasa = pd.read_csv('data/raw/tasa_hipotecaria.csv')
# Columnas: year, tasa_hipotecaria_anual (%)

desempleo = pd.read_csv('data/raw/desempleo_ciudades.csv')
# Columnas: year, city, tasa_desempleo (%)

ipvu = pd.read_csv('data/raw/ipvu_trimestral.csv')
# Columnas: year, ipvu_variacion_anual (%)

# ----- Consolidar macroeconómicos -----
macro = (salario
         .merge(ipc,   on='year', how='inner')
         .merge(tasa,  on='year', how='inner')
         .merge(ipvu,  on='year', how='left'))

# Validar cobertura temporal
print(f"Macro cubre años: {macro['year'].min()} – {macro['year'].max()}")
print(f"Registros macro: {len(macro)}")
print(macro.isnull().sum())
```

### 3.4 Integración Final y Variables Derivadas

```python
# ----- Merge vivienda + macroeconómicos -----
df_full = df.merge(macro, on='year', how='left')
df_full = df_full.merge(desempleo, on=['year', 'city'], how='left')

cobertura = df_full['salario_mensual'].notna().mean()
print(f"Cobertura macroeconómica: {cobertura:.1%}")
assert cobertura >= 0.95, "Cobertura insuficiente: revisar fechas del merge"

# ----- Variables derivadas (núcleo analítico del proyecto) -----

# 1. Salario anual
df_full['salario_anual'] = df_full['salario_mensual'] * 12

# 2. Índice de accesibilidad habitacional (IAH) — Price-to-Income Ratio
#    Número de años de salario mínimo necesarios para comprar la vivienda
df_full['IAH'] = df_full['price'] / df_full['salario_anual']

# 3. Precio real ajustado por inflación (pesos constantes base 2018)
df_full['precio_real'] = df_full['price'] / (df_full['ipc_base2018'] / 100)

# 4. Precio por metro cuadrado
df_full['precio_m2'] = df_full['price'] / df_full['area']

# 5. Cuota mensual hipotecaria estimada
#    Supuesto: crédito a 15 años, financiación del 70% del valor, cuota fija (sistema francés)
def calcular_cuota_mensual(precio, tasa_anual_pct, plazo_años=15, pct_financiado=0.70):
    monto = precio * pct_financiado
    r = (tasa_anual_pct / 100) / 12  # tasa mensual
    n = plazo_años * 12              # número de cuotas
    if r == 0 or pd.isna(r):
        return monto / n
    return monto * (r * (1 + r)**n) / ((1 + r)**n - 1)

df_full['cuota_mensual'] = df_full.apply(
    lambda row: calcular_cuota_mensual(row['price'], row['tasa_hipotecaria_anual']),
    axis=1
)

# 6. Ratio cuota / salario mínimo
#    Umbral crítico: > 0.30 (30%) según estándar internacional de vivienda asequible
df_full['ratio_cuota_salario'] = df_full['cuota_mensual'] / df_full['salario_mensual']

# 7. Clasificación de accesibilidad por registro
def clasificar_accesibilidad(iah):
    if iah <= 5:
        return 'Accesible'
    elif iah <= 10:
        return 'Moderado'
    elif iah <= 20:
        return 'Elevado'
    else:
        return 'Crítico'

df_full['nivel_accesibilidad'] = df_full['IAH'].apply(clasificar_accesibilidad)

# ----- Guardar dataset limpio -----
df_full.to_csv('data/processed/vivienda_colombia_limpio.csv', index=False)
print(f"\nDataset guardado: {len(df_full):,} registros, {df_full.shape[1]} variables")
print(f"\nTabla de variables derivadas:\n{df_full[['city','year','price','IAH','precio_real','cuota_mensual','ratio_cuota_salario']].describe().round(2)}")
```

### 3.5 Tabla de Variables Derivadas

| Variable | Fórmula | Interpretación | Unidad |
|---|---|---|---|
| `salario_anual` | `salario_mensual × 12` | Ingreso anual de referencia | COP |
| `IAH` | `price / salario_anual` | Años de salario para comprar la vivienda | Años |
| `precio_real` | `price / (IPC_base2018 / 100)` | Precio a pesos constantes 2018 | COP (real) |
| `precio_m2` | `price / area` | Valor del metro cuadrado construido | COP/m² |
| `cuota_mensual` | Sistema francés, 15 años, 70% financiado | Pago mensual hipotecario estimado | COP/mes |
| `ratio_cuota_salario` | `cuota_mensual / salario_mensual` | Proporción del ingreso comprometida en la cuota | Adimensional |
| `nivel_accesibilidad` | Clasificación basada en IAH (umbral OCDE) | Categoría de acceso: Accesible / Moderado / Elevado / Crítico | Categórica |

### 3.6 Entregable de Fase 3

**Responsable:** Kukis  
**Fecha:** Semana 5–6 del proyecto

- Notebook `02_preparacion_datos.ipynb` documentado con cada decisión de limpieza y su justificación (ej: "se eliminaron precios < percentil 5 porque corresponden a lotes o errores de carga").
- Archivo `data/processed/vivienda_colombia_limpio.csv` listo para modelado.
- Tabla comparativa: registros antes/después de cada paso de limpieza.
- Tabla de variables derivadas con definición, fórmula y estadísticas descriptivas básicas.

---

## Fase 4 — Modelado

**Responsable principal: Steve | Apoyo: Kukis**

### 4.1 Justificación de la Selección de Modelos

Se entrenan tres modelos para la tarea de regresión y dos enfoques para la segmentación. La elección se justifica así:

#### Modelos de Regresión (predicción de precio)

| Modelo | Justificación | Limitación conocida |
|---|---|---|
| **Regresión Lineal** | Baseline interpretable. Permite entender relaciones lineales directas entre área, ciudad y precio. Útil para detectar multicolinealidad. | Asume linealidad; no captura interacciones complejas entre variables. |
| **Random Forest** | Maneja bien variables categóricas codificadas, es robusto a outliers residuales y produce importancia de variables fácilmente interpretable. | Mayor costo computacional. Puede sobreajustar si los árboles son muy profundos. |
| **XGBoost** | Modelo de boosting gradiente con regularización integrada. Históricamente superior en datasets tabulares con variables mixtas. La regularización L1/L2 reduce el sobreajuste. | Requiere ajuste de hiperparámetros (n_estimators, max_depth, learning_rate). |

**Modelo seleccionado para producción:** XGBoost, condicionado a que supere a Random Forest en el conjunto de prueba. En caso contrario, se selecciona el de mayor R² con menor RMSE relativo.

#### Modelos de Clustering (segmentación de mercados)

| Modelo | Justificación | Limitación conocida |
|---|---|---|
| **KMeans (k=3 a 5)** | Algoritmo bien conocido, resultados reproducibles, permite elegir k mediante método del codo y silueta. Clusters de tamaño comparable. | Asume clusters esféricos. Sensible a la escala: requiere normalización. |
| **DBSCAN** | Detecta clusters de forma arbitraria y marca automáticamente outliers (ciudades atípicas). No requiere especificar k. | Sensible a los parámetros epsilon y min_samples; difícil calibrar. |

**Decisión:** Se usará KMeans como modelo principal de clustering por su interpretabilidad, y DBSCAN como validación para detectar posibles outliers geográficos.

### 4.2 Modelo 1 — Regresión: Predicción de Precio

```python
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np
import shap
import joblib

# ----- 4.2.1 Definir variables -----
FEATURES_NUM = ['area', 'rooms', 'bathrooms', 'year',
                'ipc_var_anual', 'tasa_hipotecaria_anual',
                'tasa_desempleo', 'ipvu_variacion_anual']
FEATURES_CAT = ['city', 'property_type']
TARGET = 'price'

df_model = df_full[FEATURES_NUM + FEATURES_CAT + [TARGET]].dropna()
X = df_model[FEATURES_NUM + FEATURES_CAT]
y = df_model[TARGET]

print(f"Tamaño del dataset de modelado: {X.shape}")
print(f"Variable objetivo — media: ${y.mean():,.0f} | mediana: ${y.median():,.0f}")

# ----- 4.2.2 Preprocesador -----
preprocessor = ColumnTransformer([
    ('num', StandardScaler(), FEATURES_NUM),
    ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), FEATURES_CAT)
])

# ----- 4.2.3 División train/test (80/20, sin data leakage) -----
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42
)
print(f"Train: {len(X_train):,} | Test: {len(X_test):,}")

# ----- 4.2.4 Entrenamiento y comparación -----
MODELOS = {
    'Regresión Lineal (Ridge)': Ridge(alpha=1.0),
    'Random Forest':            RandomForestRegressor(n_estimators=200, max_depth=15,
                                                      random_state=42, n_jobs=-1),
    'XGBoost':                  XGBRegressor(n_estimators=300, max_depth=6,
                                             learning_rate=0.05, subsample=0.8,
                                             colsample_bytree=0.8,
                                             random_state=42, verbosity=0)
}

resultados = {}
cv = KFold(n_splits=5, shuffle=True, random_state=42)

for nombre, modelo in MODELOS.items():
    pipe = Pipeline([('prep', preprocessor), ('model', modelo)])
    pipe.fit(X_train, y_train)
    y_pred = pipe.predict(X_test)

    rmse  = np.sqrt(mean_squared_error(y_test, y_pred))
    mae   = mean_absolute_error(y_test, y_pred)
    r2    = r2_score(y_test, y_pred)
    mape  = np.mean(np.abs((y_test - y_pred) / y_test)) * 100
    rmse_rel = rmse / y_test.median() * 100  # RMSE relativo al precio mediano

    cv_r2 = cross_val_score(pipe, X, y, cv=cv, scoring='r2', n_jobs=-1)

    resultados[nombre] = {
        'RMSE': rmse, 'MAE': mae, 'R²': r2,
        'MAPE (%)': mape, 'RMSE relativo (%)': rmse_rel,
        'CV R² (media)': cv_r2.mean(), 'CV R² (std)': cv_r2.std()
    }
    print(f"\n{nombre}:")
    print(f"  RMSE relativo: {rmse_rel:.1f}% | R²: {r2:.3f} | CV R²: {cv_r2.mean():.3f} ± {cv_r2.std():.3f}")

# Guardar tabla de resultados
pd.DataFrame(resultados).T.round(3).to_csv('docs/metricas_modelos.csv')

# ----- 4.2.5 Guardar mejor modelo -----
mejor_pipe = Pipeline([('prep', preprocessor),
                       ('model', MODELOS['XGBoost'])])
mejor_pipe.fit(X, y)  # reentrenar con todos los datos
joblib.dump(mejor_pipe, 'models/modelo_xgboost.pkl')
print("\nMejor modelo guardado en models/modelo_xgboost.pkl")

# ----- 4.2.6 Importancia de variables con SHAP -----
X_train_t = preprocessor.fit_transform(X_train)
explainer  = shap.Explainer(MODELOS['XGBoost'])
shap_vals  = explainer(X_train_t[:500])
shap.summary_plot(shap_vals, feature_names=preprocessor.get_feature_names_out(),
                  show=False)
plt.savefig('docs/figures/06_shap_importance.png', dpi=150, bbox_inches='tight')
plt.show()
```

### 4.3 Modelo 2 — Clustering: Segmentación de Mercados de Vivienda

```python
from sklearn.cluster import KMeans, DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, davies_bouldin_score
import matplotlib.pyplot as plt

# ----- 4.3.1 Construir tabla de resumen por ciudad-año -----
resumen = df_full.groupby(['city', 'year']).agg(
    precio_mediano         = ('price',              'median'),
    IAH_promedio           = ('IAH',                'mean'),
    ratio_cuota_promedio   = ('ratio_cuota_salario', 'mean'),
    precio_m2_mediano      = ('precio_m2',          'median'),
    tasa_desempleo         = ('tasa_desempleo',     'mean'),
    n_propiedades          = ('price',              'count')
).reset_index()

resumen = resumen[resumen['n_propiedades'] >= 30]  # solo submercados con suficiente data
print(f"Submercados ciudad-año para clustering: {len(resumen)}")

# ----- 4.3.2 Escalar variables de clustering -----
VARS_CLUSTER = ['precio_mediano', 'IAH_promedio',
                'ratio_cuota_promedio', 'precio_m2_mediano', 'tasa_desempleo']
X_cluster = resumen[VARS_CLUSTER].dropna()
scaler    = StandardScaler()
X_scaled  = scaler.fit_transform(X_cluster)

# ----- 4.3.3 Método del codo + silueta para elegir k -----
inertias, siluetas, db_scores = [], [], []
K_RANGE = range(2, 9)

for k in K_RANGE:
    km = KMeans(n_clusters=k, random_state=42, n_init=15, max_iter=300)
    labels = km.fit_predict(X_scaled)
    inertias.append(km.inertia_)
    siluetas.append(silhouette_score(X_scaled, labels))
    db_scores.append(davies_bouldin_score(X_scaled, labels))

fig, axes = plt.subplots(1, 3, figsize=(15, 4))
axes[0].plot(K_RANGE, inertias, marker='o'); axes[0].set_title('Método del codo')
axes[0].set_xlabel('k'); axes[0].set_ylabel('Inercia')
axes[1].plot(K_RANGE, siluetas, marker='o', color='green'); axes[1].set_title('Coeficiente de silueta')
axes[1].set_xlabel('k'); axes[1].set_ylabel('Silueta (mayor = mejor)')
axes[2].plot(K_RANGE, db_scores, marker='o', color='red'); axes[2].set_title('Índice Davies-Bouldin')
axes[2].set_xlabel('k'); axes[2].set_ylabel('DBI (menor = mejor)')
plt.tight_layout()
plt.savefig('docs/figures/07_seleccion_k.png', dpi=150)
plt.show()

# ----- 4.3.4 Modelo final KMeans (k=4 ajustar según resultados) -----
K_FINAL = 4  # ajustar según gráficas anteriores
km_final = KMeans(n_clusters=K_FINAL, random_state=42, n_init=15)
resumen_valido = resumen.dropna(subset=VARS_CLUSTER).copy()
resumen_valido['cluster'] = km_final.fit_predict(X_scaled[:len(resumen_valido)])

# Etiquetar clusters por IAH_promedio
medias_iah = resumen_valido.groupby('cluster')['IAH_promedio'].mean().sort_values()
ETIQUETAS = {medias_iah.index[0]: 'Accesible',
             medias_iah.index[1]: 'Moderado',
             medias_iah.index[2]: 'Elevado',
             medias_iah.index[3]: 'Crítico'}
resumen_valido['segmento'] = resumen_valido['cluster'].map(ETIQUETAS)

# Guardar tabla de segmentos
resumen_valido.to_csv('data/processed/segmentos_mercado.csv', index=False)

print("\nCaracterísticas promedio por segmento:")
print(resumen_valido.groupby('segmento')[
    ['precio_mediano', 'IAH_promedio', 'ratio_cuota_promedio', 'precio_m2_mediano']
].mean().round(2))

sil_final = silhouette_score(X_scaled[:len(resumen_valido)], resumen_valido['cluster'])
print(f"\nCoeficiente de silueta final: {sil_final:.3f}")

# ----- 4.3.5 Validación con DBSCAN -----
db = DBSCAN(eps=0.8, min_samples=3)
labels_db = db.fit_predict(X_scaled[:len(resumen_valido)])
n_outliers = (labels_db == -1).sum()
print(f"\nDBSCAN — submercados marcados como outliers: {n_outliers}")
resumen_valido['outlier_dbscan'] = labels_db == -1
print("Outliers detectados:")
print(resumen_valido[resumen_valido['outlier_dbscan']][['city', 'year', 'IAH_promedio']])
```

### 4.4 Entregable de Fase 4

**Responsable:** Steve  
**Fecha:** Semana 7–8 del proyecto

- Notebook `03_modelado.ipynb` con código completo, comentado y reproducible.
- Tabla comparativa de métricas de los 3 modelos de regresión (RMSE, MAE, R², MAPE, CV R²).
- Gráfica de importancia de variables (SHAP summary plot).
- Tabla de clusters con etiquetas interpretables y estadísticas por segmento.
- Gráficas de selección de k (codo, silueta, Davies-Bouldin).
- Archivos guardados: `models/modelo_xgboost.pkl`, `data/processed/segmentos_mercado.csv`.

---

## Fase 5 — Evaluación

**Responsable principal: Sofía | Apoyo: Steve**

### 5.1 Criterios de Aceptación del Modelo

Antes de proceder al despliegue, el modelo debe superar todos los criterios definidos en la Fase 1:

| Criterio | Umbral | ¿Cumple? |
|---|---|---|
| RMSE relativo < 15% del precio mediano | — | Por verificar |
| R² ≥ 0.75 en conjunto de prueba | — | Por verificar |
| CV R² estable (std < 0.05) | — | Por verificar |
| Silueta clustering ≥ 0.45 | — | Por verificar |
| ≥ 3 segmentos diferenciables (IAH distinto) | — | Por verificar |

### 5.2 Evaluación Completa del Modelo de Regresión

```python
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Cargar modelo guardado
mejor_modelo = joblib.load('models/modelo_xgboost.pkl')
y_pred = mejor_modelo.predict(X_test)

# ----- 5.2.1 Tabla de métricas -----
precio_mediano_test = y_test.median()
mae   = mean_absolute_error(y_test, y_pred)
rmse  = np.sqrt(mean_squared_error(y_test, y_pred))
r2    = r2_score(y_test, y_pred)
mape  = np.mean(np.abs((y_test - y_pred) / y_test)) * 100
rmse_rel = rmse / precio_mediano_test * 100

metricas = pd.DataFrame({
    'Métrica': ['MAE', 'RMSE', 'R²', 'MAPE (%)', 'RMSE relativo (%)'],
    'Valor': [f"${mae:,.0f} COP", f"${rmse:,.0f} COP", f"{r2:.4f}",
              f"{mape:.1f}%", f"{rmse_rel:.1f}%"],
    'Interpretación': [
        f"El modelo se equivoca en promedio ${mae/1e6:.1f}M COP",
        f"Error cuadrático medio de ${rmse/1e6:.1f}M COP",
        f"El modelo explica el {r2*100:.1f}% de la varianza del precio",
        f"Error porcentual promedio: {mape:.1f}%",
        f"{'✓ Cumple' if rmse_rel < 15 else '✗ No cumple'} (umbral: < 15%)"
    ]
})
print(metricas.to_string(index=False))
metricas.to_csv('docs/tabla_metricas_finales.csv', index=False)

# ----- 5.2.2 Gráfica de residuos -----
residuos = y_test - y_pred
fig, axes = plt.subplots(1, 3, figsize=(16, 5))

axes[0].scatter(y_pred, residuos, alpha=0.3, s=8)
axes[0].axhline(0, color='red', linestyle='--')
axes[0].set_title('Residuos vs Valores predichos')
axes[0].set_xlabel('Precio predicho (COP)')
axes[0].set_ylabel('Residuo (COP)')

axes[1].scatter(y_test, y_pred, alpha=0.3, s=8)
lims = [min(y_test.min(), y_pred.min()), max(y_test.max(), y_pred.max())]
axes[1].plot(lims, lims, 'r--', lw=1)
axes[1].set_title('Real vs Predicho')
axes[1].set_xlabel('Precio real (COP)')
axes[1].set_ylabel('Precio predicho (COP)')

sns.histplot(residuos / 1e6, bins=50, kde=True, ax=axes[2])
axes[2].set_title('Distribución de residuos')
axes[2].set_xlabel('Residuo (millones COP)')

plt.tight_layout()
plt.savefig('docs/figures/08_residuos.png', dpi=150)
plt.show()

# ----- 5.2.3 Validación cruzada -----
cv_scores = cross_val_score(mejor_modelo, X, y, cv=5, scoring='r2', n_jobs=-1)
print(f"\nValidación cruzada (5-fold):")
print(f"  R² por fold: {cv_scores.round(3)}")
print(f"  R² promedio: {cv_scores.mean():.3f} ± {cv_scores.std():.3f}")
print(f"  {'✓ Estable' if cv_scores.std() < 0.05 else '⚠ Inestable: revisar sobreajuste'}")

# ----- 5.2.4 Análisis por ciudad -----
df_eval = X_test.copy()
df_eval['y_real'] = y_test.values
df_eval['y_pred'] = y_pred
df_eval['error_abs'] = np.abs(df_eval['y_real'] - df_eval['y_pred'])
df_eval['error_pct'] = df_eval['error_abs'] / df_eval['y_real'] * 100

print("\nError por ciudad (MAPE):")
print(df_eval.groupby('city')['error_pct'].mean().sort_values().round(1))
```

### 5.3 Interpretación en Lenguaje de Negocio

Al presentar resultados, cada métrica debe traducirse a conclusiones que respondan las preguntas de investigación. Plantilla de conclusiones esperadas (completar con valores reales):

1. **Capacidad predictiva:** "El modelo XGBoost explica el **X%** de la variación en precios de vivienda en Colombia, con un error promedio del **Y%** sobre el precio mediano, cumpliendo el umbral de aceptación establecido."
2. **Variable más importante:** "El análisis SHAP revela que la **ciudad** es el predictor más influyente, seguida por el **área** y la **tasa hipotecaria**, lo que confirma que la ubicación geográfica determina el precio más que cualquier característica física."
3. **Índice de accesibilidad:** "En Bogotá, el precio mediano de vivienda equivale a **X años** de salario mínimo en 2024, frente a **Y años** en 2015. Esto representa un deterioro del **Z%** en la accesibilidad habitacional."
4. **Ciudades críticas:** "El **X%** de los submercados analizados caen en el segmento 'Crítico', donde la cuota hipotecaria supera el 50% del salario mínimo, concentrándose principalmente en Bogotá y Medellín."
5. **Umbrales de asequibilidad:** "Siguiendo el criterio de asequibilidad del 30% del ingreso destinado a vivienda, un hogar con un salario mínimo en Bogotá no puede acceder a ninguna vivienda cuyo precio supere los **$X millones COP**."

### 5.4 Entregable de Fase 5

**Responsable:** Sofía  
**Fecha:** Semana 9 del proyecto

- Notebook `04_evaluacion.ipynb` con todas las métricas, gráficas de residuos y validación cruzada.
- Tabla de métricas exportada a `docs/tabla_metricas_finales.csv`.
- Sección de conclusiones en lenguaje de negocio: mínimo 5 párrafos con evidencia cuantitativa.
- Verificación documentada de cada criterio de aceptación (cumple / no cumple / ajuste requerido).

---

## Fase 6 — Despliegue

**Responsable principal: Kukis | Apoyo: Sofía**

### 6.1 Requerimientos del Dashboard

El dashboard debe cumplir los siguientes requerimientos funcionales:

| Requerimiento | Descripción |
|---|---|
| RF-01 | Mostrar KPIs principales (IAH, ratio cuota/salario, precio mediano, precio/m²) actualizados según filtros |
| RF-02 | Filtro interactivo por ciudad, año y tipo de inmueble |
| RF-03 | Gráfica de evolución histórica del IAH por ciudad (2015–2024) |
| RF-04 | Mapa de Colombia con colores por segmento de accesibilidad |
| RF-05 | Comparador de ciudades (barras horizontales por IAH) |
| RF-06 | Predictor de precio: el usuario ingresa área, ciudad y número de cuartos, y obtiene el precio estimado |
| RF-07 | Tabla de segmentos (resultados del clustering) |
| RF-08 | URL pública accesible sin autenticación |

### 6.2 Dashboard Streamlit

```python
# app/app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import joblib
import numpy as np

# ----- Configuración -----
st.set_page_config(
    page_title="Accesibilidad de Vivienda · Colombia",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 Accesibilidad de Vivienda en Colombia")
st.markdown("**¿Cuántos años de salario mínimo cuesta una vivienda?** · Análisis 2015–2024")
st.markdown("---")

# ----- Cargar datos -----
@st.cache_data
def cargar_datos():
    df = pd.read_csv('data/processed/vivienda_colombia_limpio.csv')
    segmentos = pd.read_csv('data/processed/segmentos_mercado.csv')
    return df, segmentos

df, segmentos = cargar_datos()

# ----- Filtros en sidebar -----
st.sidebar.header("Filtros")
ciudades_disponibles = sorted(df['city'].unique())
ciudad_sel = st.sidebar.multiselect(
    "Ciudad", ciudades_disponibles, default=['Bogotá', 'Medellín', 'Cali']
)
año_sel = st.sidebar.slider(
    "Año", int(df['year'].min()), int(df['year'].max()),
    (2015, int(df['year'].max()))
)
tipo_sel = st.sidebar.multiselect(
    "Tipo de inmueble",
    df['property_type'].unique(),
    default=df['property_type'].unique().tolist()
)

# Filtrar datos
mask = (
    df['city'].isin(ciudad_sel) &
    df['year'].between(año_sel[0], año_sel[1]) &
    df['property_type'].isin(tipo_sel)
)
df_f = df[mask]

# ----- KPIs -----
col1, col2, col3, col4 = st.columns(4)
col1.metric("Precio mediano",     f"${df_f['price'].median() / 1e6:.1f}M COP")
col2.metric("IAH promedio",       f"{df_f['IAH'].mean():.1f} años")
col3.metric("Ratio cuota/salario",f"{df_f['ratio_cuota_salario'].mean():.1%}")
col4.metric("Precio promedio m²", f"${df_f['precio_m2'].median():,.0f} COP")

st.markdown("---")

# ----- Gráfica 1: Evolución histórica del IAH -----
st.subheader("Evolución del Índice de Accesibilidad Habitacional (IAH)")
evolucion = df_f.groupby(['year', 'city'])['IAH'].mean().reset_index()
fig_evol = px.line(
    evolucion, x='year', y='IAH', color='city', markers=True,
    labels={'IAH': 'Años de salario mínimo', 'year': 'Año', 'city': 'Ciudad'},
    color_discrete_sequence=px.colors.qualitative.Set2
)
fig_evol.add_hline(y=10, line_dash="dash", line_color="orange",
                   annotation_text="Umbral moderado (10 años)")
fig_evol.add_hline(y=20, line_dash="dash", line_color="red",
                   annotation_text="Umbral crítico (20 años)")
st.plotly_chart(fig_evol, use_container_width=True)

# ----- Gráfica 2: Comparador de ciudades -----
col_a, col_b = st.columns(2)
with col_a:
    st.subheader("IAH por ciudad (año más reciente)")
    año_max = df_f['year'].max()
    comp = df_f[df_f['year'] == año_max].groupby('city')['IAH'].mean().sort_values()
    fig_bar = px.bar(
        comp.reset_index(), x='IAH', y='city', orientation='h',
        color='IAH', color_continuous_scale='RdYlGn_r',
        labels={'IAH': 'Años de salario', 'city': 'Ciudad'}
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with col_b:
    st.subheader("Distribución del ratio cuota/salario")
    fig_box = px.box(
        df_f, x='city', y='ratio_cuota_salario', color='city',
        labels={'ratio_cuota_salario': 'Ratio cuota/salario', 'city': 'Ciudad'}
    )
    fig_box.add_hline(y=0.30, line_dash="dash", line_color="red",
                      annotation_text="Límite de asequibilidad (30%)")
    st.plotly_chart(fig_box, use_container_width=True)

# ----- Gráfica 3: Segmentos de mercado -----
st.markdown("---")
st.subheader("Segmentación de Mercados de Vivienda")
fig_seg = px.scatter(
    segmentos, x='IAH_promedio', y='ratio_cuota_promedio',
    color='segmento', size='n_propiedades',
    hover_data=['city', 'year'],
    labels={'IAH_promedio': 'IAH promedio (años de salario)',
            'ratio_cuota_promedio': 'Ratio cuota/salario promedio',
            'segmento': 'Segmento de accesibilidad'},
    color_discrete_map={
        'Accesible': '#2ecc71', 'Moderado': '#f39c12',
        'Elevado': '#e67e22',   'Crítico': '#e74c3c'
    }
)
st.plotly_chart(fig_seg, use_container_width=True)

# ----- Predictor de precio -----
st.markdown("---")
st.subheader("🔍 Estimar precio de una propiedad")
col1p, col2p, col3p, col4p = st.columns(4)
area_in    = col1p.number_input("Área (m²)", 20, 600, 80, step=5)
cuartos_in = col2p.selectbox("Habitaciones", [1, 2, 3, 4, 5], index=2)
baños_in   = col3p.selectbox("Baños", [1, 2, 3, 4], index=1)
ciudad_in  = col4p.selectbox("Ciudad", ciudades_disponibles)

if st.button("Estimar precio", type="primary"):
    modelo = joblib.load('models/modelo_xgboost.pkl')
    año_actual = df['year'].max()
    # Recuperar valores macro del año más reciente
    macro_ref = df[df['year'] == año_actual][
        ['ipc_var_anual', 'tasa_hipotecaria_anual', 'tasa_desempleo', 'ipvu_variacion_anual']
    ].mean()
    X_pred = pd.DataFrame([{
        'area': area_in, 'rooms': cuartos_in, 'bathrooms': baños_in,
        'year': año_actual, 'city': ciudad_in, 'property_type': 'Apartamento',
        'ipc_var_anual': macro_ref['ipc_var_anual'],
        'tasa_hipotecaria_anual': macro_ref['tasa_hipotecaria_anual'],
        'tasa_desempleo': macro_ref['tasa_desempleo'],
        'ipvu_variacion_anual': macro_ref['ipvu_variacion_anual']
    }])
    precio_est = modelo.predict(X_pred)[0]
    st.success(f"**Precio estimado: ${precio_est / 1e6:.0f}M COP** "
               f"(${precio_est / area_in:,.0f} COP/m²)")

    salario_actual = df[df['year'] == año_actual]['salario_mensual'].iloc[0]
    iah_est = precio_est / (salario_actual * 12)
    nivel = ('🟢 Accesible' if iah_est <= 5 else
             '🟡 Moderado'  if iah_est <= 10 else
             '🟠 Elevado'   if iah_est <= 20 else '🔴 Crítico')
    st.info(f"Esta propiedad equivale a **{iah_est:.1f} años** de salario mínimo — {nivel}")
```

### 6.3 Estructura del Repositorio GitHub

```
proyecto-vivienda-colombia/
│
├── data/
│   ├── raw/
│   │   ├── properati_colombia.csv          # Fuente A4 — histórico
│   │   ├── colombia_housing.csv            # Fuente A1
│   │   ├── colombian_properties_2023.csv   # Fuente A2
│   │   ├── real_estate_bogota.csv          # Fuente A3
│   │   ├── salario_minimo_colombia.csv     # Fuente B1
│   │   ├── ipc_colombia_anual.csv          # Fuente B2
│   │   ├── tasa_hipotecaria.csv            # Fuente B3
│   │   ├── desempleo_ciudades.csv          # Fuente B4
│   │   ├── ipvu_trimestral.csv             # Fuente B5
│   │   └── README.md                       # Origen, URL y estructura de cada fuente
│   └── processed/
│       ├── vivienda_colombia_limpio.csv    # Dataset final integrado
│       └── segmentos_mercado.csv           # Resultado del clustering
│
├── notebooks/
│   ├── 01_EDA.ipynb                        # Exploración inicial (Steve)
│   ├── 02_preparacion_datos.ipynb          # Limpieza e integración (Kukis)
│   ├── 03_modelado.ipynb                   # Modelos y métricas (Steve)
│   └── 04_evaluacion.ipynb                 # Evaluación y conclusiones (Sofía)
│
├── models/
│   └── modelo_xgboost.pkl                  # Modelo serializado
│
├── docs/
│   ├── proyecto_vivienda_crisp_dm_v2.md    # Este documento
│   ├── tabla_metricas_finales.csv
│   └── figures/
│       ├── 02_distribucion_precios.png
│       ├── 03_precio_ciudad.html
│       ├── 04_nulos.png
│       ├── 05_correlacion.png
│       ├── 06_shap_importance.png
│       ├── 07_seleccion_k.png
│       └── 08_residuos.png
│
├── app/
│   └── app.py                              # Dashboard Streamlit (Kukis)
│
├── requirements.txt
└── README.md
```

### 6.4 Entregable de Fase 6

**Responsable:** Kukis  
**Fecha:** Semana 10–11 del proyecto

- Dashboard Streamlit funcional con los 8 requerimientos RF cumplidos.
- URL pública en Streamlit Community Cloud (`streamlit.io/cloud`).
- Repositorio GitHub completo, con README claro que explica cómo ejecutar el proyecto localmente.
- Archivo `requirements.txt` con todas las dependencias y versiones fijadas.

---

## Cronograma General

| Semana | Actividad | Responsable |
|---|---|---|
| 1–2 | Fase 1: Comprensión del negocio. Aprobación del documento de planificación. | Sofía |
| 3–4 | Fase 2: Descarga de datasets, EDA, reporte de calidad de datos. | Steve |
| 5–6 | Fase 3: Limpieza, integración y construcción de variables derivadas. | Kukis |
| 7–8 | Fase 4: Entrenamiento de modelos de regresión y clustering. | Steve |
| 9 | Fase 5: Evaluación, gráficas de residuos, conclusiones. | Sofía |
| 10–11 | Fase 6: Dashboard Streamlit, despliegue y URL pública. | Kukis |
| 12 | Preparación de presentación final. Ensayo general. | Todos |
| 13 | **Presentación final ante jurado.** | Todos |

---

## Estructura de la Presentación Final

| Sección | Contenido | Responsable | Tiempo |
|---|---|---|---|
| 1. Problema y contexto | Por qué importa la accesibilidad habitacional en Colombia. Cifras de déficit. | Sofía | 3 min |
| 2. Datos y fuentes | Qué datasets se usaron, cómo se integraron, qué variables se crearon. | Steve | 3 min |
| 3. Hallazgos del EDA | Distribución de precios, evolución histórica, correlaciones clave. | Steve | 4 min |
| 4. Metodología e índice | Qué es el IAH, cómo se calculó, comparación con estándares internacionales. | Sofía | 3 min |
| 5. Modelos y métricas | Comparativa de modelos, RMSE, R², importancia de variables (SHAP). | Steve | 5 min |
| 6. Segmentación | Clusters de accesibilidad, caracterización de cada segmento. | Kukis | 3 min |
| 7. Dashboard en vivo | Demostración interactiva con filtros, predictor de precio. | Kukis | 5 min |
| 8. Conclusiones | Respuesta explícita a las 4 preguntas de investigación. Recomendaciones. | Sofía | 3 min |
| 9. Preguntas del jurado | — | Todos | 6 min |

---

## Conclusiones Esperadas del Análisis

Al finalizar el proyecto, el análisis debe poder responder con evidencia cuantitativa:

**Pregunta 1 — ¿Cuántos años de salario cuesta una vivienda?**  
El índice IAH calculado permitirá responder con precisión por ciudad y año. Se espera encontrar valores superiores a 15 años en Bogotá, consistentes con estudios previos del DANE y ONU-Hábitat, y menores a 10 años en ciudades intermedias como Bucaramanga o Pereira.

**Pregunta 2 — ¿Empeoró la accesibilidad en 10 años?**  
La comparación del IAH en 2015 vs. 2024 en precios reales (ajustados por inflación) revelará si la brecha creció. Se espera una tendencia de deterioro después de 2020, período de alta inflación y aumento de tasas hipotecarias.

**Pregunta 3 — ¿Qué variable importa más?**  
El análisis SHAP del modelo XGBoost permitirá responder con evidencia. La hipótesis es que la ciudad y el área son los predictores dominantes, pero que la tasa hipotecaria ganó peso relativo después de 2022.

**Pregunta 4 — ¿Dónde la vivienda es inalcanzable?**  
El clustering identificará los segmentos 'Crítico' y 'Elevado', y el ratio cuota/salario determinará en qué ciudades un hogar de ingreso mínimo no puede acceder a ninguna vivienda formal dentro de los umbrales de asequibilidad internacionales.

---

*Documento de planificación del proyecto final · Metodología CRISP-DM · Análisis de Datos · 2025-I*  
*Integrantes: Steve · Sofía · Kukis*
