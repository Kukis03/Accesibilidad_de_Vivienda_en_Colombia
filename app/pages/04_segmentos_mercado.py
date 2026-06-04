import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Segmentos de Mercado", page_icon="📊", layout="wide")
st.title("Segmentos de Mercado")
st.markdown("Visualización de los clusters de accesibilidad identificados mediante KMeans.")

@st.cache_data
def load_clusters():
    return pd.read_csv("data/processed/ciudades_clusters.csv")

@st.cache_data
def load_perfiles():
    return pd.read_csv("data/processed/perfiles_clusters.csv")

df_cluster = load_clusters()
perfiles = load_perfiles()

cluster_names = {0: "Elevado (IAH 29.2)", 1: "Moderado (IAH 16.2)", 2: "Accesible Relativo (IAH 18.7)", 3: "Elevado (IAH 25.4)", 4: "Accesible (IAH 12.9)"}
df_cluster['cluster_name'] = df_cluster['cluster'].map(cluster_names)

st.sidebar.header("Filtros")
anio_sel = st.sidebar.select_slider("Año", options=sorted(df_cluster['year'].unique()), value=2024)

tab1, tab2, tab3 = st.tabs(["Scatter IAH vs Precio", "Heatmap Ciudad-Año", "Perfiles de Clusters"])

with tab1:
    st.subheader("IAH Mediano vs Precio por m²")
    fig = px.scatter(df_cluster, x='IAH', y='precio_m2', color='cluster_name',
                     size=[50]*len(df_cluster), hover_name='city', hover_data={'year': True, 'PC1':True, 'PC2':True},
                     color_discrete_sequence=px.colors.qualitative.Set2,
                     title="Clusters: IAH vs Precio por m² (cada punto = ciudad-año)")
    fig.add_hline(y=df_cluster['precio_m2'].median(), line_dash="dot", line_color="gray", annotation_text="Mediana precio/m²")
    fig.add_vline(x=10, line_dash="dot", line_color="orange", annotation_text="Moderado OCDE")
    fig.add_vline(x=20, line_dash="dot", line_color="red", annotation_text="Crítico")
    fig.update_layout(xaxis_title="IAH (años de salario mínimo)", yaxis_title="Precio por m² (COP)")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Proyección PCA")
    fig2 = px.scatter(df_cluster, x='PC1', y='PC2', color='cluster_name',
                      hover_name='city', hover_data={'year': True, 'IAH':True, 'precio_m2':True},
                      color_discrete_sequence=px.colors.qualitative.Set2,
                      title="PCA de Clusters (97.2% varianza explicada)")
    st.plotly_chart(fig2, use_container_width=True)

with tab2:
    st.subheader("Evolución de Clusters por Ciudad")
    heat_data = df_cluster.pivot(index='city', columns='year', values='cluster')
    cluster_labels = {0: "E0", 1: "M1", 2: "AR2", 3: "E3", 4: "A4"}
    heat_annot = heat_data.map(lambda x: cluster_labels.get(x, ""))
    fig3 = px.imshow(heat_data.values, x=heat_data.columns, y=heat_data.index,
                     text_auto=True, color_continuous_scale='Set2',
                     labels=dict(x="Año", y="Ciudad", color="Cluster"),
                     title="Mapa de Clusters por Ciudad y Año")
    fig3.update_layout(height=500)
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("**Leyenda de clusters:**")
    for k, v in cluster_names.items():
        st.markdown(f"- **{cluster_labels[k]}**: {v}")

    st.subheader("Transiciones entre 2020 y 2024")
    df_2020 = df_cluster[df_cluster['year'] == 2020][['city', 'cluster_name']].rename(columns={'cluster_name': 'cluster_2020'})
    df_2024 = df_cluster[df_cluster['year'] == 2024][['city', 'cluster_name']].rename(columns={'cluster_name': 'cluster_2024'})
    trans = df_2020.merge(df_2024, on='city')
    trans['cambio'] = trans['cluster_2020'] != trans['cluster_2024']
    st.dataframe(trans, use_container_width=True, hide_index=True)
    n_cambio = trans['cambio'].sum()
    st.info(f"{n_cambio} de {len(trans)} ciudades cambiaron de cluster entre 2020 y 2024.")

with tab3:
    st.subheader("Perfiles de Clusters")
    perfiles_display = perfiles.copy()
    perfiles_display['IAH'] = perfiles_display['IAH'].round(1)
    perfiles_display['precio_m2'] = perfiles_display['precio_m2'].apply(lambda x: f"${x:,.0f}")
    perfiles_display['ratio_cuota_salario'] = perfiles_display['ratio_cuota_salario'].round(2)
    perfiles_display['tasa_desempleo'] = perfiles_display['tasa_desempleo'].apply(lambda x: f"{x:.1f}%")
    perfiles_display.index = perfiles_display.index.map(cluster_names)
    perfiles_display.index.name = "Cluster"
    st.dataframe(perfiles_display, use_container_width=True)

    st.subheader("Radar Comparativo de Clusters")
    df_radar = perfiles.copy()
    df_radar_norm = (df_radar - df_radar.min()) / (df_radar.max() - df_radar.min() + 1e-6)
    fig4 = go.Figure()
    for idx, row in df_radar_norm.iterrows():
        fig4.add_trace(go.Scatterpolar(r=row.values, theta=df_radar_norm.columns,
                                       fill='toself', name=cluster_names.get(idx, str(idx))))
    fig4.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1])), title="Perfil Normalizado de Clusters")
    st.plotly_chart(fig4, use_container_width=True)

    st.markdown("---")
    st.caption("**Metodología:** Clustering KMeans con K=5 sobre 4 variables estandarizadas "
               "(IAH, precio_m², ratio_cuota_salario, tasa_desempleo) agregadas por ciudad-año. "
               f"Coeficiente de silueta: 0.4874. Varianza explicada PCA: 97.2%.")
