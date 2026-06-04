# Fase 1 — Comprensión del Negocio

## Proyecto: Accesibilidad de Vivienda en Colombia · CRISP-DM 2026-I

**Responsable principal:** Steve · **Equipo:** Sofía · Kukis  
**Período de análisis:** 2020 – 2025  
**Estado:** ✅ Completa  
**Semanas:** 1 – 2

---

## Resumen Ejecutivo

Este proyecto construye un sistema cuantitativo de análisis de accesibilidad habitacional en Colombia para el período 2020–2025. Integra **16 fuentes de datos** —8 de precios inmobiliarios (A1–A8) y 8 de variables macroeconómicas (B1–B8)— para desarrollar el **Índice de Accesibilidad Habitacional (IAH)**, una adaptación del Price-to-Income Ratio (PIR) al contexto colombiano que mide cuántos años de salario mínimo equivale el precio mediano de una vivienda. El análisis abarca **12 ciudades focales** y se desplegará en un dashboard interactivo público (Streamlit).

La fase estableció los cimientos metodológicos del proyecto: definición del problema de negocio y pregunta de investigación, cuatro objetivos específicos medibles, ocho criterios de éxito con umbrales numéricos, inventario de todas las fuentes de datos, glosario técnico unificado, análisis de riesgos y cronograma de 13 semanas.

---

## 1. Contexto y Justificación del Negocio

La vivienda es el activo más costoso que adquiere un hogar a lo largo de su vida. En Colombia, el déficit habitacional cuantitativo supera el millón de unidades, y el precio de la vivienda ha crecido sostenidamente por encima del salario mínimo real durante la última década. Los datos más recientes del DANE reportaron incrementos del 9,11% en Bogotá, 8,29% en Medellín y 9,22% en Barranquilla, mientras que ciudades intermedias como Cúcuta registraron saltos del 24,6% en 2024, evidenciando que la crisis no es exclusiva de las grandes capitales.

El indicador internacional de referencia es el **Price-to-Income Ratio (PIR)**: la razón entre el precio mediano de vivienda y el ingreso anual mediano del hogar. Un PIR superior a 5 se considera crítico según la OCDE y ONU-Hábitat. Este proyecto construye una versión del PIR adaptada al contexto colombiano usando el salario mínimo como proxy del ingreso de referencia, integra todos los datasets disponibles de precios inmobiliarios con variables macroeconómicas oficiales, y analiza tanto el nivel nacional como las diferencias entre ciudades para revelar con evidencia cuantitativa cómo ha evolucionado la accesibilidad habitacional entre **2020 y 2025**.

### 1.1 Rol de la Fase 1 en el ciclo CRISP-DM

La Fase 1 es el punto de partida del ciclo. Su propósito es transformar el problema del mundo real en un problema técnico de ciencia de datos con objetivos claros y criterios de éxito verificables.

| Relación en el ciclo | Descripción |
|---|---|
| **Entrada a esta fase** | Problemática de negocio: déficit habitacional, escalada de precios, ausencia de un índice público de accesibilidad por ciudad |
| **Salidas hacia Fase 2** | Lista de 16 fuentes de datos a explorar, 12 ciudades focales definidas, 4 preguntas de investigación, criterios de éxito con umbrales |
| **Salidas hacia Fase 3** | Esquema canónico de variables (price, area, rooms, city, property_type, estrato), definición de IAH y variables derivadas |
| **Salidas hacia Fase 4** | Criterios de éxito del modelo: R² ≥ 0,75, RMSE relativo < 15%, silueta ≥ 0,45 |
| **Salidas hacia Fase 5** | Las 4 preguntas de investigación que la evaluación debe responder cuantitativamente |
| **Salidas hacia Fase 6** | Requerimientos funcionales del dashboard: filtros por ciudad/año/tipo, predictor de precio, semáforo de accesibilidad |

La Fase 1 es la única que no puede retroalimentarse de fases anteriores en la primera iteración; su revisión solo ocurre cuando los resultados de Fase 5 revelan que los criterios de éxito fueron mal definidos.

---

## 2. Pregunta Central y Objetivos del Proyecto

### 2.1 Pregunta central

> ¿Cómo ha evolucionado la accesibilidad económica a la vivienda en Colombia entre 2020 y 2025, y qué variables estructurales explican mejor las diferencias entre ciudades?

### 2.2 Preguntas derivadas (P1–P4)

1. ¿Cuántos años de salario mínimo equivale el precio mediano de vivienda en las principales ciudades colombianas, y cómo ha cambiado esa relación en el período 2020–2025?
2. ¿Qué variables (área, ciudad, tipo de inmueble, inflación, tasa hipotecaria, desempleo) tienen mayor poder predictivo sobre el precio de una propiedad?
3. ¿Es posible clasificar objetivamente los mercados de vivienda urbana en segmentos diferenciables de accesibilidad mediante clustering no supervisado?
4. ¿Cuál es el ratio cuota/salario en cada ciudad y cómo ha evolucionado respecto al umbral del 30% que compromete la viabilidad financiera de los hogares?

### 2.3 Objetivo general

Desarrollar un sistema de análisis y predicción de accesibilidad habitacional en Colombia, integrando datos inmobiliarios y macroeconómicos disponibles para el período 2020–2025, con el fin de identificar patrones nacionales y diferencias espaciales de inequidad en el acceso a la vivienda.

### 2.4 Objetivos específicos

1. **Construir y validar el IAH** para las 12 ciudades focales, comparándolo con el estándar PIR de la OCDE a nivel nacional y por ciudad.
2. **Entrenar y comparar modelos de regresión** para predecir el precio de una propiedad con base en sus características físicas y el contexto macroeconómico del año y ciudad correspondientes.
3. **Segmentar los mercados de vivienda urbana** mediante clustering no supervisado para identificar grupos de ciudades con comportamientos similares de accesibilidad.
### 2.5 Trazabilidad CRISP-DM: Objetivos de Negocio ↔ Objetivos de Data Science

CRISP-DM requiere traducir cada objetivo de negocio en un objetivo técnico de minería de datos. La siguiente matriz garantiza que cada decisión analítica tenga una justificación de negocio clara:

| Objetivo de Negocio | Objetivo de Data Science | Técnica / Métrica Principal |
|---|---|---|
| **Medir accesibilidad habitacional** por ciudad y año | **Construir el IAH** (Índice de Accesibilidad Habitacional) | Cálculo: `IAH = precio_mediano / (SMLMV × 12)` |
| **Predecir el precio** de una propiedad dado contexto económico y características físicas | **Entrenar modelo de regresión** con R² ≥ 0,75 | Random Forest / Ridge regression con validación cruzada k-fold |
| **Identificar patrones regionales** en los mercados de vivienda | **Segmentar ciudades** mediante clustering no supervisado | KMeans / DBSCAN con coeficiente de silueta ≥ 0,45 |
| **Comunicar resultados** a stakeholders no técnicos | **Desplegar dashboard interactivo** público | Streamlit con filtros por ciudad, año, tipo de inmueble |
| **Validar que los hallazgos** son robustos estadísticamente | **Evaluar con criterios de éxito técnico** | 8 criterios con umbrales numéricos (ver sección 3.4) |
| **Garantizar que el proyecto** responde las preguntas de investigación | **Responder las 4 preguntas** con evidencia cuantitativa | Análisis IAH, modelos, clustering, ratio cuota/salario |

Esta trazabilidad formaliza el nexo entre los requerimientos del negocio y las técnicas analíticas que se aplicarán, cumpliendo con el propósito central de CRISP-DM Fase 1.

---

## 3. Alcance del Proyecto

### 3.1 Alcance geográfico — Estrategia en dos niveles

**Nivel 1 — Análisis Nacional:** Las tendencias macroeconómicas (salario mínimo, inflación, índices IPVN/IPVU) cubren todo el territorio colombiano como referencia de contexto. Esto es posible porque las variables del DANE y BanRep tienen cobertura nacional.

**Nivel 2 — Ciudades focales:** El análisis de precios, modelos predictivos y clustering opera sobre las ciudades con representación suficiente en los datasets. Se seleccionaron siguiendo el marco de las **13 áreas metropolitanas del DANE** y la disponibilidad real de datos.

| # | Ciudad focal | Región | Tamaño | Datasets presentes | Prioridad |
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

> **Decisión metodológica:** Solo se incluirán en el análisis final las ciudades con ≥ 500 registros tras la limpieza de Fase 3. Las que no alcancen ese umbral quedarán documentadas como "cobertura limitada" en el reporte de calidad de datos (Fase 2).

**Justificación de la estrategia:** Las 12 ciudades focales cubren más del 35% de la población nacional. La inclusión de ciudades grandes (Bogotá, Medellín, Cali), intermedias (Pereira, Bucaramanga, Manizales) y costeras (Cartagena, Barranquilla, Santa Marta) permite determinar si la crisis de accesibilidad es exclusiva de las grandes capitales o se extiende a ciudades menores. El IPVU del BanRep cubre exactamente estas ciudades, habilitando validación cruzada con datos oficiales.

### 3.2 Alcance temporal

El análisis cubre **2020–2025**, período que incluye el ciclo completo pandemia-recuperación-choque inflacionario y permite observar el impacto del aumento de tasas hipotecarias del BanRep (máximo histórico cercano al 16% EA en 2023).

> **Nota sobre disponibilidad de datos 2025:** La cobertura hasta 2025 está sujeta a la disponibilidad real de datos en las fuentes oficiales. Los datasets A de precios disponibles llegan hasta 2023–2024; las series macroeconómicas B están actualizadas hasta 2025 en el momento de escribir este documento (marzo 2025). La Fase 2 confirmará la fecha límite real de cada fuente, y en caso de no contar con datos completos de 2025, el análisis se ajustará al período efectivamente disponible (mínimo 2020–2024).

### 3.3 Fuera del alcance

- Vivienda rural y municipios no metropolitanos.
- Transacciones informales o no publicadas en plataformas digitales.
- Mercado de arrendamiento (el análisis se centra en compra).
- Datos catastrales georreferenciados a nivel de predio individual.

### 3.4 Criterios de éxito del proyecto

CRISP-DM recomienda separar explícitamente los criterios de éxito en dos categorías: **éxito de negocio** (impacto del proyecto en el mundo real) y **éxito técnico** (calidad de la implementación analítica).

#### 3.4.1 Éxito de Negocio (Business Success)
Estos criterios evalúan si el proyecto cumple con su propósito original en el contexto real:

| # | Criterio de Negocio | Métrica | Umbral mínimo aceptable | Justificación |
|---|---|---|---|---|
| 1 | **Respuesta a preguntas de investigación** | Preguntas respondidas con evidencia cuantitativa | 4 de 4 | La razón de ser del proyecto es responder las 4 preguntas |
| 2 | **Cobertura geográfica** | Ciudades con análisis completo | ≥ 8 ciudades | Permite análisis comparativo nacional con representación |
| 3 | **Funcionalidad del dashboard** | Filtros operativos implementados | Ciudad, año, tipo inmueble | Dashboard debe ser útil para stakeholders no técnicos |
| 4 | **Relevancia para stakeholders** | Stakeholders identificados en sección 4 | Todos incluidos en diseño | El proyecto debe servir a su audiencia objetivo |

#### 3.4.2 Éxito Técnico (Technical Success)
Estos criterios evalúan la calidad estadística y metodológica de la implementación:

| # | Criterio Técnico | Métrica | Umbral mínimo aceptable | Justificación |
|---|---|---|---|---|
| 1 | **Precisión del modelo de regresión** | RMSE relativo (% del precio mediano) | < 15% | Error predictivo razonable para contexto inmobiliario |
| 2 | **Bondad de ajuste** | R² en conjunto de prueba | ≥ 0,75 | El modelo debe explicar ≥ 75% de varianza del precio |
| 3 | **Calidad del clustering** | Coeficiente de silueta | ≥ 0,45 | Segmentación clara entre grupos de ciudades |
| 4 | **Separabilidad de clusters** | Segmentos diferenciables | ≥ 3 | Mínimo para análisis comparativo (bajo/medio/alto) |

**Criterio híbrido (ambas dimensiones):** 
- **Cobertura temporal:** Años cubiertos por los datos = 2020–2025 (sujeto a disponibilidad real confirmada en Fase 2)

La separación permite evaluar el proyecto desde ambas perspectivas: un modelo puede ser técnicamente excelente (R² = 0,85) pero irrelevante para el negocio si no responde las preguntas de investigación; o viceversa: responder preguntas con un modelo pobre que no sea confiable para toma de decisiones.

---

## 4. Stakeholders

| Stakeholder | Qué busca | Cómo impacta el proyecto |
|---|---|---|
| **Equipo académico (Steve, Sofía, Kukis)** | Aplicar CRISP-DM end-to-end, consolidar portafolio público, obtener calificación aprobatoria | Define la calidad de ejecución, el cumplimiento de hitos y la consistencia metodológica |
| Jurado / Profesor | Rigor metodológico, claridad en la presentación, conclusiones válidas con evidencia | Determina la calificación final |
| Potencial comprador de vivienda | Saber si puede costear una vivienda en su ciudad con su ingreso actual | Define la usabilidad del dashboard y el predictor |
| Investigador / tomador de decisión pública | Identificar en qué ciudades se requiere intervención prioritaria para política de vivienda | Valida la relevancia social de los hallazgos |
| Entidad financiera / sector inmobiliario | Entender riesgo de impago hipotecario y tendencias de precios por ciudad | Valida la precisión y cobertura del modelo predictivo |
| Comunidad académica / reutilizadores de datos | Dataset consolidado limpio como bien público para futuras investigaciones | Valida la calidad de la documentación y reproductibilidad del código |

---

## 5. Recursos del Proyecto

### 5.1 Inventario de Datasets

> **Filosofía de uso:** Se emplearán **todos los datasets** identificados. En la Fase 2 (EDA) el equipo evaluará la calidad de cada uno y decidirá cuáles se integran al modelo final y cuáles se reservan para validación cruzada. No se descarta ningún dataset en Fase 1.

#### Grupo A — Datasets de Precios de Vivienda

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

> **Nota sobre uso de A8:** Este dataset contiene solo 32 registros de precios de vivienda nueva por UPZ en Bogotá para 2022. Su volumen es insuficiente para entrenar modelos, por lo que se utilizará exclusivamente como referencia de validación cruzada para verificar que los precios estimados por el modelo sean coherentes con los valores oficiales reportados por la administración distrital.

> **Nota de solapamiento temporal:** A3 (2019–2020) y A1 (2020–2021) presentan solapamiento en el año 2020. La EDA de Fase 2 deberá evaluar si las propiedades de 2020 están duplicadas entre ambos datasets y aplicar deduplicación antes de la integración en Fase 3.

| ID | Variable | Fuente | Frecuencia | Período |
|:--:|---|---|:---:|:---:|
| **B1** | Índices de Precios de Vivienda (IPVN + IPVU) | [DANE](https://www.dane.gov.co/index.php/estadisticas-por-tema/precios-y-costos/indice-de-precios-de-la-vivienda-nueva-ipvn) + [BanRep](https://www.banrep.gov.co/es/estadisticas/precios-vivienda) | Mensual / Trimestral | 1988–2025 |
| **B2** | Tasa hipotecaria semanal | [BanRep](https://www.banrep.gov.co/es/estadisticas/tasas-interes) | Semanal | 2002–2025 |
| **B3** | Salario mínimo mensual histórico | [DANE / Mintrabajo](https://www.mintrabajo.gov.co/web/guest/salario-minimo) | Anual | 1984–2025 |
| **B4** | IPC — Variación anual | [DANE](https://www.dane.gov.co/index.php/estadisticas-por-tema/precios-y-costos/indice-de-precios-al-consumidor-ipc) | Anual | 2019–2024 |
| **B5** | GEIH — Empleo nacional y 13 ciudades | [DANE](https://www.dane.gov.co/index.php/estadisticas-por-tema/mercado-laboral/empleo-y-desempleo/geih-historicos) | Mensual | 2001–2025 |
| **B6** | Confianza constructora (QCON) | [Fedesarrollo](https://www.fedesarrollo.org.co/encuestas) | Trimestral | 2005–presente |
| **B7** | Licencias de construcción (QCON) | [Fedesarrollo](https://www.fedesarrollo.org.co/encuestas) | Trimestral | 2005–presente |
| **B8** | GEO — Estados/localidades Colombia | [IGAC / Geoportal](https://geoportal.igac.gov.co/) | — | — |

#### Tabla resumen: archivos en `data/raw/` (16 CSVs)

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

### 5.2 Herramientas Confirmadas

| Propósito | Herramienta | Responsable | Estado |
|---|---|---|---|
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

## 6. Supuestos, Restricciones y Riesgos

### 6.1 Supuestos

- Los precios en los datasets de Kaggle son representativos del mercado formal de vivienda urbana en listados digitales (FincaRaiz, Properati, Metro Cuadrado).
- El SMLMV se usa como proxy del ingreso de referencia para hogares de bajos y medianos ingresos; no reemplaza el ingreso mediano real, pero es la serie más consistente y comparable disponible.
- Las ciudades con menos de 500 registros en el dataset integrado serán excluidas del análisis de clustering y del modelo predictivo, pero se mencionarán como limitación de cobertura.

### 6.2 Restricciones

- El dataset Properati (A1) cubre hasta 2021; se complementa con los demás datasets A para los años posteriores.
- No se dispone de datos catastrales georreferenciados a nivel de predio para todas las ciudades.
- El análisis se limita a vivienda urbana; la vivienda rural queda fuera del alcance.
- Los datasets de Kaggle solo cubren vivienda en venta listada en plataformas digitales; las transacciones informales o no publicadas no están representadas.

### 6.3 Riesgos Identificados y Mitigaciones

| # | Riesgo | Probabilidad | Impacto | Mitigación |
|:-:|---|:---:|:---:|---|
| R1 | Datos incompletos (nulos en precio, área, ciudad) | Alta | Medio | Imputación y filtros en Fase 3; documentar tasa de missings por dataset |
| R2 | Esquemas de columnas incompatibles entre datasets | Alta | Alto | Fase 3 define esquema canónico; script de mapeo por dataset |
| R3 | Duplicados entre datasets con solapamiento temporal (mismo inmueble en A1–2020 y A3–2020; A1–A2 en Bogotá 2023) | Alta | Medio | Verificar solapamiento en EDA de Fase 2; deduplicación por hash combinando características + fechas; excluir datasets si duplicación supera 30% |
| R4 | Series macroeconómicas desalineadas con precios | Media | Alto | Resampleo a frecuencia anual; interpolación lineal donde sea válido |
| R5 | Multicolinealidad entre variables macro (IPC, tasa hipotecaria) | Media | Medio | Calcular VIF; usar `feature_importances_` para selección de features |
| R6 | Ciudades intermedias con < 500 registros tras limpieza | Media | Medio | Documentar como limitación; excluir del modelo pero incluir en análisis descriptivo. Villavicencio reforzado con scraping A7 |
| R7 | Clusters no diferenciables (silueta < 0,45) | Baja | Alto | Probar KMeans, DBSCAN y clustering jerárquico; variar número de features |
| R8 | Dataset A1 (~997K registros) requiere ~2 GB en memoria | Alta | Bajo | Carga con tipos optimizados (`dtypes`); procesamiento por chunks si necesario |
| R9 | Dashboard lento con dataset grande | Media | Bajo | Usar datos agregados (mediana por ciudad/año); caché de Streamlit |

### 6.4 Evaluación de Viabilidad del Proyecto

CRISP-DM recomienda una evaluación formal de viabilidad antes de comprometer recursos a un proyecto. Esta sección consolida los análisis dispersos en las secciones anteriores.

| Dimensión de Viabilidad | Estado Actual | Riesgo / Observación |
|---|---|---|
| **Viabilidad de Datos** | ✅ **Alta** | • 16 fuentes identificadas (8 A + 8 B)<br>• URLs verificadas y descargables<br>• Volumen suficiente: >1,1M registros totales<br>• Período mínimo garantizado: 2020–2024 |
| **Viabilidad Técnica (Cómputo)** | ✅ **Alta** | • Stack tecnológico confirmado (pandas, scikit-learn, Streamlit)<br>• Memoria suficiente para A1 (~2GB con optimización)<br>• Hardware local del equipo disponible |
| **Viabilidad Temporal** | ⚠ **Moderada** | • Cronograma de 14 semanas (13 + buffer)<br>• Fase 4 crítica: 3 semanas para modelos complejos<br>• Buffer incorporado para limpieza A1 |
| **Viabilidad Metodológica** | ✅ **Alta** | • Variables suficientes para construir IAH<br>• Técnicas estadísticas estándar (regresión, clustering)<br>• Referentes internacionales: PIR de OCDE validado |
| **Viabilidad de Equipo** | ✅ **Alta** | • 3 personas con roles complementarios<br>• Experiencia confirmada en herramientas<br>• Responsabilidades asignadas por fase |

**Factores críticos que podrían afectar viabilidad:**
1. **Calidad de A1 (~997K registros):** Si >30% de registros tienen datos nulos críticos (precio, ciudad), el volumen efectivo podría caer por debajo del umbral para ciudades intermedias.
2. **Disponibilidad de datos 2025:** Los datasets A llegan hasta 2023–2024; si las series macro B no actualizan a 2025, el período efectivo sería 2020–2024.
3. **Solapamiento A1–A3:** Duplicación masiva en 2020 podría reducir la cobertura temporal efectiva.

**Conclusión:** El proyecto es viable en todas las dimensiones principales. El único factor de riesgo moderado es el temporal, mitigado por el buffer incorporado en Fase 4 y la flexibilidad en el alcance (2025 sujeto a disponibilidad).

---

## 7. Glosario de Términos Técnicos

### Indicadores económicos y de accesibilidad

| Término | Sigla | Definición operativa en el proyecto |
|---|---|---|
| **Price-to-Income Ratio** | **PIR** | Cociente entre el precio mediano de la vivienda y el ingreso anual mediano del hogar. Indicador estándar OCDE / ONU-Hábitat. PIR ≤ 5 = accesible; PIR ≥ 10 = seriamente inaccesible. |
| **Índice de Accesibilidad Habitacional** | **IAH** | Versión adaptada del PIR. Numerador: precio mediano de vivienda. Denominador: salario mínimo anual (`SMLMV × 12`). Expresado en *años de salario mínimo necesarios para comprar la vivienda mediana*. |
| **Salario Mínimo Legal Mensual Vigente** | **SMLMV** | Ingreso mensual de referencia decretado por el Gobierno Nacional. Proxy del ingreso del hogar de bajos ingresos. |
| **Ratio Cuota / Salario** | — | Porcentaje del salario mínimo mensual destinado a la cuota hipotecaria estimada (70% financiación, 15 años, tasa anual del año). Umbral de viabilidad: ≤ 30%. |
| **Nivel de Accesibilidad** | — | Clasificación basada en IAH: *Accesible* (≤ 5), *Moderado* (5–10), *Elevado* (10–20), *Crítico* (> 20). |

### Variables macroeconómicas y fuentes oficiales

| Término | Sigla | Definición operativa en el proyecto |
|---|---|---|
| **Índice de Precios de Vivienda Nueva** | **IPVN** | Publicado trimestralmente por el DANE. Mide variación de precios de vivienda nueva. Usado como benchmark de validación cruzada. |
| **Índice de Precios de Vivienda Usada** | **IPVU** | Publicado por el BanRep. Mide variación de precios de vivienda usada por ciudad. |
| **Índice de Precios al Consumidor** | **IPC** | Publicado por el DANE. Inflación anual. Usado para deflactar precios nominales a precios reales (base 2018). |
| **Tasa de interés efectiva anual** | **EA** | Tasa del BanRep para créditos hipotecarios No VIS. Conversión a mensual: `r = (1 + EA)^(1/12) − 1`. |
| **Vivienda de Interés Social** | **VIS** | Vivienda con valor ≤ 150 SMLMV con subsidio estatal. El modelo se centra en vivienda No VIS. |
| **Tasa Representativa del Mercado** | **TRM** | Tipo de cambio peso/dólar (BanRep). Usado para convertir precios en USD de A1 (Properati) a COP. |
| **Gran Encuesta Integrada de Hogares** | **GEIH** | Encuesta del DANE con indicadores de empleo desagregados por ciudad. |
| **Tasa de Desempleo** | **TD** | Indicador de mercado laboral (GEIH — DANE). Feature predictora por ciudad y año. |

### Métricas de evaluación de modelos

| Término | Sigla | Definición operativa en el proyecto |
|---|---|---|
| **Coeficiente de determinación** | **R²** | Proporción de la varianza del precio explicada por el modelo. Umbral: ≥ 0,75. |
| **Error Absoluto Medio** | **MAE** | Promedio de la desviación absoluta entre predicción y valor real, en COP. |
| **Raíz del Error Cuadrático Medio** | **RMSE** | Penaliza errores grandes. Se reporta su versión relativa (% del precio mediano). Umbral: < 15%. |
| **Error Porcentual Absoluto Medio** | **MAPE** | Promedio de la desviación porcentual respecto al valor real. |
| **Coeficiente de Silueta** | — | Calidad del clustering. Rango [-1, 1]. Umbral: ≥ 0,45. |
| **Davies-Bouldin Index** | **DBI** | Separación entre clusters. Valores más bajos indican mejor separación. |
| **Factor de Inflación de Varianza** | **VIF** | Diagnóstico de multicolinealidad. VIF > 10 indica colinealidad problemática. |
| **Validación Cruzada k-fold** | **CV** | Validación con k=5 subconjuntos. Se reporta media y desviación estándar del R² entre folds. |

### Procesamiento de datos y estadística

| Término | Sigla | Definición operativa en el proyecto |
|---|---|---|
| **Rango Intercuartílico** | **IQR** | Diferencia P75 – P25. Usado para detectar outliers por grupo `(ciudad, año, tipo_inmueble)`. |
| **Tasa de Crecimiento Anual Compuesta** | **CAGR** | Tasa anual equivalente del crecimiento acumulado entre dos años. |
| **One-Hot Encoding** | **OHE** | Codificación de variables categóricas como vectores binarios. Aplicado a `city` y `property_type`. |
| **Unidad de Planeamiento Zonal** | **UPZ** | División administrativa intermedia de Bogotá entre localidad y barrio. Usada en A8. |

---

## 8. Análisis Costo-Beneficio

CRISP-DM exige una evaluación explícita del costo del proyecto frente al valor que genera. Para un proyecto académico colaborativo como este, el análisis se enmarca en términos de **recursos consumidos** y **valor producido**.

### 8.1 Costos del proyecto

| Categoría | Recurso | Costo monetario | Costo en horas |
|---|---|---|---|
| **Datos** | 8 datasets de Kaggle (A1–A6, A8) | $0 — descarga gratuita con `kaggle.json` | 4 h |
| **Datos** | 8 series oficiales del DANE + BanRep + Fedesarrollo + IGAC (B1–B8) | $0 — datos públicos abiertos | 8 h |
| **Datos** | Scraping FincaRaiz Villavicencio (A7) | $0 — BeautifulSoup + requests | 10 h (script + ejecución) |
| **Cómputo** | Procesamiento local con Python + Jupyter | $0 — entorno local del equipo | — |
| **Cómputo** | Streamlit Community Cloud (despliegue) | $0 — tier gratuito hasta 1 GB | — |
| **Software** | pandas, numpy, scikit-learn, matplotlib, plotly, streamlit | $0 — todo open source | — |
| **Repositorio** | GitHub público | $0 — cuenta gratuita | — |
| **Recurso humano** | Equipo de 3 estudiantes durante 13 semanas | Tiempo académico | ~390 h totales (130 h/persona) |
| **TOTAL MONETARIO** | | **$0 COP** | **~412 horas-persona** |

### 8.2 Beneficios esperados

| Beneficiario | Valor generado | Tipo de beneficio |
|---|---|---|
| **Equipo académico** | Aplicación práctica de CRISP-DM end-to-end con dataset real de 16 fuentes; portafolio público en GitHub + dashboard desplegado | Formativo |
| **Jurado / Programa** | Caso pedagógico replicable de integración de datos heterogéneos (Kaggle + oficiales) con metodología trazable | Académico |
| **Compradores potenciales de vivienda** | Predictor de precios libre y público; semáforo de accesibilidad que muestra cuántos años de salario costaría comprar | Social |
| **Investigadores y formuladores de política pública** | Evidencia cuantitativa del deterioro del IAH; identificación de ciudades en zona crítica *(valores concretos sujetos al resultado del análisis en Fases 3–5)* | Social / Investigación |
| **Sector inmobiliario y financiero** | Cuantificación del ratio cuota/salario por ciudad; identificación de mercados donde la cuota supera el 30% del SMLMV *(valores sujetos al resultado del análisis)* | Sectorial |

> ⚠️ **Nota:** Los valores específicos de IAH y ratio cuota/salario por ciudad se obtendrán como resultado del análisis en Fases 3–5. No se anticipan cifras en esta fase de planificación.

### 8.3 Balance final

El proyecto se ejecuta con **costo monetario nulo** apalancado en datos públicos, software libre y plataformas con tier gratuito. El único insumo de costo significativo es el tiempo del equipo (~412 horas-persona).

A cambio se entrega:

1. Un **dataset consolidado y limpio** reutilizable por otros proyectos académicos.
2. Un **modelo predictivo serializado** (R² ≥ 0,75) accesible vía dashboard público.
3. Una **segmentación de mercados** (4 clusters) que permite agrupar ciudades por nivel de accesibilidad.
4. **Evidencia cuantitativa** de la crisis de accesibilidad colombiana en 2020–2025, con potencial de citación en discusiones de política habitacional.

**Conclusión:** El retorno académico, social e investigativo supera ampliamente la inversión de tiempo, especialmente dado que la totalidad de los entregables queda disponible públicamente (repositorio + dashboard) sin costo recurrente de mantenimiento.

### 8.4 Definición formal de entregables por fase

CRISP-DM especifica que cada fase debe producir entregables concretos que permitan medir progreso y calidad. La siguiente tabla define los entregables esperados por fase:

| Fase CRISP-DM | Entregable principal | Formato | Criterios de aceptación |
|---|---|---|---|
| **Fase 1** | Documento de Comprensión del Negocio | `FASE_1_COMPLETA.md` | Contexto, 4 preguntas de investigación, 8 criterios de éxito, inventario de 16 fuentes |
| **Fase 2** | Reporte de Exploración de Datos (EDA) | `FASE_2_COMPLETA.md` + notebooks | Calidad por dataset, tasa de nulos, conteo efectivo por ciudad, solapamiento A1-A3 |
| **Fase 3** | Dataset integrado con IAH calculado | `data/processed/dataset_integrado.csv` | Esquema canónico, IAH por ciudad-año, variables macro unificadas, transformaciones documentadas |
| **Fase 4** | Modelos entrenados y serializados | `models/regression.pkl` + `models/clustering.pkl` | R² ≥ 0,75 en test, silueta ≥ 0,45, hiperparámetros documentados, reproducible |
| **Fase 5** | Informe de evaluación con conclusiones | `FASE_5_EVALUACION.md` | Respuestas a 4 preguntas, gráficas de residuos, validación con A8, análisis de errores |
| **Fase 6** | Dashboard interactivo desplegado | URL pública Streamlit | Filtros ciudad/año/tipo, predictor operativo, IAH por ciudad, documentación de uso |

**Entregables de gestión del proyecto:** `GUIA_FASE_1.md`, `HALLAZGOS_FASE_2.md`, `README.md`, repositorio GitHub con ramas por fase.

---

## 9. Plan del Proyecto — Cronograma

| Semana | Actividad | Responsable |
|:---:|---|:---:|
| 1–2 | **Fase 1:** Comprensión del negocio. Documento de planificación aprobado. | Steve |
| 3–4 | **Fase 2:** Descarga de los 16 archivos, EDA inicial, reporte de calidad por dataset. | Sofía |
| 5–6 | **Fase 3:** Normalización de esquemas, deduplicación, integración y construcción del IAH. | Kukis |
| 7–9 | **Fase 4:** Entrenamiento de modelos de regresión y clustering. | Steve |
| 10 | **Fase 5:** Evaluación, gráficas de residuos, conclusiones cuantitativas. | Sofía |
| 11–12 | **Fase 6:** Dashboard Streamlit con vistas nacional y por ciudad. Despliegue URL pública. | Kukis |
| 13 | Preparación de presentación final. Ensayo general. | Todos |
| 14 | **Presentación final ante jurado.** | Todos |

**Nota de planificación:** Fase 4 tiene un buffer de una semana adicional para acomodar cualquier problema con la calidad de datos en A1 (~997K registros), que podría consumir tiempo de limpieza adicional. La versión anterior del cronograma solo asignaba 2 semanas a Fase 4, lo cual era optimista dado el tamaño del dataset integrado (16 fuentes) y la complejidad de entrenar modelos tanto de regresión como de clustering. Con 3 semanas, el equipo tendrá tiempo de iterar entre modelos, afinar hiperparámetros y validar resultados intermedios.

### 9.1 Matriz de Responsabilidades (RACI)

La matriz RACI complementa el cronograma asignando responsabilidad granular por actividad técnica. **R** = Responsable (ejecuta), **A** = Accountable (responde por el resultado), **C** = Consulted (aporta experiencia), **I** = Informed (recibe reporte de avance).

| Actividad | Steve | Sofía | Kukis |
|---|---|---|---|
| **Fase 1:** Definición del problema y planificación | R/A | C | C |
| **Fase 2:** Descarga y EDA de los 16 datasets | C | R/A | I |
| **Fase 3:** Limpieza, integración y construcción del IAH | C | C | R/A |
| **Fase 4:** Modelos de regresión y clustering | R/A | C | C |
| **Fase 5:** Evaluación y respuesta a preguntas de investigación | C | R/A | I |
| **Fase 6:** Dashboard Streamlit y despliegue | I | C | R/A |
| Presentación final ante jurado | R/A | R/A | R/A |
| Control de versiones (GitHub) | C | R/A | C |

**Roles principales del equipo:**
- **Steve:** Responsable de definición del problema, modelado y métricas de desempeño. Lidera las decisiones metodológicas.
- **Sofía:** Responsable de datos (EDA, integración, calidad). Administra el repositorio GitHub y la documentación.
- **Kukis:** Responsable de preparación técnica (limpieza de datos, clustering, dashboard). Soporte técnico general.

---

## 10. Actividades Realizadas en Fase 1

Durante la Fase 1 se ejecutaron las siguientes actividades:

1. **Revisión bibliográfica y contextualización:** Análisis del déficit habitacional colombiano, evolución del PIR según OCDE/ONU-Hábitat, estadísticas recientes del DANE sobre variación de precios por ciudad.
2. **Definición del problema de negocio:** Formulación de la pregunta central de investigación y sus cuatro preguntas derivadas medibles y específicas.
3. **Definición de objetivos y criterios de éxito:** Cuatro objetivos específicos con métricas concretas; ocho criterios de éxito con umbrales numéricos verificables.
4. **Inventario de fuentes de datos:** Identificación, clasificación y verificación de disponibilidad de 16 fuentes (8 datasets A de precios + 8 series B macroeconómicas). Verificación de URLs de descarga.
5. **Definición del IAH y variables derivadas:** Especificación de las fórmulas del Índice de Accesibilidad Habitacional, ratio cuota/salario y clasificación cualitativa de niveles de accesibilidad.
6. **Elaboración del glosario técnico:** 30+ términos definidos operativamente para el contexto del proyecto (indicadores económicos, métricas de modelos, variables macroeconómicas, conceptos estadísticos).
7. **Análisis costo-beneficio:** Valoración de recursos consumidos (~412 horas-persona, $0 COP) versus entregables generados.
8. **Identificación y documentación de riesgos:** 9 riesgos técnicos con probabilidad, impacto y estrategia de mitigación.
9. **Elaboración del cronograma:** Plan de 13 semanas con responsable por fase y actividades clave.
10. **Validación interna del documento:** Revisión de coherencia entre preguntas, objetivos y criterios de éxito; verificación de URLs y disponibilidad de herramientas.

---

## 11. Metodología Aplicada

La Fase 1 planifica el proyecto; no genera datos experimentales ni resultados cuantitativos propios. La metodología empleada fue:

- **Revisión documental:** Consulta de estadísticas del DANE, BanRep, Fedesarrollo, ONU-Hábitat y OCDE para fundamentar la justificación del proyecto con datos reales del mercado inmobiliario colombiano.

### 11.1 Justificación metodológica del uso del SMLMV en el IAH

El **IAH** usa el salario mínimo como denominador en lugar del ingreso mediano del hogar (disponible en la GEIH del DANE). Esta decisión metodológica requiere justificación explícita porque se desvía del PIR estándar de la OCDE, que usa el ingreso mediano del hogar.

**Comparación de alternativas de denominador:**

| Opción | Ventajas | Desventajas |
|---|---|---|
| **Ingreso mediano del hogar (GEIH)** | Más cercano al PIR original; refleja distribución real de ingresos | Menor disponibilidad histórica; alta varianza muestral en ciudades intermedias; GEIH tiene cobertura temporal limitada (2010–presente); no permite desagregación confiable por ciudad para todos los años del período 2020–2025 |
| **SMLMV (Salario Mínimo)** | Serie homogénea y oficial disponible continuamente desde 1984; misma metodología todo el período; comparable entre ciudades; aprobado por decreto anual nacional | Es un proxy del ingreso de hogares de bajos ingresos, no del ingreso mediano real; sobreestima sistemáticamente el IAH (diferencia estimada ~1,5×–2×) |

**Decisión final:** Se selecciona el **SMLMV** como denominador del IAH por las siguientes razones:
1. **Disponibilidad histórica completa:** Cubre sin interrupciones todo el período 2020–2025 (y desde 1984), mientras que la GEIH tiene limitaciones de cobertura por ciudad y año.
2. **Homogeneidad metodológica:** El SMLMV se calcula con la misma fórmula año tras año, a diferencia del ingreso mediano de la GEIH que depende de la muestra de cada oleada.
3. **Pertinencia para el segmento estudiado:** El proyecto se enfoca en accesibilidad para hogares de ingresos bajos y medios, que son precisamente quienes dependen del salario mínimo como referencia.
4. **Transparencia del sesgo:** La sobreestimación del IAH (~1,5×–2×) se documenta explícitamente como limitación en el informe final (ver sección 6, Limitaciones), y no invalida la comparación relativa entre ciudades y años.

**Impacto en la interpretación:** Al usar SMLMV, los valores del IAH para Colombia serán sistemáticamente superiores a los del PIR internacional para el mismo mercado. Por ejemplo, si el PIR internacional de Bogotá fuera ~8 (moderado), el IAH podría mostrar ~14 (elevado). Esto NO indica error metodológico, sino que el numerador está referido a una población de menor ingreso que la mediana nacional.

- **Clasificación de niveles de accesibilidad:** Basada en el marco de la OCDE/ONU-Hábitat adaptado al contexto:
  - *Accesible*: IAH ≤ 5 años
  - *Moderado*: 5 < IAH ≤ 10 años
  - *Elevado*: 10 < IAH ≤ 20 años
  - *Crítico*: IAH > 20 años
- **Evaluación de riesgos:** Matriz cualitativa de probabilidad × impacto con mitigaciones específicas por riesgo identificado.
- **Planificación CRISP-DM:** Asignación de fases según competencias del equipo (Steve: negocio + modelado; Sofía: datos + evaluación; Kukis: preparación + despliegue), cronograma de 13 semanas con entregables por fase.

---

## 12. Entregables Generados

| Entregable | Ubicación | Estado |
|---|---|---|
| Documento FASE_1_COMPLETA.md | `docs/FASE_1_COMPLETA.md` | ✅ Generado |
| Repositorio GitHub con estructura de ramas por fase | GitHub (rama `main` + ramas por fase) | ✅ Creado |
| Inventario de 16 fuentes de datos con metadatos | Sección 5 de este documento | ✅ Documentado |
| Glosario técnico (30+ términos) | Sección 7 de este documento | ✅ Documentado |
| Especificación de criterios de éxito (8) | Sección 3.4 de este documento | ✅ Documentado |
| Cronograma de 13 semanas | Sección 9 de este documento | ✅ Documentado |
| Análisis de riesgos (9 riesgos) | Sección 6.3 de este documento | ✅ Documentado |
| Guía de Fase 1 para el equipo | `docs/GUIA_FASE_1.md` | ✅ Generado |

---

## 13. Validaciones y Checklist de Cierre

- [x] **Contexto y justificación** — incluye cifras reales de déficit habitacional, PIR, datos DANE
- [x] **Pregunta central** (1) + **4 preguntas derivadas** — específicas, medibles, relevantes
- [x] **Objetivo general** (1) + **4 objetivos específicos** — redacción evaluable por el jurado
- [x] **Criterios de éxito** (8) — cada uno con métrica y umbral numérico concreto
- [x] **Alcance geográfico definido** — análisis nacional + 12 ciudades focales con justificación
- [x] **Tabla de stakeholders** (4) — con interés y modo de impacto
- [x] **Supuestos y restricciones** — documentados explícitamente
- [x] **Herramientas confirmadas** — 9 herramientas con responsable y estado
- [x] **Inventario de 16 datasets** — URLs, tamaño, registros, período
- [x] **Glosario técnico** — 30+ términos en 4 categorías
- [x] **Análisis costo-beneficio** — costos, beneficios y balance
- [x] **9 riesgos identificados** — con probabilidad, impacto y mitigación concreta
- [x] **Cronograma completo** — Fases 1–6 + presentación, con responsables y semanas
- [x] **Revisión interna del equipo** — coherencia entre preguntas, objetivos y criterios verificada
- [ ] **Visto bueno del profesor/jurado** — pendiente entrega Semana 2

**Tasa de cumplimiento:** 14 de 15 ítems (93%) — el ítem pendiente (aprobación externa) está fuera del control del equipo.

---

## 14. Conclusiones

La Fase 1 cumplió su rol dentro del ciclo CRISP-DM: convertir la problemática de accesibilidad habitacional en un proyecto de ciencia de datos estructurado, trazable y con criterios de éxito verificables.

**Contribución clave al ciclo:** Se diseñó un indicador propio —el IAH— que adapta el PIR estándar al contexto colombiano usando el SMLMV como proxy del ingreso. Esta decisión es técnicamente justificada por la disponibilidad y consistencia histórica de la serie, aunque implica que los valores del IAH serán sistemáticamente superiores a los valores internacionales del PIR para el mismo mercado. Esta diferencia se documenta como limitación metodológica explícita.

**Estado del proyecto al cierre de Fase 1:** El proyecto cuenta con una base metodológica completa. Las 16 fuentes de datos están identificadas y sus URLs verificadas. El stack tecnológico está confirmado. Los ocho criterios de éxito funcionarán como contrato de calidad entre las fases de modelado (Fase 4) y evaluación (Fase 5). El único ítem pendiente es la aprobación formal del jurado, que no está dentro del control del equipo.

**Validez del alcance:** La selección de 12 ciudades focales cubre un espectro suficiente de contextos urbanos colombianos (capitales principales, ciudades intermedias, ciudades costeras, fronterizas y cafeteras) para responder las preguntas de investigación con contraste regional genuino. La cobertura temporal 2020–2025 captura el ciclo pandemia-recuperación-choque inflacionario, los eventos económicos más relevantes para la accesibilidad habitacional en el período reciente.

---

## 15. Preparación para la Siguiente Fase

La **Fase 2 — Comprensión de los Datos** puede iniciarse inmediatamente al cierre de esta fase.

### Artefactos entregados por Fase 1 a Fase 2

| Artefacto | Ubicación | Uso en Fase 2 |
|---|---|---|
| Inventario de 16 fuentes (A1–A8, B1–B8) con URLs | Sección 5 de este documento | Guía de descarga y carga inicial |
| Lista de 12 ciudades focales | Sección 3.1 de este documento | Criterio de filtro en EDA por ciudad |
| Criterio de umbral (≥ 500 registros por ciudad) | Sección 3.1, nota metodológica | Determina qué ciudades entran al análisis |
| Variables de interés definidas (price, area, rooms, city, etc.) | Sección 7 + §2.4 | Estructura el perfil de calidad de datos |
| Criterios de éxito del modelo | Sección 3.4 | Orienta la evaluación de completitud de features |

### Actividades prioritarias de Fase 2

1. **Descarga** de los 8 datasets A usando la API de Kaggle (`kaggle.json` de Steve) y de las 8 series B desde fuentes oficiales.
2. **Verificación de integridad:** tamaño real de archivos, conteo de registros, rango temporal efectivo vs. reportado en los metadatos.
3. **Perfil de calidad:** tasa de nulos por columna, tipos de datos, distribución de ciudades, rango de precios.
4. **Identificación del registro de conteo por ciudad** para aplicar el criterio de ≥ 500 registros y confirmar qué ciudades entran al análisis final.
5. **Exploración de esquemas de columnas** en cada dataset A para anticipar el trabajo de mapeo de Fase 3.

### Riesgos heredados con mayor relevancia para Fase 2

- **R2 (esquemas incompatibles):** Fase 2 debe documentar los esquemas reales de cada dataset para que Fase 3 pueda diseñar el mapeo canónico.
- **R6 (ciudades con pocos registros):** Fase 2 debe cuantificar exactamente cuántos registros tiene cada ciudad antes de la limpieza.
- **R3 (duplicados entre datasets):** Fase 2 debe identificar si hay propiedades en común entre A1, A2, A4, A5 y A6 (todos incluyen Bogotá/Medellín).

---

*Documento de Fase 1 · CRISP-DM 2026-I · Proyecto Accesibilidad Habitacional Colombia — 2020–2025*  
*Equipo: Steve · Sofía · Kukis*
