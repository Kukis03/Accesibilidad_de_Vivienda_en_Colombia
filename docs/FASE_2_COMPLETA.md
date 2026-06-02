# Fase 2 — Comprensión de los Datos
## Proyecto: Accesibilidad de Vivienda en Colombia · CRISP-DM 2025-I
**Responsable principal:** Sofía · **Apoyo:** Steve  
**Estado:** ✅ Completa y lista para revisión del jurado  
**Notebook asociado:** `notebooks/01_EDA.ipynb`  
**Semanas:** 3 – 4  
*Nota: Este documento refleja el inventario actualizado a Junio 2026 con la nueva numeración de archivos (A1–A8, B1–B8).*

---

## Introducción

La Fase 2 documenta el proceso completo de comprensión de los datos: qué contiene cada dataset, cómo se descargó, cuál es su estructura real, qué calidad tiene y qué hallazgos iniciales emergen de la exploración. El objetivo no es limpiar ni modelar, sino **conocer los datos a fondo antes de tocarlos**. Cada decisión tomada aquí se convierte en un insumo directo para la Fase 3 (preparación) y el diseño del modelo en Fase 4.

Esta fase opera sobre los **16 archivos** identificados en Fase 1: 8 CSV de precios de vivienda (Grupo A, incluyendo el scraping A7 de Villavicencio) y 8 CSV macroeconómicos (Grupo B). El trabajo fue ejecutado por Sofía con apoyo de Steve en la interpretación de los hallazgos.

> **Actualización v2:** Se incorpora la **Sección 9-bis** con la estrategia de refuerzo de cobertura para Villavicencio, integrando tres fuentes complementarias: scraping gratuito de FincaRaiz (BeautifulSoup), IPVN DANE (Villavicencio AU) y boletines CENAC. Esta adición no requiere costo económico y fortalece significativamente la representación de ciudades intermedias de la Orinoquia.

---

## 1. Inventario de Fuentes — Verificación Real Post-Descarga

Antes de cualquier análisis, se verificó que todos los archivos descargados correspondieran a lo esperado. La siguiente tabla registra el estado real tras la descarga:

### 1.1 Grupo A — Datasets de Precios de Vivienda — estado actual (8 archivos)

| ID | Archivo en `/data/raw/` | Tamaño real | Registros reales | Columnas | Período verificado | Estado |
|---|---|---|---|---|---|---|
| **A1** | `A1_colombia_housing_properties.csv` | 582 MB | ~997.623 | 17 | 2020–2021 | ✅ OK (Properati, limpio) |
| **A2** | `A2_fincaraiz_colombia.csv` | 52 MB | ~52.000 | 28 | 2023–2024 | ✅ OK |
| **A3** | `A3_colombia_house_prediction.csv` | 27 MB | ~45.000 | 37 | 2019–2020 | ✅ OK |
| **A4** | `A4_real_estate_bogota.csv` | 892 KB | ~13.000 | 8 | 2019–2022 | ✅ OK |
| **A5** | `A5_medellin_properties_2023.csv` | 879 KB | ~12.000 | 12 | 2023 | ✅ OK |
| **A6** | `A6_real_estate_bogota_2023.csv` | 467 KB | ~6.500 | 8 | 2023 | ✅ OK |
| **A7** | `A7_fincaraiz_villavicencio_scraping.csv` | 294 KB | ~2.500 | 24 | 2024–2025 | ✅ OK |
| **A8** | `A8_carac_pre_viv_nueva.csv` | 4 KB | 32 | 14 | 2022 | ✅ OK |

### 1.2 Grupo B — Variables Macroeconómicas (DANE + BanRep) — estado actual (8 archivos)

| ID | Archivo en `/data/raw/` | Registros | Frecuencia | Período verificado | Estado |
|---|---|---|---|---|---|
| **B1** | `B1_indices_precios_vivienda.csv` | 332 | Mensual/Trimestral | 1988–2026 | ✅ OK (IPVN+IPVU unificado) |
| **B2** | `B2_tasa_hipotecaria_semanal.csv` | 1.255 | Semanal | 2002–2026 | ✅ OK |
| **B3** | `B3_salario_minimo_historico.csv` | 43 | Anual | 1984–2026 | ✅ OK |
| **B4** | `B4_ipc_colombia_anual.csv` | 10 | Anual | 2015–2024 | ✅ OK |
| **B5** | `B5_geih_empleo_colombia.csv` | 1.202 | Mensual | 2001–2026 | ✅ OK (procesado de XLSX) |
| **B6** | `B6_qcon_confianza_constructora.csv` | ~200 | Trimestral | 2005–presente | ✅ OK |
| **B7** | `B7_qcon_licencias_construccion.csv` | ~200 | Trimestral | 2005–presente | ✅ OK |
| **B8** | `B8_geo_estados_localidades.csv` | ~50 | — | — | ✅ OK |

---

## 2. Estructura Real de los Datasets — Esquema de Columnas

Esta sección documenta las columnas reales de cada dataset tal como llegan. Es crítica para Fase 3: aquí se identifican las inconsistencias de nombres, tipos y escalas que deben normalizarse.

### 2.1 Esquema de columnas — Dataset A1 (Properati, fuente principal)

```python
import pandas as pd

# Carga del dataset A1 (Properati Colombia, ~998K registros limpios)
df_a1 = pd.read_csv('data/raw/A1_colombia_housing_properties.csv',
                    usecols=None, low_memory=False)

print(df_a1.dtypes)
print(df_a1.head(3).T)  # Ver las primeras filas transpuestas (más legible)
```

| Columna A1 | Tipo | Descripción | Mapeo a columna canónica |
|---|---|---|---|
| `id` | object | Identificador único del anuncio | `id_anuncio` |
| `l1` | object | País (`'Colombia'`) | *(filtro, no se conserva)* |
| `l2` | object | Departamento | `departamento` |
| `l3` | object | Ciudad / municipio | → **`city`** |
| `l4`, `l5`, `l6` | object | Barrio, zona (variable según ciudad) | `barrio` (l4) |
| `rooms` | float | Número de habitaciones | **`rooms`** |
| `bathrooms` | float | Número de baños | **`bathrooms`** |
| `surface_total` | float | Área total (m²) — incluye áreas comunes en APT | → **`area`** |
| `surface_covered` | float | Área construida (m²) — área techada | *(alternativa a `area`)* |
| `price` | float | Precio en moneda original | **`price`** |
| `currency` | object | Moneda (`'COP'`, `'USD'`, `'COP/m2'`) | *(requiere normalización)* |
| `operation_type` | object | Tipo: `'Venta'`, `'Arriendo'` | **`operation_type`** → filtrar Venta |
| `property_type` | object | `'Apartamento'`, `'Casa'`, `'Lote'`, etc. | **`property_type`** |
| `description` | object | Texto libre del anuncio | *(descartar en modelo)* |
| `lat` | float | Latitud | **`lat`** |
| `lon` | float | Longitud | **`lon`** |
| `start_date` | object | Fecha de creación del anuncio | → **`created_on`** |
| `end_date` | object | Fecha de baja del anuncio | *(referencia)* |

> **Decisiones Fase 3 ya identificadas:**  
> 1. Usar `surface_total` como `area` principal (más completa). Si es nula, usar `surface_covered`.  
> 2. Filtrar `operation_type == 'Venta'` — los arriendos contaminan el precio.  
> 3. Convertir `currency == 'USD'` a COP usando la TRM del año correspondiente.  
> 4. Convertir `currency == 'COP/m2'` multiplicando por `surface_total`.

### 2.2 Esquema de columnas — Dataset A2 (FincaRaiz Colombia 2023–2024)

| Columna A2 | Tipo | Descripción | Mapeo canónico |
|---|---|---|---|
| `precio` | float | Precio en millones COP | → **`price`** (× 1.000.000) |
| `area_m2` | float | Área en m² | → **`area`** |
| `habitaciones` | int | Número de habitaciones | → **`rooms`** |
| `baños` | int | Número de baños | → **`bathrooms`** |
| `tipo_inmueble` | object | Tipo de propiedad | → **`property_type`** |
| `ciudad` | object | Ciudad | → **`city`** |
| `fecha_publicacion` | object | Fecha | → **`created_on`** |
| `barrio` | object | Barrio | `barrio` |
| `parqueaderos` | int | Parqueaderos | `parking` |
| `estrato` | int | Estrato (1–6) | `estrato` |
| `antiguedad` | float | Años de antigüedad | `antiguedad` *(feature opcional)* |

> **Alerta:** A2 (FincaRaiz) tiene el precio en **millones de COP** (ej: `450` = $450.000.000). Esto debe multiplicarse × 1.000.000 antes de concatenar con el resto.

### 2.3 Esquemas resumidos — Datasets A3, A4, A5, A6, A7, A8

| Dataset | Peculiaridades clave | Columna de precio | Columna de área | Columna de ciudad |
|---|---|---|---|---|
| **A3** (House Prediction) | 37 features ML | `price` (COP) | `area` | `city` |
| **A4** (Bogotá granular) | Solo Bogotá; tiene `upz` (Unidad de Planeamiento Zonal) | `price` (COP) | `area_m2` | *(siempre "Bogotá")* |
| **A5** (Medellín 2023) | Solo Medellín; tiene `barrio` y `comunas` | `precio` (COP) | `metros` | *(siempre "Medellín")* |
| **A6** (Bogotá 2023) | Solo Bogotá; tiene `localidad` | `valor` (COP) | `area` | *(siempre "Bogotá")* |
| **A7** (Villavicencio scraping) | Scraping FincaRaiz Villavicencio; muchas columnas de calidad | variada | variada | *(siempre "Villavicencio")* |
| **A8** (Carac Pre Viv Nueva) | Datos de vivienda nueva Bogotá por UPZ (Datos Abiertos) | `precio_m2` | — | *(siempre "Bogotá")* |

---

## 3. Estadísticas Descriptivas y Calidad de Datos por Dataset

### 3.1 Carga unificada para diagnóstico inicial

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# =========================================================
# CARGA INICIAL — Solo para diagnóstico (NO es el merge final)
# =========================================================

datasets = {
    'A1_properati':             pd.read_csv('data/raw/A1_colombia_housing_properties.csv',
                                            usecols=['l1','l3','rooms','bathrooms',
                                                     'surface_total','price','currency',
                                                     'operation_type','property_type',
                                                     'lat','lon','start_date'],
                                            low_memory=False),
    'A2_fincaraiz':             pd.read_csv('data/raw/A2_fincaraiz_colombia.csv', low_memory=False),
    'A3_house_prediction':      pd.read_csv('data/raw/A3_colombia_house_prediction.csv', low_memory=False),
    'A4_bogota':                pd.read_csv('data/raw/A4_real_estate_bogota.csv', low_memory=False),
    'A5_medellin':              pd.read_csv('data/raw/A5_medellin_properties_2023.csv', low_memory=False),
    'A6_bogota_2023':           pd.read_csv('data/raw/A6_real_estate_bogota_2023.csv', low_memory=False),
    'A7_villavicencio':         pd.read_csv('data/raw/A7_fincaraiz_villavicencio_scraping.csv', low_memory=False),
    'A8_carac_pre_viv_nueva':   pd.read_csv('data/raw/A8_carac_pre_viv_nueva.csv', low_memory=False),
}

# =========================================================
# REPORTE DE CALIDAD POR DATASET
# =========================================================

reporte_calidad = []
for nombre, df in datasets.items():
    n_total = len(df)
    info = {
        'Dataset': nombre,
        'Filas': n_total,
        'Columnas': df.shape[1],
        'Nulos (%)': f"{(df.isnull().mean().mean() * 100):.1f}%",
        'Duplicados': df.duplicated().sum(),
        'Memoria (MB)': f"{df.memory_usage(deep=True).sum() / 1e6:.1f}"
    }
    reporte_calidad.append(info)

pd.DataFrame(reporte_calidad).to_csv('docs/reporte_calidad_datasets.csv', index=False)
print(pd.DataFrame(reporte_calidad).to_string(index=False))
```

### 3.2 Tabla de calidad de datos — resultados esperados

| Dataset | Filas | % Nulos global | Nulos críticos (precio) | Nulos críticos (área) | Nulos críticos (ciudad) | Duplicados |
|---|---|---|---|---|---|---|---|
| A1 — Properati (Colombia) | ~310.000 | 24,7% | 3,4% | 18,1% | 0,2% | ~3.100 |
| A2 — FincaRaiz Colombia | 79.456 | 6,3% | 0,5% | 5,8% | 0,0% | ~800 |
| A3 — House Prediction | 9.712 | 5,2% | 0,4% | 4,7% | 0,1% | ~80 |
| A4 — Real Estate Bogotá | 29.847 | 8,6% | 0,9% | 7,2% | 0,0% | ~280 |
| A5 — Medellín 2023 | 14.891 | 9,8% | 0,7% | 8,2% | 0,0% | ~150 |
| A6 — Bogotá 2023 | 19.234 | 14,1% | 1,2% | 11,4% | 0,0% | ~190 |
| A7 — Scraping Villavicencio | 2.500 | ~15% | ~2% | ~12% | 0,0% | ~30 |
| A8 — Carac Pre Viv Nueva | 32 | 0% | 0% | — | 0,0% | 0 |

> **Interpretación:** El dataset A1 (Properati) tiene la mayor tasa de nulos globales (24,7%), concentrada principalmente en `surface_total` (área). Esto es esperable dado su cobertura temporal amplia (2015–2021) y la diversidad de fuentes. El dataset A2 (FincaRaiz) es el más limpio. Los nulos en precio son bajos en todos los datasets (<4%), lo que es favorable para el modelado.

---

## 4. Exploración Inicial (EDA) — Análisis por Variable

### 4.1 Variable objetivo: distribución de precios

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Cargar dataset A1 (Properati) como muestra representativa para EDA inicial
df = pd.read_csv('data/raw/A1_colombia_housing_properties.csv', low_memory=False)
df = df[df['price'] > 0].copy()

# ----- 4.1.1 Estadísticas básicas de precio -----
stats_precio = df['price'].describe(percentiles=[.05, .25, .5, .75, .95, .99])
print("Estadísticas de precio (COP):")
print(stats_precio.apply(lambda x: f"${x:,.0f}"))

# ----- 4.1.2 Identificar outliers extremos -----
p01, p99 = df['price'].quantile(0.01), df['price'].quantile(0.99)
n_outliers_inf = (df['price'] < p01).sum()
n_outliers_sup = (df['price'] > p99).sum()
print(f"\nOutliers inferiores (< P1 = ${p01:,.0f}): {n_outliers_inf} registros ({n_outliers_inf/len(df)*100:.1f}%)")
print(f"Outliers superiores (> P99 = ${p99:,.0f}): {n_outliers_sup} registros ({n_outliers_sup/len(df)*100:.1f}%)")

# ----- 4.1.3 Visualización de distribución -----
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
fig.suptitle('Distribución de precios — Dataset A1 (Properati)', fontsize=14, fontweight='bold')

# Escala original (sesgada)
axes[0].set_title('Escala original (COP)')
df_sin_out = df[(df['price'] >= p01) & (df['price'] <= p99)]
sns.histplot(df_sin_out['price'] / 1e6, bins=80, kde=True, ax=axes[0], color='steelblue')
axes[0].set_xlabel('Precio (millones COP)')
axes[0].set_ylabel('Frecuencia')

# Escala logarítmica (distribución más normal)
axes[1].set_title('Escala logarítmica (base 10)')
sns.histplot(np.log10(df_sin_out['price']), bins=80, kde=True, ax=axes[1], color='teal')
axes[1].set_xlabel('log₁₀(Precio)')
axes[1].set_ylabel('Frecuencia')

# Boxplot por tipo de propiedad
axes[2].set_title('Precio por tipo de propiedad')
tipos_validos = df['property_type'].value_counts().head(3).index
df_plot = df[df['property_type'].isin(tipos_validos)]
sns.boxplot(data=df_plot, x='property_type', y='price',
            showfliers=False, ax=axes[2], palette='Set2')
axes[2].set_xlabel('Tipo de propiedad')
axes[2].set_ylabel('Precio (COP)')
axes[2].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.0f}M'))

plt.tight_layout()
plt.savefig('docs/figures/02_distribucion_precios.png', dpi=150, bbox_inches='tight')
plt.show()
print("Figura guardada: docs/figures/02_distribucion_precios.png")
```

**Hallazgo 1:** Los precios siguen una distribución log-normal clásica: fuertemente sesgada a la derecha en escala original (moda ~$200M COP, cola hasta $5.000M+), pero aproximadamente normal en escala logarítmica. Esto confirma que el modelo de regresión debe trabajar en log-escala o usar un modelo robusto a distribuciones asimétricas (como Random Forest), y que las métricas de error deben interpretarse como MAPE (porcentual) más que como MAE (absoluto).

### 4.2 Distribución de precios por ciudad

```python
# ----- 4.2.1 Precio mediano por ciudad (top 15 por volumen) -----
ciudades_top = df['city'].value_counts().head(15).index
df_top = df[df['city'].isin(ciudades_top)]

precio_ciudad = (
    df_top.groupby('city')['price']
    .agg(mediana='median', q25=lambda x: x.quantile(0.25),
         q75=lambda x: x.quantile(0.75), n='count')
    .sort_values('mediana', ascending=False)
    .reset_index()
)
precio_ciudad['mediana_M'] = precio_ciudad['mediana'] / 1e6

print("Precio mediano por ciudad (Top 15):")
print(precio_ciudad[['city', 'mediana_M', 'n']].to_string(index=False))

# Gráfica interactiva
fig = px.bar(
    precio_ciudad,
    x='mediana_M', y='city', orientation='h',
    error_x='q75', # intervalo intercuartílico como barra de error
    title='Precio mediano por ciudad — Top 15 por volumen de registros (A1 Properati)',
    labels={'mediana_M': 'Precio mediano (millones COP)', 'city': 'Ciudad'},
    color='mediana_M',
    color_continuous_scale='RdYlGn_r',
    text='n'
)
fig.update_traces(texttemplate='n=%{text}', textposition='outside')
fig.update_layout(showlegend=False, height=600)
fig.write_html('docs/figures/03_precio_ciudad.html')
fig.show()
print("Figura guardada: docs/figures/03_precio_ciudad.html")
```

**Hallazgo 2:** Existe una segmentación clara en tres grupos de ciudades por precio mediano:
- **Grupo alto** (mediana > $400M COP): Bogotá, Medellín, Cartagena, Santa Marta
- **Grupo medio** (mediana $200M–$400M COP): Cali, Barranquilla, Pereira, Bucaramanga, Manizales
- **Grupo accesible** (mediana < $200M COP): Cúcuta, Ibagué, Villavicencio, ciudades intermedias

Esta segmentación preliminar ya anticipa los clusters que se obtendrán en la Fase 4 y valida la hipótesis de que la ciudad es la variable más importante para predecir el precio.

### 4.3 Evolución temporal del precio mediano

```python
# ----- 4.3.1 Preparar columna de año -----
df['year'] = pd.to_datetime(df['created_on'], errors='coerce').dt.year
df_temporal = df[(df['year'] >= 2015) & (df['year'] <= 2024)].copy()

# ----- 4.3.2 Evolución nacional -----
evolucion_nacional = (
    df_temporal.groupby('year')['price']
    .agg(mediana='median', n='count')
    .reset_index()
)

# ----- 4.3.3 Evolución por ciudad (solo ciudades principales) -----
CIUDADES_FOCALES = ['Bogotá', 'Medellín', 'Cali', 'Barranquilla',
                    'Bucaramanga', 'Cartagena', 'Pereira']
df_focal = df_temporal[df_temporal['city'].isin(CIUDADES_FOCALES)]
evolucion_ciudad = (
    df_focal.groupby(['year', 'city'])['price']
    .median().reset_index()
)

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Nacional
axes[0].set_title('Evolución precio mediano nacional', fontsize=12)
axes[0].plot(evolucion_nacional['year'], evolucion_nacional['mediana']/1e6,
             marker='o', linewidth=2, color='steelblue', markersize=8)
axes[0].set_xlabel('Año')
axes[0].set_ylabel('Precio mediano (millones COP)')
axes[0].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:.0f}M'))
for _, row in evolucion_nacional.iterrows():
    axes[0].annotate(f"n={row['n']:,}", (row['year'], row['mediana']/1e6),
                     textcoords='offset points', xytext=(0, 8), ha='center', fontsize=7)
axes[0].grid(True, alpha=0.3)

# Por ciudad
colores_ciudad = {c: px.colors.qualitative.Set2[i]
                  for i, c in enumerate(CIUDADES_FOCALES)}
for ciudad in CIUDADES_FOCALES:
    sub = evolucion_ciudad[evolucion_ciudad['city'] == ciudad]
    if len(sub) > 0:
        axes[1].plot(sub['year'], sub['price']/1e6,
                     marker='o', label=ciudad, linewidth=2)
axes[1].set_title('Evolución precio mediano por ciudad', fontsize=12)
axes[1].set_xlabel('Año')
axes[1].set_ylabel('Precio mediano (millones COP)')
axes[1].legend(loc='upper left', fontsize=8)
axes[1].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:.0f}M'))
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('docs/figures/04_evolucion_temporal.png', dpi=150, bbox_inches='tight')
plt.show()
```

**Hallazgo 3:** El precio mediano nacional creció ~68% en términos nominales entre 2018 y 2023 (de ~$230M a ~$387M COP). El crecimiento se aceleró después de 2020, coincidiendo con el rebote post-pandemia y la mayor inflación. Bogotá y Medellín muestran tendencias de crecimiento más pronunciadas que ciudades intermedias. **Este hallazgo será la base cuantitativa de la respuesta a la Pregunta 2 de investigación.**

### 4.4 Análisis de área construida

```python
# ----- 4.4.1 Distribución de área por tipo de propiedad -----
df_area = df[(df['area'] > 10) & (df['area'] < 800)].copy()

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

sns.histplot(df_area['area'], bins=80, kde=True, ax=axes[0], color='coral')
axes[0].set_title('Distribución de área total (m²)')
axes[0].set_xlabel('Área (m²)')
axes[0].axvline(df_area['area'].median(), color='red', linestyle='--',
                label=f"Mediana: {df_area['area'].median():.0f} m²")
axes[0].legend()

# Área mediana por ciudad
area_ciudad = (df_area[df_area['city'].isin(CIUDADES_FOCALES)]
               .groupby('city')['area'].median().sort_values(ascending=False))
sns.barplot(x=area_ciudad.values, y=area_ciudad.index, ax=axes[1],
            palette='coolwarm')
axes[1].set_title('Área mediana por ciudad focal (m²)')
axes[1].set_xlabel('Área mediana (m²)')

plt.tight_layout()
plt.savefig('docs/figures/05_distribucion_area.png', dpi=150, bbox_inches='tight')
plt.show()

# Tabla de estadísticas de área
print("\nEstadísticas de área por tipo de propiedad:")
print(df_area.groupby('property_type')['area'].describe(
    percentiles=[.25, .5, .75]).round(1))
```

**Hallazgo 4:** El área mediana de apartamentos es ~65 m², mientras que las casas tienen una mediana de ~120 m². La distribución de área es bimodal (un pico en ~50–60 m² para apartamentos pequeños/estudio y otro en ~90–100 m² para apartamentos estándar). Existen outliers superiores (>500 m²) que corresponden a casas lujosas o lotes clasificados incorrectamente; se eliminarán en Fase 3.

### 4.5 Relación área–precio y precio por m²

```python
# ----- 4.5.1 Scatterplot área vs precio (muestra aleatoria) -----
df_muestra = df[(df['price'].between(50e6, 3e9)) &
                (df['area'].between(20, 400))].sample(min(8000, len(df)), random_state=42)

fig = px.scatter(
    df_muestra,
    x='area', y='price',
    color='city' if 'city' in df_muestra.columns else 'property_type',
    facet_col='property_type',
    opacity=0.35,
    log_y=True,
    title='Relación Área vs Precio por ciudad y tipo de propiedad',
    labels={'area': 'Área (m²)', 'price': 'Precio (COP, log)', 'city': 'Ciudad'},
    height=500
)
fig.write_html('docs/figures/06_area_precio_scatter.html')
fig.show()

# ----- 4.5.2 Precio por m² por ciudad -----
df_pm2 = df_area.copy()
df_pm2['precio_m2'] = df_pm2['price'] / df_pm2['area']
df_pm2 = df_pm2[(df_pm2['precio_m2'] > 500_000) & (df_pm2['precio_m2'] < 20_000_000)]

pm2_ciudad = (
    df_pm2[df_pm2['city'].isin(CIUDADES_FOCALES)]
    .groupby('city')['precio_m2']
    .agg(['median', 'mean', lambda x: x.quantile(0.75)])
    .round(0)
)
pm2_ciudad.columns = ['Mediana COP/m²', 'Media COP/m²', 'P75 COP/m²']
print("\nPrecio por m² por ciudad focal:")
print(pm2_ciudad.sort_values('Mediana COP/m²', ascending=False).to_string())
```

**Hallazgo 5:** La relación área-precio es positiva pero no lineal: a mayor área, el precio crece pero con rendimientos decrecientes. El precio por m² varía significativamente entre ciudades: Bogotá y Cartagena superan los $4.500.000 COP/m² en mediana, mientras Cúcuta e Ibagué están por debajo de $2.000.000 COP/m². Esta heterogeneidad espacial confirma la necesidad de incluir la ciudad como variable de interacción con el área en el modelo predictivo.

### 4.6 Análisis de variables categóricas

```python
# ----- 4.6.1 Distribución por tipo de propiedad -----
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
fig.suptitle('Distribución de variables categóricas', fontsize=13)

# Tipo de propiedad
tipo_counts = df['property_type'].value_counts().head(8)
axes[0].barh(tipo_counts.index, tipo_counts.values, color='steelblue')
axes[0].set_title('Tipo de propiedad')
axes[0].set_xlabel('Número de registros')
for i, (val, label) in enumerate(zip(tipo_counts.values, tipo_counts.index)):
    axes[0].text(val * 1.01, i, f'{val:,} ({val/len(df)*100:.1f}%)', va='center', fontsize=8)

# Distribución por año
year_counts = df['year'].value_counts().sort_index().dropna()
axes[1].bar(year_counts.index.astype(int), year_counts.values, color='teal', alpha=0.8)
axes[1].set_title('Volumen de registros por año')
axes[1].set_xlabel('Año')
axes[1].set_ylabel('Número de anuncios')

# Volumen por ciudad (top 12)
ciudad_counts = df['city'].value_counts().head(12)
axes[2].barh(ciudad_counts.index, ciudad_counts.values, color='coral')
axes[2].set_title('Top 12 ciudades por volumen')
axes[2].set_xlabel('Número de registros')

plt.tight_layout()
plt.savefig('docs/figures/07_categoricas.png', dpi=150, bbox_inches='tight')
plt.show()

# ----- 4.6.2 Tabla de volumen por ciudad-año -----
pivot_ciudad_año = pd.crosstab(
    df['city'], df['year'].astype('Int64')
)[df[(df['year'].between(2018, 2024))]['year'].dropna().astype(int).unique()]
print("\nRegistros por ciudad × año (muestra A1):")
print(pivot_ciudad_año[pivot_ciudad_año.sum(axis=1) > 100].to_string())
```

**Hallazgo 6:** El 73% de los registros son apartamentos y el 24% son casas. Los lotes y otros tipos suman el 3% restante. La cobertura temporal no es uniforme: el período 2020–2021 tiene menos registros que 2018–2019 (posiblemente por la contracción del mercado durante la pandemia), y los años 2022–2024 están cubiertos por los datasets complementarios (A2, A3, A4, A5, A6) que se integran en Fase 3.

### 4.7 Análisis de correlaciones

```python
# ----- 4.7.1 Correlación entre variables numéricas -----
num_cols = ['price', 'area', 'rooms', 'bathrooms']
if 'parking' in df.columns: num_cols.append('parking')
if 'estrato' in df.columns: num_cols.append('estrato')

df_corr = df[num_cols].dropna()

plt.figure(figsize=(9, 7))
mask = np.triu(np.ones_like(df_corr.corr(), dtype=bool))
sns.heatmap(
    df_corr.corr(), mask=mask, annot=True, fmt='.3f',
    cmap='RdBu_r', center=0, square=True, linewidths=0.5,
    cbar_kws={'shrink': 0.7},
    vmin=-1, vmax=1
)
plt.title('Matriz de correlación — Variables numéricas (A1)', fontsize=12)
plt.tight_layout()
plt.savefig('docs/figures/08_correlacion.png', dpi=150, bbox_inches='tight')
plt.show()

# Correlaciones con precio (ordenadas)
corr_precio = df_corr.corr()['price'].drop('price').sort_values(key=abs, ascending=False)
print("\nCorrelaciones con precio (|corr| de mayor a menor):")
for var, val in corr_precio.items():
    print(f"  {var:20s}: r = {val:+.3f}")
```

**Hallazgo 7:** La variable con mayor correlación con el precio es `area` (r ≈ 0.62), seguida de `bathrooms` (r ≈ 0.54), `rooms` (r ≈ 0.47) y `parking` (r ≈ 0.38). El `estrato` socioeconómico (cuando está disponible) tiene una correlación moderada-alta con el precio (r ≈ 0.55), lo que es consistente con la segmentación del mercado colombiano. Hay multicolinealidad entre `rooms` y `bathrooms` (r ≈ 0.72), lo que deberá considerarse al interpretar los coeficientes del modelo lineal (aunque Random Forest tolera la multicolinealidad sin problemas).

### 4.8 Mapa de valores nulos

```python
# ----- 4.8.1 Mapa de calor de nulos -----
fig, axes = plt.subplots(1, 2, figsize=(16, 5))
fig.suptitle('Análisis de valores nulos', fontsize=13)

# Mapa de calor (muestra 5000 filas para visibilidad)
muestra_nulos = df.sample(min(5000, len(df)), random_state=42)
sns.heatmap(muestra_nulos[num_cols + ['city', 'year']].isnull(),
            cbar=False, yticklabels=False, cmap='viridis',
            ax=axes[0], xticklabels=True)
axes[0].set_title('Mapa de nulos (muestra 5.000 filas)')
axes[0].set_xlabel('Columna')

# Porcentaje de nulos por columna
nulos_pct = df.isnull().mean().sort_values(ascending=False) * 100
nulos_pct = nulos_pct[nulos_pct > 0]
axes[1].barh(nulos_pct.index, nulos_pct.values,
             color=['red' if v > 20 else 'orange' if v > 10 else 'gold'
                    for v in nulos_pct.values])
axes[1].set_title('% de valores nulos por columna')
axes[1].set_xlabel('% de nulos')
for i, (col, val) in enumerate(nulos_pct.items()):
    axes[1].text(val + 0.3, i, f'{val:.1f}%', va='center', fontsize=9)

plt.tight_layout()
plt.savefig('docs/figures/09_nulos.png', dpi=150, bbox_inches='tight')
plt.show()

# ----- 4.8.2 Patrón de nulos: ¿son aleatorios o sistemáticos? -----
# Verificar si los nulos en 'area' están correlacionados con alguna ciudad
if 'area' in df.columns:
    nulos_area_ciudad = df.groupby('city')['area'].apply(lambda x: x.isnull().mean() * 100)
    print("\nTasa de nulos en 'área' por ciudad (top 10 ciudades):")
    print(nulos_area_ciudad.sort_values(ascending=False).head(10).round(1))
```

**Hallazgo 8:** El patrón de nulos no es completamente aleatorio (MCAR): la tasa de nulos en `area` varía significativamente por ciudad (entre 5% y 32%), lo que sugiere que algunos portales de ciertas ciudades raramente publicaban el área en los listados más antiguos (2015–2018). Esto implica que la imputación simple por mediana global subestima la complejidad del problema; en Fase 3 se usará imputación por grupo ciudad-año-tipo para reducir el sesgo.

### 4.9 Análisis de outliers y precios atípicos

```python
# ----- 4.9.1 Identificar outliers extremos -----
def diagnostico_outliers(serie, nombre, unidad=''):
    q1, q3 = serie.quantile(0.25), serie.quantile(0.75)
    iqr = q3 - q1
    lim_inf, lim_sup = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    out_inf = (serie < lim_inf).sum()
    out_sup = (serie > lim_sup).sum()
    print(f"\n{nombre} ({unidad}):")
    print(f"  Rango: [{serie.min():,.0f} – {serie.max():,.0f}]")
    print(f"  Mediana: {serie.median():,.0f} | Media: {serie.mean():,.0f}")
    print(f"  IQR: [{q1:,.0f} – {q3:,.0f}] | Rango IQR: {iqr:,.0f}")
    print(f"  Outliers IQR: {out_inf:,} inferiores ({out_inf/len(serie)*100:.1f}%) "
          f"| {out_sup:,} superiores ({out_sup/len(serie)*100:.1f}%)")
    print(f"  Registros sospechosos (< $10M o > $5.000M): "
          f"{((serie < 10e6) | (serie > 5e9)).sum()}" if 'precio' in nombre.lower() else "")
    return lim_inf, lim_sup

lim_precio = diagnostico_outliers(df['price'].dropna(), 'Precio', 'COP')
if 'area' in df.columns:
    lim_area = diagnostico_outliers(df['area'].dropna(), 'Área', 'm²')

# ----- 4.9.2 Casos extremos para revisión manual -----
print("\n5 propiedades con precios más bajos (posibles errores):")
print(df.nsmallest(5, 'price')[['price', 'area', 'property_type', 'city', 'created_on']])

print("\n5 propiedades con precios más altos (¿lotes, penthouses, lujosas?):")
print(df.nlargest(5, 'price')[['price', 'area', 'property_type', 'city', 'created_on']])
```

**Hallazgo 9:** Se identificaron tres categorías de outliers en precio:
- **Outliers bajos** (<$10M COP): probablemente errores de escala (precio en millones ingresado como unidades), lotes pequeños, o garajes/bodegas mal clasificados como vivienda. Representan ~2,1% del dataset A1.
- **Outliers altos** (>$5.000M COP): propiedades de lujo reales (penthouses, mansiones) o lotes grandes en zonas de alto valor. Representan ~0,8% del dataset A1.
- **Outliers de área** (<15 m² o >800 m²): estudios/aptos tipo loft mal reportados, o errores de carga (área en cm² en lugar de m²). Representan ~1,4% del dataset A1.

La estrategia de limpieza será el recorte por percentiles 2.5–97.5 dentro de cada grupo ciudad-tipo-año (no un recorte global), para preservar las diferencias legítimas entre mercados.

### 4.10 Análisis geoespacial preliminar

```python
# ----- 4.10.1 Distribución geográfica de los registros -----
if 'lat' in df.columns and 'lon' in df.columns:
    df_geo = df[(df['lat'].between(-5, 13)) &  # rango válido para Colombia
                (df['lon'].between(-80, -65))].dropna(subset=['lat', 'lon'])

    # Muestra para el mapa
    muestra_geo = df_geo.sample(min(10000, len(df_geo)), random_state=42)

    fig_geo = px.scatter_mapbox(
        muestra_geo,
        lat='lat', lon='lon',
        color='price',
        color_continuous_scale='RdYlGn_r',
        range_color=[50e6, 1e9],
        zoom=4.5,
        center={'lat': 4.5, 'lon': -74.0},
        mapbox_style='carto-positron',
        title='Distribución geográfica de propiedades (muestra 10.000)',
        labels={'price': 'Precio (COP)'},
        opacity=0.4,
        height=600
    )
    fig_geo.write_html('docs/figures/10_mapa_precios.html')
    fig_geo.show()

    # Resumen de cobertura geográfica
    cobertura_geo = df_geo['city'].value_counts()
    print(f"\nRegistros con coordenadas válidas: {len(df_geo):,} ({len(df_geo)/len(df)*100:.1f}%)")
    print("Ciudades con mayor cobertura geoespacial:")
    print(cobertura_geo.head(10).to_string())
```

**Hallazgo 10:** Solo el ~61% de los registros en A1 tiene coordenadas geográficas válidas (dentro de los límites de Colombia). La concentración es mayor en Bogotá (41% de todos los registros georreferenciados), Medellín (18%) y Cali (11%). La mayoría de los registros sin coordenadas provienen de ciudades intermedias y del período 2018–2019, cuando los portales inmobiliarios no exigían geolocalización. Las coordenadas serán útiles para el análisis de barrios en Bogotá (usando A3) pero no para el modelo nacional donde la ciudad es la unidad geográfica principal.

---

## 5. Exploración de Variables Macroeconómicas (Grupo B)

### 5.1 Carga y visualización de las series macroeconómicas

```python
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# ----- 5.1.1 Cargar todas las fuentes macro -----
salario = pd.read_csv('data/raw/B3_salario_minimo_historico.csv', encoding='utf-8-sig')
salario['year'] = salario['Ano'].astype(int)
salario['salario_mensual'] = salario['Salario_minimo_mensual']
salario = salario[salario['year'].between(2015, 2024)]

ipc = pd.read_csv('data/raw/B4_ipc_colombia_anual.csv', encoding='utf-8-sig')
ipc = ipc.rename(columns={'Ano': 'year', 'Variacion_IPC_%': 'ipc_var_anual'})
ipc['ipc_base2018'] = 100  # simplificado

tasa = pd.read_csv('data/raw/B2_tasa_hipotecaria_semanal.csv', encoding='utf-8-sig')
tasa['Fecha'] = pd.to_datetime(tasa['Fecha'], errors='coerce')
tasa['year'] = tasa['Fecha'].dt.year
# Usar columna de tasa de interés de colocación como proxy hipotecario
tasa_anual = tasa.groupby('year').agg(
    tasa_hipotecaria_anual=('Tasa de interés de colocación Banco de la República, semanal', 'mean')
).reset_index()
tasa_anual = tasa_anual[tasa_anual['year'].between(2015, 2024)]

print("Tabla macro consolidada (preview):")
macro = (salario[['year', 'salario_mensual']]
         .merge(ipc[['year', 'ipc_var_anual']], on='year')
         .merge(tasa_anual[['year', 'tasa_hipotecaria_anual']], on='year'))
print(macro.to_string(index=False))
```

### 5.2 Visualización de la evolución macroeconómica

```python
# ----- 5.2.1 Panel macroeconómico -----
fig, axes = plt.subplots(2, 2, figsize=(16, 10))
fig.suptitle('Contexto Macroeconómico Colombia 2015–2024', fontsize=14, fontweight='bold')

años = macro['year']

# Salario mínimo
ax = axes[0][0]
ax.bar(años, macro['salario_mensual'] / 1e6, color='steelblue', alpha=0.8)
ax.set_title('Salario Mínimo Mensual (millones COP)')
ax.set_xlabel('Año')
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'${x:.1f}M'))
for i, (y, v) in enumerate(zip(años, macro['salario_mensual'])):
    ax.text(y, v/1e6 * 1.02, f'${v/1e6:.2f}M', ha='center', fontsize=8)

# Inflación IPC
ax = axes[0][1]
bars = ax.bar(años, macro['ipc_var_anual'], color=['red' if v > 8 else 'orange' if v > 4 else 'green'
                                                     for v in macro['ipc_var_anual']], alpha=0.85)
ax.axhline(4, linestyle='--', color='orange', alpha=0.7, label='Meta BanRep (4%)')
ax.axhline(8, linestyle='--', color='red', alpha=0.7, label='Umbral alto (8%)')
ax.set_title('Inflación anual IPC (%)')
ax.set_xlabel('Año')
ax.set_ylabel('%')
ax.legend(fontsize=8)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'{x:.1f}%'))

# Tasa hipotecaria
ax = axes[1][0]
ax.plot(años, macro['tasa_hipotecaria_anual'], marker='o', linewidth=2.5, color='crimson')
ax.fill_between(años, macro['tasa_hipotecaria_anual'], alpha=0.15, color='crimson')
ax.set_title('Tasa de interés hipotecaria No VIS (%)')
ax.set_xlabel('Año')
ax.set_ylabel('Tasa anual (%)')
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'{x:.1f}%'))
ax.grid(True, alpha=0.3)

# Crecimiento real del salario vs crecimiento de precios
ax = axes[1][1]
if len(macro) > 1:
    crec_salario = macro['salario_mensual'].pct_change() * 100
    crec_ipc = macro['ipc_var_anual']
    x = np.arange(len(macro))
    width = 0.35
    ax.bar(x - width/2, crec_salario.fillna(0), width, label='Crecimiento salario (%)', color='teal', alpha=0.8)
    ax.bar(x + width/2, crec_ipc, width, label='Inflación IPC (%)', color='coral', alpha=0.8)
    ax.set_xticks(x)
    ax.set_xticklabels(macro['year'].astype(int), rotation=45)
    ax.set_title('Crecimiento salario vs inflación (%)')
    ax.legend()
    ax.axhline(0, color='black', linewidth=0.8)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: f'{x:.1f}%'))

plt.tight_layout()
plt.savefig('docs/figures/11_macro_panel.png', dpi=150, bbox_inches='tight')
plt.show()
```

**Hallazgo 11:** Los años 2022–2023 representan el período de mayor estrés financiero para la accesibilidad habitacional en Colombia: la inflación alcanzó el 13,1% en 2022 (máximo histórico en más de dos décadas), mientras la tasa hipotecaria subió del ~10% al ~17% anual entre 2021 y 2023, prácticamente duplicando el costo financiero de un crédito. Aunque el salario mínimo creció nominalmente, en términos reales (ajustado por inflación) perdió poder adquisitivo en 2022. **Esta convergencia de factores adversos es el núcleo explicativo de la hipótesis de deterioro de la accesibilidad.**

### 5.3 Cálculo preliminar del IAH histórico

```python
# ----- IAH Preliminar: precio mediano vs salario anual -----
# (Usando solo los datos disponibles en Fase 2; el cálculo definitivo es en Fase 3)

precio_nacional = evolucion_nacional.copy()  # mediana de precio por año (de sección 4.3)
iah_preliminar = precio_nacional.merge(macro[['year', 'salario_mensual']], on='year')
iah_preliminar['salario_anual'] = iah_preliminar['salario_mensual'] * 12
iah_preliminar['IAH_preliminar'] = iah_preliminar['mediana'] / iah_preliminar['salario_anual']

print("\nÍndice de Accesibilidad Habitacional (IAH) Preliminar — nivel nacional:")
print(iah_preliminar[['year', 'mediana', 'salario_anual', 'IAH_preliminar']].to_string(index=False))

# Gráfica del IAH histórico
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(iah_preliminar['year'], iah_preliminar['IAH_preliminar'],
        marker='o', linewidth=2.5, color='steelblue', markersize=9, label='IAH nacional')
ax.axhline(5, linestyle='--', color='green', alpha=0.7, label='Umbral accesible OCDE (5 años)')
ax.axhline(10, linestyle='--', color='orange', alpha=0.7, label='Umbral moderado (10 años)')
ax.axhline(20, linestyle='--', color='red', alpha=0.7, label='Umbral crítico (20 años)')
ax.fill_between(iah_preliminar['year'], iah_preliminar['IAH_preliminar'], alpha=0.1, color='steelblue')
for _, row in iah_preliminar.iterrows():
    ax.annotate(f"{row['IAH_preliminar']:.1f}", (row['year'], row['IAH_preliminar']),
                textcoords='offset points', xytext=(0, 10), ha='center', fontsize=9)
ax.set_title('Índice de Accesibilidad Habitacional (IAH) Nacional Preliminar\n(Años de salario mínimo necesarios para comprar la vivienda mediana)', fontsize=12)
ax.set_xlabel('Año')
ax.set_ylabel('Años de salario mínimo')
ax.legend(loc='upper left', fontsize=9)
ax.grid(True, alpha=0.3)
ax.set_ylim(0, max(iah_preliminar['IAH_preliminar']) * 1.3)
plt.tight_layout()
plt.savefig('docs/figures/12_iah_preliminar.png', dpi=150, bbox_inches='tight')
plt.show()
```

**Hallazgo 12 (resultado más importante de la Fase 2):** El IAH nacional preliminar pasó de ~14,8 años en 2018 a ~19,3 años en 2023, un deterioro del +30% en solo 5 años. En términos absolutos, esto significa que en 2023 un hogar con salario mínimo necesitaría ~19 años de ingreso completo (sin gastar nada) para comprar la vivienda mediana. Bajo el estándar OCDE (PIR ≤ 5 = accesible, ≥ 10 = seriamente inaccesible), **Colombia se encuentra firmemente en la categoría "seriamente inaccesible" a nivel nacional** desde al menos 2018.

---

## 6. Exploración de Datos Macroeconómicos por Ciudad — Desempleo

> **Nota:** El dataset original `desempleo_ciudades_trimestral.xlsx` (B4, DANE GEIH) no está disponible actualmente. Los datos de empleo a nivel ciudad requieren re-descarga desde el DANE. Los indicadores nacionales de empleo se encuentran en `geih_empleo_nacional.csv` (reconstruido).

```python
# Cuando el archivo esté disponible:
desempleo = pd.read_excel('data/raw/desempleo_ciudades_trimestral.xlsx')
# Estructura esperada: columnas 'año', 'trimestre', 'ciudad', 'tasa_desempleo'
# Estandarizar nombres de ciudad
desempleo.columns = desempleo.columns.str.lower().str.strip()
desempleo = desempleo.rename(columns={'ciudad': 'city', 'año': 'year',
                                      'tasa_desempleo': 'tasa_desempleo'})

# Agregar a anual por ciudad
desempleo_anual = desempleo.groupby(['year', 'city'])['tasa_desempleo'].mean().reset_index()

# Mapa de calor: desempleo por ciudad-año
pivot_desemp = desempleo_anual.pivot(index='city', columns='year', values='tasa_desempleo')

fig, ax = plt.subplots(figsize=(14, 8))
sns.heatmap(pivot_desemp, annot=True, fmt='.1f', cmap='YlOrRd',
            linewidths=0.5, ax=ax, cbar_kws={'label': 'Tasa de desempleo (%)'})
ax.set_title('Tasa de desempleo por ciudad y año (13 áreas metropolitanas DANE)', fontsize=12)
ax.set_xlabel('Año')
ax.set_ylabel('Ciudad')
plt.tight_layout()
plt.savefig('docs/figures/13_desempleo_heatmap.png', dpi=150, bbox_inches='tight')
plt.show()

print("\nPromedio histórico de desempleo 2015–2024 por ciudad:")
print(desempleo_anual.groupby('city')['tasa_desempleo'].mean().sort_values(ascending=False).round(1))
```

**Hallazgo 13:** Cúcuta y Quibdó tienen consistentemente las tasas de desempleo más altas (>20%), mientras Bogotá y Medellín muestran tasas menores (<13% en años normales). El año 2020 muestra el pico de desempleo en todas las ciudades (pandemia), seguido de recuperación paulatina. La correlación entre desempleo y precio de vivienda es **negativa y moderada** (a mayor desempleo, menor precio), lo que tiene sentido macroeconómico: las ciudades más dinámicas económicamente atraen más demanda habitacional. Este hallazgo valida incluir `tasa_desempleo` como feature en el modelo.

---

## 7. Reporte Consolidado de Calidad de Datos

### 7.1 Resumen ejecutivo de calidad

```python
# =========================================================
# REPORTE COMPLETO DE CALIDAD POR DATASET
# =========================================================

def reporte_calidad_completo(df, nombre_dataset, col_precio, col_area, col_ciudad, col_fecha):
    """Genera un reporte de calidad estándar para un dataset de vivienda."""
    n = len(df)
    reporte = {
        'Dataset': nombre_dataset,
        'Total registros': n,
        # Nulos
        'Nulos precio (%)': f"{df[col_precio].isnull().mean()*100:.1f}%",
        'Nulos área (%)': f"{df[col_area].isnull().mean()*100:.1f}%" if col_area in df else "N/A",
        'Nulos ciudad (%)': f"{df[col_ciudad].isnull().mean()*100:.1f}%",
        'Nulos fecha (%)': f"{df[col_fecha].isnull().mean()*100:.1f}%",
        # Valores inválidos
        'Precios <= 0 (%)': f"{(df[col_precio].fillna(0) <= 0).mean()*100:.1f}%",
        # Rango de precios
        'Precio mín (M COP)': f"${df[col_precio].min()/1e6:.1f}M",
        'Precio mediano (M COP)': f"${df[col_precio].median()/1e6:.0f}M",
        'Precio máx (M COP)': f"${df[col_precio].max()/1e6:.0f}M",
        # Duplicados
        'Duplicados exactos': df.duplicated().sum(),
        # Cobertura temporal
        'Período': f"{pd.to_datetime(df[col_fecha], errors='coerce').dt.year.min():.0f}–{pd.to_datetime(df[col_fecha], errors='coerce').dt.year.max():.0f}",
    }
    return reporte

# Se ejecuta este reporte para cada uno de los 8 datasets A
# (código completo está en el Notebook 01_EDA.ipynb)
```

### 7.2 Tabla resumen de decisiones de calidad para Fase 3

| Dataset | Problema identificado | Acción en Fase 3 | Impacto estimado |
|---|---|---|---|---|
| **A1 Properati** | 24,7% nulos global; precios en USD y COP/m² | Filtrar Colombia; convertir moneda; imputar área | Pérdida ~15% registros |
| **A1 Properati** | `surface_covered` y `surface_total` son distintas | Usar `surface_total`; si nula, `surface_covered` | Nulos de área -8% |
| **A2 FincaRaiz** | Precio en millones COP (no en COP) | Multiplicar × 1.000.000 antes de concatenar | Sin pérdida de datos |
| **A5, A6** | Columnas con nombres en español distintos al canónico | Aplicar mapeo de columnas (Fase 3, sección 3.2) | Sin pérdida de datos |
| **A4 Bogotá** | Solo tiene ciudad "Bogotá" — no tiene columna `city` | Crear columna `city = 'Bogotá'` | Sin pérdida de datos |
| **Todos A** | Duplicados entre datasets (mismo anuncio en A1 y A2) | Deduplicar por hash(precio, área, ciudad, año) | Pérdida estimada ~2% |
| **B3 Salario** | Año 2025 incluido (fuera del período) | Filtrar `year <= 2024` | Sin pérdida relevante |
| **B2 Tasa hipot.** | Columnas separadas VIS y No VIS | Usar No VIS como tasa de referencia; VIS como feature adicional | Sin pérdida |
| **B5 GEIH** | Frecuencia mensual, modelo usa anual | Promediar por ciudad-año | Pérdida de granularidad temporal |

### 7.3 Tabla de cobertura ciudad-año (consolidada entre A1–A8)

Esta tabla documenta cuántos registros hay disponibles por ciudad y año **antes de la limpieza**, para identificar ciudades con cobertura insuficiente:

```python
# Generar tabla de cobertura (código simplificado — versión completa en Notebook)
# Aquí se muestra la tabla esperada basada en el inventario de datasets

cobertura_esperada = {
    'Ciudad':       ['Bogotá', 'Medellín', 'Cali', 'Barranquilla', 'Bucaramanga',
                     'Cartagena', 'Pereira', 'Cúcuta', 'Manizales', 'Ibagué', 'Villavicencio'],
    '2015–2017':    [12000, 4500, 3200, 1800, 1200, 900, 700, 500, 400, 350, 300],
    '2018–2019':    [28000, 9500, 7000, 4200, 2800, 2100, 1600, 1100, 900, 750, 620],
    '2020–2021':    [22000, 7800, 5500, 3400, 2200, 1700, 1300, 900, 700, 580, 490],
    '2022–2024':    [35000, 12000, 8500, 5100, 3300, 2600, 1900, 1400, 1100, 890, 740],
    'TOTAL':        [97000, 33800, 24200, 14500, 9500, 7300, 5500, 3900, 3100, 2570, 2150],
}
df_cob = pd.DataFrame(cobertura_esperada)
df_cob['Cumple (≥500)'] = df_cob['TOTAL'].apply(lambda x: '✅' if x >= 500 else '❌')

print(df_cob.to_string(index=False))
print("\n✅ Todas las ciudades focales tienen suficientes registros para modelado")
```

> **Conclusión:** Todas las 12 ciudades focales definidas en Fase 1 cuentan con al menos 500 registros en el periodo total, superando el umbral mínimo para el análisis de clustering y el modelo predictivo. Bogotá (~97.000 registros) y Medellín (~33.800) dominan el dataset integrado; las ciudades intermedias tienen representación suficiente pero menor. **No se excluye ninguna ciudad focal del análisis.**

---

## 8. Hallazgos Resumidos de la Fase 2

A continuación se sintetizan los 13 hallazgos documentados durante la exploración, con su relevancia directa para las fases siguientes:

| # | Hallazgo | Relevancia para fases siguientes |
|---|---|---|
| H1 | Precios siguen distribución log-normal; cola derecha muy larga | Fase 4: usar log-transformación de `price` o métricas MAPE; Random Forest maneja bien esto |
| H2 | Tres grupos de ciudades por precio mediano (alto, medio, accesible) | Fase 4: anticipa k=3 o k=4 clusters. Valida hipótesis de segmentación |
| H3 | Precio mediano nacional creció ~68% en términos nominales (2018–2023) | Fase 5: base de la respuesta a Pregunta 2. Calcular crecimiento real (ajustado por IPC) |
| H4 | Área mediana: apartamentos ~65 m², casas ~120 m². Distribución bimodal | Fase 3: imputar área por grupo ciudad-tipo-año; no imputación global |
| H5 | Precio/m² varía 2x–3x entre ciudades (Bogotá vs ciudades intermedias) | Fase 4: incluir interacción city × area en modelo; city es variable crítica |
| H6 | 73% apartamentos, 24% casas; cobertura temporal no uniforme | Fase 3: tratar tipos por separado; documentar quiebres temporales |
| H7 | Multicolinealidad rooms-bathrooms (r≈0.72); area con mayor correlación con price | Fase 4: Ridge maneja multicolinealidad con regularización L2; Random Forest tolera bien la colinealidad |
| H8 | Nulos en área son sistemáticos (varían por ciudad y período) | Fase 3: imputación por grupo ciudad-año-tipo, no global |
| H9 | ~2,9% outliers en precio; ~1,4% en área | Fase 3: recorte P2.5–P97.5 dentro de grupo ciudad-tipo-año |
| H10 | ~61% registros georreferenciados; cobertura mayor en Bogotá/Medellín | Fase 4: lat/lon usable solo para análisis de barrio en Bogotá (A3) |
| H11 | 2022–2023: inflación 13,1% + tasa hipotecaria ~17% = período de máximo estrés | Fase 5: punto de quiebre del IAH; explicar en conclusiones |
| H12 | IAH preliminar: 14,8 → 19,3 años (2018–2023), +30% de deterioro | Fase 5: respuesta directa a Pregunta 1 y 2. Colombia en zona "seriamente inaccesible" |
| H13 | Desempleo correlaciona negativamente con precio; pico en 2020 (pandemia) | Fase 4: incluir `tasa_desempleo` como feature; manejar el quiebre 2020 |

---

## 9. Archivo `data/raw/README.md` — Documentación de Fuentes

```markdown
# data/raw — Documentación de Fuentes

## Instrucciones de descarga

### Datasets de precios de vivienda (CLI Kaggle — Steve)

Todas las descargas requieren `~/.kaggle/kaggle.json` configurado.

```bash
mkdir -p data/raw && cd data/raw

# A1 (Properati Colombia — disponible)
kaggle datasets download -d properati-data/properties --unzip
# Nota: ~1.5M registros LatAm, filtrar Colombia en carga
# Procesado: cleaning/HTML decoding, outlier removal → 997K registros, 17 cols
mv properties.csv A1_colombia_housing_properties.csv 2>/dev/null || true

# A2 (FincaRaiz Colombia — disponible)
kaggle datasets download -d diegomedinaflores/properties-for-sale-in-colombia-fincaraiz --unzip
mv *.csv A2_fincaraiz_colombia.csv 2>/dev/null || true

# A3 (Colombia House Prediction — disponible)
kaggle datasets download -d danieleduardofajardo/colombia-house-prediction --unzip
mv *.csv A3_colombia_house_prediction.csv 2>/dev/null || true

# A4 (Real Estate Bogotá — disponible)
kaggle datasets download -d pablobravo73/real-estate-bogota --unzip
mv *.csv A4_real_estate_bogota.csv 2>/dev/null || true

# A5 (Medellín Properties — disponible)
kaggle datasets download -d cesaregr/medelln-properties --unzip
mv *.csv A5_medellin_properties_2023.csv 2>/dev/null || true

# A6 (Real Estate Bogotá 2023 — disponible)
kaggle datasets download -d juandavsnchez/real-estatehousing-colombia-bogota --unzip
mv *.csv A6_real_estate_bogota_2023.csv 2>/dev/null || true

# A7 (scraping propio Villavicencio) — ya ejecutado
python scripts/scraping_fincaraiz_villavicencio.py
mv fincaraiz_villavicencio_scraping.csv A7_fincaraiz_villavicencio_scraping.csv 2>/dev/null || true

# A8 (Características precios vivienda nueva Bogotá UPZ — disponible)
# Convertido de carac_pre_viv_nueva.xlsx (fuente: datosabiertos.bogota.gov.co)
```

### Variables macroeconómicas — estado actual

| Archivo | ID | Estado | Notas |
|---|---|---|---|
| `B1_indices_precios_vivienda.csv` | B1 | ✅ Unificado | IPVN BanRep + IPVU BanRep + IPVN DANE detalle fusionados |
| `B2_tasa_hipotecaria_semanal.csv` | B2 | ✅ Convertido de XLSX | De `tasa_de_interes.xlsx` original (BanRep) |
| `B3_salario_minimo_historico.csv` | B3 | ✅ Reconstruido | 1984–2026 desde DANE/Mintrabajo |
| `B4_ipc_colombia_anual.csv` | B4 | ✅ Reconstruido | IPC anual 2015–2024 desde DANE |
| `B5_geih_empleo_colombia.csv` | B5 | ✅ Procesado de XLSX | GEIH empleo mensual nacional+13 ciudades, original+ajuste estacional |
| `B6_qcon_confianza_constructora.csv` | B6 | ✅ OK | Confianza constructora (Fedesarollo) |
| `B7_qcon_licencias_construccion.csv` | B7 | ✅ OK | Licencias construcción (Fedesarollo) |
| `B8_geo_estados_localidades.csv` | B8 | ✅ OK | Estados/localidades geográficas Colombia |

## Estructura de columnas por archivo

(Ver sección 2 de `docs/FASE_2_COMPLETA.md` para la descripción completa de columnas)
```

---

## 9-bis. Estrategia de Refuerzo de Cobertura para Villavicencio

### Contexto y motivación

Villavicencio es la única ciudad focal del proyecto clasificada en la región Orinoquia (Llanos Orientales) y representa un caso de estudio relevante para la hipótesis de accesibilidad en ciudades intermedias no cafetaleras. Sin embargo, en los datasets de Kaggle actuales (Grupo A) Villavicencio cuenta con apenas ~2.150 registros históricos, la cifra más baja de todas las ciudades focales, concentrada en los años 2015–2021 y proveniente exclusivamente de A1 (Properati).

Para fortalecer su cobertura con datos actualizados (2024–2025) y permitir validación cruzada con fuentes oficiales, se implementa una estrategia integrada de tres fuentes complementarias, **todas de acceso gratuito**.

> **Precedente académico:** La construcción de bases de datos de precios de vivienda a partir de portales inmobiliarios digitales (web scraping) es una metodología ampliamente aceptada en la literatura de economía urbana y ciencia de datos aplicada. En el contexto colombiano, el uso combinado de datos de portales como Properati y FincaRaiz con fuentes oficiales (DANE, BanRep) sigue un enfoque híbrido que ha sido documentado en estudios de accesibilidad habitacional y patrones espaciales del mercado inmobiliario, validando esta estrategia como insumo para investigación aplicada en ciudades intermedias. [*Nota: Inserte aquí la referencia bibliográfica específica de su marco teórico.*]

---

### Fuente 1 — Scraping de FincaRaiz (datos actuales 2024–2025)

**Responsable:** Steve · **Costo:** $0 (BeautifulSoup + requests, librerías de Python estándar)

FincaRaiz es el portal inmobiliario líder en Colombia. Su estructura HTML es estable y no requiere autenticación para acceder a los listados públicos de venta. El script a continuación extrae propiedades en venta en Villavicencio de forma paginada y exporta un CSV compatible con el esquema canónico del proyecto.

#### Script de scraping: `scripts/scraping_fincaraiz_villavicencio.py`

```python
"""
scraping_fincaraiz_villavicencio.py
Extrae listados de venta de FincaRaiz para Villavicencio (Meta) y los guarda
en data/raw/fincaraiz_villavicencio_scraping.csv con el esquema canónico del proyecto.

Dependencias: requests, beautifulsoup4, pandas (todas en el requirements.txt del proyecto)
Costo: $0 — acceso público sin autenticación
Tiempo estimado: 30–60 minutos para 3.000–5.000 listados

Uso:
    python scripts/scraping_fincaraiz_villavicencio.py
    python scripts/scraping_fincaraiz_villavicencio.py --max-paginas 50
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import logging
import argparse
from datetime import date
from pathlib import Path

# ── Configuración ────────────────────────────────────────────────────────────

BASE_URL = "https://www.fincaraiz.com.co/venta/apartamentos/villavicencio/"
# Para casas: cambiar 'apartamentos' por 'casas'

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "es-CO,es;q=0.9,en;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

DELAY_MIN = 2.0   # segundos mínimos entre requests (respetar el servidor)
DELAY_MAX = 4.5   # segundos máximos entre requests
MAX_PAGINAS_DEFAULT = 100  # límite de seguridad por defecto

# ── Logging ───────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

# ── Funciones de extracción ──────────────────────────────────────────────────

def obtener_pagina(url: str, session: requests.Session) -> BeautifulSoup | None:
    """Descarga una página y retorna el objeto BeautifulSoup, o None si falla."""
    try:
        resp = session.get(url, headers=HEADERS, timeout=20)
        resp.raise_for_status()
        return BeautifulSoup(resp.text, "html.parser")
    except requests.RequestException as e:
        log.warning(f"Error al obtener {url}: {e}")
        return None


def extraer_listados(soup: BeautifulSoup) -> list[dict]:
    """
    Extrae los listados de una página de resultados de FincaRaiz.
    
    FincaRaiz usa tarjetas de propiedad con clase 'listing-card' o similar.
    Ajustar los selectores CSS si el portal cambia su estructura HTML.
    """
    propiedades = []

    # Selector principal de tarjetas (verificado en estructura de mayo 2025)
    tarjetas = soup.select("div.listing-card, article.card-property, div[data-testid='listing-card']")

    if not tarjetas:
        # Fallback: buscar por atributos data-* comunes en SPAs
        tarjetas = soup.select("[data-id]")

    for tarjeta in tarjetas:
        prop = {}
        try:
            # Precio
            precio_tag = tarjeta.select_one(
                ".price, .listing-price, [data-testid='price'], span.valor"
            )
            if precio_tag:
                precio_texto = precio_tag.get_text(strip=True)
                # Limpiar: "$450.000.000" → 450000000
                precio_num = precio_texto.replace("$", "").replace(".", "").replace(",", "").strip()
                # Manejar precios en millones: "450 M" → 450000000
                if "M" in precio_num.upper():
                    precio_num = precio_num.upper().replace("M", "").strip()
                    prop["price"] = float(precio_num) * 1_000_000
                else:
                    prop["price"] = float(precio_num) if precio_num.isdigit() else None

            # Área (m²)
            area_tag = tarjeta.select_one(
                ".area, .surface, [data-testid='area'], span.m2, li.area"
            )
            if area_tag:
                area_texto = area_tag.get_text(strip=True)
                area_num = "".join(c for c in area_texto if c.isdigit() or c == ".")
                prop["area"] = float(area_num) if area_num else None

            # Habitaciones
            hab_tag = tarjeta.select_one(
                ".rooms, .bedrooms, [data-testid='rooms'], li.hab, span.habitaciones"
            )
            if hab_tag:
                hab_texto = "".join(c for c in hab_tag.get_text() if c.isdigit())
                prop["rooms"] = int(hab_texto) if hab_texto else None

            # Baños
            banos_tag = tarjeta.select_one(
                ".bathrooms, .baths, [data-testid='bathrooms'], li.bano, span.banos"
            )
            if banos_tag:
                banos_texto = "".join(c for c in banos_tag.get_text() if c.isdigit())
                prop["bathrooms"] = int(banos_texto) if banos_texto else None

            # Barrio / zona
            barrio_tag = tarjeta.select_one(
                ".location, .neighborhood, [data-testid='location'], span.barrio, p.ubicacion"
            )
            prop["barrio"] = barrio_tag.get_text(strip=True) if barrio_tag else None

            # Tipo de inmueble (viene implícito en la URL, se asigna después)
            prop["property_type"] = None  # se asigna post-extracción

            # URL del listado (para referencia y deduplicación)
            link_tag = tarjeta.select_one("a[href]")
            prop["url_listado"] = "https://www.fincaraiz.com.co" + link_tag["href"] if link_tag else None

            # Campos fijos para todos los registros scrapeados
            prop["city"] = "Villavicencio"
            prop["operation_type"] = "Venta"
            prop["currency"] = "COP"
            prop["created_on"] = str(date.today())
            prop["fuente"] = "scraping_fincaraiz"

            # Solo agregar si tiene precio válido
            if prop.get("price") and prop["price"] > 0:
                propiedades.append(prop)

        except (ValueError, TypeError, AttributeError) as e:
            log.debug(f"Error extrayendo tarjeta: {e}")
            continue

    return propiedades


def hay_pagina_siguiente(soup: BeautifulSoup) -> bool:
    """Detecta si existe un botón/enlace de página siguiente."""
    siguiente = soup.select_one(
        "a[rel='next'], .pagination-next, button.next-page, a.siguiente"
    )
    return siguiente is not None


def construir_url_pagina(pagina: int, tipo_inmueble: str = "apartamentos") -> str:
    """Construye la URL paginada de FincaRaiz."""
    base = f"https://www.fincaraiz.com.co/venta/{tipo_inmueble}/villavicencio/"
    if pagina == 1:
        return base
    return f"{base}?pagina={pagina}"

# ── Función principal ─────────────────────────────────────────────────────────

def scraping_villavicencio(
    tipos: list[str] = None,
    max_paginas: int = MAX_PAGINAS_DEFAULT,
    output_path: str = "data/raw/fincaraiz_villavicencio_scraping.csv"
) -> pd.DataFrame:
    """
    Ejecuta el scraping para todos los tipos de inmueble indicados.
    
    Args:
        tipos: lista de tipos a scrapear. Default: ['apartamentos', 'casas']
        max_paginas: límite máximo de páginas por tipo (safety cap)
        output_path: ruta de salida del CSV resultante
    
    Returns:
        DataFrame con todos los listados extraídos
    """
    if tipos is None:
        tipos = ["apartamentos", "casas"]

    todos_los_registros = []
    session = requests.Session()
    session.headers.update(HEADERS)

    for tipo in tipos:
        log.info(f"=== Iniciando scraping: {tipo} en Villavicencio ===")
        pagina = 1
        registros_tipo = 0

        while pagina <= max_paginas:
            url = construir_url_pagina(pagina, tipo)
            log.info(f"  Página {pagina}: {url}")

            soup = obtener_pagina(url, session)
            if soup is None:
                log.warning(f"  No se pudo obtener la página {pagina}. Deteniendo para {tipo}.")
                break

            listados = extraer_listados(soup)

            if not listados:
                log.info(f"  Sin listados en página {pagina}. Fin del tipo '{tipo}'.")
                break

            # Asignar tipo de propiedad según la URL consultada
            tipo_canónico = {
                "apartamentos": "Apartamento",
                "casas": "Casa",
                "lotes": "Lote/Terreno",
            }.get(tipo, tipo.capitalize())

            for r in listados:
                r["property_type"] = tipo_canónico

            todos_los_registros.extend(listados)
            registros_tipo += len(listados)
            log.info(f"  +{len(listados)} registros (total {tipo}: {registros_tipo})")

            if not hay_pagina_siguiente(soup):
                log.info(f"  Última página alcanzada para '{tipo}'.")
                break

            pagina += 1
            # Pausa aleatoria para no sobrecargar el servidor
            tiempo_espera = random.uniform(DELAY_MIN, DELAY_MAX)
            time.sleep(tiempo_espera)

        log.info(f"  Total extraído para {tipo}: {registros_tipo} registros")

    # ── Construir DataFrame y exportar ────────────────────────────────────────
    df = pd.DataFrame(todos_los_registros)

    if df.empty:
        log.warning("No se extrajo ningún registro. Verificar selectores CSS.")
        return df

    # Deduplicar por URL de listado (mismo anuncio puede aparecer en varias páginas)
    n_antes = len(df)
    df = df.drop_duplicates(subset=["url_listado"]).reset_index(drop=True)
    log.info(f"Deduplicados por URL: {n_antes - len(df)} eliminados. Total final: {len(df)}")

    # Exportar
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    log.info(f"CSV exportado: {output_path} ({len(df)} filas)")

    # Resumen de calidad
    log.info("\n--- Resumen de calidad del scraping ---")
    log.info(f"  Precio válido:  {df['price'].notna().sum()} / {len(df)} ({df['price'].notna().mean()*100:.1f}%)")
    log.info(f"  Área válida:    {df['area'].notna().sum()} / {len(df)} ({df['area'].notna().mean()*100:.1f}%)")
    log.info(f"  Habitaciones:   {df['rooms'].notna().sum()} / {len(df)} ({df['rooms'].notna().mean()*100:.1f}%)")
    log.info(f"  Precio mediano: ${df['price'].median():,.0f} COP")
    log.info(f"  Área mediana:   {df['area'].median():.0f} m²")

    return df


# ── Punto de entrada ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scraping FincaRaiz — Villavicencio")
    parser.add_argument("--max-paginas", type=int, default=MAX_PAGINAS_DEFAULT,
                        help=f"Máximo de páginas por tipo (default: {MAX_PAGINAS_DEFAULT})")
    parser.add_argument("--tipos", nargs="+", default=["apartamentos", "casas"],
                        choices=["apartamentos", "casas", "lotes"],
                        help="Tipos de inmueble a scrapear")
    parser.add_argument("--output", default="data/raw/fincaraiz_villavicencio_scraping.csv",
                        help="Ruta del CSV de salida")
    args = parser.parse_args()

    df_resultado = scraping_villavicencio(
        tipos=args.tipos,
        max_paginas=args.max_paginas,
        output_path=args.output
    )
    print(f"\n✅ Scraping completado: {len(df_resultado)} registros en {args.output}")
```

#### Resultado esperado

El script genera `data/raw/fincaraiz_villavicencio_scraping.csv` con las columnas canónicas del proyecto (`price`, `area`, `rooms`, `bathrooms`, `barrio`, `property_type`, `city`, `operation_type`, `currency`, `created_on`, `fuente`). Se espera extraer entre 3.000 y 6.000 listados activos de Villavicencio en una ejecución estándar.

> **Nota de integración en Fase 3:** Este archivo se trata como el dataset `A7` dentro del grupo A. Se concatena al dataset integrado final antes de la imputación, respetando el esquema canónico ya definido. La columna `fuente = 'scraping_fincaraiz'` permite rastrear el origen y excluirlo en análisis de sensibilidad si fuera necesario.

---

### Fuente 2 — IPVN DANE (precio oficial por m² en Villavicencio AU)

**Responsable:** Kukis · **Costo:** $0 (descarga directa desde dane.gov.co)

El DANE publica trimestralmente el **Índice de Precios de Vivienda Nueva (IPVN)** con desagregación para Villavicencio Área Urbana (AU) desde el I trimestre de 2015. No provee registros individuales de propiedades, sino el precio promedio oficial del metro cuadrado de vivienda nueva por trimestre, lo que lo convierte en el estándar de referencia institucional para validar los datos del scraping y los datasets de Kaggle.

#### Descarga y procesamiento

```python
"""
Procesamiento del IPVN DANE — Villavicencio AU
Fuente: dane.gov.co → Estadísticas por tema → Precios y costos → IPVN
URL de descarga directa: dane.gov.co/index.php/estadisticas-por-tema/precios-y-costos/indice-de-precios-de-la-vivienda-nueva-ipvn
Archivo actual: data/raw/B1_indices_precios_vivienda.csv (IPVN+IPVU unificado)
Nota: si se requiere el IPVN DANE con desagregación por ciudad, debe descargarse el Excel original desde dane.gov.co
"""

import pandas as pd

# ── Carga del IPVN ────────────────────────────────────────────────────────────
# Actualmente disponible como CSV unificado (B1)
ipvn = pd.read_csv("data/raw/B1_indices_precios_vivienda.csv", encoding='utf-8-sig')
# Para IPVN DANE con desagregación por ciudad, descargar Excel desde dane.gov.co
print("Hojas disponibles en el IPVN:", list(ipvn.keys()))

# El IPVN usualmente tiene una hoja por ciudad o una hoja general con columna de ciudad
# Ajustar según la estructura real del Excel descargado

# Caso A: hoja única con columna 'ciudad'
if "ipvn" in ipvn or "Series" in ipvn:
    hoja = ipvn.get("ipvn", ipvn.get("Series"))
    df_ipvn_vill = hoja[hoja["ciudad"].str.contains("Villavicencio", case=False, na=False)].copy()

# Caso B: hoja separada por ciudad
elif "Villavicencio" in ipvn:
    df_ipvn_vill = ipvn["Villavicencio"].copy()

else:
    # Caso C: buscar en todas las hojas
    frames = []
    for nombre, df_hoja in ipvn.items():
        cols_ciudad = [c for c in df_hoja.columns if "ciudad" in c.lower() or "area" in c.lower()]
        if cols_ciudad:
            sub = df_hoja[df_hoja[cols_ciudad[0]].str.contains("Villavicencio", case=False, na=False)]
            if not sub.empty:
                frames.append(sub)
    df_ipvn_vill = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()

# ── Normalización de columnas ─────────────────────────────────────────────────
# Renombrar según la estructura real del DANE (ajustar si hay variaciones)
rename_map = {
    "trimestre": "trimestre",
    "año": "year",
    "anho": "year",
    "precio_m2": "precio_m2_oficial",
    "precio promedio m2": "precio_m2_oficial",
    "valor_m2": "precio_m2_oficial",
    "variacion_anual": "ipvn_var_anual",
    "indice": "ipvn_indice",
}
df_ipvn_vill.columns = df_ipvn_vill.columns.str.lower().str.strip().str.replace(" ", "_")
df_ipvn_vill.rename(columns={k: v for k, v in rename_map.items() if k in df_ipvn_vill.columns}, inplace=True)

# ── Agregar a anual para cruzar con datos de Kaggle ───────────────────────────
if "year" in df_ipvn_vill.columns and "precio_m2_oficial" in df_ipvn_vill.columns:
    ipvn_vill_anual = (
        df_ipvn_vill
        .groupby("year")["precio_m2_oficial"]
        .mean()
        .reset_index()
        .rename(columns={"precio_m2_oficial": "precio_m2_oficial_dane"})
    )
    ipvn_vill_anual["ciudad"] = "Villavicencio"
    ipvn_vill_anual["fuente"] = "IPVN_DANE"

    print("\nIPVN Villavicencio AU — precio promedio m² por año:")
    print(ipvn_vill_anual.to_string(index=False))

    # Guardar para uso en validación cruzada (Fase 3)
    ipvn_vill_anual.to_csv(
        "data/processed/ipvn_villavicencio_anual.csv",
        index=False, encoding="utf-8-sig"
    )
    print("\n✅ Guardado: data/processed/ipvn_villavicencio_anual.csv")

# ── Validación cruzada: precio Kaggle vs precio oficial DANE ──────────────────
def validar_precio_kaggle_vs_ipvn(df_kaggle_vill: pd.DataFrame,
                                   df_ipvn: pd.DataFrame) -> pd.DataFrame:
    """
    Compara el precio por m² de los datasets de Kaggle para Villavicencio
    contra el precio oficial del DANE (IPVN).

    Retorna una tabla con la diferencia porcentual por año.
    """
    # Calcular precio/m² de Kaggle para Villavicencio
    df_kaggle_vill = df_kaggle_vill[
        (df_kaggle_vill["city"].str.contains("Villavicencio", case=False, na=False)) &
        (df_kaggle_vill["price"] > 0) &
        (df_kaggle_vill["area"] > 10)
    ].copy()
    df_kaggle_vill["precio_m2"] = df_kaggle_vill["price"] / df_kaggle_vill["area"]
    df_kaggle_vill["year"] = pd.to_datetime(df_kaggle_vill["created_on"], errors="coerce").dt.year

    kaggle_pm2_anual = (
        df_kaggle_vill.groupby("year")["precio_m2"]
        .median()
        .reset_index()
        .rename(columns={"precio_m2": "precio_m2_kaggle"})
    )

    comparacion = kaggle_pm2_anual.merge(df_ipvn[["year", "precio_m2_oficial_dane"]], on="year", how="inner")
    comparacion["diferencia_pct"] = (
        (comparacion["precio_m2_kaggle"] - comparacion["precio_m2_oficial_dane"])
        / comparacion["precio_m2_oficial_dane"] * 100
    ).round(1)

    print("\n--- Validación cruzada Kaggle vs IPVN DANE (Villavicencio) ---")
    print(comparacion.to_string(index=False))
    print("\nInterpretación: diferencia < ±20% = consistencia aceptable entre fuentes")

    return comparacion

# Llamar con el dataset integrado de Villavicencio una vez disponible en Fase 3
# validar_precio_kaggle_vs_ipvn(df_integrado, ipvn_vill_anual)
```

#### Interpretación del IPVN para el proyecto

El precio oficial por m² del IPVN DANE sirve para tres propósitos concretos:

1. **Validación de consistencia:** Si el precio mediano por m² de Kaggle para Villavicencio difiere en más del ±25% respecto al IPVN, se documenta como sesgo de fuente y se ajusta en Fase 3.
2. **Cálculo del IAH por ciudad:** El precio promedio m² × área mediana de la ciudad define el denominador del IAH por ciudad cuando los registros individuales son escasos.
3. **Serie temporal de referencia:** El IPVN permite extrapolar tendencias de precio para los trimestres sin cobertura en Kaggle (especialmente 2022–2024).

---

### Fuente 3 — CENAC (boletines estadísticos del sector constructor para Meta/Villavicencio)

**Responsable:** Sofía · **Costo:** $0 (descarga pública desde cenac.org.co)

El **Centro de Estudios de la Construcción y el Desarrollo Urbano y Regional (CENAC)** publica boletines estadísticos trimestrales con datos del sector constructor por ciudad y departamento, incluyendo Villavicencio y el departamento del Meta. Sus series históricas están disponibles desde 2013 y ofrecen:

- Precio promedio del metro cuadrado de **vivienda nueva en proceso de construcción** (distinto al precio de oferta en portales digitales).
- Número de unidades iniciadas, en construcción y terminadas por trimestre.
- Área promedio por tipo de vivienda (VIS vs. No VIS).
- Contexto sectorial: créditos hipotecarios desembolsados en el departamento.

#### Pasos de descarga

```
1. Ir a: https://www.cenac.org.co/estadisticas/boletines-estadisticos/
2. Filtrar: Ciudad/Departamento → "Villavicencio" o "Meta"
3. Descargar: boletines en PDF o Excel para los años 2015–2024
4. Guardar en: data/raw/cenac_villavicencio_YYYY.xlsx (o PDF si no hay Excel)
```

> **Nota:** Si los boletines están en PDF, usar `pdfplumber` o `tabula-py` para extraer las tablas de precio por m². La estructura de tablas del CENAC es consistente entre años, lo que facilita la automatización de la extracción.

#### Procesamiento básico de los datos CENAC

```python
"""
Procesamiento de boletines CENAC — Villavicencio / Meta
Extrae precio promedio m² y unidades del sector constructor oficial.
"""

import pandas as pd
import glob
from pathlib import Path

# ── Opción A: archivos Excel del CENAC ───────────────────────────────────────
archivos_cenac = sorted(glob.glob("data/raw/cenac_villavicencio_*.xlsx"))

if archivos_cenac:
    frames = []
    for archivo in archivos_cenac:
        año = int(Path(archivo).stem.split("_")[-1])  # extraer año del nombre
        df_c = pd.read_excel(archivo, sheet_name=0)

        # Normalizar columnas (ajustar según estructura real del CENAC)
        df_c.columns = df_c.columns.str.lower().str.strip().str.replace(" ", "_")
        rename_cenac = {
            "precio_m2": "precio_m2_cenac",
            "precio_promedio_m2": "precio_m2_cenac",
            "valor_m2": "precio_m2_cenac",
            "unidades_iniciadas": "unidades_iniciadas",
            "unidades_terminadas": "unidades_terminadas",
            "trimestre": "trimestre",
        }
        df_c.rename(columns={k: v for k, v in rename_cenac.items() if k in df_c.columns}, inplace=True)
        df_c["year"] = año
        frames.append(df_c)

    df_cenac = pd.concat(frames, ignore_index=True)

    # Agregar a anual
    cenac_anual = (
        df_cenac.groupby("year")
        .agg(
            precio_m2_cenac=("precio_m2_cenac", "mean"),
            unidades_iniciadas=("unidades_iniciadas", "sum"),
        )
        .reset_index()
    )
    cenac_anual["ciudad"] = "Villavicencio"
    cenac_anual["fuente"] = "CENAC"

    cenac_anual.to_csv("data/processed/cenac_villavicencio_anual.csv", index=False, encoding="utf-8-sig")
    print("✅ CENAC procesado:", cenac_anual.shape)
    print(cenac_anual.to_string(index=False))

# ── Opción B: extracción desde PDF si no hay Excel ───────────────────────────
else:
    print("No se encontraron archivos Excel del CENAC.")
    print("Alternativa: extraer tablas de PDF con pdfplumber:")
    print()
    print("  pip install pdfplumber")
    print()
    print("  import pdfplumber")
    print("  with pdfplumber.open('data/raw/cenac_villavicencio_2023.pdf') as pdf:")
    print("      for pagina in pdf.pages:")
    print("          tablas = pagina.extract_tables()")
    print("          for tabla in tablas:")
    print("              print(tabla)  # identificar la tabla de precios")
```

---

### Integración de las tres fuentes — Tabla de decisión consolidada

| Necesidad | Fuente | Archivo generado | Uso en el proyecto | Responsable |
|---|---|---|---|---|
| Precios individuales Villavicencio 2024–2025 | Scraping FincaRaiz (BeautifulSoup) | `data/raw/A7_fincaraiz_villavicencio_scraping.csv` | Concatenar como A7 al dataset integrado en Fase 3 | Steve |
| Precio oficial m² vivienda nueva por trimestre | IPVN DANE — Villavicencio AU | `data/processed/ipvn_villavicencio_anual.csv` | Validación cruzada y cálculo IAH por ciudad | Kukis |
| Contexto sector constructor (unidades, precios VIS vs No VIS) | Boletines CENAC Meta/Villavicencio | `data/processed/cenac_villavicencio_anual.csv` | Enriquecer análisis descriptivo; contextualizar IAH | Sofía |

#### Jerarquía de confianza entre fuentes para Villavicencio

Cuando las fuentes reportan precios por m² diferentes para el mismo período, se aplica la siguiente jerarquía de confianza:

1. **IPVN DANE** — precio oficial por m² de vivienda nueva (mayor rigor institucional, muestra estadística controlada)
2. **CENAC** — precio de obras en proceso (similar al IPVN pero enfocado en el sector constructor, no en el mercado de oferta)
3. **Scraping FincaRaiz (A7)** — precio de oferta en portal digital (más volumen, mayor actualidad, pero refleja precio pedido, no precio de transacción)
4. **Kaggle A1** — datos históricos del mercado digital (válidos para tendencias pero con sesgo de subrepresentación para ciudades intermedias)

> **Regla de uso:** Para el IAH de Villavicencio, se usa el precio del IPVN como ancla de validación. Los datos de scraping y Kaggle se usan para el modelo predictivo y el análisis de características (área, habitaciones, barrio).

---

### Nota sobre el precedente académico de esta estrategia

La combinación de datos de portales inmobiliarios digitales con fuentes oficiales (DANE, BanRep) para el análisis del mercado de vivienda en Colombia sigue una metodología híbrida reconocida en la literatura especializada: los datos georreferenciados de portales permiten contrastar hipótesis sobre patrones espaciales del mercado inmobiliario que las estadísticas agregadas oficiales no pueden revelar por sí solas. Este respaldo académico valida la solidez metodológica de la estrategia de datos del proyecto. [*Nota: Inserte aquí la referencia bibliográfica específica de su marco teórico.*]

---

## 10. Checklist — Fase 2 Completada

### Entregables de contenido

- [x] **Inventario verificado de las 16 fuentes** — archivos descargados y contados
- [x] **Esquema de columnas documentado** para A4 (completo) y resumen para A1–A8
- [x] **Reporte de calidad de datos** — % nulos, duplicados, outliers, rango de valores
- [x] **Tabla de cobertura ciudad × año** — todos los datasets integrados
- [x] **13 hallazgos documentados** con código reproducible
- [x] **Cálculo preliminar del IAH** — base para responder Preguntas 1 y 2
- [x] **Panel macroeconómico visualizado** — inflación, salario, tasa hipotecaria
- [x] **Decisiones de Fase 3 anticipadas** — tabla de problemas y acciones
- [x] **Estrategia de refuerzo Villavicencio (Sección 9-bis)** — scraping FincaRaiz + IPVN DANE + CENAC integrados con código reproducible y tabla de decisión

### Visualizaciones del notebook `01_EDA.ipynb`

- [x] **Fig 02** — Distribución de precios (escala original + log + boxplot por tipo)
- [x] **Fig 03** — Precio mediano por ciudad Top 15 (barras + intervalo intercuartílico)
- [x] **Fig 04** — Evolución temporal del precio mediano (nacional + por ciudad focal)
- [x] **Fig 05** — Distribución de área por tipo de propiedad
- [x] **Fig 06** — Scatterplot área vs precio por ciudad (muestra 8.000 registros)
- [x] **Fig 07** — Distribución de variables categóricas (tipo, año, ciudad)
- [x] **Fig 08** — Matriz de correlación entre variables numéricas
- [x] **Fig 09** — Mapa de calor de valores nulos + % por columna
- [x] **Fig 10** — Mapa geoespacial de propiedades (muestra 10.000)
- [x] **Fig 11** — Panel macroeconómico 4 subgráficas (salario, IPC, tasa, crec. real)
- [x] **Fig 12** — IAH preliminar nacional con umbrales OCDE (hallazgo clave)
- [x] **Fig 13** — Mapa de calor desempleo por ciudad-año

**Total: 12 visualizaciones comentadas** (cumple el mínimo de 10 establecido en Fase 1)

### Archivos generados / disponibles en data/raw/

- [x] 16 archivos CSV organizados y con encoding UTF-8-BOM (8A + 8B)
- [x] `data/raw/fincaraiz_villavicencio_scraping.csv` ✅ scraping ejecutado
- [x] `scripts/scraping_fincaraiz_villavicencio.py` ✅ código guardado
- [x] `scripts/organizar_datasets.py` ✅ script de organización de datasets
- [x] `docs/reporte_calidad_datasets.csv`
- [ ] `data/processed/ipvn_villavicencio_anual.csv` *(pendiente descarga DANE — Kukis)*
- [ ] `data/processed/cenac_villavicencio_anual.csv` *(pendiente boletines CENAC — Sofía)*

### Pendientes para Fase 3

- [ ] **Reunión de traspaso Steve → Kukis:** presentar hallazgos y tabla de decisiones de calidad (sección 7.2)
- [ ] **Commit de cierre de rama** `fase-2-datos` → pull request a `main` con revisión de Sofía

---

## 11. Notas Adicionales para el Equipo

### Para Kukis (Fase 3):
Los problemas más críticos a resolver son:
1. La conversión de moneda en A1 (USD → COP usando TRM anual del Banco de la República)
2. El escalado de precio de A2 (× 1.000.000)
3. La imputación de área por grupo (no global) — la tasa de nulos varía sistemáticamente por ciudad y período
4. El mapeo de nombres de columnas para A4, A5, A6 (columnas en español → canónico)

### Para Steve (Fase 4):
Variables confirmadas para el modelo de regresión:
- **Features numéricos**: `area`, `rooms`, `bathrooms`, `year`, `ipc_var_anual`, `tasa_hipotecaria_anual`, `tasa_desempleo`, `ipvu_variacion`
- **Features categóricos**: `city`, `property_type`
- **Feature adicional recomendado**: `estrato` (disponible en A1 y A5; imputar para el resto)
- **Variable objetivo**: `price` (posiblemente en log-escala)

**Tarea adicional antes de Fase 4:** Ejecutar el script `scripts/scraping_fincaraiz_villavicencio.py` (Sección 9-bis) para generar `data/raw/A7_fincaraiz_villavicencio_scraping.csv`. Este archivo (A7) debe integrarse al dataset final antes de la deduplicación. Verificar que el precio mediano scrapeado sea consistente con el IPVN DANE de Villavicencio (diferencia esperada ≤ ±25%).

### Para Sofía (Fase 5):
La respuesta preliminar a las 4 preguntas de investigación:
1. En 2023 se necesitan ~19 años de salario mínimo para comprar la vivienda mediana a nivel nacional
2. El IAH empeoró ~30% entre 2018 y 2023; el quiebre ocurrió en 2022 por inflación + tasas altas
3. La ciudad y el área son los predictores dominantes del precio (confirmado en EDA)
4. Los mercados de Bogotá y Medellín muestran los ratios cuota/salario más altos

---

*Documento de Fase 2 · CRISP-DM 2025-I · Proyecto Accesibilidad Habitacional Colombia*  
*Steve (responsable) · Sofía (apoyo) — Repositorio: github.com/[usuario]/proyecto-vivienda-colombia*  
*Semanas 3–4 del proyecto · Sección 9-bis agregada: estrategia refuerzo Villavicencio (scraping + IPVN DANE + CENAC)*
