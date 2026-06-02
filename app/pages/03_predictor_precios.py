import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

st.set_page_config(page_title="Predictor de Precio", page_icon="🔮", layout="wide")
st.title("🔮 Predicción del Precio y Accesibilidad en Tiempo Real")

# Estilos CSS
st.markdown("""
    <style>
    .result-card { border-radius: 10px; padding: 25px; margin-top: 20px; text-align: center; }
    .card-verde { background-color: #d4edda; border: 2px solid #c3e6cb; color: #155724; }
    .card-amarillo { background-color: #fff3cd; border: 2px solid #ffeeba; color: #856404; }
    .card-rojo { background-color: #f8d7da; border: 2px solid #f5c6cb; color: #721c24; }
    .res-val { font-size: 32px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# Cargar Modelo Guardado en Fase 4
@st.cache_resource
def cargar_modelo():
    ruta = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '..', 'models', 'modelo_random_forest.pkl')
    if os.path.exists(ruta):
        return joblib.load(ruta)
    return None

modelo = cargar_modelo()

if modelo is not None:
    st.subheader("Ingrese las Características del Inmueble a Valorar")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        area = st.number_input("Área Construida (m²)", min_value=15.0, max_value=800.0, value=70.0, step=1.0)
        property_type = st.selectbox("Tipo de Propiedad", ["Apartamento", "Casa"])
    with col2:
        rooms = st.selectbox("Habitaciones", [1, 2, 3, 4, 5, 6], index=2)
        bathrooms = st.selectbox("Baños", [1, 2, 3, 4, 5, 6], index=1)
    with col3:
        city = st.selectbox("Ciudad", ['Bogotá', 'Medellín', 'Cali', 'Barranquilla', 'Cartagena', 
                                       'Bucaramanga', 'Pereira', 'Manizales', 'Armenia', 'Cúcuta', 
                                       'Ibagué', 'Villavicencio'])
        estrato = st.slider("Estrato Socioeconómico", 1, 6, 3)

    # Variables macro fijadas para el año 2024
    year = 2024
    ipc_var_anual = 6.80
    tasa_hipotecaria_anual = 12.50
    tasa_desempleo = 10.5
    ipvu_variacion_anual = 7.20
    
    # Crear dataframe para la predicción
    df_predict = pd.DataFrame([{
        'area': area, 'rooms': rooms, 'bathrooms': bathrooms, 'estrato': estrato, 'year': year,
        'ipc_var_anual': ipc_var_anual, 'tasa_hipotecaria_anual': tasa_hipotecaria_anual,
        'tasa_desempleo': tasa_desempleo, 'ipvu_variacion_anual': ipvu_variacion_anual,
        'city': city, 'property_type': property_type
    }])
    
    if st.button("Calcular Precio Estimado"):
        # Realizar predicción
        precio_pred = modelo.predict(df_predict)[0]
        
        # Fórmulas de Variables Derivadas (Fase 3)
        salario_minimo_2024 = 1300000
        salario_anual_2024 = salario_minimo_2024 * 12
        iah_estimado = precio_pred / salario_anual_2024
        
        # Calcular cuota mensual (15 años, 70% financiado)
        monto_credito = precio_pred * 0.70
        tasa_mensual = (1 + (tasa_hipotecaria_anual / 100)) ** (1/12) - 1
        cuota_mensual = monto_credito * (tasa_mensual * (1 + tasa_mensual)**180) / ((1 + tasa_mensual)**180 - 1)
        ratio_cuota = cuota_mensual / salario_minimo_2024
        
        # Determinar semáforo de asequibilidad
        if iah_estimado <= 5 and ratio_cuota <= 0.30:
            estilo = "card-verde"
            mensaje = "Accesible (Cumple con los estándares OCDE)"
        elif iah_estimado <= 15:
            estilo = "card-amarillo"
            mensaje = "Moderado / Esfuerzo Financiero Elevado"
        else:
            estilo = "card-rojo"
            mensaje = "🚨 Crítico / Financieramente Inviable para Salario Mínimo"
            
        st.markdown(f"""
            <div class='result-card {estilo}'>
                <h3>Precio Predicho Estimado:</h3>
                <div class='res-val'>${precio_pred:,.0f} COP</div>
                <p>Nivel de Accesibilidad: <strong>{mensaje}</strong></p>
                <p>Índice IAH: <strong>{iah_estimado:.1f} años</strong> de salario mínimo | Cuota Mensual Estimada: <strong>${cuota_mensual:,.0f} COP/mes</strong> ({ratio_cuota*100:.1f}% del salario)</p>
            </div>
        """, unsafe_allow_html=True)
else:
    st.error("Error: No se pudo cargar el archivo del modelo `models/modelo_random_forest.pkl`. Asegúrese de haber completado la Fase 4.")
