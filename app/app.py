import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Accesibilidad de Vivienda en Colombia", page_icon="🏠", layout="wide", initial_sidebar_state="expanded")

@st.cache_data
def load_data():
    return pd.read_csv("data/processed/vivienda_colombia_limpio.csv", encoding="utf-8-sig")

@st.cache_data
def load_clusters():
    return pd.read_csv("data/processed/ciudades_clusters.csv")

df = load_data()
df_clusters = load_clusters()

# ── Sidebar ─────────────────────────────────────────────────────
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/2/21/Flag_of_Colombia.svg", width=60)
st.sidebar.title("Panel de Control")
st.sidebar.markdown("Filtra los datos para explorar ciudades, años y tipos de vivienda específicos.")

ciudades = ["Todas"] + sorted(df['city'].unique().tolist())
ciudad_sel = st.sidebar.selectbox("Ciudad", ciudades, index=0)
anios = sorted(df['year'].unique())
anio_sel = st.sidebar.select_slider("Año", options=anios, value=anios[-1])
tipos = ["Todos"] + sorted(df['property_type'].unique().tolist())
tipo_sel = st.sidebar.radio("Tipo de propiedad", tipos, index=0, horizontal=True)

df_f = df.copy()
if ciudad_sel != "Todas":
    df_f = df_f[df_f['city'] == ciudad_sel]
if tipo_sel != "Todos":
    df_f = df_f[df_f['property_type'] == tipo_sel]

# ── Hero ────────────────────────────────────────────────────────
st.title("🏡 Accesibilidad de Vivienda en Colombia")
st.markdown("""
Dashboard interactivo del proyecto **CRISP-DM** que analiza la evolución de la accesibilidad económica 
a la vivienda urbana en **12 ciudades colombianas (2020–2024)**. 

**Pregunta central:** *¿Cómo ha evolucionado la accesibilidad económica a la vivienda y qué variables 
explican las diferencias entre ciudades?*
""")

# ── KPIs ────────────────────────────────────────────────────────
st.subheader("Indicadores Clave")
pm = df_f['price'].median()
iah = df_f['IAH'].median()
crit = (df_f['IAH'] > 20).mean() * 100
cuota = (df_f['ratio_cuota_salario'] > 0.30).mean() * 100

k1, k2, k3, k4 = st.columns(4)
k1.metric("Precio Mediano", f"${pm:,.0f}" if not np.isnan(pm) else "N/A", help="Precio mediano de vivienda en COP")
k2.metric("IAH Mediano", f"{iah:.1f} años" if not np.isnan(iah) else "N/A", help="Índice de Accesibilidad Habitacional: años de salario mínimo para comprar una vivienda")
k3.metric("Mercado Crítico", f"{crit:.1f}%" if not np.isnan(crit) else "N/A", help="Porcentaje del mercado con IAH > 20 años (crítico)")
k4.metric("Cuota >30% Salario", f"{cuota:.1f}%" if not np.isnan(cuota) else "N/A", help="Porcentaje con cuota hipotecaria superior al 30% del salario mínimo")

# ── Mapa mejorado ──────────────────────────────────────────────
st.markdown("---")
st.subheader("🗺️ Distribución Geográfica")
st.markdown("Cada punto representa una propiedad listada. El color indica el precio y el tamaño el área construida.")

try:
    n_sample = min(3000, len(df_f))
    if n_sample > 0:
        df_map = df_f.sample(n_sample, random_state=42)
        fig_map = px.scatter_mapbox(
            df_map, lat="lat", lon="lon",
            color="price", size="area",
            hover_name="city",
            hover_data={"price": ":,.0f", "area": ":,.0f", "rooms": True, "estrato": True, "year": True},
            color_continuous_scale="Viridis",
            zoom=4.8, height=520,
            title="Propiedades por Precio y Ubicación"
        )
        fig_map.update_layout(
            mapbox_style="carto-positron",
            margin=dict(l=0, r=0, t=30, b=0),
            coloraxis_colorbar=dict(title="Precio (COP)", tickprefix="$")
        )
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.warning("No hay datos con los filtros seleccionados.")
except Exception as e:
    st.error(f"Error al generar el mapa: {e}")
    st.info("Usando mapa alternativo sin mapa base...")
    fig_fallback = px.scatter(df_f.sample(min(500, len(df_f))), x="lon", y="lat", color="price",
                               hover_name="city", title="Vista simplificada")
    st.plotly_chart(fig_fallback, use_container_width=True)

# ── Insights r├ípidos ────────────────────────────────────────────
st.markdown("---")
st.subheader("🔍 Insights Rápidos")
if ciudad_sel == "Todas":
    c_mejor = df_f[df_f['year'] == anio_sel].groupby('city')['IAH'].median().idxmin()
    c_peor = df_f[df_f['year'] == anio_sel].groupby('city')['IAH'].median().idxmax()
    st.markdown(f"""
| Métrica | Valor |
|---|---|
| Ciudad más accesible en {anio_sel} | **{c_mejor}** |
| Ciudad menos accesible en {anio_sel} | **{c_peor}** |
| IAH nacional en {anio_sel} | **{iah:.1f}** años de salario mínimo |
| Mercado con cuota > 30% salario | **{cuota:.0f}%** del total |
| Viviendas analizadas | **{len(df_f):,}** registros |

💡 **Conclusión:** Ninguna ciudad colombiana cumple el estándar OCDE de accesibilidad (IAH < 5 años). 
El mercado de vivienda es **financieramente inviable para un hogar de salario mínimo** en su totalidad.
""")
else:
    st.markdown(f"""
| Métrica | Valor |
|---|---|
| Ciudad seleccionada | **{ciudad_sel}** |
| Precio mediano | **${pm:,.0f}** COP |
| IAH en {anio_sel} | **{iah:.1f}** años de salario mínimo |
| Registros analizados | **{len(df_f):,}** |
""")

# ── Navegaci├│n ─────────────────────────────────────────────────
st.markdown("---")
st.subheader("📂 Explorar en Detalle")
st.markdown("Usa las páginas del menú lateral para análisis más profundos:")
col_a, col_b, col_c, col_d = st.columns(4)
col_a.info("🇨🇴 **Análisis Nacional**\nEvolución temporal de accesibilidad, macroeconomía y niveles de IAH.")
col_b.info("🏙️ **Comparador**\nContrasta indicadores entre ciudades una al lado de la otra.")
col_c.info("💵 **Predictor**\nEstima el precio de una vivienda según sus características.")
col_d.info("📊 **Segmentos**\nExplora los clusters de mercado identificados por KMeans.")
