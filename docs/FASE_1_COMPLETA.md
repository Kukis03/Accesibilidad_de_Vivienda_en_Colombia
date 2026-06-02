# Fase 1 — Comprensión del Negocio

---

**Proyecto:** Accesibilidad de Vivienda en Colombia · CRISP-DM 2025-I  
**Equipo:** Steve (responsable) · Sofía · Kukis  
**Período de análisis:** 2019 – 2024  
**Estado:** Completa y lista para revisión del jurado

---

## Resumen Ejecutivo

Este proyecto construye un sistema cuantitativo de análisis de accesibilidad habitacional en Colombia para el período 2019–2024. Integra 16 fuentes de datos (8 de precios inmobiliarios y 8 de variables macroeconómicas), desarrolla un Índice de Accesibilidad Habitacional (IAH) basado en el Price-to-Income Ratio (PIR) adaptado al contexto colombiano, y despliega los resultados en un dashboard interactivo público. El análisis abarca 12 ciudades focales con cobertura comparativa nacional.

---

## 1. Contexto y Justificación

La vivienda es el activo más costoso que adquiere un hogar a lo largo de su vida. En Colombia, el déficit habitacional cuantitativo supera el millón de unidades, y el precio de la vivienda ha crecido sostenidamente por encima del salario mínimo real durante la última década. Los datos más recientes del DANE reportaron incrementos del 9,11% en Bogotá, 8,29% en Medellín y 9,22% en Barranquilla, mientras que ciudades intermedias como Cúcuta registraron saltos del 24,6% en 2024, evidenciando una crisis que no es exclusiva de las grandes capitales.

El indicador internacional de referencia es el **Price-to-Income Ratio (PIR)**: la razón entre el precio mediano de vivienda y el ingreso anual mediano del hogar. Un PIR superior a 5 se considera crítico según la OCDE y ONU-Hábitat. Este proyecto construye una versión del PIR adaptada al contexto colombiano usando el salario mínimo como proxy del ingreso de referencia, integra todos los datasets disponibles de precios inmobiliarios con variables macroeconómicas oficiales, y analiza tanto el nivel nacional como las diferencias entre ciudades para revelar con evidencia cuantitativa cómo ha evolucionado la accesibilidad habitacional entre **2019 y 2024**.

---

## 2. Pregunta Central y Preguntas Derivadas

**Pregunta central:**

> ¿Cómo ha evolucionado la accesibilidad económica a la vivienda en Colombia entre 2019 y 2024, y qué variables estructurales explican mejor las diferencias entre ciudades?

**Preguntas derivadas:**

1. ¿Cuántos años de salario mínimo equivale el precio mediano de vivienda en las principales ciudades colombianas, y cómo ha cambiado esa relación en el período 2019–2024?
2. ¿Qué variables (área, ciudad, tipo de inmueble, inflación, tasa hipotecaria, desempleo) tienen mayor poder predictivo sobre el precio de una propiedad?
3. ¿Es posible clasificar objetivamente los mercados de vivienda urbana en segmentos diferenciables de accesibilidad mediante clustering no supervisado?
4. ¿En qué ciudades la cuota hipotecaria mensual supera el 30% del ingreso mínimo, comprometiendo la viabilidad financiera de los hogares?

---

## 3. Objetivos del Proyecto

**Objetivo general:**  
Desarrollar un sistema de análisis y predicción de accesibilidad habitacional en Colombia, integrando datos inmobiliarios y macroeconómicos disponibles para el período 2019–2024, con el fin de identificar patrones nacionales y diferencias espaciales de inequidad en el acceso a la vivienda.

**Objetivos específicos:**

1. Construir y validar un Índice de Accesibilidad Habitacional (IAH) para las ciudades con cobertura de datos, comparándolo con el estándar PIR de la OCDE a nivel nacional y por ciudad.
2. Entrenar y comparar modelos de regresión para predecir el precio de una propiedad con base en sus características físicas y el contexto macroeconómico del año y ciudad correspondientes.
3. Segmentar los mercados de vivienda urbana mediante clustering no supervisado para identificar grupos de ciudades con comportamientos similares de accesibilidad.
4. Desplegar los resultados en un dashboard interactivo público (Streamlit) que permita exploración a nivel nacional y por ciudad, año y tipo de inmueble, incluyendo un predictor de precio.

---

## 4. Alcance Geográfico — Estrategia Nacional + Ciudades Focales

### Nivel 1 — Análisis Nacional

El análisis de tendencias macroeconómicas (evolución del salario mínimo vs. inflación de vivienda, PIR nacional) cubre **todo el territorio colombiano** como referencia de contexto. Esto es posible porque las variables macro del DANE y BanRep son de cobertura nacional.

### Nivel 2 — Ciudades Focales

El análisis de precios, modelos predictivos y clustering se realizará sobre las ciudades con suficiente representación en los datasets. La selección sigue el marco de las **13 áreas metropolitanas del DANE** y la disponibilidad real de datos en Kaggle.

| # | Ciudad focal | Región | Tamaño | Presencia en datasets | Prioridad |
|:-:|---|---|---|:---:|:---:|
| 1 | **Bogotá D.C.** | Centro-Oriente | Metrópoli (+7M hab) | A1, A2, A3, A4, A5, A6 | Alta |
| 2 | **Medellín** | Occidente | Metrópoli (+2,5M hab) | A1, A4, A5 | Alta |
| 3 | **Cali** | Occidente | Metrópoli (+2M hab) | A1, A4 | Alta |
| 4 | **Barranquilla** | Caribe | Grande (+1,2M hab) | A1, A4 | Alta |
| 5 | **Bucaramanga** | Nororiente | Intermedia (+600K hab) | A1, A4 | Media |
| 6 | **Cartagena** | Caribe | Grande (+900K hab) | A1, A4 | Media |
| 7 | **Pereira** | Eje Cafetero | Intermedia (+450K hab) | A1, A4 | Media |
| 8 | **Cúcuta** | Nororiente | Intermedia (+700K hab) | A1 | Media |
| 9 | **Manizales** | Eje Cafetero | Intermedia (+400K hab) | A1 | Media |
| 10 | **Ibagué** | Centro-Oriente | Intermedia (+550K hab) | A1 | Baja |
| 11 | **Santa Marta** | Caribe | Intermedia (+500K hab) | A4, A5 | Baja |
| 12 | **Villavicencio** | Orinoquia | Intermedia (+500K hab) | A1, A7 (scraping) | Media |

> **Decisión metodológica:** Se incluirán en el análisis final solo las ciudades con ≥ 500 registros de vivienda en el dataset integrado. Las demás quedarán documentadas como "cobertura limitada" en el reporte de calidad de datos (Fase 2).

### Justificación de la estrategia

- **Cobertura real:** El 47% de la población colombiana vive en ciudades capitales (DANE 2023). Las 12 ciudades focales cubren más del 35% de la población nacional.
- **Contraste útil:** Incluir ciudades grandes (Bogotá, Medellín, Cali), intermedias (Pereira, Bucaramanga, Manizales) y costeras (Cartagena, Barranquilla, Santa Marta) permite responder si la crisis de accesibilidad es un fenómeno de grandes capitales o se extiende a ciudades menores.
- **Rigor académico:** El IPVU del BanRep ya cubre exactamente estas ciudades, lo que permite validación cruzada con datos oficiales.

---

## 5. Criterios de Éxito

| # | Criterio | Métrica | Umbral mínimo aceptable |
|:-:|---|---|:---:|
| 1 | Precisión del modelo de regresión | RMSE relativo (% del precio mediano) | < 15% |
| 2 | Bondad de ajuste | R² en conjunto de prueba | ≥ 0,75 |
| 3 | Calidad del clustering | Coeficiente de silueta | ≥ 0,45 |
| 4 | Separabilidad de clusters | Segmentos diferenciables | ≥ 3 |
| 5 | Cobertura geográfica | Ciudades con análisis completo | ≥ 8 ciudades |
| 6 | Cobertura temporal | Años cubiertos por los datos | 2019 – 2024 |
| 7 | Funcionalidad del dashboard | Filtros operativos implementados | Ciudad, año, tipo inmueble |
| 8 | Respuesta a preguntas de investigación | Preguntas respondidas con evidencia cuantitativa | 4 de 4 |

---

## 6. Stakeholders

| Stakeholder | Qué busca | Cómo impacta el proyecto |
|---|---|---|
| Jurado / Profesor | Rigor metodológico, claridad en la presentación, conclusiones válidas con evidencia | Determina la calificación final |
| Potencial comprador de vivienda | Saber si puede costear una vivienda en su ciudad con su ingreso actual | Define la usabilidad del dashboard y el predictor |
| Investigador / tomador de decisión pública | Identificar en qué ciudades se requiere intervención prioritaria para política de vivienda | Valida la relevancia social de los hallazgos |
| Entidad financiera / sector inmobiliario | Entender riesgo de impago hipotecario y tendencias de precios por ciudad | Valida la precisión y cobertura del modelo predictivo |

---

## 7. Supuestos y Restricciones

### Supuestos

- Los precios en los datasets de Kaggle son representativos del mercado formal de vivienda urbana en listados digitales (FincaRaiz, Properati, Metro Cuadrado).
- El salario mínimo legal mensual se usa como proxy del ingreso de referencia para hogares de bajos y medianos ingresos; no reemplaza el ingreso mediano real, pero es la serie más consistente y comparable disponible.
- Las ciudades con menos de 500 registros en el dataset integrado serán excluidas del análisis de clustering y del modelo predictivo, pero se mencionarán como limitación de cobertura.

### Restricciones

- El dataset Properati (A1) cubre hasta 2021; se complementa con los demás datasets A para los años posteriores.
- No se dispone de datos catastrales georreferenciados a nivel de predio para todas las ciudades.
- El análisis se limita a vivienda urbana; la vivienda rural queda fuera del alcance.
- Los datasets de Kaggle solo cubren vivienda en venta listada en plataformas digitales; las transacciones informales o no publicadas no están representadas.

---

## 8. Herramientas Confirmadas

| Propósito | Herramienta | Responsable | Estado |
|---|---|:---:|:---:|
| Descarga de datos Kaggle | Kaggle API (`kaggle.json`) | Steve | ✅ Confirmado |
| Notebooks interactivos | Jupyter / Google Colab | Steve | ✅ Disponible |
| Análisis y manipulación de datos | pandas, numpy | Steve | ✅ Disponible |
| Visualización exploratoria | matplotlib, seaborn, plotly | Steve | ✅ Disponible |
| Modelado supervisado | scikit-learn (Random Forest, Ridge) | Steve | ✅ Disponible |
| Modelado no supervisado | scikit-learn (KMeans, DBSCAN) | Kukis | ✅ Disponible |
| Web scraping datos vivienda | BeautifulSoup + requests | Steve / Sofía | ✅ Disponible |
| Dashboard interactivo | Streamlit | Kukis | ✅ Disponible |
| Control de versiones | GitHub (rama por fase CRISP-DM) | Sofía | ✅ Disponible |

---

## 9. Inventario de Datasets

> **Filosofía de uso:** Se emplearán **todos los datasets** identificados. En la Fase 2 (EDA) el equipo evaluará la calidad de cada uno y decidirá cuáles se integran al modelo final y cuáles se reservan para validación cruzada. No se descarta ningún dataset en Fase 1.

### Grupo A — Datasets de Precios de Vivienda

| ID | Dataset | Fuente | Tamaño | Registros aprox. | Variables | Período |
|:--:|---|---|:---:|:---:|:---:|:---:|
| **A1** | Properati Colombia | [Kaggle](https://www.kaggle.com/datasets/julianusugaortiz/colombia-housing-properties-price) | 582 MB | ~997.623 | 17 | 2020–2021 |
| **A2** | FincaRaiz Colombia | [Kaggle](https://www.kaggle.com/datasets/diegomedinaflores/properties-for-sale-in-colombia-fincaraiz) | 52 MB | ~52.000 | 28 | 2023–2024 |
| **A3** | Colombia House Prediction | [Kaggle](https://www.kaggle.com/datasets/danieleduardofajardo/colombia-house-prediction) | 27 MB | ~45.000 | 37 | 2019–2020 |
| **A4** | Real Estate Bogotá (por barrio) | [Kaggle](https://www.kaggle.com/datasets/pablobravo73/real-estate-bogota) | 892 KB | ~13.000 | 8 | 2019–2022 |
| **A5** | Medellín Properties 2023 | [Kaggle](https://www.kaggle.com/datasets/cesaregr/medelln-properties) | 879 KB | ~12.000 | 12 | 2023 |
| **A6** | Real Estate Bogotá 2023 | [Kaggle](https://www.kaggle.com/datasets/juandavsnchez/real-estatehousing-colombia-bogota) | 467 KB | ~6.500 | 8 | 2023 |
| **A7** | Scraping FincaRaiz Villavicencio | Scraping propio | 294 KB | ~2.500 | 24 | 2024 |
| **A8** | Precios vivienda nueva Bogotá (UPZ) | [Datos Abiertos Bogotá](https://datosabiertos.bogota.gov.co/dataset/vivienda) | 4 KB | 32 | 14 | 2022 |

### Grupo B — Variables Macroeconómicas

| ID | Variable | Fuente | Frecuencia | Período |
|:--:|---|---|:---:|:---:|
| **B1** | Índices de Precios de Vivienda (IPVN + IPVU) | [DANE](https://www.dane.gov.co/index.php/estadisticas-por-tema/precios-y-costos/indice-de-precios-de-la-vivienda-nueva-ipvn) + [BanRep](https://www.banrep.gov.co/es/estadisticas/precios-vivienda) | Mensual / Trimestral | 1988–2026 |
| **B2** | Tasa hipotecaria semanal | [BanRep](https://www.banrep.gov.co/es/estadisticas/tasas-interes) | Semanal | 2002–2026 |
| **B3** | Salario mínimo mensual histórico | [DANE / Mintrabajo](https://www.mintrabajo.gov.co/web/guest/salario-minimo) | Anual | 1984–2026 |
| **B4** | IPC — Variación anual | [DANE](https://www.dane.gov.co/index.php/estadisticas-por-tema/precios-y-costos/indice-de-precios-al-consumidor-ipc) | Anual | 2019–2024 |
| **B5** | GEIH — Empleo nacional y 13 ciudades | [DANE](https://www.dane.gov.co/index.php/estadisticas-por-tema/mercado-laboral/empleo-y-desempleo/geih-historicos) | Mensual | 2001–2026 |
| **B6** | Confianza constructora (QCON) | [Fedesarrollo](https://www.fedesarrollo.org.co/encuestas) | Trimestral | 2005–presente |
| **B7** | Licencias de construcción (QCON) | [Fedesarrollo](https://www.fedesarrollo.org.co/encuestas) | Trimestral | 2005–presente |
| **B8** | GEO — Estados/localidades Colombia | [IGAC / Geoportal](https://geoportal.igac.gov.co/) | — | — |

### Tabla resumen: archivos en `data/raw/` (16 CSVs)

| # | Archivo | ID | Descripción |
|:-:|---|:--:|---|
| 1 | `A1_colombia_housing_properties.csv` | A1 | Properati Colombia — fuente histórica principal (~998K registros) |
| 2 | `A2_fincaraiz_colombia.csv` | A2 | FincaRaiz Colombia 2023–2024 |
| 3 | `A3_colombia_house_prediction.csv` | A3 | Colombia House Prediction — 37 features ML |
| 4 | `A4_real_estate_bogota.csv` | A4 | Real Estate Bogotá por barrio |
| 5 | `A5_medellin_properties_2023.csv` | A5 | Medellín Properties 2023 |
| 6 | `A6_real_estate_bogota_2023.csv` | A6 | Real Estate Bogotá 2023 |
| 7 | `A7_fincaraiz_villavicencio_scraping.csv` | A7 | Scraping propio FincaRaiz Villavicencio |
| 8 | `A8_carac_pre_viv_nueva.csv` | A8 | Características precios vivienda nueva Bogotá UPZ (DANE) |
| 9 | `B1_indices_precios_vivienda.csv` | B1 | IPVN + IPVU unificado (BanRep + DANE) |
| 10 | `B2_tasa_hipotecaria_semanal.csv` | B2 | Tasa interés crédito hipotecario (BanRep) |
| 11 | `B3_salario_minimo_historico.csv` | B3 | Salario mínimo histórico (DANE) |
| 12 | `B4_ipc_colombia_anual.csv` | B4 | IPC variación anual (DANE) |
| 13 | `B5_geih_empleo_colombia.csv` | B5 | GEIH empleo mensual (DANE) |
| 14 | `B6_qcon_confianza_constructora.csv` | B6 | Confianza constructora (Fedesarrollo) |
| 15 | `B7_qcon_licencias_construccion.csv` | B7 | Licencias de construcción (Fedesarrollo) |
| 16 | `B8_geo_estados_localidades.csv` | B8 | Estados/localidades geográficas Colombia (IGAC) |

**Total: 16 archivos CSV**

---

## 10. Riesgos Identificados y Mitigaciones

| # | Riesgo | Probabilidad | Impacto | Mitigación |
|:-:|---|:---:|:---:|---|
| R1 | Datos incompletos (valores nulos en precio, área, ciudad) | Alta | Medio | Imputación y filtros en Fase 3; documentar tasa de missings por dataset |
| R2 | Esquemas de columnas diferentes entre datasets | Alta | Alto | Fase 3 define esquema canónico; script de mapeo de columnas por dataset |
| R3 | Duplicados entre datasets (mismo inmueble en A1 y A2) | Media | Medio | Deduplicación por hash de (ciudad, precio, área, tipo); registrar eliminados |
| R4 | Series temporales macroeconómicas desalineadas con precios | Media | Alto | Resampleo a frecuencia anual; interpolación lineal donde sea válido |
| R5 | Multicolinealidad entre variables macro (IPC, tasa hipotecaria) | Media | Medio | Calcular VIF; usar `feature_importances_` para selección de features |
| R6 | Ciudades intermedias con < 500 registros tras limpieza | Media | Medio | Documentar como limitación; excluir del modelo pero incluir en análisis descriptivo. Villavicencio reforzado con scraping A7 |
| R7 | Clusters no diferenciables (silueta < 0,45) | Baja | Alto | Probar KMeans, DBSCAN y clustering jerárquico; variar número de features |
| R8 | Dataset A1 (~997K registros) requiere ~2 GB en memoria | Alta | Bajo | Carga con tipos optimizados (`dtypes`); procesamiento por chunks si es necesario |
| R9 | Dashboard lento con dataset grande | Media | Bajo | Usar datos agregados (mediana por ciudad/año); caché de Streamlit |

---

## 11. Cronograma General del Proyecto

| Semana | Actividad | Responsable |
|:---:|---|:---:|
| 1–2 | **Fase 1:** Comprensión del negocio. Documento de planificación aprobado. | Steve |
| 3–4 | **Fase 2:** Descarga de los 16 archivos, EDA inicial, reporte de calidad por dataset. | Sofía |
| 5–6 | **Fase 3:** Normalización de esquemas, deduplicación, integración y construcción del IAH. | Kukis |
| 7–8 | **Fase 4:** Entrenamiento de modelos de regresión y clustering. | Steve |
| 9 | **Fase 5:** Evaluación, gráficas de residuos, conclusiones cuantitativas. | Sofía |
| 10–11 | **Fase 6:** Dashboard Streamlit con vistas nacional y por ciudad. Despliegue URL pública. | Kukis |
| 12 | Preparación de presentación final. Ensayo general. | Todos |
| 13 | **Presentación final ante jurado.** | Todos |

---

## 12. Checklist de Cierre — Fase 1

### Entregables de contenido

- [x] **Contexto y justificación** — incluye cifras reales de déficit habitacional, PIR, datos DANE
- [x] **Pregunta central** (1) + **4 preguntas derivadas** — específicas, medibles, relevantes
- [x] **Objetivo general** (1) + **4 objetivos específicos** — redacción evaluable por el jurado
- [x] **Criterios de éxito** (8) — cada uno con métrica y umbral numérico concreto
- [x] **Alcance geográfico definido** — análisis nacional + 12 ciudades focales con justificación
- [x] **Tabla de stakeholders** (4) — con interés y modo de impacto
- [x] **Supuestos y restricciones** — documentados explícitamente

### Herramientas y entorno

- [x] Python + Jupyter/Colab confirmados (Steve)
- [x] pandas, numpy, matplotlib, seaborn, plotly disponibles
- [x] scikit-learn disponible (Random Forest, Ridge, KMeans, DBSCAN)
- [x] Streamlit disponible (Kukis)
- [x] GitHub con repositorio creado y estructura de ramas por fase (Sofía)
- [x] Cuenta Kaggle de Steve activa — token `kaggle.json` configurado

### Fuentes de datos — links verificados

**Grupo A — Datasets de precios:**

- [x] A1 — Properati Colombia — [Kaggle](https://www.kaggle.com/datasets/julianusugaortiz/colombia-housing-properties-price)
- [x] A2 — FincaRaiz Colombia 2023–2024 — [Kaggle](https://www.kaggle.com/datasets/diegomedinaflores/properties-for-sale-in-colombia-fincaraiz)
- [x] A3 — Colombia House Prediction — [Kaggle](https://www.kaggle.com/datasets/danieleduardofajardo/colombia-house-prediction)
- [x] A4 — Real Estate Bogotá — [Kaggle](https://www.kaggle.com/datasets/pablobravo73/real-estate-bogota)
- [x] A5 — Medellín Properties 2023 — [Kaggle](https://www.kaggle.com/datasets/cesaregr/medelln-properties)
- [x] A6 — Real Estate Bogotá 2023 — [Kaggle](https://www.kaggle.com/datasets/juandavsnchez/real-estatehousing-colombia-bogota)
- [x] A7 — Scraping FincaRaiz Villavicencio (propio)
- [x] A8 — Características precios vivienda nueva Bogotá UPZ — [Datos Abiertos](https://datosabiertos.bogota.gov.co/dataset/vivienda)

**Grupo B — Variables macroeconómicas:**

- [x] B1 — IPVN + IPVU unificado — [DANE](https://www.dane.gov.co/index.php/estadisticas-por-tema/precios-y-costos/indice-de-precios-de-la-vivienda-nueva-ipvn) + [BanRep](https://www.banrep.gov.co/es/estadisticas/precios-vivienda)
- [x] B2 — Tasa hipotecaria semanal BanRep — [BanRep](https://www.banrep.gov.co/es/estadisticas/tasas-interes)
- [x] B3 — Salario mínimo histórico DANE — [Mintrabajo](https://www.mintrabajo.gov.co/web/guest/salario-minimo)
- [x] B4 — IPC variación anual DANE — [DANE](https://www.dane.gov.co/index.php/estadisticas-por-tema/precios-y-costos/indice-de-precios-al-consumidor-ipc)
- [x] B5 — GEIH empleo mensual nacional + 13 ciudades — [DANE](https://www.dane.gov.co/index.php/estadisticas-por-tema/mercado-laboral/empleo-y-desempleo/geih-historicos)
- [x] B6 — Confianza constructora Fedesarrollo — [Fedesarrollo](https://www.fedesarrollo.org.co/encuestas)
- [x] B7 — Licencias construcción Fedesarrollo — [Fedesarrollo](https://www.fedesarrollo.org.co/encuestas)
- [x] B8 — GEO estados/localidades Colombia — [IGAC](https://geoportal.igac.gov.co/)

### Riesgos

- [x] 9 riesgos identificados con probabilidad, impacto y mitigación concreta
- [ ] Riesgos revisados y aprobados por todo el equipo en sesión conjunta

### Documento final

- [x] Cronograma completo (Fases 1–6 + presentación) con responsables y semanas
- [x] Documento integrado en un solo `.md`
- [ ] **Revisión y visto bueno del profesor/jurado** — pendiente entrega Semana 2

---

*Documento de Fase 1 · CRISP-DM 2025-I · Proyecto Accesibilidad Habitacional Colombia — 2019–2024*  
*Equipo: Steve · Sofía · Kukis*
