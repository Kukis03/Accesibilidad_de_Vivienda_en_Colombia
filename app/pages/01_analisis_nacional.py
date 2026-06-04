import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Análisis Nacional", page_icon="🇨🇴", layout="wide")
st.title("Análisis Nacional")
st.markdown("Evolución temporal de la accesibilidad económica a la vivienda en Colombia (2020–2024).")

DATA_PATH = "data/processed/vivienda_colombia_limpio.csv"
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH, encoding="utf-8-sig")
    df['nivel_accesibilidad'] = df['nivel_accesibilidad'].astype(str)
    return df
df = load_data()

st.sidebar.header("Filtros")
ciudades = sorted(df['city'].unique())
ciudad_sel = st.sidebar.selectbox("Ciudad focal", ["Todas"] + ciudades, index=0)

if ciudad_sel != "Todas":
    df_plot = df[df['city'] == ciudad_sel]
    titulo = f" ({ciudad_sel})"
else:
    df_plot = df
    titulo = " (Nacional)"

tab1, tab2, tab3, tab4 = st.tabs(["IAH y Accesibilidad", "Macro y Precios", "Niveles de Accesibilidad", "Datos por Año"])

with tab1:
    st.subheader(f"Evolución del IAH{titulo}")
    iah_anual = df_plot.groupby('year')['IAH'].median().reset_index()
    fig = px.line(iah_anual, x='year', y='IAH', markers=True,
                  title=f"IAH Mediano por Año{titulo}")
    fig.add_hline(y=5, line_dash="dash", line_color="green", annotation_text="Accesible OCDE (5)")
    fig.add_hline(y=10, line_dash="dash", line_color="orange", annotation_text="Moderado OCDE (10)")
    fig.add_hline(y=20, line_dash="dash", line_color="red", annotation_text="Crítico (20)")
    fig.update_layout(yaxis_title="IAH (años de salario mínimo)", xaxis=dict(dtick=1))
    st.plotly_chart(fig, width='stretch')

    st.subheader("Salario Mínimo vs Precio Mediano")
    sal_anual = df_plot.groupby('year').agg(precio_mediano=('price','median'), salario=('salario_anual','first')).reset_index()
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=sal_anual['year'], y=sal_anual['precio_mediano']/1e6, mode='lines+markers', name='Precio Mediano (Millones COP)', yaxis='y'))
    fig2.add_trace(go.Scatter(x=sal_anual['year'], y=sal_anual['salario']/1e6, mode='lines+markers', name='Salario Anual (Millones COP)', yaxis='y2'))
    fig2.update_layout(yaxis=dict(title="Precio Mediano (Millones COP)"), yaxis2=dict(title="Salario Anual (Millones COP)", overlaying='y', side='right'),
                       title=f"Precio vs Salario por Año{titulo}", xaxis=dict(dtick=1))
    st.plotly_chart(fig2, width='stretch')

with tab2:
    st.subheader(f"Indicadores Macroeconómicos{titulo}")
    macro = df_plot.groupby('year')[['tasa_hipotecaria_anual', 'ipc_var_anual', 'tasa_desempleo', 'ipvu_variacion_anual']].first().reset_index()
    fig3 = px.line(macro, x='year', y=['tasa_hipotecaria_anual', 'ipc_var_anual', 'tasa_desempleo'], markers=True,
                   title="Tasa Hipotecaria, IPC y Desempleo", labels={'value': '%', 'variable': 'Indicador'})
    fig3.update_layout(xaxis=dict(dtick=1))
    st.plotly_chart(fig3, width='stretch')

    st.subheader("Precio Nominal vs Real")
    precios = df_plot.groupby('year').agg(nominal=('price','median'), real=('precio_real','median')).reset_index()
    fig4 = px.line(precios, x='year', y=['nominal', 'real'], markers=True,
                   title="Precio Mediano: Nominal vs Ajustado por Inflación",
                   labels={'value': 'Precio (COP)', 'variable': 'Tipo'})
    fig4.update_layout(xaxis=dict(dtick=1))
    st.plotly_chart(fig4, width='stretch')

with tab3:
    st.subheader(f"Distribución de Niveles de Accesibilidad{titulo}")
    niv_anual = df_plot.groupby(['year', 'nivel_accesibilidad']).size().reset_index(name='count')
    niv_anual['pct'] = niv_anual.groupby('year')['count'].transform(lambda x: x / x.sum() * 100)
    fig5 = px.bar(niv_anual, x='year', y='pct', color='nivel_accesibilidad',
                  title="Composición de Niveles de Accesibilidad por Año",
                  labels={'pct': '% del mercado', 'nivel_accesibilidad': 'Nivel'},
                  color_discrete_map={'Accesible': 'green', 'Moderado': 'yellow', 'Elevado': 'orange', 'Crítico': 'red'},
                  category_orders={"nivel_accesibilidad": ["Accesible", "Moderado", "Elevado", "Crítico"]})
    fig5.update_layout(xaxis=dict(dtick=1), yaxis_title="%")
    st.plotly_chart(fig5, width='stretch')

    if ciudad_sel == "Todas":
        st.subheader("Composición por Ciudad (2024)")
        df2024 = df[df['year'] == 2024]
        niv_ciudad = df2024.groupby(['city', 'nivel_accesibilidad']).size().reset_index(name='count')
        niv_ciudad['pct'] = niv_ciudad.groupby('city')['count'].transform(lambda x: x / x.sum() * 100)
        fig6 = px.bar(niv_ciudad, x='city', y='pct', color='nivel_accesibilidad',
                      title="Niveles de Accesibilidad por Ciudad (2024)",
                      labels={'pct': '%', 'city': 'Ciudad'},
                      color_discrete_map={'Accesible': 'green', 'Moderado': 'yellow', 'Elevado': 'orange', 'Crítico': 'red'},
                      category_orders={"nivel_accesibilidad": ["Accesible", "Moderado", "Elevado", "Crítico"]})
        st.plotly_chart(fig6, width='stretch')

with tab4:
    st.subheader("Tabla Resumen Anual")
    resumen = df_plot.groupby('year').agg(
        precio_mediano=('price', 'median'),
        IAH=('IAH', 'median'),
        precio_m2=('precio_m2', 'median'),
        ratio_cuota=('ratio_cuota_salario', 'median'),
        n=(n:=('price', 'count')),
    ).reset_index()
    resumen['precio_mediano'] = resumen['precio_mediano'].apply(lambda x: f"${x:,.0f}")
    resumen['precio_m2'] = resumen['precio_m2'].apply(lambda x: f"${x:,.0f}")
    resumen['IAH'] = resumen['IAH'].round(1)
    resumen['ratio_cuota'] = resumen['ratio_cuota'].round(2)
    st.dataframe(resumen, width='stretch', hide_index=True)
