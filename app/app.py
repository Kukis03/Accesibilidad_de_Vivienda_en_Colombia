import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

st.set_page_config(
    page_title="Accesibilidad de Vivienda en Colombia",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main-title { font-size: 38px; font-weight: bold; color: #2c3e50; text-align: center; margin-bottom: 4px; }
    .main-sub   { font-size: 16px; color: #7f8c8d; text-align: center; margin-bottom: 24px; }
    .kpi-container { background-color: #f8f9fa; border-radius: 10px; padding: 15px;
                     border-left: 5px solid #3498db; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .kpi-value  { font-size: 26px; font-weight: bold; color: #2c3e50; }
    .kpi-label  { font-size: 13px; color: #7f8c8d; margin-top: 4px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🏠 Accesibilidad de Vivienda en Colombia</h1>", unsafe_allow_html=True)
st.markdown("<p class='main-sub'>Proyecto CRISP-DM 2026-I · 12 ciudades · 2020–2023 · IAH, precios y variables macroeconómicas</p>", unsafe_allow_html=True)

# ── Carga de datos ────────────────────────────────────────────────────────────
@st.cache_data
def cargar_datos():
    ruta = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        '..', 'data', 'processed', 'vivienda_colombia_limpio.csv'
    )
    if os.path.exists(ruta):
        return pd.read_csv(ruta, encoding='utf-8-sig', low_memory=False)
    st.error(f"No se encontró el archivo de datos en: {os.path.normpath(ruta)}")
    return pd.DataFrame()

df = cargar_datos()

if df.empty:
    st.warning("⚠️ No se encontró `data/processed/vivienda_colombia_limpio.csv`. Completa la Fase 3 primero.")
    st.stop()

# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.markdown("## ⚙️ Filtros Generales")

ciudades_disponibles = sorted(df['city'].unique())
ciudades_sel = st.sidebar.multiselect(
    "Ciudades", ciudades_disponibles, default=ciudades_disponibles
)

años_disponibles = sorted(df['year'].unique())
año_min, año_max = int(min(años_disponibles)), int(max(años_disponibles))
años_sel = st.sidebar.slider(
    "Rango de Años", año_min, año_max, (año_min, año_max)
)

tipos_disponibles = sorted(df['property_type'].unique())
tipos_sel = st.sidebar.multiselect(
    "Tipo de Propiedad", tipos_disponibles, default=tipos_disponibles
)

# ── Filtro ────────────────────────────────────────────────────────────────────
df_f = df[
    df['city'].isin(ciudades_sel) &
    df['year'].between(años_sel[0], años_sel[1]) &
    df['property_type'].isin(tipos_sel)
]

if df_f.empty:
    st.warning("⚠️ No hay datos con los filtros seleccionados. Amplia la selección.")
    st.stop()

# ── KPIs ──────────────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

with col1:
    val = df_f['price'].median()
    st.markdown(f"""
        <div class='kpi-container'>
          <div class='kpi-value'>${val/1e6:.1f}M COP</div>
          <div class='kpi-label'>💰 Precio Mediano</div>
        </div>""", unsafe_allow_html=True)

with col2:
    val = df_f['area'].median()
    st.markdown(f"""
        <div class='kpi-container'>
          <div class='kpi-value'>{val:.0f} m²</div>
          <div class='kpi-label'>📐 Área Mediana</div>
        </div>""", unsafe_allow_html=True)

with col3:
    val = df_f['IAH'].median()
    st.markdown(f"""
        <div class='kpi-container'>
          <div class='kpi-value'>{val:.1f} años</div>
          <div class='kpi-label'>📊 IAH Mediano</div>
        </div>""", unsafe_allow_html=True)

with col4:
    val = (df_f['ratio_cuota_salario'] > 0.30).mean() * 100
    st.markdown(f"""
        <div class='kpi-container'>
          <div class='kpi-value'>{val:.1f}%</div>
          <div class='kpi-label'>⚠️ Cuota > 30% del salario</div>
        </div>""", unsafe_allow_html=True)

st.write("")

# ── Pestañas ──────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📈 Evolución del IAH", "💵 Distribución de Precios", "ℹ️ Sobre el Proyecto"])

with tab1:
    st.subheader("Índice de Accesibilidad Habitacional por Ciudad")
    iah_hist = df_f.groupby(['year', 'city'])['IAH'].median().reset_index()
    fig_iah = px.line(
        iah_hist, x='year', y='IAH', color='city', markers=True,
        labels={'IAH': 'IAH (años de salario)', 'year': 'Año', 'city': 'Ciudad'},
        title="Años de salario mínimo necesarios para comprar vivienda (mediana)"
    )
    fig_iah.add_hline(y=5,  line_dash="dash", line_color="green",
                      annotation_text="Accesible OCDE (IAH ≤ 5)")
    fig_iah.add_hline(y=10, line_dash="dash", line_color="orange",
                      annotation_text="Moderado (IAH ≤ 10)")
    fig_iah.add_hline(y=20, line_dash="dash", line_color="red",
                      annotation_text="Crítico (IAH > 20)")
    fig_iah.update_layout(xaxis=dict(dtick=1))
    st.plotly_chart(fig_iah, use_container_width=True)

with tab2:
    st.subheader("Distribución de Precios de Venta por Ciudad")
    fig_box = px.box(
        df_f, x='city', y='price', color='property_type',
        labels={'price': 'Precio (COP)', 'city': 'Ciudad', 'property_type': 'Tipo'},
        title="Distribución de Precios — Casa vs Apartamento"
    )
    fig_box.update_yaxes(tickformat=",.0f")
    st.plotly_chart(fig_box, use_container_width=True)

with tab3:
    st.markdown("""
    ### Accesibilidad de Vivienda en Colombia · CRISP-DM 2026-I

    Este dashboard presenta los resultados del análisis de accesibilidad habitacional
    para **12 ciudades principales de Colombia** durante el período **2020–2023**.

    #### Metodología
    Se aplicó la metodología **CRISP-DM** (Cross-Industry Standard Process for Data Mining)
    en 6 fases:

    | Fase | Descripción | Responsable |
    |---|---|---|
    | 1 — Comprensión del Negocio | Definición del IAH y objetivos | Steve |
    | 2 — Comprensión de los Datos | EDA de 16 datasets (8A + 8B) | Sofía |
    | 3 — Preparación de los Datos | Pipeline de limpieza → 259,407 registros | Kukis |
    | 4 — Modelado | Random Forest + KMeans clustering | Steve |
    | 5 — Evaluación | Validación de modelos vs criterios de Fase 1 | Sofía |
    | 6 — Despliegue | Dashboard interactivo Streamlit | Kukis |

    #### Dataset
    - **Fuentes:** Properati, FincaRaiz, Kaggle, scraping propio (Villavicencio)
    - **Registros:** 259,407 inmuebles en venta
    - **Variables:** 26 columnas (precio, área, habitaciones, estrato, IAH, macrovariables)

    #### Índice de Accesibilidad Habitacional (IAH)
    `IAH = Precio del inmueble / Salario mínimo anual`

    Representa los años de salario mínimo que una persona necesitaría para comprar
    la vivienda sin financiación. Umbral OCDE: ≤ 5 años = Accesible.
    """)

