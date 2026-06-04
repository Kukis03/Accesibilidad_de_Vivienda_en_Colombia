import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Segmentos de Mercado", page_icon="", layout="wide")

CLUSTER_VARS = ['IAH', 'precio_m2', 'ratio_cuota_salario', 'tasa_desempleo']
REQUIRED_COLS = {'city', 'year', 'IAH', 'precio_m2', 'ratio_cuota_salario',
                 'tasa_desempleo', 'cluster', 'PC1', 'PC2'}

# ─────────────────────────────────────────────────────────────────────────────
# NOMENCLATURA DE CLUSTERS
# ─────────────────────────────────────────────────────────────────────────────
# Los clusters se ordenan según su nivel de accesibilidad (IAH promedio):
#   Tier 1 → más accesible (menos años de salario para comprar)
#   Tier 5 → más inaccesible
# Esta nomenclatura es la que se usa de forma consistente en todo el dashboard.

CLUSTER_NAMES = {
    4: "Tier 1 · Accesibilidad relativa (≈ 13 años)",
    1: "Tier 2 · Inaccesibilidad moderada (≈ 16 años)",
    2: "Tier 3 · Inaccesibilidad elevada (≈ 19 años)",
    3: "Tier 4 · Inaccesibilidad crítica (≈ 25 años)",
    0: "Tier 5 · Inaccesibilidad extrema (≈ 29 años)",
}

CLUSTER_ORDER = [
    "Tier 1 · Accesibilidad relativa (≈ 13 años)",
    "Tier 2 · Inaccesibilidad moderada (≈ 16 años)",
    "Tier 3 · Inaccesibilidad elevada (≈ 19 años)",
    "Tier 4 · Inaccesibilidad crítica (≈ 25 años)",
    "Tier 5 · Inaccesibilidad extrema (≈ 29 años)",
]

# Paleta semántica verde → rojo (mejor → peor accesibilidad)
CLUSTER_COLORS = {
    "Tier 1 · Accesibilidad relativa (≈ 13 años)":   "#2E7D32",  # verde
    "Tier 2 · Inaccesibilidad moderada (≈ 16 años)": "#9ACD32",  # verde claro
    "Tier 3 · Inaccesibilidad elevada (≈ 19 años)":  "#F9A825",  # amarillo-naranja
    "Tier 4 · Inaccesibilidad crítica (≈ 25 años)":  "#E65100",  # naranja-rojo
    "Tier 5 · Inaccesibilidad extrema (≈ 29 años)":  "#B71C1C",  # rojo intenso
}

CLUSTER_DESCRIPTION = {
    "Tier 1 · Accesibilidad relativa (≈ 13 años)":
        "El mercado más accesible del país, aunque aún por encima del umbral OCDE "
        "(≤ 5 años). Una familia con salario mínimo necesita ~13 años de ingreso "
        "íntegro para comprar la vivienda mediana.",
    "Tier 2 · Inaccesibilidad moderada (≈ 16 años)":
        "Ciudades intermedias con costos moderados pero ya en zona seriamente "
        "inaccesible según OCDE.",
    "Tier 3 · Inaccesibilidad elevada (≈ 19 años)":
        "Mercados con precios por m² elevados y ratio cuota/salario que excede el "
        "umbral del 30%. Acceso vía crédito hipotecario es financieramente difícil.",
    "Tier 4 · Inaccesibilidad crítica (≈ 25 años)":
        "Grandes capitales con altos precios por m². Comprar requiere acumular "
        "ingresos durante un cuarto de siglo sin gastar nada.",
    "Tier 5 · Inaccesibilidad extrema (≈ 29 años)":
        "El segmento más caro del país. La vivienda mediana cuesta cerca de 29 "
        "años de salario mínimo — virtualmente inaccesible sin patrimonio previo "
        "o subsidio sustancial.",
}


# ─────────────────────────────────────────────────────────────────────────────
# CARGA DE DATOS
# ─────────────────────────────────────────────────────────────────────────────

def _rebuild_clusters():
    """Reconstruye ciudades_clusters.csv desde vivienda_colombia_limpio.csv + modelos guardados."""
    import joblib
    from sklearn.decomposition import PCA

    df = pd.read_csv("data/processed/vivienda_colombia_limpio.csv")
    dfc = df.groupby(['city', 'year'])[CLUSTER_VARS].median().reset_index()

    scaler = joblib.load('models/scaler_cluster.pkl')
    kmeans = joblib.load('models/kmeans_segmentacion.pkl')

    X = scaler.transform(dfc[CLUSTER_VARS])
    dfc['cluster'] = kmeans.predict(X)

    pcs = PCA(n_components=2).fit_transform(X)
    dfc['PC1'] = pcs[:, 0]
    dfc['PC2'] = pcs[:, 1]

    dfc.to_csv("data/processed/ciudades_clusters.csv", index=False)
    return dfc


@st.cache_data
def load_clusters():
    try:
        dfc = pd.read_csv("data/processed/ciudades_clusters.csv")
        if not REQUIRED_COLS.issubset(dfc.columns):
            dfc = _rebuild_clusters()
    except FileNotFoundError:
        dfc = _rebuild_clusters()
    return dfc


def _rebuild_perfiles(dfc):
    """Reconstruye perfiles_clusters.csv desde el DataFrame de clusters ya cargado."""
    perfiles = dfc.groupby('cluster')[CLUSTER_VARS].mean().round(2)
    perfiles['count'] = dfc.groupby('cluster').size()
    perfiles = perfiles.reset_index()
    perfiles.to_csv("data/processed/perfiles_clusters.csv", index=False)
    return perfiles


@st.cache_data
def load_perfiles(cluster_hash: str):
    try:
        perf = pd.read_csv("data/processed/perfiles_clusters.csv")
        if 'cluster' not in perf.columns:
            raise ValueError("missing cluster column")
    except (FileNotFoundError, ValueError):
        perf = None
    return perf


dfc = load_clusters()
_cluster_hash = str(sorted(dfc['cluster'].unique().tolist()))
perfiles = load_perfiles(_cluster_hash)
if perfiles is None:
    perfiles = _rebuild_perfiles(dfc)

dfc['cluster_name'] = dfc['cluster'].map(CLUSTER_NAMES)


# ─────────────────────────────────────────────────────────────────────────────
# ENCABEZADO
# ─────────────────────────────────────────────────────────────────────────────

st.title("Segmentos de Mercado de Vivienda")
st.markdown(
    "Agrupamos las 12 ciudades focales con **KMeans (K = 5)** según cuatro variables que "
    "describen su nivel de accesibilidad habitacional: **IAH** (años de salario mínimo "
    "necesarios para comprar), **precio por m²**, **ratio cuota/salario** y **tasa de "
    "desempleo**."
)
st.caption(
    "Cada combinación *ciudad-año* es un punto. Coeficiente de silueta = **0.49** · "
    "Varianza explicada por PCA (2 componentes) = **97.2 %**."
)

# Leyenda visual de los 5 tiers
st.markdown("### Leyenda de tiers de accesibilidad")
cols = st.columns(5)
for col, name in zip(cols, CLUSTER_ORDER):
    color = CLUSTER_COLORS[name]
    tier_short = name.split(" · ")[0]
    label = name.split(" · ")[1]
    col.markdown(
        f"""
        <div style="background:{color};padding:10px;border-radius:8px;color:white;text-align:center;height:90px;display:flex;flex-direction:column;justify-content:center;">
            <b style="font-size:13px;">{tier_short}</b><br>
            <span style="font-size:11px;">{label}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")


# ─────────────────────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────────────────────

tab1, tab2, tab3, tab4 = st.tabs([
    "Mapa de Clusters",
    "Evolución Temporal",
    "Perfiles",
    "Glosario",
])

# ──────────────────────────── TAB 1: MAPA ────────────────────────────────────
with tab1:
    st.subheader("IAH vs Precio por m²")
    st.caption(
        "Cada punto es una ciudad observada en un año del período 2019–2024. "
        "El **color** indica su tier de accesibilidad."
    )

    fig1 = px.scatter(
        dfc, x='IAH', y='precio_m2',
        color='cluster_name',
        category_orders={'cluster_name': CLUSTER_ORDER},
        color_discrete_map=CLUSTER_COLORS,
        hover_name='city',
        hover_data={'year': True, 'IAH': ':.1f', 'precio_m2': ':,.0f', 'cluster_name': False},
        labels={
            'IAH': 'IAH (años de salario mínimo)',
            'precio_m2': 'Precio por m² (COP)',
            'cluster_name': 'Tier',
        },
    )
    fig1.add_vline(x=5,  line_dash="dot", line_color="green",
                   annotation_text="Accesible OCDE (≤5)", annotation_position="top")
    fig1.add_vline(x=10, line_dash="dot", line_color="orange",
                   annotation_text="Seriamente inaccesible (≥10)", annotation_position="top")
    fig1.add_vline(x=20, line_dash="dot", line_color="red",
                   annotation_text="Crítico (>20)", annotation_position="top")
    fig1.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.35, xanchor="left", x=0))
    st.plotly_chart(fig1, use_container_width=True)

    col_a, col_b = st.columns([1.2, 1])
    with col_a:
        st.subheader("Proyección PCA")
        st.caption("Los 5 tiers son visualmente separables en el plano de componentes principales.")
        fig2 = px.scatter(
            dfc, x='PC1', y='PC2',
            color='cluster_name',
            category_orders={'cluster_name': CLUSTER_ORDER},
            color_discrete_map=CLUSTER_COLORS,
            hover_name='city',
            hover_data={'year': True, 'IAH': ':.1f', 'cluster_name': False},
        )
        fig2.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.45, xanchor="left", x=0))
        st.plotly_chart(fig2, use_container_width=True)

    with col_b:
        st.subheader("Ciudades en 2024")
        d24 = dfc[dfc['year'] == 2024][['city', 'cluster_name']].copy()
        d24['tier_num'] = d24['cluster_name'].map(
            {name: i for i, name in enumerate(CLUSTER_ORDER)}
        )
        d24 = d24.sort_values(['tier_num', 'city'])
        current_tier = None
        for _, r in d24.iterrows():
            if r['cluster_name'] != current_tier:
                current_tier = r['cluster_name']
                color = CLUSTER_COLORS[current_tier]
                tier_label = current_tier.split(" · ")[0]
                st.markdown(
                    f"<div style='background:{color};color:white;padding:4px 10px;"
                    f"border-radius:5px;margin-top:8px;font-weight:bold;font-size:13px;'>"
                    f"{tier_label}</div>",
                    unsafe_allow_html=True,
                )
            st.markdown(f"&nbsp;&nbsp;&nbsp;**{r['city']}**", unsafe_allow_html=True)


# ──────────────────────── TAB 2: EVOLUCIÓN TEMPORAL ──────────────────────────
with tab2:
    st.subheader("Heatmap Ciudad × Año")
    st.caption(
        "El número en cada celda es el **identificador interno** del cluster (0–4). "
        "Las ciudades están ordenadas por tier promedio para que las más críticas queden abajo."
    )

    # Mapear el cluster a su orden de tier (0 = mejor, 4 = peor)
    tier_order_map = {
        name: i for i, name in enumerate(CLUSTER_ORDER)
    }
    dfc['tier_num'] = dfc['cluster_name'].map(tier_order_map)

    hm = dfc.pivot(index='city', columns='year', values='tier_num')
    # Orden de ciudades: las con peor tier promedio quedan abajo
    ciudad_orden = hm.mean(axis=1).sort_values(ascending=True).index
    hm = hm.loc[ciudad_orden]

    fig3 = px.imshow(
        hm.values,
        x=hm.columns.astype(str),
        y=hm.index,
        text_auto=True,
        color_continuous_scale='RdYlGn_r',
        zmin=0, zmax=4,
        aspect="auto",
        labels=dict(x="Año", y="Ciudad", color="Tier (0=mejor, 4=peor)"),
    )
    fig3.update_layout(height=500)
    st.plotly_chart(fig3, use_container_width=True)

    # ── Explicación de transiciones ──────────────────────────────────────────
    with st.expander("¿Qué significa que una ciudad cambie de cluster entre años?", expanded=True):
        st.markdown(
            """
**Un cambio de cluster (o tier) refleja un cambio estructural en el mercado de esa
ciudad durante ese año**, capturado simultáneamente por las cuatro variables del
modelo: IAH, precio por m², ratio cuota/salario y tasa de desempleo.

#### Las tres formas de cambio:

| Movimiento | Qué pasó en la realidad | Causa típica |
|---|---|---|
| **Subió de tier** (a uno más crítico) | La vivienda se volvió **menos accesible** ese año | Subida de precios > subida de salario, o subida fuerte de la tasa hipotecaria (encarece la cuota) |
| **Bajó de tier** (a uno más accesible) | La vivienda se volvió **más accesible** ese año | Incremento del salario mínimo > inflación del precio, o caída de la tasa hipotecaria |
| **Se mantuvo** | El mercado es **estable** en términos relativos | Las cuatro variables se movieron de forma proporcional al resto de ciudades |

#### Ejemplos típicos del período 2019–2024:

- **2022 → 2023:** Varias ciudades suben de tier porque la tasa hipotecaria pasó de
  ~9,5 % a ~15,8 % EA, lo que disparó el `ratio_cuota_salario`.
- **2024:** El aumento del SMLMV (+12 %) hizo que algunas ciudades bajaran un tier
  al mejorar la relación precio/ingreso.
- **Ciudades estables:** Bogotá y Medellín tienden a permanecer en los tiers más
  altos (4–5) durante todo el período — su mercado es estructuralmente caro.

#### Lectura rápida del heatmap:

- **Filas con colores constantes** → ciudades con mercado estable.
- **Filas con degradado** → ciudades cuyo mercado se movió significativamente.
- **Columnas con dominio rojo** → años de máximo estrés (2022–2023).
            """
        )

    st.subheader("Resumen de transiciones 2019 → 2024")
    d_inicio = dfc[dfc['year'] == 2019][['city', 'cluster_name']].rename(columns={'cluster_name': '2019'})
    d_fin    = dfc[dfc['year'] == 2024][['city', 'cluster_name']].rename(columns={'cluster_name': '2024'})
    tr = d_inicio.merge(d_fin, on='city')
    tr['tier_inicio'] = tr['2019'].map(tier_order_map)
    tr['tier_fin']    = tr['2024'].map(tier_order_map)
    tr['Δ tier']      = tr['tier_fin'] - tr['tier_inicio']

    def flecha(delta):
        if delta > 0:
            return f"+{int(delta)} (menos accesible)"
        elif delta < 0:
            return f"{int(delta)} (más accesible)"
        else:
            return "sin cambio"

    tr['Movimiento'] = tr['Δ tier'].apply(flecha)
    st.dataframe(
        tr[['city', '2019', '2024', 'Movimiento']].rename(columns={'city': 'Ciudad'}),
        use_container_width=True, hide_index=True,
    )

    n_sube = (tr['Δ tier'] > 0).sum()
    n_baja = (tr['Δ tier'] < 0).sum()
    n_igual = (tr['Δ tier'] == 0).sum()
    c1, c2, c3 = st.columns(3)
    c1.metric("Empeoraron", n_sube, help="Subieron a un tier menos accesible")
    c2.metric("Estables", n_igual, help="Permanecieron en el mismo tier")
    c3.metric("Mejoraron", n_baja, help="Bajaron a un tier más accesible")


# ──────────────────────────── TAB 3: PERFILES ────────────────────────────────
with tab3:
    st.subheader("Perfil promedio de cada tier")
    st.caption(
        "Cada tier se define por el promedio de sus cuatro variables. "
        "Los nombres se ordenan de **más accesible (Tier 1)** a **menos accesible (Tier 5)**."
    )

    perf = perfiles.copy().set_index('cluster')
    perf.columns = ['IAH (años)', 'Precio m² (COP)', 'Ratio Cuota/Salario', 'Tasa Desempleo (%)', 'Registros']
    perf.index = [CLUSTER_NAMES.get(i, str(i)) for i in perf.index]
    perf = perf.loc[[name for name in CLUSTER_ORDER if name in perf.index]]

    perf_view = perf.copy()
    perf_view['Precio m² (COP)']     = perf_view['Precio m² (COP)'].apply(lambda x: f"${x:,.0f}")
    perf_view['IAH (años)']          = perf_view['IAH (años)'].round(1)
    perf_view['Tasa Desempleo (%)']  = perf_view['Tasa Desempleo (%)'].apply(lambda x: f"{x:.1f}%")
    perf_view['Ratio Cuota/Salario'] = perf_view['Ratio Cuota/Salario'].round(2)
    perf_view['Registros']           = perf_view['Registros'].astype(int)

    st.dataframe(perf_view, use_container_width=True)

    # Descripción cualitativa
    st.subheader("Descripción de cada tier")
    for name in CLUSTER_ORDER:
        if name in perf.index:
            color = CLUSTER_COLORS[name]
            with st.container():
                st.markdown(
                    f"<div style='border-left:5px solid {color};padding:8px 14px;"
                    f"margin:8px 0;background:#fafafa;'>"
                    f"<b>{name}</b><br><span style='color:#444;'>{CLUSTER_DESCRIPTION[name]}</span>"
                    f"</div>",
                    unsafe_allow_html=True,
                )

    # Radar
    st.subheader("Radar comparativo")
    st.caption("Cada eje normalizado entre 0 (mínimo del cluster más bajo) y 1 (máximo del más alto).")
    features_radar = ['IAH', 'precio_m2', 'ratio_cuota_salario', 'tasa_desempleo']
    radar_labels = {
        'IAH': 'IAH',
        'precio_m2': 'Precio m²',
        'ratio_cuota_salario': 'Cuota/Salario',
        'tasa_desempleo': 'Desempleo',
    }
    rn = (perfiles[features_radar] - perfiles[features_radar].min()) / \
         (perfiles[features_radar].max() - perfiles[features_radar].min() + 1e-6)
    rn = rn.rename(columns=radar_labels)
    rn.index = perfiles['cluster']

    fig4 = go.Figure()
    for cluster_id in [4, 1, 2, 3, 0]:  # mismo orden que CLUSTER_ORDER
        if cluster_id in rn.index:
            name = CLUSTER_NAMES[cluster_id]
            fig4.add_trace(go.Scatterpolar(
                r=rn.loc[cluster_id].values,
                theta=rn.columns,
                fill='toself',
                name=name.split(" · ")[0],  # solo "Tier X"
                line=dict(color=CLUSTER_COLORS[name]),
            ))
    fig4.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        title="Perfil normalizado por tier",
        legend=dict(orientation="h", yanchor="bottom", y=-0.2),
    )
    st.plotly_chart(fig4, use_container_width=True)


# ──────────────────────────── TAB 4: GLOSARIO ────────────────────────────────
with tab4:
    st.subheader("Glosario de variables del modelo de segmentación")
    st.markdown(
        "Los cuatro indicadores que el algoritmo K-Means usa para agrupar las ciudades. "
        "Entender cada uno te permite leer correctamente la tabla de perfiles y el radar."
    )

    # ── Ratio Cuota / Salario ────────────────────────────────────────────────
    st.markdown("### Ratio Cuota / Salario")
    st.markdown(
        """
**Definición:** Proporción del salario mínimo mensual que se destina a pagar la
**cuota mensual del crédito hipotecario** para comprar la vivienda mediana de
esa ciudad y año.

**Fórmula:**

$$
\\text{ratio\\_cuota\\_salario} = \\frac{\\text{cuota mensual estimada}}{\\text{salario mínimo mensual}}
$$

**Supuestos del crédito** (estándar Banco de la República para crédito No VIS):
- Se financia el **70 %** del valor de la vivienda
- Plazo de **15 años** (180 meses)
- Tasa de interés: tasa hipotecaria efectiva anual del año correspondiente
- Sistema de amortización francés (cuota fija)

**Cómo interpretarlo:**

| Valor | Lectura |
|:---:|---|
| **≤ 0,30** | Cuota cabe en el 30 % del ingreso — financieramente saludable |
| **0,30 – 0,50** | Cuota presiona el presupuesto familiar — riesgo de impago |
| **0,50 – 1,00** | La cuota es la mitad del salario o más — inviable sin codeudor |
| **> 1,00** | La cuota **supera** el salario completo — inviable financieramente |

**Estándar internacional:** la regla 30/30 (BCE, FED, ONU-Hábitat) define como
saludable un ratio ≤ 0,30. Por encima de ese umbral, el hogar entra en
*sobrecarga de deuda hipotecaria*.

**En este proyecto:** las 12 ciudades focales tienen un ratio mediano superior
a 1,00 durante todo el período 2019–2024, lo que significa que la cuota
mensual del crédito **excede el salario mínimo completo** en todas ellas.
        """
    )

    st.markdown("---")

    # ── IAH ──────────────────────────────────────────────────────────────────
    st.markdown("### IAH — Índice de Accesibilidad Habitacional")
    st.markdown(
        """
**Definición:** Número de años de salario mínimo íntegros que un hogar necesita
para acumular el precio de la vivienda mediana de esa ciudad.

**Fórmula:**

$$
\\text{IAH} = \\frac{\\text{precio mediano de vivienda}}{\\text{salario mínimo anual}}
$$

**Adaptación local del PIR** *(Price-to-Income Ratio)* de la OCDE y ONU-Hábitat,
usando el SMLMV como proxy del ingreso de referencia (no del ingreso mediano
real, que en Colombia no se publica oficialmente por ciudad-año de forma
consistente).

**Umbrales de referencia OCDE:**

| Rango | Categoría |
|:---:|---|
| IAH ≤ 5 años | Accesible |
| 5 < IAH ≤ 10 | Moderado |
| 10 < IAH ≤ 20 | Seriamente inaccesible |
| IAH > 20 | Crítico |
        """
    )

    st.markdown("---")

    # ── Precio por m² ────────────────────────────────────────────────────────
    st.markdown("### Precio por metro cuadrado")
    st.markdown(
        """
**Definición:** Costo mediano del metro cuadrado construido en la ciudad,
calculado como `precio / area` por registro y luego mediano por ciudad-año.

Permite comparar la **valoración unitaria** del suelo entre ciudades de
distinto tamaño promedio de inmueble. Una ciudad puede tener precios totales
bajos por vender viviendas más pequeñas — el precio/m² corrige por ese efecto.
        """
    )

    st.markdown("---")

    # ── Tasa de desempleo ───────────────────────────────────────────────────
    st.markdown("### Tasa de Desempleo")
    st.markdown(
        """
**Definición:** Tasa de desempleo (TD) anual promedio por ciudad, proveniente
de la **GEIH del DANE** (13 áreas metropolitanas).

**¿Por qué entra al clustering?** El desempleo afecta la **demanda efectiva**
de vivienda. Ciudades con desempleo alto tienen menor poder adquisitivo
agregado y menor presión sobre los precios, lo que reconfigura el segmento
de mercado al que pertenecen.
        """
    )

    st.markdown("---")

    # ── Metodología técnica ─────────────────────────────────────────────────
    st.markdown("### Metodología del clustering")
    st.markdown(
        """
| Aspecto | Valor |
|---|---|
| Algoritmo | **K-Means** con `init='k-means++'`, `n_init=20`, `random_state=42` |
| Número de clusters | **K = 5** (seleccionado con método del codo + silueta) |
| Escalado | `StandardScaler` sobre las 4 features |
| Coeficiente de silueta | **0.49** (criterio Fase 1: ≥ 0,45 — cumple) |
| Índice Davies-Bouldin | **0.64** (menor = mejor) |
| Varianza explicada (PCA 2D) | **97.2 %** |
| Validación | DBSCAN (detección de outliers) + PCA (visualización) |

> Los modelos serializados están en `models/kmeans_segmentacion.pkl` y
> `models/scaler_cluster.pkl`. Se reconstruyen automáticamente desde
> `vivienda_colombia_limpio.csv` si el archivo de clusters no existe.
        """
    )
