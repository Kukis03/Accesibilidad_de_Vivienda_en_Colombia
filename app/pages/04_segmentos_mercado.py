import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Segmentos de Mercado", page_icon="📌", layout="wide")
st.title("📌 Segmentación de Mercados Inmobiliarios")

# ── Nota metodológica (siempre visible) ───────────────────────────────────────
with st.expander("ℹ️ Metodología del Clustering", expanded=False):
    st.markdown("""
    **Algoritmo:** KMeans (Fase 4 — Steve)

    El clustering agrupa las 12 ciudades en segmentos de mercado según 4 variables:
    - `IAH mediano` — accesibilidad habitacional por años de salario
    - `precio_m2 mediano` — costo por metro cuadrado
    - `ratio_cuota_salario mediano` — esfuerzo de amortización mensual
    - `tasa_desempleo` — condición del mercado laboral local

    Cada combinación ciudad-año recibe una etiqueta de cluster (0 a K-1).
    La variación de la etiqueta en el tiempo refleja cambios estructurales en el mercado.

    **Archivos requeridos:** `data/processed/ciudades_clusters.csv` · `data/processed/perfiles_clusters.csv`
    """)

# ── Carga de datos de clustering ──────────────────────────────────────────────
base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ruta_clusters  = os.path.join(base_path, 'data', 'processed', 'ciudades_clusters.csv')
ruta_perfiles  = os.path.join(base_path, 'data', 'processed', 'perfiles_clusters.csv')

if not os.path.exists(ruta_clusters):
    st.warning("⏳ **Datos de clustering no disponibles aún**")
    st.info(f"""
    Esta página requiere los archivos generados en la **Fase 4 (Steve)**:
    - `{os.path.normpath(ruta_clusters)}` — asignación ciudad-año → cluster
    - `{os.path.normpath(ruta_perfiles)}` — estadísticas descriptivas por cluster (opcional)

    Mientras tanto, puedes explorar:
    - 📈 **Análisis Nacional** — Evolución histórica del IAH
    - 📊 **Comparador de Ciudades** — Contrasta dos ciudades
    """)
    st.stop()

df_clusters = pd.read_csv(ruta_clusters)
df_perfiles = pd.read_csv(ruta_perfiles) if os.path.exists(ruta_perfiles) else None

# ── Scatter: IAH vs precio/m² por cluster ────────────────────────────────────
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Mapa de Segmentos: IAH vs Precio/m²")
    fig_scatter = px.scatter(
        df_clusters,
        x='IAH_promedio' if 'IAH_promedio' in df_clusters.columns else df_clusters.columns[2],
        y='ratio_cuota_promedio' if 'ratio_cuota_promedio' in df_clusters.columns else df_clusters.columns[3],
        color='cluster' if 'cluster' in df_clusters.columns else df_clusters.columns[-1],
        hover_name='city' if 'city' in df_clusters.columns else df_clusters.columns[0],
        text='city' if 'city' in df_clusters.columns else df_clusters.columns[0],
        title="Clustering KMeans — Segmentos de Mercado Inmobiliario"
    )
    fig_scatter.update_traces(textposition='top center')
    st.plotly_chart(fig_scatter, use_container_width=True)

with col2:
    st.subheader("Perfiles por Cluster")
    if df_perfiles is not None:
        st.dataframe(df_perfiles.round(2), use_container_width=True)
    else:
        st.info("Archivo `perfiles_clusters.csv` no encontrado.")

# ── Heatmap: transición histórica de cluster por ciudad ───────────────────────
if 'year' in df_clusters.columns and 'city' in df_clusters.columns:
    st.subheader("Transición Histórica de Segmento por Ciudad")
    st.caption("Cada celda muestra el cluster asignado a esa ciudad en ese año")

    cluster_col = 'cluster' if 'cluster' in df_clusters.columns else df_clusters.columns[-1]
    pivot = df_clusters.pivot(index='city', columns='year', values=cluster_col)

    fig_heat = px.imshow(
        pivot,
        labels=dict(x="Año", y="Ciudad", color="Cluster"),
        title="Asignación de Cluster por Ciudad y Año",
        color_continuous_scale="RdYlGn_r",
        text_auto=True
    )
    fig_heat.update_layout(coloraxis_showscale=True)
    st.plotly_chart(fig_heat, use_container_width=True)
