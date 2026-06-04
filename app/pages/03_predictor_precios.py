import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import json

st.set_page_config(page_title="Predictor de Precios", page_icon="💵", layout="wide")
st.title("Predictor de Precios de Vivienda")
st.markdown("Ingresa las características de una vivienda para estimar su precio de mercado y evaluar su accesibilidad.")

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

# Macro vars por año-ciudad
macro_vars = df.groupby(['city', 'year'])[['ipc_var_anual', 'tasa_hipotecaria_anual', 'tasa_desempleo', 'ipvu_variacion_anual', 'salario_anual']].first().reset_index()

st.subheader("Características de la Vivienda")
with st.form("predictor_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        ciudad = st.selectbox("Ciudad", ciudades)
        tipo = st.selectbox("Tipo de propiedad", tipos)
        estrato = st.selectbox("Estrato", [1, 2, 3, 4, 5, 6], index=2)
    with col2:
        area = st.number_input("Área (m²)", min_value=20, max_value=500, value=70, step=5)
        habitaciones = st.number_input("Habitaciones", min_value=1, max_value=10, value=3, step=1)
        banos = st.number_input("Baños", min_value=1, max_value=8, value=2, step=1)
    with col3:
        anio = st.selectbox("Año", anios, index=len(anios)-1)
    submitted = st.form_submit_button("Estimar Precio", type="primary", use_container_width=True)

if submitted:
    with st.spinner("Estimando precio..."):
        macro_row = macro_vars[(macro_vars['city'] == ciudad) & (macro_vars['year'] == anio)]
        if macro_row.empty:
            # Fallback: promedio de todas las ciudades para ese año
            macro_row = macro_vars[macro_vars['year'] == anio].mean().to_frame().T
            macro_row['city'] = ciudad

        X_input = pd.DataFrame([{
            'area': area, 'rooms': habitaciones, 'bathrooms': banos,
            'estrato': estrato,
            'ipc_var_anual': macro_row['ipc_var_anual'].values[0],
            'tasa_hipotecaria_anual': macro_row['tasa_hipotecaria_anual'].values[0],
            'tasa_desempleo': macro_row['tasa_desempleo'].values[0],
            'ipvu_variacion_anual': macro_row['ipvu_variacion_anual'].values[0],
            'city': ciudad, 'property_type': tipo, 'year': anio
        }])
        X_input = X_input[features_order]

        pred = model.predict(X_input)[0]
        salario_anual = macro_row['salario_anual'].values[0] if 'salario_anual' in macro_row.columns else df['salario_anual'].iloc[0]
        iah = pred / salario_anual if salario_anual > 0 else 0
        tasa_h = macro_row['tasa_hipotecaria_anual'].values[0] / 100
        cuota_mensual = (pred * 0.70 * (tasa_h / 12) * (1 + tasa_h/12)**180) / ((1 + tasa_h/12)**180 - 1) if tasa_h > 0 else 0
        ratio_cuota = cuota_mensual / (salario_anual / 12) if salario_anual > 0 else 0

        st.markdown("---")
        res1, res2, res3 = st.columns(3)
        res1.metric("Precio Estimado", f"${pred:,.0f}")
        res2.metric("IAH Estimado", f"{iah:.1f} años")
        res3.metric("Cuota Mensual Est.", f"${cuota_mensual:,.0f}" if cuota_mensual > 0 else "N/A")

        st.subheader("Semáforo de Accesibilidad")
        if iah <= 5: color, nivel = "green", "Accesible"
        elif iah <= 10: color, nivel = "yellow", "Moderado"
        elif iah <= 20: color, nivel = "orange", "Elevado"
        else: color, nivel = "red", "Crítico"
        st.markdown(f"<h3 style='text-align:center; color:{color}; background-color:#1E1E1E; padding:20px; border-radius:10px;'>Nivel: {nivel} (IAH = {iah:.1f})</h3>", unsafe_allow_html=True)

        st.subheader("Indicadores Financieros")
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("Relación Cuota/Salario", f"{ratio_cuota:.2f}")
        col_b.metric("Tasa Hipotecaria", f"{tasa_h*100:.2f}%")
        col_c.metric("Salario Anual Ref.", f"${salario_anual:,.0f}")

        pct = (df[(df['city'] == ciudad) & (df['year'] == anio)]['price'] < pred).mean() * 100
        st.info(f"Esta vivienda está en el percentil **{pct:.0f}** de precios en **{ciudad}** para **{anio}** (más cara que el {pct:.0f}% de las viviendas listadas).")

        st.markdown("---")
        st.caption("**Limitaciones:** El modelo RF tiene R²=0.6348. Las estimaciones son orientativas. "
                   "Los datos provienen de plataformas digitales (FincaRaíz, Properati, Kaggle) y no incluyen "
                   "todo el mercado inmobiliario formal. La cuota mensual es una estimación basada en "
                   "70% financiación a 15 años con la tasa hipotecaria del año.")
