# 🏠 Accesibilidad de Vivienda en Colombia · CRISP-DM

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/framework-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![Model](https://img.shields.io/badge/model-Random%20Forest-green.svg)](https://scikit-learn.org/)
[![Methodology](https://img.shields.io/badge/methodology-CRISP--DM-orange.svg)](https://en.wikipedia.org/wiki/Cross-industry_standard_process_for_data_mining)

Este repositorio contiene el código, los datos y la documentación del proyecto final de Ciencia de Datos orientado a analizar la **Accesibilidad Económica a la Vivienda Urbana en Colombia** entre los años **2019 y 2024**. El proyecto integra un gran volumen de listados inmobiliarios con variables macroeconómicas oficiales bajo la metodología estándar **CRISP-DM**.

👉 **URL de Producción:** [https://colombia-housing-accessibility.streamlit.app/](https://colombia-housing-accessibility.streamlit.app/)

---

## 📌 Resumen del Proyecto

Adquirir una vivienda es la decisión financiera más importante para un hogar. Este estudio diseña y valida el **Índice de Accesibilidad Habitacional (IAH)** para Colombia, adaptando el indicador internacional *Price-to-Income Ratio (PIR)* de la OCDE y la ONU. Al utilizar el salario mínimo legal mensual como proxy del ingreso de referencia de los hogares, cuantificamos el desajuste estructural entre el costo de la vivienda formal y los ingresos reales de la población.

El proyecto abarca:
1. **Unificación masiva de datos:** Integración de **8 datasets de precios inmobiliarios** (más de 629K registros brutos) y **8 fuentes macroeconómicas** de entidades oficiales como el DANE y el Banco de la República.
2. **Modelado Supervisado:** Un regresor basado en **Random Forest** (R² = 0.792, MAPE = 15.8%) para estimar el precio nominal de cualquier inmueble en tiempo real.
3. **Modelado No Supervisado:** Agrupamiento de submercados locales mediante **KMeans** (K=4, Silueta = 0.54) para clasificar y mapear las ciudades de Colombia según su accesibilidad financiera.

---

## 🛠️ Arquitectura y Estructura del Repositorio

El repositorio está organizado siguiendo las mejores prácticas de estructuración de proyectos de ciencia de datos:

```text
ACCESIBILIDAD_DE_VIVIENDA_EN_COLOMBIA/
├── .streamlit/
│   └── config.toml                         # Configuración de estilización del dashboard
├── app/
│   ├── app.py                              # Vista principal del dashboard de Streamlit
│   └── pages/
│       ├── 01_analisis_nacional.py         # Módulo de tendencias macroeconómicas nacionales
│       ├── 02_comparador_ciudades.py       # Módulo para contraste visual de ciudades
│       ├── 03_predictor_precios.py         # Interfaz para predicción con Random Forest
│       └── 04_segmentos_mercado.py         # Panel del clustering y transición temporal
├── data/
│   ├── raw/                                # Datasets brutos (inmobiliarios y macro)
│   └── processed/
│       ├── vivienda_colombia_limpio.csv    # Dataset consolidado final (315K registros)
│       └── segmentos_mercado.csv           # Asignación de clústeres por ciudad-año
├── docs/                                   # Reportes detallados por cada fase de CRISP-DM
│   ├── FASE_1_COMPLETA.md                  # Comprensión del Negocio (Steve)
│   ├── FASE_2_COMPLETA.md                  # Comprensión de los Datos (Sofía)
│   ├── FASE_3_COMPLETA.md                  # Preparación de los Datos (Kukis)
│   ├── FASE_4_COMPLETA.md                  # Modelado (Steve)
│   ├── FASE_5_COMPLETA.md                  # Evaluación (Sofía)
│   ├── FASE_6_COMPLETA.md                  # Despliegue (Kukis)
│   └── figures/                            # Gráficos y diagramas exportados
├── models/
│   └── modelo_random_forest.pkl            # Pipeline de regresión serializado (pickle)
├── scripts/
│   └── scraping_fincaraiz_villavicencio.py # Script de BeautifulSoup para recolección de datos
├── requirements.txt                        # Lista de dependencias del proyecto
└── README.md                               # Este archivo de presentación
```

---

## 🚀 Guía de Instalación y Ejecución Local

Sigue estos pasos para replicar el entorno de desarrollo y ejecutar la aplicación interactiva localmente:

### 1. Clonar el repositorio
```bash
git clone https://github.com/AlexanderPineda25/Accesibilidad_de_Vivienda_en_Colombia
cd ACCESIBILIDAD_DE_VIVIENDA_EN_COLOMBIA
```

### 2. Crear y activar un entorno virtual
* **En Windows:**
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```
* **En macOS/Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 3. Instalar las dependencias
```bash
pip install -r requirements.txt
```

### 4. Ejecutar el servidor de Streamlit
```bash
streamlit run app/app.py
```
El panel se abrirá automáticamente en tu navegador web predeterminado en la dirección local `http://localhost:8501`.

---

## 📈 Hallazgos Clave del Análisis

* **Inaccesibilidad Crítica:** El promedio nacional del IAH en 2024 se situó en **18.4 años** de salario mínimo. Según el estándar de la OCDE (donde un índice mayor a 10 se considera severamente inasequible), **Colombia se encuentra en una crisis generalizada de accesibilidad habitacional**.
* **El Abismo Territorial:** Adquirir la vivienda mediana en **Bogotá exige 25.4 años** de ingresos frente a los **8.1 años necesarios en Cúcuta**, evidenciando una enorme disparidad de costo por metro cuadrado ($3.98M/m² vs. $1.62M/m²).
* **Sobrecarga de Deuda:** En 10 de las 12 capitales analizadas, la cuota mensual de amortización de un crédito hipotecario estándar (70% financiado a 15 años) **supera el límite saludable del 30% del ingreso mensual**, llegando en Bogotá y Medellín a requerir más de **1.5 salarios mínimos completos tan solo para cubrir la cuota**.
* **Extinción del Mercado Accesible:** El análisis temporal revela que mientras en 2019 la mitad de las ciudades focalizadas clasificaban en submercados de accesibilidad 'Moderado' o 'Accesible', **para 2024 ninguna ciudad del estudio califica en el nivel 'Accesible'**.

---

## 🤖 Modelado Estadístico e Inferencia

El proyecto implementa modelos de analítica avanzada entrenados sobre **315,487 observaciones limpias**:

### Regresión (Estimación de Precios de Venta)
* **Algoritmo final:** Random Forest Regressor (300 estimadores, profundidad máxima 16).
* **Métricas en conjunto de pruebas:**
  * **R²:** 0.792 (el modelo explica el 79.2% de la varianza).
  * **MAPE:** 15.8% (desviación porcentual promedio de predicción).
  * **Estabilidad:** CV R² std de apenas 0.022.
* **Predictores dominantes (Feature Importance):** Área construida (38.4%), Condición geográfica Bogotá (21.7%) y Tasa de interés hipotecaria No VIS (11.2%).

### Clustering (Segmentación de Mercados)
* **Algoritmo:** KMeans con K=4 (Silueta = 0.54, Davies-Bouldin = 0.81).
* **Segmentos definidos:**
  1. *Crítico* (Bogotá, Medellín, Cartagena)
  2. *Elevado* (Cali, Barranquilla, Bucaramanga)
  3. *Moderado* (Pereira, Manizales, Villavicencio, Armenia)
  4. *Accesible* (Cúcuta, Ibagué - *extintos para 2024*).

---

## 👥 Equipo y Distribución de Roles (Metodología CRISP-DM)

La asignación de responsables asegura la especialización y la revisión cruzada de los entregables:

* **Steve** (Líder de Fases 1 y 4): Comprensión del Negocio, diseño del modelo de regresión y análisis de importancia de variables.
* **Sofía** (Líder de Fases 2 y 5): Comprensión de los Datos (EDA), validación de hipótesis de negocio y evaluación estadística.
* **Kukis** (Líder de Fases 3 y 6): Limpieza e integración de datos macro, construcción de variables derivadas y desarrollo del dashboard multipágina en Streamlit.

---
*Proyecto Académico · Minería de Datos 2025-I · Colombia*  
*Para mayor detalle técnico y de negocio, por favor consulte los reportes completos en la carpeta [/docs]*
