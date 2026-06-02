import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Segmentos de Mercado", page_icon="📌", layout="wide")
st.title("📌 Segmentación de Mercados Inmobiliarios (Clustering)")

ruta = "../data/processed/segmentos_mercado.csv"
if os.path.exists(ruta):
    df_sub = pd.read_csv(ruta)

    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("Mapa Conceptual de Segmentos Inmobiliarios")
        fig_scatter = px.scatter(df_sub, x='IAH_promedio', y='ratio_cuota_promedio', color='segmento',
                                 hover_name='city', text='city',
                                 title="Visualización Bidimensional del Clustering (KMeans)")
        st.plotly_chart(fig_scatter, use_container_width=True)

    with col2:
        st.subheader("Estadísticas del Segmento")
        resumen_seg = df_sub.groupby('segmento')[['precio_mediano', 'IAH_promedio', 'ratio_cuota_promedio']].mean()
        st.dataframe(resumen_seg.round(2))

    st.subheader("Transición Histórica de Segmento por Ciudad (2015-2024)")
    pivot_seg = df_sub.pivot(index='city', columns='year', values='segmento')
    st.dataframe(pivot_seg)
else:
    st.warning("El archivo de segmentos `segmentos_mercado.csv` no se encuentra disponible. Ejecute el clustering de la Fase 4.")
