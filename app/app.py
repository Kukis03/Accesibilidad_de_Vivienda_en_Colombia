import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os, sys, warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Accesibilidad de Vivienda en Colombia", page_icon="🏠", layout="wide", initial_sidebar_state="expanded")

DATA_PATH = "data/processed/vivienda_colombia_limpio.csv"
MODEL_PATH = "models/modelo_random_forest.pkl"
CLUSTERS_PATH = "data/processed/ciudades_clusters.csv"
PERFILES_PATH = "data/processed/perfiles_clusters.csv"
FEATURES_PATH = "models/features_order.json"
SCALER_PATH = "models/scaler_cluster.pkl"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH, encoding="utf-8-sig")
    return df

@st.cache_data
def load_clusters():
    return pd.read_csv(CLUSTERS_PATH)

@st.cache_data
def load_perfiles():
    return pd.read_csv(PERFILES_PATH)

@st.cache_resource
def load_model():
    import joblib
    return joblib.load(MODEL_PATH)

df = load_data()
cluster_names = {0: "Elevado (IAH 29.2)", 1: "Moderado (IAH 16.2)", 2: "Accesible Relativo (IAH 18.7)", 3: "Elevado (IAH 25.4)", 4: "Accesible (IAH 12.9)"}

st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/2/21/Flag_of_Colombia.svg", width=60)
st.sidebar.title("Filtros Globales")
ciudades = ["Todas"] + sorted(df['city'].unique().tolist())
ciudad_sel = st.sidebar.selectbox("Ciudad", ciudades, index=0)
anios = sorted(df['year'].unique())
anio_sel = st.sidebar.select_slider("Año", options=anios, value=anios[-1])
tipos = ["Todos"] + sorted(df['property_type'].unique().tolist())
tipo_sel = st.sidebar.radio("Tipo de propiedad", tipos, index=0)

df_filtered = df.copy()
if ciudad_sel != "Todas":
    df_filtered = df_filtered[df_filtered['city'] == ciudad_sel]
if tipo_sel != "Todos":
    df_filtered = df_filtered[df_filtered['property_type'] == tipo_sel]

st.title("Accesibilidad de Vivienda en Colombia")
st.markdown("Dashboard interactivo del proyecto CRISP-DM **Accesibilidad de Vivienda en Colombia** (2020–2024). Explora la evolución de la accesibilidad económica, compara ciudades, predice precios y analiza segmentos de mercado.")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
precio_med = df_filtered['price'].median()
iah_med = df_filtered['IAH'].median()
pct_critico = (df_filtered['IAH'] > 20).mean() * 100
pct_cuota = (df_filtered['ratio_cuota_salario'] > 0.30).mean() * 100

kpi1.metric("Precio Mediano", f"${precio_med:,.0f}" if not np.isnan(precio_med) else "N/A")
kpi2.metric("IAH Mediano", f"{iah_med:.1f} años" if not np.isnan(iah_med) else "N/A")
kpi3.metric("Mercado Crítico (IAH>20)", f"{pct_critico:.1f}%" if not np.isnan(pct_critico) else "N/A")
kpi4.metric("Cuota >30% Salario", f"{pct_cuota:.1f}%" if not np.isnan(pct_cuota) else "N/A")

st.markdown("---")
st.subheader("Distribución Geográfica")
fig_map = px.scatter_mapbox(
    df_filtered.sample(min(5000, len(df_filtered))),
    lat="lat", lon="lon", color="price",
    size="area", hover_name="city",
    hover_data={"price": ":,.0f", "area": ":,.0f", "rooms": True, "estrato": True},
    color_continuous_scale="Viridis",
    zoom=4.5, height=500,
    title="Mapa de Propiedades por Precio"
)
fig_map.update_layout(mapbox_style="carto-darkmatter", margin=dict(l=0, r=0, t=30, b=0))
st.plotly_chart(fig_map, use_container_width=True)

st.markdown("---")
st.subheader("Vista Rápida del Dataset")
col1, col2 = st.columns(2)
with col1:
    st.dataframe(df_filtered.describe().round(2), use_container_width=True)
with col2:
    st.dataframe(df_filtered.head(100)[["city","year","price","area","rooms","bathrooms","estrato","IAH","nivel_accesibilidad"]].style.format({"price": "${:,.0f}"}), use_container_width=True, height=300)
