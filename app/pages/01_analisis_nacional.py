import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Análisis Nacional", page_icon="🇨🇴", layout="wide")
st.title("🇨🇴 Comportamiento Macroeconómico Nacional")

<<<<<<< HEAD
ruta = "../data/processed/vivienda_colombia_limpio.csv"
if os.path.exists(ruta):
    df = pd.read_csv(ruta)

=======
ruta = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '..', 'data', 'processed', 'vivienda_colombia_limpio.csv')
if os.path.exists(ruta):
    df = pd.read_csv(ruta)
    
    # Análisis agregado anual
>>>>>>> 2711ad8c08d83362df73b02abfd236a5caf862f0
    df_nacional = df.groupby('year').agg({
        'price': 'median',
        'IAH': 'mean',
        'tasa_hipotecaria_anual': 'mean',
        'ipc_var_anual': 'mean',
        'salario_mensual': 'first'
    }).reset_index()
<<<<<<< HEAD

=======
    
>>>>>>> 2711ad8c08d83362df73b02abfd236a5caf862f0
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Evolución de Tasa de Interés vs Crecimiento de Precios")
        fig_tasa = px.line(df_nacional, x='year', y=['tasa_hipotecaria_anual', 'ipc_var_anual'],
                            labels={'value': 'Porcentaje (%)', 'year': 'Año'},
                            title="Tasas de Interés Créditos VIS/No VIS vs Inflación")
        st.plotly_chart(fig_tasa, use_container_width=True)
<<<<<<< HEAD

=======
        
>>>>>>> 2711ad8c08d83362df73b02abfd236a5caf862f0
    with col2:
        st.subheader("Índice de Precios Real vs Salario Mínimo Real")
        df_nacional['precio_real_base100'] = (df_nacional['price'] / df_nacional.loc[0, 'price']) * 100
        df_nacional['salario_real_base100'] = (df_nacional['salario_mensual'] / df_nacional.loc[0, 'salario_mensual']) * 100
<<<<<<< HEAD

=======
        
>>>>>>> 2711ad8c08d83362df73b02abfd236a5caf862f0
        fig_base = px.line(df_nacional, x='year', y=['precio_real_base100', 'salario_real_base100'],
                           labels={'value': 'Índice (Base 2015 = 100)', 'year': 'Año'},
                           title="Brecha de Crecimiento del Precio vs Ingreso Real")
        st.plotly_chart(fig_base, use_container_width=True)
<<<<<<< HEAD

=======
        
>>>>>>> 2711ad8c08d83362df73b02abfd236a5caf862f0
    st.markdown("""
        > **Interpretación Económica:** Se evidencia que el precio mediano de la vivienda formal ha crecido a una velocidad
        muy superior a la del ajuste salarial. Para 2024, el precio real acumuló un incremento del **84%** respecto a 2015,
        mientras que el salario mínimo real creció solo un **24%** en el mismo periodo.
    """)
<<<<<<< HEAD
=======
else:
    st.warning("⚠️ No se encontró el archivo de datos. Asegúrese de haber completado la Fase 3 de preparación de datos.")
    st.info(f"Ruta esperada: `{ruta}`")
>>>>>>> 2711ad8c08d83362df73b02abfd236a5caf862f0
