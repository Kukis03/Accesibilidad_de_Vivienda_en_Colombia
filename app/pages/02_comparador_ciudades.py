import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Comparador de Ciudades", page_icon="🏙️", layout="wide")
st.title("Comparador de Ciudades")
st.markdown("Compara indicadores de accesibilidad entre ciudades.")

@st.cache_data
def load_data():
    return pd.read_csv("data/processed/vivienda_colombia_limpio.csv", encoding="utf-8-sig")

df = load_data()
ciudades = sorted(df['city'].unique())
anios = sorted(df['year'].unique())

col1, col2 = st.columns(2)
with col1:
    ciudades_sel = st.multiselect("Seleccionar ciudades (máx 4)", ciudades, default=ciudades[:3], max_selections=4)
with col2:
    anio_sel = st.select_slider("Año", options=anios, value=anios[-1])

if len(ciudades_sel) < 2:
    st.warning("Selecciona al menos 2 ciudades para comparar.")
    st.stop()

df_comp = df[(df['city'].isin(ciudades_sel)) & (df['year'] == anio_sel)]

tab1, tab2 = st.tabs(["Tabla Comparativa", "Gráficos"])

with tab1:
    st.subheader(f"Comparación {anio_sel}")
    tabla = df_comp.groupby('city').agg(
        precio_mediano=('price', 'median'),
        precio_m2=('precio_m2', 'median'),
        IAH=('IAH', 'median'),
        ratio_cuota=('ratio_cuota_salario', 'median'),
        area_med=('area', 'median'),
        estrato_med=('estrato', 'median'),
        desempleo=('tasa_desempleo', 'first'),
        n=('price', 'count')
    ).reset_index()
    tabla['precio_mediano'] = tabla['precio_mediano'].apply(lambda x: f"${x:,.0f}")
    tabla['precio_m2'] = tabla['precio_m2'].apply(lambda x: f"${x:,.0f}")
    tabla['IAH'] = tabla['IAH'].round(1)
    tabla['ratio_cuota'] = tabla['ratio_cuota'].round(2)
    tabla['area_med'] = tabla['area_med'].round(0).astype(int)
    tabla['estrato_med'] = tabla['estrato_med'].round(1)
    tabla['desempleo'] = tabla['desempleo'].apply(lambda x: f"{x:.1f}%")
    st.dataframe(tabla, width='stretch', hide_index=True)

    st.info(f"Registros disponibles en {anio_sel}: " + ", ".join([f"{r['city']}: {r['n']:,}" for _, r in tabla.iterrows()]))
    if any(tabla['n'] < 500):
        st.warning("Alguna(s) ciudad(es) tiene(n) < 500 registros - las estimaciones pueden ser inestables.")

with tab2:
    st.subheader("Precio Mediano por Ciudad")
    fig1 = px.bar(tabla.sort_values('precio_mediano', ascending=True), x='precio_mediano', y='city', orientation='h',
                  title=f"Precio Mediano por Ciudad ({anio_sel})", color='IAH', color_continuous_scale='RdYlGn_r')
    fig1.update_layout(xaxis_title="Precio Mediano (COP)")
    st.plotly_chart(fig1, width='stretch')

    st.subheader("Evolución del IAH")
    df_evol = df[df['city'].isin(ciudades_sel)].groupby(['city', 'year'])['IAH'].median().reset_index()
    fig2 = px.line(df_evol, x='year', y='IAH', color='city', markers=True,
                   title="IAH Mediano 2020-2024")
    fig2.add_hline(y=5, line_dash="dash", line_color="green", annotation_text="OCDE 5")
    fig2.add_hline(y=10, line_dash="dash", line_color="orange", annotation_text="OCDE 10")
    fig2.add_hline(y=20, line_dash="dash", line_color="red", annotation_text="Crítico 20")
    fig2.update_layout(xaxis=dict(dtick=1))
    st.plotly_chart(fig2, width='stretch')

    st.subheader("Distribución de Precios")
    fig3 = px.box(df_comp, x='city', y='price', color='city',
                  title=f"Distribución de Precios por Ciudad ({anio_sel})",
                  labels={'price': 'Precio (COP)', 'city': 'Ciudad'})
    st.plotly_chart(fig3, width='stretch')
