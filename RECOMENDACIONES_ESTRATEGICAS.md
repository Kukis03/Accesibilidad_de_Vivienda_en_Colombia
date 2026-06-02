# Recomendaciones Estratégicas y Técnicas
## Proyecto: Accesibilidad de Vivienda en Colombia · CRISP-DM 2025-I

Este documento resume las recomendaciones clave derivadas del análisis de las Fases 1 y 2 del proyecto, enfocadas en maximizar el rigor metodológico y el impacto del producto final.

---

## 1. Robustez en la Integración de Datos (Fase 3)
Dado que el proyecto integra **9 datasets de precios** con fuentes y periodos distintos, la calidad del modelo final dependerá de la limpieza inicial.

*   **Deduplicación por Proximidad:** Implementar una lógica de deduplicación que vaya más allá del hash exacto. Un mismo inmueble puede aparecer en múltiples datasets con variaciones menores en el precio.
    *   *Sugerencia:* Agrupar por `(ciudad, área, habitaciones, baños)` y filtrar registros con precios que tengan una diferencia menor al 5% en el mismo año.
*   **Normalización de Moneda (TRM Histórica):** Para el dataset A4 (Properati), no usar una TRM fija. Es crítico cruzar con una tabla de TRM mensual/anual para convertir los precios en USD a COP de forma precisa según la fecha del anuncio.

## 2. Refinamiento del Modelo Predictivo (Fase 4)
El EDA confirmó que los precios siguen una **distribución log-normal**, lo cual es estándar en economía urbana.

*   **Transformación Logarítmica:** Entrenar el modelo para predecir `log(precio)` en lugar del valor nominal. Esto reduce el impacto de los outliers de lujo y estabiliza el error porcentual (MAPE).
*   **LightGBM / XGBoost:** Evaluar el uso de modelos de Gradient Boosting en lugar de Random Forest simple. Estos manejan mejor las variables categóricas de alta cardinalidad (como la columna `city`) y las relaciones no lineales.
*   **Interacciones Espaciales:** Incluir términos de interacción entre `área` y `ciudad`. El valor del metro cuadrado adicional es drásticamente diferente entre una metrópoli (Bogotá) y una ciudad intermedia.

## 3. Enriquecimiento del Índice de Accesibilidad (IAH)
El uso del salario mínimo es un gran acierto comunicativo, pero puede refinarse para el análisis de inequidad.

*   **IAH de Capacidad Real:** Calcular un índice que reste el costo de la **canasta básica** (IPC DANE) al ingreso. Esto revelará la "capacidad de ahorro" real para la cuota inicial, que suele ser el mayor cuello de botella.
*   **Segmentación por Estrato:** Si el campo `estrato` se mantiene tras la limpieza, calcular el IAH por nivel socioeconómico. Es probable que la accesibilidad esté empeorando más rápido en los estratos medios que en los bajos (debido a los subsidios VIS).

## 4. Estrategia para el Dashboard (Streamlit)
El dashboard no debe ser solo descriptivo, sino también una herramienta de toma de decisiones.

*   **Simulador Hipotecario:** Incluir un widget donde el usuario ingrese su salario y el sistema le recomiende en qué ciudades o barrios (para el caso de Bogotá) tiene una mayor probabilidad de costear una vivienda sin superar el 30% de ley de cuota mensual.
*   **Visualización de Clusters:** Mostrar geográficamente los grupos de ciudades identificados en el clustering para que el usuario entienda qué mercados se comportan de forma similar (ej. ciudades costeras vs. ciudades del interior).

## 5. Validación de Villavicencio (Sección 9-bis)
La estrategia de refuerzo con scraping es excelente, pero requiere validación.

*   **Consistencia de Fuentes:** Antes de integrar el dataset A9 (Scraping), realizar un test de hipótesis para verificar si el precio mediano del scraping es significativamente diferente al de los datasets de Kaggle para el mismo año.
*   **Factor de Corrección:** Si el scraping refleja "precios de oferta" inflados frente a los "precios de transacción" históricos, aplicar un factor de ajuste para evitar sesgos en la serie temporal 2024-2025.

---
*Documento generado por Gemini CLI para el equipo de proyecto (Steve, Sofía, Kukis)*
