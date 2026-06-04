import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Segmentos de Mercado", page_icon="📊", layout="wide")

@st.cache_data
def load_clusters():
    return pd.read_csv("data/processed/ciudades_clusters.csv")

@st.cache_data
def load_perfiles():
    return pd.read_csv("data/processed/perfiles_clusters.csv")

dfc = load_clusters()
perfiles = load_perfiles()

cluster_names = {0: "Premium (IAH 29.2)", 1: "Intermedio (IAH 16.2)", 2: "Intermedio-Alto (IAH 18.7)", 3: "Premium (IAH 25.4)", 4: "Intermedio-Bajo (IAH 12.9)"}
dfc['cluster_name'] = dfc['cluster'].map(cluster_names)

st.title("📊 Segmentos de Mercado")
st.markdown("""
Utilizamos **KMeans (K=5)** para segmentar las 12 ciudades colombianas según su nivel de accesibilidad. 
Las variables usadas son: IAH, precio por m², ratio cuota/salario y tasa de desempleo.

**Coeficiente de silueta:** 0.4874 (buena separabilidad). **Varianza explicada PCA:** 97.2%.
""")



tab1, tab2, tab3 = st.tabs(["📌 Mapa de Clusters", "🗺️ Evolución Temporal", "📋 Perfiles"])

with tab1:
    st.subheader("IAH vs Precio por m²")
    fig1 = px.scatter(dfc, x='IAH', y='precio_m2', color='cluster_name',
                      hover_name='city', hover_data={'year': True, 'IAH': True, 'precio_m2': ':,.0f'},
                      color_discrete_sequence=px.colors.qualitative.Set2,
                      title="Cada punto es una ciudad en un año. El color indica su cluster de accesibilidad.",
                      labels={'IAH': 'Años de salario mínimo', 'precio_m2': 'Precio por m² (COP)', 'cluster_name': 'Cluster'})
    fig1.add_vline(x=10, line_dash="dot", line_color="orange", annotation_text="Moderado OCDE")
    fig1.add_vline(x=20, line_dash="dot", line_color="red", annotation_text="Crítico")
    st.plotly_chart(fig1, use_container_width=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Proyección PCA")
        fig2 = px.scatter(dfc, x='PC1', y='PC2', color='cluster_name',
                          hover_name='city', hover_data={'year': True, 'IAH': True},
                          color_discrete_sequence=px.colors.qualitative.Set2,
                          title="Componentes principales (97.2% de varianza explicada)")
        st.plotly_chart(fig2, use_container_width=True)
    with col_b:
        st.subheader("Ciudades en 2024")
        cluster_emoji = {0: "🔴", 1: "🟡", 2: "🟠", 3: "🔴", 4: "🟢"}
        d24 = dfc[dfc['year'] == 2024][['city', 'cluster', 'cluster_name']].sort_values('cluster_name')
        for _, r in d24.iterrows():
            st.markdown(f"{cluster_emoji.get(r['cluster'], '⚪')} **{r['city']}** — {r['cluster_name']}")

with tab2:
    st.subheader("Heatmap Ciudad × Año")
    hm = dfc.pivot(index='city', columns='year', values='cluster')
    fig3 = px.imshow(hm.values, x=hm.columns, y=hm.index, text_auto=True,
                     color_continuous_scale='Viridis', aspect="auto",
                     labels=dict(x="Año", y="Ciudad", color="Cluster"),
                     title="¿Cómo han cambiado los clusters a lo largo del tiempo?")
    fig3.update_layout(height=500)
    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("Transiciones")
    d20 = dfc[dfc['year'] == 2020][['city', 'cluster_name']].rename(columns={'cluster_name': '2020'})
    d24 = dfc[dfc['year'] == 2024][['city', 'cluster_name']].rename(columns={'cluster_name': '2024'})
    tr = d20.merge(d24, on='city')
    tr['cambio'] = tr['2020'] != tr['2024']
    st.dataframe(tr, use_container_width=True, hide_index=True)
    nc = tr['cambio'].sum()
    if nc > 0:
        st.info(f"🔄 {nc} de {len(tr)} ciudades cambiaron de cluster entre 2020 y 2024.")
    else:
        st.success("✅ Ninguna ciudad cambió de cluster — la segmentación es estable en el tiempo.")

with tab3:
    st.subheader("Perfiles de los 5 Clusters")
    perf = perfiles.copy()
    perf = perf.set_index('cluster')
    perf.columns = ['IAH', 'Precio m²', 'Ratio Cuota/Salario', 'Tasa Desempleo', 'Registros']
    perf.index = [cluster_names.get(i, str(i)) for i in perf.index]
    perf['Precio m²'] = perf['Precio m²'].apply(lambda x: f"${x:,.0f}")
    perf['IAH'] = perf['IAH'].round(1)
    perf['Tasa Desempleo'] = perf['Tasa Desempleo'].apply(lambda x: f"{x:.1f}%")
    perf['Ratio Cuota/Salario'] = perf['Ratio Cuota/Salario'].round(2)
    perf['Registros'] = perf['Registros'].astype(int)
    st.dataframe(perf, use_container_width=True)

    # Radar
    st.subheader("Radar Comparativo")
    features_radar = ['IAH', 'precio_m2', 'ratio_cuota_salario', 'tasa_desempleo']
    radar_labels = {'IAH': 'IAH', 'precio_m2': 'Precio m²', 'ratio_cuota_salario': 'Cuota/Salario', 'tasa_desempleo': 'Desempleo'}
    rn = (perfiles[features_radar] - perfiles[features_radar].min()) / (perfiles[features_radar].max() - perfiles[features_radar].min() + 1e-6)
    rn = rn.rename(columns=radar_labels)
    fig4 = go.Figure()
    for idx, row in rn.iterrows():
        fig4.add_trace(go.Scatterpolar(r=row.values, theta=rn.columns, fill='toself',
                                       name=cluster_names.get(idx, str(idx))))
    fig4.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
                       title="Perfil Normalizado de Clusters")
    st.plotly_chart(fig4, use_container_width=True)

    st.caption("""
    **Metodología:** KMeans con K=5, features estandarizadas (IAH, precio_m², ratio_cuota_salario, tasa_desempleo).
    Silueta = 0.4874. PCA con 97.2% de varianza explicada en 2 componentes.
    """)
