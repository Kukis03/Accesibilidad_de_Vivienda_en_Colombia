import streamlit as st
import pandas as pd
import plotly.express as px
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Comparador de Ciudades", layout="wide")

# Paleta coherente con app.py
LEVEL_COLORS = {
    'Accesible': '#2E7D32',
    'Moderado':  '#F9A825',
    'Elevado':   '#EF6C00',
    'Critico':   '#C62828',
}
CITY_COLORS = [
    '#1565C0', '#AD1457', '#2E7D32', '#E65100',
    '#6A1B9A', '#00838F', '#F9A825', '#4E342E',
    '#37474F', '#558B2F', '#C62828', '#0277BD',
]

@st.cache_data
def load_data():
    return pd.read_csv("data/processed/vivienda_colombia_limpio.csv", encoding="utf-8-sig")

df = load_data()
ciudades = sorted(df['city'].unique())
anios    = sorted(df['year'].unique())

# Defaults seguros: primeras 3 ciudades que existan en los datos
DEFAULT_CITIES = [c for c in ["Bogotá", "Medellín", "Cali"] if c in ciudades] or ciudades[:3]

st.title("Comparador de Ciudades")
st.markdown("Selecciona **2 a 4 ciudades** para comparar sus indicadores de accesibilidad, precios y condiciones del mercado.")

with st.expander("Glosario de terminos"):
    st.markdown("""
**IAH — Indice de Accesibilidad Habitacional**
Anos de salario minimo completo necesarios para comprar una vivienda al precio mediano.
Formula: `IAH = Precio vivienda / Salario anual minimo`.
Referencia OCDE: IAH <= 5 es accesible; > 20 es critico.

**Precio por m²**
Precio de venta dividido entre el area construida. Permite comparar propiedades de distinto tamano.

**Ratio cuota / salario**
Fraccion del salario minimo mensual que representa la cuota hipotecaria estimada.
Formula: `Cuota mensual / Salario minimo mensual`.
El umbral critico es **0.30 (30%)**: superarlo implica sobreendeudamiento.

**Tasa de desempleo**
Porcentaje de la poblacion economicamente activa sin trabajo. Fuente: GEIH - DANE.

**Estrato**
Clasificacion socieconomica del predio en Colombia (1 = mas bajo, 6 = mas alto).
Determina subsidios y contribuciones en servicios publicos.

**Ingresos medio-altos**
Hogares con ingresos entre 4 y 8 salarios minimos mensuales (~$5.2M a $10.4M COP en 2024).
Para este perfil un IAH de 5 a 10 es exigente pero alcanzable con credito hipotecario a largo plazo.
    """)

col1, col2 = st.columns(2)
with col1:
    cities_sel = st.multiselect("Ciudades a comparar (2 a 4)", ciudades, default=DEFAULT_CITIES, max_selections=4)
with col2:
    yr = st.select_slider("Año de comparacion", options=anios, value=anios[-1])

if len(cities_sel) < 2:
    st.warning("Selecciona al menos 2 ciudades para comparar.")
    st.stop()

city_color_map = {c: CITY_COLORS[i % len(CITY_COLORS)] for i, c in enumerate(sorted(cities_sel))}
dc = df[(df['city'].isin(cities_sel)) & (df['year'] == yr)]

tab1, tab2 = st.tabs(["Tabla Comparativa", "Visualizaciones"])

with tab1:
    st.subheader(f"Comparacion Directa — {yr}")
    tbl = dc.groupby('city').agg(
        precio_mediano=('price', 'median'),
        precio_m2=('precio_m2', 'median'),
        IAH=('IAH', 'median'),
        ratio_cuota=('ratio_cuota_salario', 'median'),
        area_med=('area', 'median'),
        estrato_med=('estrato', 'median'),
        desempleo=('tasa_desempleo', 'first'),
        n=('price', 'count')
    ).reset_index()

    tbl_display = tbl.copy()
    tbl_display['precio_mediano'] = tbl_display['precio_mediano'].apply(lambda x: f"${x:,.0f}")
    tbl_display['precio_m2']      = tbl_display['precio_m2'].apply(lambda x: f"${x:,.0f}")
    tbl_display['IAH']            = tbl_display['IAH'].round(1)
    tbl_display['ratio_cuota']    = tbl_display['ratio_cuota'].apply(lambda x: f"{x:.2f} ({x*100:.0f}%)")
    tbl_display['area_med']       = tbl_display['area_med'].round(0).astype(int)
    tbl_display['estrato_med']    = tbl_display['estrato_med'].round(1)
    tbl_display['desempleo']      = tbl_display['desempleo'].apply(lambda x: f"{x:.1f}%")
    tbl_display.columns = [
        'Ciudad', 'Precio mediano (COP)', 'Precio por m² (COP)',
        'IAH (anos sal. min.)', 'Ratio cuota / salario',
        'Area mediana (m²)', 'Estrato mediano', 'Tasa desempleo', 'Registros'
    ]
    st.dataframe(tbl_display, use_container_width=True, hide_index=True)

    reg_info = ", ".join([f"**{r['city']}**: {r['n']:,}" for _, r in tbl.iterrows()])
    st.info(f"Registros analizados en {yr}: {reg_info}")
    if any(tbl['n'] < 500):
        st.warning("Alguna ciudad tiene menos de 500 registros — las estimaciones pueden ser inestables.")

with tab2:
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("Precio Mediano por Ciudad")
        fig_bar = px.bar(
            tbl.sort_values('precio_mediano'), x='city', y='precio_mediano',
            color='IAH', color_continuous_scale='RdYlGn_r',
            labels={'precio_mediano': 'Precio (COP)', 'city': '', 'IAH': 'IAH'},
            title=f"Precio mediano — {yr}"
        )
        fig_bar.update_layout(xaxis_title="", yaxis_tickprefix="$")
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_b:
        st.subheader("IAH por Ciudad")
        fig_iah = px.bar(
            tbl.sort_values('IAH'), x='city', y='IAH',
            color='IAH', color_continuous_scale='RdYlGn_r',
            labels={'IAH': 'Anos de salario minimo', 'city': ''},
            title=f"Anos de salario minimo para comprar vivienda — {yr}"
        )
        fig_iah.add_hline(y=5,  line_dash="dash", line_color=LEVEL_COLORS['Accesible'], annotation_text="Accesible (<=5)")
        fig_iah.add_hline(y=10, line_dash="dash", line_color=LEVEL_COLORS['Moderado'],  annotation_text="Moderado (<=10)")
        fig_iah.add_hline(y=20, line_dash="dash", line_color=LEVEL_COLORS['Critico'],   annotation_text="Critico (>20)")
        st.plotly_chart(fig_iah, use_container_width=True)

    st.subheader("Evolucion del IAH (2020–2024)")
    ev = df[df['city'].isin(cities_sel)].groupby(['city', 'year'])['IAH'].median().reset_index()
    fig_ev = px.line(
        ev, x='year', y='IAH', color='city', markers=True,
        color_discrete_map=city_color_map,
        labels={'IAH': 'IAH (anos sal. min.)', 'year': 'Año', 'city': 'Ciudad'},
        title="Como ha cambiado la accesibilidad en el tiempo"
    )
    fig_ev.add_hline(y=5,  line_dash="dash", line_color=LEVEL_COLORS['Accesible'], annotation_text="Accesible (<=5)")
    fig_ev.add_hline(y=10, line_dash="dash", line_color=LEVEL_COLORS['Moderado'],  annotation_text="Moderado (<=10)")
    fig_ev.add_hline(y=20, line_dash="dash", line_color=LEVEL_COLORS['Critico'],   annotation_text="Critico (>20)")
    fig_ev.update_layout(xaxis=dict(dtick=1), hovermode='x unified')
    st.plotly_chart(fig_ev, use_container_width=True)

    st.subheader("Distribucion de Precios por Ciudad")
    fig_box = px.box(
        dc, x='city', y='price', color='city',
        color_discrete_map=city_color_map,
        labels={'price': 'Precio (COP)', 'city': ''},
        title="Como se distribuyen los precios dentro de cada ciudad",
        points=False
    )
    fig_box.update_layout(yaxis_tickprefix="$", showlegend=False)
    st.plotly_chart(fig_box, use_container_width=True)

    st.markdown("---")
    st.subheader("Ratio Cuota / Salario — Evolucion Temporal")
    st.markdown("""
El **ratio cuota / salario** mide que fraccion del salario minimo mensual representa la cuota hipotecaria.
El umbral critico es **0.30 (30%)**: superarlo implica sobreendeudamiento segun estandares financieros internacionales.
    """)
    pct_total   = (df['ratio_cuota_salario'] > 0.30).mean() * 100
    ratio_all   = df[df['city'].isin(cities_sel)].groupby(['city', 'year'])['ratio_cuota_salario'].median().reset_index()
    ratio_pivot = ratio_all.pivot(index='city', columns='year', values='ratio_cuota_salario')
    fig_heat = px.imshow(
        ratio_pivot.values,
        x=list(ratio_pivot.columns), y=list(ratio_pivot.index),
        color_continuous_scale='RdYlGn_r',
        zmin=0, zmax=1,
        aspect="auto",
        labels=dict(x="Año", y="Ciudad", color="Ratio cuota/salario"),
        title="Ratio cuota / salario por ciudad y año (rojo = mayor sobreendeudamiento)"
    )
    fig_heat.update_layout(height=350)
    st.plotly_chart(fig_heat, use_container_width=True)

    st.error(
        f"**Hallazgo:** El **{pct_total:.1f}%** del mercado tiene cuota hipotecaria superior al 30% del salario minimo. "
        f"Todas las ciudades en todos los años superan este umbral. "
        f"El mercado es financieramente inviable para un hogar de salario minimo."
    )
    st.info(
        "**Implicacion:** La politica de vivienda deberia enfocarse en reducir el precio por m² "
        "(especialmente en Bogota y Medellin) y/o subsidiar la cuota hipotecaria para hogares de bajos ingresos."
    )
