import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

st.set_page_config(page_title="Predictor de Precio", page_icon="🔮", layout="wide")
st.title("🔮 Predicción del Precio y Accesibilidad en Tiempo Real")

st.markdown("""
    <style>
    .result-card    { border-radius: 10px; padding: 25px; margin-top: 20px; text-align: center; }
    .card-verde     { background-color: #d4edda; border: 2px solid #c3e6cb; color: #155724; }
    .card-amarillo  { background-color: #fff3cd; border: 2px solid #ffeeba; color: #856404; }
    .card-naranja   { background-color: #ffe5d0; border: 2px solid #ffcba4; color: #7d3c07; }
    .card-rojo      { background-color: #f8d7da; border: 2px solid #f5c6cb; color: #721c24; }
    .res-val        { font-size: 32px; font-weight: bold; margin: 8px 0; }
    </style>
""", unsafe_allow_html=True)

# ── Carga del modelo ──────────────────────────────────────────────────────────
@st.cache_resource
def cargar_modelo():
    ruta = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        'models', 'modelo_random_forest.pkl'
    )
    if os.path.exists(ruta):
        return joblib.load(ruta), ruta
    return None, ruta

# ── Carga de macrovariables desde el CSV ──────────────────────────────────────
@st.cache_data
def cargar_macro():
    ruta = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        'data', 'processed', 'vivienda_colombia_limpio.csv'
    )
    if os.path.exists(ruta):
        df = pd.read_csv(ruta, encoding='utf-8-sig', low_memory=False,
                         usecols=['year', 'city', 'salario_mensual', 'ipc_var_anual',
                                  'tasa_hipotecaria_anual', 'tasa_desempleo', 'ipvu_variacion_anual'])
        return df, ruta
    return pd.DataFrame(), ruta

modelo, ruta_modelo = cargar_modelo()
df_macro, ruta_macro = cargar_macro()

# ── Sin modelo: mostrar mensaje claro ────────────────────────────────────────
if modelo is None:
    st.warning("⏳ **Modelo no disponible aún**")
    st.info(f"""
    El predictor requiere el archivo `models/modelo_random_forest.pkl` generado en la **Fase 4 (Steve)**.
    
    Ruta esperada: `{os.path.normpath(ruta_modelo)}`

    Mientras tanto, puedes explorar las otras secciones del dashboard:
    - 📈 **Análisis Nacional** — Evolución histórica del IAH
    - 📊 **Comparador de Ciudades** — Contrasta dos ciudades
    """)
    st.stop()

if df_macro.empty:
    st.error("No se encontró el dataset de datos. Completa la Fase 3.")
    st.info(f"Ruta esperada: `{os.path.normpath(ruta_macro)}`")
    st.stop()

# ── Formulario de predicción ──────────────────────────────────────────────────
st.subheader("Características del Inmueble a Valorar")

col1, col2, col3 = st.columns(3)

with col1:
    area          = st.number_input("Área Construida (m²)", min_value=15.0, max_value=800.0, value=70.0, step=5.0)
    property_type = st.selectbox("Tipo de Propiedad", ["Apartamento", "Casa"])

with col2:
    rooms     = st.selectbox("Habitaciones", [1, 2, 3, 4, 5, 6], index=2)
    bathrooms = st.selectbox("Baños", [1, 2, 3, 4, 5, 6], index=1)

with col3:
    city    = st.selectbox("Ciudad", sorted(['Bogotá', 'Medellín', 'Cali', 'Barranquilla',
                                              'Cartagena', 'Bucaramanga', 'Pereira', 'Manizales',
                                              'Armenia', 'Cúcuta', 'Ibagué', 'Villavicencio']))
    estrato = st.slider("Estrato Socioeconómico", 1, 6, 3)

# Selección de año de análisis (macro)
años_disp = sorted(df_macro['year'].unique(), reverse=True)
year = st.selectbox("Año de referencia (macrovariables)", años_disp, index=0)

# Obtener macro del año y ciudad seleccionada (fallback nacional)
macro_ciudad = df_macro[(df_macro['year'] == year) & (df_macro['city'] == city)]
macro_nac    = df_macro[df_macro['year'] == year]

def get_macro(col):
    if not macro_ciudad.empty:
        return macro_ciudad[col].iloc[0]
    return macro_nac[col].median() if not macro_nac.empty else 0.0

ipc_var_anual         = get_macro('ipc_var_anual')
tasa_hipotecaria_anual = get_macro('tasa_hipotecaria_anual')
tasa_desempleo         = get_macro('tasa_desempleo')
ipvu_variacion_anual   = get_macro('ipvu_variacion_anual')
salario_mensual        = get_macro('salario_mensual')

with st.expander("📊 Variables macroeconómicas utilizadas"):
    st.caption(f"Valores extraídos del dataset para {city} · {year}")
    mc1, mc2, mc3, mc4 = st.columns(4)
    mc1.metric("Salario Mínimo Mensual", f"${salario_mensual:,.0f}")
    mc2.metric("IPC Anual", f"{ipc_var_anual:.2f}%")
    mc3.metric("Tasa Hipotecaria", f"{tasa_hipotecaria_anual:.2f}%")
    mc4.metric("Tasa Desempleo", f"{tasa_desempleo:.1f}%")

# ── Predicción ────────────────────────────────────────────────────────────────
if st.button("🔮 Calcular Precio Estimado", type="primary"):

    df_input = pd.DataFrame([{
        'area': area, 'rooms': rooms, 'bathrooms': bathrooms,
        'estrato': estrato, 'year': year,
        'ipc_var_anual': ipc_var_anual,
        'tasa_hipotecaria_anual': tasa_hipotecaria_anual,
        'tasa_desempleo': tasa_desempleo,
        'ipvu_variacion_anual': ipvu_variacion_anual,
        'city': city, 'property_type': property_type
    }])

    precio_pred   = modelo.predict(df_input)[0]
    salario_anual = salario_mensual * 12
    iah_estimado  = precio_pred / salario_anual

    monto_credito = precio_pred * 0.70
    tasa_mensual  = (1 + (tasa_hipotecaria_anual / 100)) ** (1/12) - 1
    cuota_mensual = monto_credito * (tasa_mensual * (1 + tasa_mensual)**180) / ((1 + tasa_mensual)**180 - 1)
    ratio_cuota   = cuota_mensual / salario_mensual

    # Semáforo
    if iah_estimado <= 5:
        estilo, nivel, emoji = "card-verde",    "Accesible — cumple estándares OCDE",                       "🟢"
    elif iah_estimado <= 10:
        estilo, nivel, emoji = "card-amarillo", "Moderado — esfuerzo financiero significativo",              "🟡"
    elif iah_estimado <= 20:
        estilo, nivel, emoji = "card-naranja",  "Elevado — requiere ingresos superiores al salario mínimo", "🟠"
    else:
        estilo, nivel, emoji = "card-rojo",     "Crítico — financieramente inviable con salario mínimo",    "🔴"

    st.markdown(f"""
        <div class='result-card {estilo}'>
            <h2>{emoji} {nivel}</h2>
            <div class='res-val'>${precio_pred:,.0f} COP</div>
            <p><strong>IAH estimado:</strong> {iah_estimado:.1f} años de salario mínimo</p>
            <p><strong>Cuota mensual (70% financiado, 15 años):</strong>
               ${cuota_mensual:,.0f} COP/mes ({ratio_cuota*100:.1f}% del salario)</p>
        </div>
    """, unsafe_allow_html=True)

    st.caption("""
    ⚠️ *Precio estimado con base en listados de portales inmobiliarios digitales (2020–2023).
    No representa precios de transacción real. El IAH usa el salario mínimo legal vigente como
    referencia; familias con ingresos superiores tendrán un IAH más favorable.*
    """)
