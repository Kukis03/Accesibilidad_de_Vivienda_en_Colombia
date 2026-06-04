import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import warnings
from utils import fmt_cop
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Accesibilidad de Vivienda en Colombia",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_data():
    return pd.read_csv("data/processed/vivienda_colombia_limpio.csv", encoding="utf-8-sig")

df = load_data()

# ── Sidebar ─────────────────────────────────────────────────────
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/2/21/Flag_of_Colombia.svg", width=60)
st.sidebar.title("Panel de Control")
st.sidebar.markdown("Filtra los datos para explorar ciudades, años y tipos de vivienda.")

ciudades = ["Todas"] + sorted(df['city'].unique().tolist())
ciudad_sel = st.sidebar.selectbox("Ciudad", ciudades, index=0)

anios_disponibles = sorted(df['year'].unique())
opciones_anio = ["Todos (2020–2024)"] + anios_disponibles
anio_sel = st.sidebar.selectbox("Año", opciones_anio, index=0)

tipos = ["Todos"] + sorted(df['property_type'].unique().tolist())
tipo_sel = st.sidebar.radio("Tipo de propiedad", tipos, index=0, horizontal=True)

with st.sidebar.expander("Que es el IAH?"):
    st.markdown("""
El **Indice de Accesibilidad Habitacional (IAH)** mide cuantos años de salario minimo completo necesitaria
un hogar para comprar una vivienda al precio mediano del mercado.

**Formula:** `IAH = Precio vivienda / Salario anual minimo`

| IAH | Nivel | Referencia |
|---|---|---|
| <= 5 | Accesible | Estandar OCDE |
| 5 – 10 | Moderado | Ingresos medio-altos |
| 10 – 20 | Elevado | Doble ingreso necesario |
| > 20 | Critico | Inaccesible para la mayoria |

**Ingresos medio-altos:** hogares con ingresos entre 4 y 8 salarios minimos mensuales (~$5.2M a $10.4M COP en 2024). Para ellos un IAH de 5 a 10 es exigente pero alcanzable con ahorro disciplinado y credito hipotecario.

Un IAH de 15 significa que el hogar necesitaria **15 años** ahorrando el 100% de su salario para comprar la vivienda.
    """)

# ── Filtrado ────────────────────────────────────────────────────
df_f = df.copy()
if ciudad_sel != "Todas":
    df_f = df_f[df_f['city'] == ciudad_sel]
if tipo_sel != "Todos":
    df_f = df_f[df_f['property_type'] == tipo_sel]
if anio_sel != "Todos (2020–2024)":
    df_f = df_f[df_f['year'] == anio_sel]

anio_label = str(anio_sel) if anio_sel != "Todos (2020–2024)" else "2020–2024"

# ── Titulo ──────────────────────────────────────────────────────
st.title("Accesibilidad de Vivienda en Colombia")
st.markdown("""
Dashboard interactivo del proyecto CRISP-DM que analiza la evolucion de la accesibilidad economica
a la vivienda urbana en **12 ciudades colombianas (2020–2024)**.

**Pregunta central:** *Como ha evolucionado la accesibilidad economica a la vivienda y que variables
explican las diferencias entre ciudades?*
""")

# ── KPIs ────────────────────────────────────────────────────────
st.subheader("Indicadores Clave")
pm = df_f['price'].median()
iah = df_f['IAH'].median()
crit = (df_f['IAH'] > 20).mean() * 100
cuota = (df_f['ratio_cuota_salario'] > 0.30).mean() * 100

k1, k2, k3, k4 = st.columns(4)
k1.metric(
    "Precio Mediano",
    fmt_cop(pm) if not np.isnan(pm) else "N/A",
    help="Precio mediano de vivienda en COP para los filtros seleccionados."
)
k2.metric(
    "IAH Mediano",
    f"{iah:.1f} años" if not np.isnan(iah) else "N/A",
    help="Años de salario minimo necesarios para comprar una vivienda al precio mediano. Ver 'Que es el IAH?' en el panel lateral."
)
k3.metric(
    "Mercado Critico (IAH > 20)",
    f"{crit:.1f}%" if not np.isnan(crit) else "N/A",
    help="Porcentaje de propiedades con IAH mayor a 20 años (inaccesibles para un hogar de salario minimo)."
)
k4.metric(
    "Cuota > 30% Salario",
    f"{cuota:.1f}%" if not np.isnan(cuota) else "N/A",
    help="Porcentaje de propiedades cuya cuota hipotecaria mensual supera el 30% del salario minimo (umbral de sobreendeudamiento)."
)

# ── Distribucion de Accesibilidad ───────────────────────────────
st.markdown("---")
col_pie, col_txt = st.columns([2, 1])
with col_pie:
    st.subheader(f"Distribucion del Mercado por Nivel de Accesibilidad — {ciudad_sel}, {anio_label}")
    if not df_f.empty:
        niv = df_f['nivel_accesibilidad'].value_counts().reset_index()
        niv.columns = ['Nivel', 'Registros']
        niv['%'] = (niv['Registros'] / niv['Registros'].sum() * 100).round(1)
        color_map = {'Accesible': '#2E7D32', 'Moderado': '#F9A825', 'Elevado': '#EF6C00', 'Crítico': '#C62828'}
        fig_pie = px.pie(
            niv, values='Registros', names='Nivel',
            color='Nivel', color_discrete_map=color_map,
            hole=0.4
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        fig_pie.update_layout(legend=dict(orientation='h', yanchor='bottom', y=-0.2))
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("Sin datos para los filtros seleccionados.")

with col_txt:
    st.subheader("Niveles de Accesibilidad (IAH)")
    st.markdown("""
El IAH clasifica cada propiedad segun cuantos años de salario minimo cuesta:

**Accesible — IAH menor o igual a 5**
Cumple el estandar OCDE. Practicamente inexistente en Colombia.

**Moderado — IAH entre 5 y 10**
Viable para hogares de ingresos medio-altos o con dos ingresos. Exige disciplina de ahorro sostenida.

**Elevado — IAH entre 10 y 20**
Requiere ahorro prolongado, doble ingreso o subsidio. Fuera del alcance del salario minimo unico.

**Critico — IAH mayor a 20**
Inaccesible para la gran mayoria de hogares colombianos. Demanda patrimonio previo o credito de largo plazo.
    """)

# ── Mapa ────────────────────────────────────────────────────────
st.markdown("---")
st.subheader("Distribucion Geografica de Propiedades")
st.markdown("Cada punto es una propiedad listada. El color indica el precio y el tamano el area construida.")

if df_f.empty:
    st.info("Sin datos para los filtros seleccionados.")
else:
    try:
        n_sample = min(3000, len(df_f))
        df_map = df_f.sample(n_sample, random_state=42).copy()
        df_map['precio_fmt'] = df_map['price'].apply(lambda v: f"${v:,.0f} COP")
        df_map['area_fmt']   = df_map['area'].apply(lambda v: f"{v:,.0f} m²")
        fig_map = px.scatter_mapbox(
            df_map, lat="lat", lon="lon",
            color="price", size="area",
            hover_name="city",
            hover_data={
                "precio_fmt": True, "area_fmt": True,
                "rooms": True, "estrato": True, "year": True,
                "price": False, "area": False
            },
            labels={"precio_fmt": "Precio", "area_fmt": "Area", "rooms": "Habitaciones",
                    "estrato": "Estrato", "year": "Año"},
            color_continuous_scale="RdYlGn_r",
            zoom=4.8, height=600,
        )
        fig_map.update_layout(
            mapbox_style="open-street-map",
            margin=dict(l=0, r=0, t=30, b=0),
            coloraxis_colorbar=dict(
                title="Precio (COP)",
                tickprefix="$",
                tickformat=",.0f",
                thickness=15,
                len=0.7,
                x=1.02
            ),
            hovermode="closest",
            font=dict(size=11)
        )
        st.plotly_chart(fig_map, use_container_width=True, key="mapbox_chart")
    except Exception as e:
        st.error(f"Error al generar el mapa: {e}")
        fig_fallback = px.scatter(
            df_f.sample(min(500, len(df_f))), x="lon", y="lat",
            color="price", hover_name="city", title="Vista simplificada"
        )
        st.plotly_chart(fig_fallback, use_container_width=True)

# ── Insights ────────────────────────────────────────────────────
st.markdown("---")
st.subheader("Resumen")
if df_f.empty:
    st.info("No hay registros para resumir con los filtros actuales.")
elif ciudad_sel == "Todas":
    c_mejor = df_f.groupby('city')['IAH'].median().idxmin()
    c_peor  = df_f.groupby('city')['IAH'].median().idxmax()
    st.markdown(f"""
| Metrica | Valor |
|---|---|
| Ciudad mas accesible ({anio_label}) | **{c_mejor}** |
| Ciudad menos accesible ({anio_label}) | **{c_peor}** |
| IAH nacional ({anio_label}) | **{iah:.1f}** años de salario minimo |
| Propiedades con cuota > 30% salario | **{cuota:.0f}%** del total |
| Propiedades analizadas | **{len(df_f):,}** registros |

**Conclusion:** Ninguna ciudad colombiana cumple el estandar OCDE de accesibilidad (IAH menor a 5 años).
El mercado es financieramente inviable para un hogar de salario minimo en su totalidad.
""")
else:
    st.markdown(f"""
| Metrica | Valor |
|---|---|
| Ciudad | **{ciudad_sel}** |
| Periodo | **{anio_label}** |
| Precio mediano | **{fmt_cop(pm)}** COP |
| IAH mediano | **{iah:.1f}** años de salario minimo |
| Propiedades analizadas | **{len(df_f):,}** registros |
""")

# ── Navegacion ──────────────────────────────────────────────────
st.markdown("---")
st.subheader("Explorar en Detalle")
st.markdown("Usa las paginas del menu lateral para analisis mas profundos:")
col_a, col_b, col_c, col_d = st.columns(4)
col_a.info("**Analisis Nacional**\nEvolucion temporal de accesibilidad, macroeconomia y niveles de IAH.")
col_b.info("**Comparador de Ciudades**\nContrasta indicadores entre ciudades una al lado de la otra.")
col_c.info("**Predictor de Precios**\nEstima el precio de una vivienda segun sus caracteristicas.")
col_d.info("**Segmentos de Mercado**\nExplora los clusters de mercado identificados por KMeans.")
