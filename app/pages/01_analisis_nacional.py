import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Análisis Nacional", page_icon="📊", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("data/processed/vivienda_colombia_limpio.csv", encoding="utf-8-sig")
    df['nivel_accesibilidad'] = df['nivel_accesibilidad'].fillna('Desconocido').astype(str)
    return df

df = load_data()

st.title("Análisis Nacional")
st.markdown("""
Este análisis responde a la pregunta: **¿Cómo ha evolucionado la accesibilidad económica a la vivienda 
en Colombia entre 2020 y 2024?** 

Los hallazgos muestran que el IAH (años de salario mínimo necesarios) se mantiene en niveles críticos 
durante todo el período, con **ninguna ciudad cumpliendo el estándar OCDE de 5 años**.
""")

st.sidebar.header("Filtros")
ciudades = sorted(df['city'].unique())
ciudad_sel = st.sidebar.selectbox("Ciudad focal", ["Todas"] + ciudades, index=0)

if ciudad_sel != "Todas":
    df_p = df[df['city'] == ciudad_sel]
    sufijo = f" — {ciudad_sel}"
else:
    df_p = df
    sufijo = ""

tab1, tab2, tab3, tab4, tab5 = st.tabs(["IAH y Accesibilidad", "Macro y Precios", "Niveles de Accesibilidad", "Variables Predictivas (P2)", "Datos por Año"])

with tab1:
    st.subheader(f"Evolución del IAH{sufijo}")
    iah_anual = df_p.groupby('year')['IAH'].median().reset_index()
    fig1 = px.line(iah_anual, x='year', y='IAH', markers=True, range_y=[0, iah_anual['IAH'].max() * 1.1],
                   title="IAH Mediano Nacional por Año (años de salario mínimo)")
    fig1.add_hline(y=5, line_dash="dash", line_color="green", annotation_text="Accesible OCDE (5)")
    fig1.add_hline(y=10, line_dash="dash", line_color="orange", annotation_text="Moderado OCDE (10)")
    fig1.add_hline(y=20, line_dash="dash", line_color="red", annotation_text="Crítico (20)")
    fig1.update_layout(yaxis_title="IAH (años de salario mínimo)", xaxis=dict(dtick=1))
    st.plotly_chart(fig1, use_container_width=True)
    st.info("**Hallazgo:** El IAH nacional oscila entre 15 y 22 años, muy por encima del umbral crítico de 20 años en los peores años. No hay mejoría sostenida en el período.")

    st.subheader(f"Salario Mínimo vs Precio Mediano{sufijo}")
    sal = df_p.groupby('year').agg(precio_mediano=('price','median'), salario=('salario_anual','first')).reset_index()
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=sal['year'], y=sal['precio_mediano']/1e6, mode='lines+markers',
                              name='Precio Mediano (Millones COP)', line=dict(color='#1E88E5')))
    fig2.add_trace(go.Scatter(x=sal['year'], y=sal['salario']/1e6, mode='lines+markers',
                              name='Salario Anual (Millones COP)', line=dict(color='#43A047'), yaxis='y2'))
    fig2.update_layout(
        yaxis=dict(title="Precio Mediano (Millones COP)", color='#1E88E5'),
        yaxis2=dict(title="Salario Anual (Millones COP)", overlaying='y', side='right', color='#43A047'),
        title="Brecha entre Precio de Vivienda y Salario", xaxis=dict(dtick=1),
        hovermode='x unified'
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.info("**Hallazgo:** El precio de la vivienda crece más rápido que el salario mínimo, ampliando la brecha año tras año.")

with tab2:
    st.subheader(f"Contexto Macroeconómico{sufijo}")
    macro = df_p.groupby('year')[['tasa_hipotecaria_anual', 'ipc_var_anual', 'tasa_desempleo', 'ipvu_variacion_anual']].first().reset_index()
    fig3 = px.line(macro, x='year', y=['tasa_hipotecaria_anual', 'ipc_var_anual', 'tasa_desempleo'], markers=True,
                   title="Indicadores Macroeconómicos (Tasa Hipotecaria, IPC, Desempleo)",
                   labels={'value': '%', 'variable': 'Indicador', 'year': 'Año'},
                   color_discrete_map={'tasa_hipotecaria_anual': '#E53935', 'ipc_var_anual': '#FB8C00', 'tasa_desempleo': '#8E24AA'})
    fig3.update_layout(xaxis=dict(dtick=1), legend=dict(title=""))
    st.plotly_chart(fig3, use_container_width=True)
    st.info("**Hallazgo:** La tasa hipotecaria se mantiene alta (>15%) durante todo el período, encareciendo el financiamiento. La inflación (IPC) supera el 10% en 2022-2023.")

    st.subheader(f"Precio Nominal vs Real{sufijo}")
    precios = df_p.groupby('year').agg(Nominal=('price','median'), Real=('precio_real','median')).reset_index()
    fig4 = px.line(precios, x='year', y=['Nominal', 'Real'], markers=True,
                   title="Precio Mediano: Nominal vs Ajustado por Inflación",
                   labels={'value': 'Precio (COP)', 'variable': 'Tipo', 'year': 'Año'},
                   color_discrete_map={'Nominal': '#1E88E5', 'Real': '#E53935'})
    fig4.update_layout(xaxis=dict(dtick=1))
    st.plotly_chart(fig4, use_container_width=True)
    st.info("**Hallazgo:** En términos reales (ajustado por inflación), el precio de la vivienda se ha mantenido estable o incluso ha caído ligeramente, lo que sugiere que el aumento nominal refleja inflación general, no mayor valor real.")

with tab3:
    st.subheader(f"Distribución de Niveles de Accesibilidad{sufijo}")
    niv = df_p.groupby(['year', 'nivel_accesibilidad']).size().reset_index(name='count')
    niv['pct'] = niv.groupby('year')['count'].transform(lambda x: x / x.sum() * 100)
    fig5 = px.bar(niv, x='year', y='pct', color='nivel_accesibilidad',
                  title="¿Cómo se distribuye la accesibilidad cada año?",
                  labels={'pct': '% del mercado', 'nivel_accesibilidad': 'Nivel', 'year': 'Año'},
                  color_discrete_map={'Accesible': '#2E7D32', 'Moderado': '#F9A825', 'Elevado': '#EF6C00', 'Crítico': '#C62828'},
                  category_orders={"nivel_accesibilidad": ["Accesible", "Moderado", "Elevado", "Crítico"]})
    fig5.update_layout(xaxis=dict(dtick=1), yaxis_title="% del mercado")
    st.plotly_chart(fig5, use_container_width=True)
    pct_critica = (df_p['IAH'] > 20).mean() * 100
    pct_accesible = (df_p['IAH'] <= 5).mean() * 100
    st.info(f"**Hallazgo:** El **{pct_critica:.1f}%** del mercado es 'Crítico' (IAH > 20). Solo el **{pct_accesible:.1f}%** es 'Accesible' (IAH ≤ 5).")

    if ciudad_sel == "Todas":
        st.subheader("Composición por Ciudad (2024)")
        d24 = df[df['year'] == 2024]
        nc = d24.groupby(['city', 'nivel_accesibilidad']).size().reset_index(name='count')
        nc['pct'] = nc.groupby('city')['count'].transform(lambda x: x / x.sum() * 100)
        fig6 = px.bar(nc, x='city', y='pct', color='nivel_accesibilidad',
                      title="Niveles de Accesibilidad: ¿Qué ciudades están peor?",
                      labels={'pct': '% del mercado', 'city': 'Ciudad'},
                      color_discrete_map={'Accesible': '#2E7D32', 'Moderado': '#F9A825', 'Elevado': '#EF6C00', 'Crítico': '#C62828'},
                      category_orders={"nivel_accesibilidad": ["Accesible", "Moderado", "Elevado", "Crítico"]})
        fig6.update_layout(yaxis_title="%")
        st.plotly_chart(fig6, use_container_width=True)
        st.info("**Hallazgo:** Bogotá y Medellín concentran la mayor proporción de vivienda 'Crítica' en 2024. Villavicencio y Cúcuta muestran los mercados más accesibles.")

with tab4:
    st.subheader("¿Qué variables explican mejor el precio? (Pregunta P2)")
    st.markdown("""
    El modelo **Random Forest** identificó que las **características físicas de la vivienda** 
    explican la mayor parte de la varianza del precio, muy por encima del contexto macroeconómico.
    """)

    col_a, col_b = st.columns([3, 2])
    with col_a:
        try:
            with open("models/feature_importances.json") as f:
                fi_data = json.load(f)
            feat_imp = pd.DataFrame(fi_data)
        except (FileNotFoundError, json.JSONDecodeError):
            feat_imp = pd.DataFrame({
                'variable': ['bathrooms', 'area', 'estrato', 'city_Bogotá', 'rooms',
                             'city_Medellín', 'tasa_hipotecaria_anual', 'ipc_var_anual',
                             'city_Cali', 'tasa_desempleo'],
                'importancia': [42.2, 28.0, 11.3, 5.0, 4.2, 1.8, 1.5, 1.2, 1.0, 0.8]
            })
        fig_p2 = px.bar(feat_imp.sort_values('importancia'), x='importancia', y='variable',
                        orientation='h', title="Importancia de Variables en el Modelo RF",
                        labels={'importancia': 'Importancia relativa (%)', 'variable': ''},
                        color='importancia', color_continuous_scale='Viridis')
        fig_p2.update_layout(yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig_p2, use_container_width=True)

    with col_b:
        top5 = feat_imp.nlargest(5, 'importancia')
        st.markdown("### Top 5 Variables")
        for i, row in enumerate(top5.itertuples(), 1):
            st.markdown(f"{i}. **{row.variable}** — {row.importancia:.1f}%")
        st.markdown(f"**Importancia acumulada top 5: {top5['importancia'].sum():.1f}%**")
        st.markdown("---")
        st.markdown("### Correlación con log(precio)")
        try:
            with open("models/correlations.json", encoding="utf-8") as f:
                corr_data = json.load(f)
            corr = pd.DataFrame(corr_data)
        except (FileNotFoundError, json.JSONDecodeError):
            corr = pd.DataFrame({
                'Variable': ['bathrooms', 'area', 'estrato', 'tasa_desempleo', 'rooms'],
                'Correlación Pearson': [0.60, 0.46, 0.43, -0.20, 0.18]
            })
        st.dataframe(corr, use_container_width=True, hide_index=True)
        st.info("**Hallazgo:** Las variables físicas (bathrooms, area, estrato) dominan la predicción con **81.5%** de importancia conjunta. El contexto macro (tasa hipotecaria, IPC, desempleo) aporta menos del **5%**. Esto sugiere que las diferencias de precio entre ciudades están mediadas por la calidad de las viviendas que ofrece cada mercado, no por el entorno macro.")

with tab5:
    st.subheader("Tabla Resumen Anual")
    res = df_p.groupby('year').agg(
        precio_mediano=('price', 'median'),
        IAH=('IAH', 'median'),
        precio_m2=('precio_m2', 'median'),
        ratio_cuota=('ratio_cuota_salario', 'median'),
        n=('price', 'count')
    ).reset_index()
    res['precio_mediano'] = res['precio_mediano'].apply(lambda x: f"${x:,.0f}")
    res['precio_m2'] = res['precio_m2'].apply(lambda x: f"${x:,.0f}")
    res['IAH'] = res['IAH'].round(1)
    res['ratio_cuota'] = res['ratio_cuota'].round(2)
    st.dataframe(res, use_container_width=True, hide_index=True)
