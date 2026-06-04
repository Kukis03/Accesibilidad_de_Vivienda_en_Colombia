import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(page_title="Análisis Nacional", page_icon="🇨🇴", layout="wide")
st.title("🇨🇴 Comportamiento Macroeconómico Nacional")

# ── Carga de datos ────────────────────────────────────────────────────────────
@st.cache_data
def cargar_datos():
    ruta = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        'data', 'processed', 'vivienda_colombia_limpio.csv'
    )
    if os.path.exists(ruta):
        return pd.read_csv(ruta, encoding='utf-8-sig', low_memory=False), ruta
    return pd.DataFrame(), ruta

df, ruta_buscada = cargar_datos()

if df.empty:
    st.error("⚠️ No se encontró el archivo de datos. Completa la Fase 3 primero.")
    st.info(f"Ruta esperada: `{os.path.normpath(ruta_buscada)}`")
    st.stop()

# ── Agregados anuales ─────────────────────────────────────────────────────────
df_nacional = df.groupby('year').agg(
    price_med=('price', 'median'),
    IAH_med=('IAH', 'median'),
    IAH_mean=('IAH', 'mean'),
    tasa_hip=('tasa_hipotecaria_anual', 'first'),
    ipc=('ipc_var_anual', 'first'),
    salario=('salario_mensual', 'first'),
    n=('price', 'count')
).reset_index()

# Índices base año inicial = 100
base_precio  = df_nacional.loc[0, 'price_med']
base_salario = df_nacional.loc[0, 'salario']
df_nacional['precio_idx']  = (df_nacional['price_med']  / base_precio)  * 100
df_nacional['salario_idx'] = (df_nacional['salario'] / base_salario) * 100

# ── Gráfico 1: Tasa hipotecaria vs IPC ───────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("Tasa Hipotecaria vs Inflación Anual")
    fig_tasa = px.line(
        df_nacional, x='year',
        y=['tasa_hip', 'ipc'],
        markers=True,
        labels={'value': '(%)', 'year': 'Año', 'variable': 'Indicador'},
        color_discrete_map={'tasa_hip': '#3498db', 'ipc': '#e74c3c'},
        title="Tasas de Interés Créditos No VIS vs Inflación (IPC)"
    )
    fig_tasa.for_each_trace(lambda t: t.update(
        name='Tasa Hipotecaria' if t.name == 'tasa_hip' else 'IPC Anual'
    ))
    fig_tasa.update_layout(xaxis=dict(dtick=1))
    st.plotly_chart(fig_tasa, use_container_width=True)

with col2:
    st.subheader("Brecha Precio vs Salario (Base = 100)")
    fig_brecha = px.line(
        df_nacional, x='year',
        y=['precio_idx', 'salario_idx'],
        markers=True,
        labels={'value': 'Índice (año inicial = 100)', 'year': 'Año', 'variable': 'Indicador'},
        color_discrete_map={'precio_idx': '#e67e22', 'salario_idx': '#2ecc71'},
        title="Crecimiento Acumulado del Precio vs Salario Mínimo"
    )
    fig_brecha.for_each_trace(lambda t: t.update(
        name='Precio Mediano' if t.name == 'precio_idx' else 'Salario Mínimo'
    ))
    fig_brecha.add_hline(y=100, line_dash="dot", line_color="gray", opacity=0.5)
    fig_brecha.update_layout(xaxis=dict(dtick=1))
    st.plotly_chart(fig_brecha, use_container_width=True)

# ── Gráfico 2: Evolución del IAH por ciudad ───────────────────────────────────
st.subheader("Evolución del IAH Mediano por Ciudad")
st.caption("Umbral OCDE: ≤ 5 años = Accesible | ≥ 10 años = Seriamente inaccesible")

ciudades = sorted(df['city'].unique())
ciudades_sel = st.multiselect(
    "Selecciona ciudades a visualizar", ciudades, default=ciudades
)

if ciudades_sel:
    iah_ciudad = (
        df[df['city'].isin(ciudades_sel)]
        .groupby(['year', 'city'])['IAH']
        .median()
        .reset_index()
    )
    fig_iah = px.line(
        iah_ciudad, x='year', y='IAH', color='city', markers=True,
        labels={'IAH': 'IAH mediano (años)', 'year': 'Año', 'city': 'Ciudad'},
        title="Años de salario mínimo necesarios para comprar vivienda"
    )
    fig_iah.add_hline(y=5,  line_dash="dash", line_color="green",  annotation_text="Accesible OCDE (≤ 5)")
    fig_iah.add_hline(y=10, line_dash="dash", line_color="orange", annotation_text="Moderado (≤ 10)")
    fig_iah.add_hline(y=20, line_dash="dash", line_color="red",    annotation_text="Crítico (> 20)")
    fig_iah.update_layout(xaxis=dict(dtick=1))
    st.plotly_chart(fig_iah, use_container_width=True)

# ── Tabla resumen anual ───────────────────────────────────────────────────────
st.subheader("Resumen de Indicadores por Año")
tabla = df_nacional[['year', 'price_med', 'salario', 'IAH_med', 'tasa_hip', 'ipc', 'n']].copy()
tabla.columns = ['Año', 'Precio Mediano (COP)', 'Salario Mínimo (COP)', 'IAH Mediano',
                 'Tasa Hipotecaria (%)', 'IPC Anual (%)', 'Registros']
tabla['Precio Mediano (COP)'] = tabla['Precio Mediano (COP)'].apply(lambda x: f"${x/1e6:.1f}M")
tabla['Salario Mínimo (COP)'] = tabla['Salario Mínimo (COP)'].apply(lambda x: f"${x:,.0f}")
tabla['IAH Mediano'] = tabla['IAH Mediano'].apply(lambda x: f"{x:.1f} años")
tabla['Tasa Hipotecaria (%)'] = tabla['Tasa Hipotecaria (%)'].apply(lambda x: f"{x:.2f}%")
tabla['IPC Anual (%)'] = tabla['IPC Anual (%)'].apply(lambda x: f"{x:.2f}%")
tabla['Registros'] = tabla['Registros'].apply(lambda x: f"{x:,}")
st.dataframe(tabla.set_index('Año'), use_container_width=True)

st.info("""
**Interpretación:** El precio mediano de la vivienda ha crecido a mayor velocidad que el
salario mínimo, ampliando la brecha de accesibilidad. El IAH mediano se deterioró un
**~30 % entre 2020 y 2023**, pasando de ~20 a ~26 años de salario necesarios.
""")
