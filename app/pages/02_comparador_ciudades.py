import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Comparador de Ciudades", page_icon="📊", layout="wide")
st.title("📊 Comparador Inmobiliario de Ciudades")

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

# ── Selección de ciudades y año ───────────────────────────────────────────────
ciudades = sorted(df['city'].unique())
año_max  = int(df['year'].max())
año_min  = int(df['year'].min())

col_c1, col_c2, col_c3 = st.columns([2, 2, 1])
with col_c1:
    c1 = st.selectbox("Ciudad A", ciudades, index=0)
with col_c2:
    c2 = st.selectbox("Ciudad B", ciudades, index=1 if len(ciudades) > 1 else 0)
with col_c3:
    año_sel = st.selectbox("Año de comparación", sorted(df['year'].unique(), reverse=True))

if c1 == c2:
    st.warning("Selecciona dos ciudades diferentes para comparar.")
    st.stop()

# ── KPIs comparativos ─────────────────────────────────────────────────────────
df_comp = df[df['city'].isin([c1, c2]) & (df['year'] == año_sel)]

# Advertencia si poca muestra
for ciudad in [c1, c2]:
    n = len(df_comp[df_comp['city'] == ciudad])
    if n < 500:
        st.warning(f"⚠️ {ciudad} tiene solo {n} registros en {año_sel}. Las métricas pueden no ser representativas.")

if df_comp.empty:
    st.warning(f"No hay datos disponibles para {año_sel}. Prueba con otro año.")
    st.stop()

st.subheader(f"Métricas clave — {año_sel}")
col_m1, col_m2 = st.columns(2)

def metricas_ciudad(col, ciudad, df_comp):
    sub = df_comp[df_comp['city'] == ciudad]
    with col:
        st.markdown(f"### 🏙️ {ciudad}")
        m1, m2 = st.columns(2)
        m1.metric("Precio Mediano", f"${sub['price'].median()/1e6:.1f}M COP")
        m2.metric("Precio/m² Mediano", f"${sub['precio_m2'].median()/1e6:.2f}M")
        m3, m4 = st.columns(2)
        m3.metric("IAH Mediano", f"{sub['IAH'].median():.1f} años")
        m4.metric("Ratio Cuota/Salario", f"{sub['ratio_cuota_salario'].median()*100:.1f}%")

metricas_ciudad(col_m1, c1, df_comp)
metricas_ciudad(col_m2, c2, df_comp)

st.write("---")

# ── Gráfico 1: Boxplot ratio cuota/salario ────────────────────────────────────
col_g1, col_g2 = st.columns(2)

with col_g1:
    st.subheader(f"Esfuerzo de Cuota Mensual — {año_sel}")
    fig_box = px.box(
        df_comp, x='city', y='ratio_cuota_salario', color='property_type',
        labels={'ratio_cuota_salario': 'Cuota / Salario', 'city': 'Ciudad', 'property_type': 'Tipo'},
        title="Proporción de la cuota hipotecaria sobre el salario mínimo"
    )
    fig_box.add_hline(y=0.30, line_dash="dash", line_color="red",
                      annotation_text="Límite recomendado (30%)")
    st.plotly_chart(fig_box, use_container_width=True)

with col_g2:
    st.subheader("Distribución de Precios por Tipo")
    fig_violin = px.violin(
        df_comp, x='city', y='price', color='property_type',
        box=True,
        labels={'price': 'Precio (COP)', 'city': 'Ciudad', 'property_type': 'Tipo'},
        title=f"Distribución de precios de venta — {año_sel}"
    )
    st.plotly_chart(fig_violin, use_container_width=True)

# ── Gráfico 2: Evolución del IAH en período completo ─────────────────────────
st.subheader(f"Evolución del IAH — {c1} vs {c2} (período completo)")
iah_evol = (
    df[df['city'].isin([c1, c2])]
    .groupby(['year', 'city'])['IAH']
    .median()
    .reset_index()
)
fig_linea = px.line(
    iah_evol, x='year', y='IAH', color='city', markers=True,
    labels={'IAH': 'IAH mediano (años)', 'year': 'Año', 'city': 'Ciudad'},
    title="Años de salario mínimo necesarios para comprar vivienda"
)
fig_linea.add_hline(y=10, line_dash="dash", line_color="orange",
                    annotation_text="Seriamente inaccesible OCDE (≥ 10)")
fig_linea.update_layout(xaxis=dict(dtick=1))
st.plotly_chart(fig_linea, use_container_width=True)

# ── Tabla comparativa ─────────────────────────────────────────────────────────
st.subheader("Tabla Comparativa Completa")
resumen = (
    df_comp
    .groupby('city')
    .agg(
        Registros=('price', 'count'),
        Precio_Mediano=('price', 'median'),
        Precio_m2_Mediano=('precio_m2', 'median'),
        IAH_Mediano=('IAH', 'median'),
        Ratio_Cuota=('ratio_cuota_salario', 'median'),
        Tasa_Desempleo=('tasa_desempleo', 'first'),
    )
    .reset_index()
)
resumen['Precio_Mediano']   = resumen['Precio_Mediano'].apply(lambda x: f"${x/1e6:.1f}M COP")
resumen['Precio_m2_Mediano']= resumen['Precio_m2_Mediano'].apply(lambda x: f"${x/1e6:.2f}M/m²")
resumen['IAH_Mediano']      = resumen['IAH_Mediano'].apply(lambda x: f"{x:.1f} años")
resumen['Ratio_Cuota']      = resumen['Ratio_Cuota'].apply(lambda x: f"{x*100:.1f}%")
resumen['Tasa_Desempleo']   = resumen['Tasa_Desempleo'].apply(lambda x: f"{x:.1f}%")
resumen.columns = ['Ciudad', 'Registros', 'Precio Mediano', 'Precio/m²',
                   'IAH Mediano', 'Ratio Cuota/Salario', 'Tasa Desempleo']
st.dataframe(resumen.set_index('Ciudad'), use_container_width=True)
