import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Comparador de Ciudades", page_icon="🏙️", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("data/processed/vivienda_colombia_limpio.csv", encoding="utf-8-sig")

df = load_data()
ciudades = sorted(df['city'].unique())
anios = sorted(df['year'].unique())

st.title("🏙️ Comparador de Ciudades")
st.markdown("""
Selecciona **2 a 4 ciudades** para comparar sus indicadores de accesibilidad, precios y condiciones del mercado.
¿Qué ciudades son más accesibles? ¿Dónde es más caro el metro cuadrado?
""")

col1, col2 = st.columns(2)
with col1:
    cities_sel = st.multiselect("Seleccionar ciudades", ciudades, default=["Bogotá", "Medellín", "Cali"], max_selections=4)
with col2:
    yr = st.select_slider("Año de comparación", options=anios, value=anios[-1])

if len(cities_sel) < 2:
    st.warning("⚠️ Selecciona al menos 2 ciudades para comparar.")
    st.stop()

dc = df[(df['city'].isin(cities_sel)) & (df['year'] == yr)]

tab1, tab2 = st.tabs(["📋 Tabla Comparativa", "📊 Visualizaciones"])

with tab1:
    st.subheader(f"Comparación Directa — {yr}")
    tbl = dc.groupby('city').agg(
        precio_mediano=('price', 'median'),
        precio_m2=('precio_m2', 'median'),
        IAH=('IAH', 'median'),
        ratio_cuota=('ratio_cuota_salario', 'median'),
        area_med=('area', 'median'),
        estrato_med=('estrato', 'median'),
        desempleo=('tasa_desempleo', 'first'),
        n=('price', 'count')
    ).reset_index()
    # Keep numeric for chart, display formatted
    tbl_display = tbl.copy()
    tbl_display['precio_mediano'] = tbl_display['precio_mediano'].apply(lambda x: f"${x:,.0f}")
    tbl_display['precio_m2'] = tbl_display['precio_m2'].apply(lambda x: f"${x:,.0f}")
    tbl_display['IAH'] = tbl_display['IAH'].round(1)
    tbl_display['ratio_cuota'] = tbl_display['ratio_cuota'].round(2)
    tbl_display['area_med'] = tbl_display['area_med'].round(0).astype(int)
    tbl_display['estrato_med'] = tbl_display['estrato_med'].round(1)
    tbl_display['desempleo'] = tbl_display['desempleo'].apply(lambda x: f"{x:.1f}%")
    st.dataframe(tbl_display, use_container_width=True, hide_index=True)

    reg_info = ", ".join([f"**{r['city']}**: {r['n']:,}" for _, r in tbl.iterrows()])
    st.info(f"Registros en {yr}: {reg_info}")
    if any(tbl['n'] < 500):
        st.warning("⚠️ Alguna ciudad tiene menos de 500 registros — las estimaciones pueden ser inestables.")

with tab2:
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Precio Mediano")
        fig_bar = px.bar(tbl.sort_values('precio_mediano'), x='city', y='precio_mediano',
                          title=f"Precio Mediano por Ciudad ({yr})",
                          color='IAH', color_continuous_scale='RdYlGn_r',
                          labels={'precio_mediano': 'Precio (COP)', 'city': ''})
        fig_bar.update_layout(xaxis_title="", yaxis_tickprefix="$")
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_b:
        st.subheader("IAH (Años de Salario)")
        fig_iah = px.bar(tbl.sort_values('IAH'), x='city', y='IAH',
                         title=f"IAH por Ciudad ({yr})",
                         color='IAH', color_continuous_scale='RdYlGn_r',
                         labels={'IAH': 'Años de salario mínimo', 'city': ''})
        fig_iah.add_hline(y=5, line_dash="dash", line_color="green", annotation_text="OCDE 5")
        fig_iah.add_hline(y=10, line_dash="dash", line_color="orange", annotation_text="OCDE 10")
        fig_iah.add_hline(y=20, line_dash="dash", line_color="red", annotation_text="Crítico 20")
        st.plotly_chart(fig_iah, use_container_width=True)

    st.subheader("Evolución del IAH (2020-2024)")
    ev = df[df['city'].isin(cities_sel)].groupby(['city', 'year'])['IAH'].median().reset_index()
    fig_ev = px.line(ev, x='year', y='IAH', color='city', markers=True,
                     title="¿Cómo ha cambiado la accesibilidad en el tiempo?")
    fig_ev.add_hline(y=5, line_dash="dash", line_color="green", annotation_text="OCDE 5")
    fig_ev.add_hline(y=10, line_dash="dash", line_color="orange", annotation_text="OCDE 10")
    fig_ev.add_hline(y=20, line_dash="dash", line_color="red", annotation_text="Crítico 20")
    fig_ev.update_layout(xaxis=dict(dtick=1), hovermode='x unified')
    st.plotly_chart(fig_ev, use_container_width=True)

    st.subheader("Distribución de Precios")
    fig_box = px.box(dc, x='city', y='price', color='city',
                     title="¿Cómo se distribuyen los precios dentro de cada ciudad?",
                     labels={'price': 'Precio (COP)', 'city': ''}, points=False)
    fig_box.update_layout(yaxis_tickprefix="$", showlegend=False)
    st.plotly_chart(fig_box, use_container_width=True)
