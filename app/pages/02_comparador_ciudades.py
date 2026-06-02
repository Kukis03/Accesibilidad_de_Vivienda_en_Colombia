import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Comparador", page_icon="📊", layout="wide")
st.title("📊 Comparador Inmobiliario de Ciudades")

<<<<<<< HEAD
ruta = "../data/processed/vivienda_colombia_limpio.csv"
if os.path.exists(ruta):
    df = pd.read_csv(ruta)

    ciudades = sorted(df['city'].unique())

=======
ruta = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '..', 'data', 'processed', 'vivienda_colombia_limpio.csv')
if os.path.exists(ruta):
    df = pd.read_csv(ruta)
    
    ciudades = sorted(df['city'].unique())
    
>>>>>>> 2711ad8c08d83362df73b02abfd236a5caf862f0
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        c1 = st.selectbox("Seleccione Ciudad A", ciudades, index=0)
    with col_c2:
        c2 = st.selectbox("Seleccione Ciudad B", ciudades, index=1)
<<<<<<< HEAD

    df_comp = df[df['city'].isin([c1, c2]) & (df['year'] == 2024)]

=======
        
    df_comp = df[df['city'].isin([c1, c2]) & (df['year'] == 2024)]
    
>>>>>>> 2711ad8c08d83362df73b02abfd236a5caf862f0
    if not df_comp.empty:
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.metric(f"IAH Promedio {c1}", f"{df_comp[df_comp['city']==c1]['IAH'].mean():.1f} Años")
            st.metric(f"Precio m² Mediano {c1}", f"${df_comp[df_comp['city']==c1]['precio_m2'].median()/1e6:.2f}M COP")
        with col_m2:
            st.metric(f"IAH Promedio {c2}", f"{df_comp[df_comp['city']==c2]['IAH'].mean():.1f} Años")
            st.metric(f"Precio m² Mediano {c2}", f"${df_comp[df_comp['city']==c2]['precio_m2'].median()/1e6:.2f}M COP")
<<<<<<< HEAD

=======
            
>>>>>>> 2711ad8c08d83362df73b02abfd236a5caf862f0
        fig_radar = px.box(df_comp, x='city', y='ratio_cuota_salario', color='property_type',
                           title="Ratio de Esfuerzo de Amortización Mensual (2024)")
        fig_radar.add_hline(y=0.3, line_dash="dash", line_color="red", annotation_text="Límite Accesibilidad (30%)")
        st.plotly_chart(fig_radar, use_container_width=True)
<<<<<<< HEAD
=======
    else:
        st.warning("No hay datos disponibles para el año 2024 en las ciudades seleccionadas.")
else:
    st.warning("⚠️ No se encontró el archivo de datos. Asegúrese de haber completado la Fase 3 de preparación de datos.")
    st.info(f"Ruta esperada: `{ruta}`")
>>>>>>> 2711ad8c08d83362df73b02abfd236a5caf862f0
