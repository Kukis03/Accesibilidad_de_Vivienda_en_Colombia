import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import json
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Predictor de Precios", page_icon="💵", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("data/processed/vivienda_colombia_limpio.csv", encoding="utf-8-sig")

@st.cache_resource
def load_model():
    import joblib
    return joblib.load("models/modelo_random_forest.pkl")

@st.cache_data
def load_features():
    with open("models/features_order.json") as f:
        return json.load(f)

df = load_data()
model = load_model()
features_order = load_features()

ciudades = sorted(df['city'].unique())
anios = sorted(df['year'].unique())
tipos = sorted(df['property_type'].unique())

macro_vars = df.groupby(['city', 'year'])[
    ['ipc_var_anual', 'tasa_hipotecaria_anual', 'tasa_desempleo', 'ipvu_variacion_anual', 'salario_anual']
].first().reset_index()

st.title("💵 Predictor de Precios")
st.markdown("""
Este predictor usa un modelo **Random Forest** entrenado con 282,660 registros de vivienda 
(R² = 0.6348). Ingresa las características de una vivienda para estimar su precio de mercado 
y conocer su nivel de accesibilidad.
""")

st.subheader("Características de la Vivienda")
with st.form("form"):
    c1, c2, c3 = st.columns(3)
    with c1:
        ciudad = st.selectbox("Ciudad", ciudades)
        tipo = st.selectbox("Tipo", tipos)
        estrato = st.selectbox("Estrato", [1,2,3,4,5,6], index=2)
    with c2:
        area = st.number_input("Área (m²)", 20, 500, 70, 5)
        habs = st.number_input("Habitaciones", 1, 10, 3, 1)
        banos = st.number_input("Baños", 1, 8, 2, 1)
    with c3:
        anio = st.selectbox("Año", anios, index=len(anios)-1)
    ok = st.form_submit_button("💵 Estimar Precio", type="primary", use_container_width=True)

if ok:
    with st.spinner("Calculando..."):
        macro = macro_vars[(macro_vars['city'] == ciudad) & (macro_vars['year'] == anio)]
        if macro.empty:
            cols_num = ['ipc_var_anual', 'tasa_hipotecaria_anual', 'tasa_desempleo', 'ipvu_variacion_anual', 'salario_anual']
            vals = macro_vars[macro_vars['year'] == anio][cols_num].mean()
            vals['city'] = ciudad
            vals['year'] = anio
            macro = vals.to_frame().T

        x = pd.DataFrame([{
            'area': area, 'rooms': habs, 'bathrooms': banos, 'estrato': estrato,
            'ipc_var_anual': float(macro['ipc_var_anual'].values[0]),
            'tasa_hipotecaria_anual': float(macro['tasa_hipotecaria_anual'].values[0]),
            'tasa_desempleo': float(macro['tasa_desempleo'].values[0]),
            'ipvu_variacion_anual': float(macro['ipvu_variacion_anual'].values[0]),
            'city': ciudad, 'property_type': tipo, 'year': anio
        }])
        x = x[features_order]
        pred = model.predict(x)[0]
        sal = float(macro['salario_anual'].values[0])
        iah = pred / sal if sal > 0 else 0
        tasa = float(macro['tasa_hipotecaria_anual'].values[0]) / 100
        if tasa > 0:
            r = tasa / 12
            cuota = (pred * 0.70 * r * (1 + r)**180) / ((1 + r)**180 - 1)
        else:
            cuota = 0
        ratio = cuota / (sal / 12) if sal > 0 else 0

        st.markdown("---")
        st.subheader("Resultados")

        r1, r2, r3, r4 = st.columns(4)
        r1.metric("Precio Estimado", f"${pred:,.0f}")
        r2.metric("IAH", f"{iah:.1f} años")
        r3.metric("Cuota Mensual", f"${cuota:,.0f}" if cuota > 0 else "N/A")
        r4.metric("Relación Cuota/Salario", f"{ratio:.2f}")

        if iah <= 5:
            color, nivel = "#2E7D32", "Accesible"
        elif iah <= 10:
            color, nivel = "#F9A825", "Moderado"
        elif iah <= 20:
            color, nivel = "#EF6C00", "Elevado"
        else:
            color, nivel = "#C62828", "Crítico"

        st.markdown(f"""
        <div style="text-align:center;background:#1E1E1E;padding:20px;border-radius:10px;border-left:5px solid {color};">
            <h3 style="color:{color};margin:0;">Nivel de Accesibilidad: {nivel}</h3>
            <p style="color:#ccc;margin:5px 0;">IAH = {iah:.1f} años de salario mínimo</p>
            <p style="color:#999;font-size:0.9em;">Estándar OCDE: < 5 años (Accesible)</p>
        </div>
        """, unsafe_allow_html=True)

        pct = (df[(df['city'] == ciudad) & (df['year'] == anio)]['price'] < pred).mean() * 100
        st.info(f"📊 Esta vivienda está en el **percentil {pct:.0f}** de precios en **{ciudad}** ({anio}). "
                f"Es más cara que el {pct:.0f}% de las viviendas listadas en esa ciudad y año.")

        st.warning("""
        **Limitaciones del predictor:**
        - El modelo Random Forest solo explica el **63.5%** de la varianza del precio (R² = 0.6348)
        - Los datos provienen de plataformas digitales (FincaRaíz, Properati, Kaggle), no del mercado formal completo
        - La cuota mensual es una estimación basada en 70% financiación a 15 años
        - No incluye vivienda de interés social (VIS) ni alquiler
        """)
