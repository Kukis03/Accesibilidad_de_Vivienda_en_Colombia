import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

# Configuración de página
st.set_page_config(
    page_title="Accesibilidad de Vivienda en Colombia",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilización CSS personalizada
st.markdown("""
    <style>
    .main-title { font-size: 38px; font-weight: bold; color: #2c3e50; text-align: center; margin-bottom: 20px; }
    .kpi-container { background-color: #f8f9fa; border-radius: 10px; padding: 15px; border-left: 5px solid #3498db; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .kpi-value { font-size: 24px; font-weight: bold; color: #2c3e50; }
    .kpi-label { font-size: 14px; color: #7f8c8d; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>Accesibilidad de Vivienda en Colombia · CRISP-DM</h1>", unsafe_allow_html=True)

# Lógica de carga de datos optimizada con caché
@st.cache_data
def cargar_datos():
    ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'processed', 'vivienda_colombia_limpio.csv')
    if os.path.exists(ruta):
        return pd.read_csv(ruta)
    else:
        st.error(f"No se encontró el archivo de datos en {ruta}")
        return pd.DataFrame()

df = cargar_datos()

if not df.empty:
    # Sidebar de filtros generales
    st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/2/2a/Flag_of_Colombia.svg", width=100)
    st.sidebar.header("Filtros Generales")
    
    ciudades_disponibles = sorted(df['city'].unique())
    ciudades_sel = st.sidebar.multiselect("Seleccione Ciudades", ciudades_disponibles, default=ciudades_disponibles[:3])
    
    anos_disponibles = sorted(df['year'].unique())
    anos_sel = st.sidebar.slider("Rango de Años", min(anos_disponibles), max(anos_disponibles), (2018, 2024))
    
    tipos_disponibles = df['property_type'].unique()
    tipos_sel = st.sidebar.multiselect("Tipo de Propiedad", tipos_disponibles, default=list(tipos_disponibles))
    
    # Filtrar datos
    df_filtrado = df[
        (df['city'].isin(ciudades_sel)) & 
        (df['year'].between(anos_sel[0], anos_sel[1])) & 
        (df['property_type'].isin(tipos_sel))
    ]
    
    # Grid de KPIs
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        precio_med = df_filtrado['price'].median()
        st.markdown(f"<div class='kpi-container'><div class='kpi-value'>${precio_med/1e6:.1f}M COP</div><div class='kpi-label'>Precio Mediano</div></div>", unsafe_allow_html=True)
    with col2:
        area_med = df_filtrado['area'].median()
        st.markdown(f"<div class='kpi-container'><div class='kpi-value'>{area_med:.1f} m²</div><div class='kpi-label'>Área Mediana</div></div>", unsafe_allow_html=True)
    with col3:
        iah_prom = df_filtrado['IAH'].mean()
        st.markdown(f"<div class='kpi-container'><div class='kpi-value'>{iah_prom:.1f} Años</div><div class='kpi-label'>IAH Promedio</div></div>", unsafe_allow_html=True)
    with col4:
        ratio_prom = df_filtrado['ratio_cuota_salario'].mean() * 100
        st.markdown(f"<div class='kpi-container'><div class='kpi-value'>{ratio_prom:.1f}%</div><div class='kpi-label'>Carga Cuota Hipotecaria</div></div>", unsafe_allow_html=True)
        
    st.write("---")
    
    # Pestaña Principal
    tab1, tab2 = st.tabs(["Evolución del IAH", "Distribución de Precios"])
    with tab1:
        st.subheader("Índice de Accesibilidad Habitacional Histórico")
        iah_hist = df_filtrado.groupby(['year', 'city'])['IAH'].mean().reset_index()
        fig_iah = px.line(iah_hist, x='year', y='IAH', color='city', markers=True,
                          title="Evolución de Años de Salario Mínimo Necesarios para Compra")
        fig_iah.add_hline(y=5, line_dash="dash", line_color="green", annotation_text="Accesible (PIR <= 5)")
        fig_iah.add_hline(y=10, line_dash="dash", line_color="orange", annotation_text="Moderado")
        fig_iah.add_hline(y=20, line_dash="dash", line_color="red", annotation_text="Crítico (PIR > 20)")
        st.plotly_chart(fig_iah, use_container_width=True)
        
    with tab2:
        st.subheader("Distribución de Precios por Ciudad")
        fig_box = px.box(df_filtrado, x='city', y='price', color='property_type',
                         title="Rango de Precios de Venta")
        st.plotly_chart(fig_box, use_container_width=True)
else:
    st.warning("⚠️ No se encontró el archivo de datos procesados. Asegúrese de haber completado la Fase 3 de preparación de datos.")
    st.info("El archivo esperado es: `data/processed/vivienda_colombia_limpio.csv`")
    st.markdown("""
    ### 📋 Estado del Dashboard
    Este dashboard necesita los siguientes archivos para funcionar:
    
    | Archivo | Descripción | Estado |
    |---|---|---|
    | `data/processed/vivienda_colombia_limpio.csv` | Dataset consolidado (Fase 3) | ❌ Pendiente |
    | `models/modelo_random_forest.pkl` | Modelo predictivo (Fase 4) | ❌ Pendiente |
    | `data/processed/segmentos_mercado.csv` | Clusters de mercado (Fase 4) | ❌ Pendiente |
    
    Una vez generados estos archivos, el dashboard se activará automáticamente.
    """)
