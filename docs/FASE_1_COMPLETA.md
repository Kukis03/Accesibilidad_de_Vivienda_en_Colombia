# Fase 1 — Comprensión del Negocio
## Proyecto: Accesibilidad de Vivienda en Colombia · CRISP-DM 2025-I
**Responsable:** Steve · **Apoyo:** Sofía, Kukis
**Estado:** ✅ Completa y lista para revisión del jurado

---

## 1. Contexto y Justificación

La vivienda es el activo más costoso que adquiere un hogar a lo largo de su vida. En Colombia, el déficit habitacional cuantitativo supera el millón de unidades, y el precio de la vivienda ha crecido sostenidamente por encima del salario mínimo real durante la última década: en 2025, el DANE reportó incrementos del 9,11% en Bogotá, 8,29% en Medellín y 9,22% en Barranquilla, mientras que ciudades intermedias como Cúcuta registraron saltos del 24,6% en 2024, evidenciando una crisis que no es exclusiva de las grandes capitales. El indicador internacional de referencia es el **Price-to-Income Ratio (PIR)**: la razón entre el precio mediano de vivienda y el ingreso anual mediano del hogar; un PIR superior a 5 se considera crítico según OCDE y ONU-Hábitat. Este proyecto construye una versión del PIR adaptada al contexto colombiano usando el salario mínimo como proxy del ingreso de referencia, integra todos los datasets disponibles de precios inmobiliarios con variables macroeconómicas oficiales, y analiza tanto el nivel nacional como las diferencias entre ciudades para revelar con evidencia cuantitativa cómo ha evolucionado la accesibilidad habitacional entre 2015 y 2024.

---

## 2. Pregunta Central y Preguntas Derivadas

**Pregunta central:**
> ¿Cómo ha evolucionado la accesibilidad económica a la vivienda en Colombia entre 2015 y 2024, y qué variables estructurales explican mejor las diferencias entre ciudades?

**Preguntas derivadas:**

1. ¿Cuántos años de salario mínimo equivale el precio mediano de vivienda en las principales ciudades colombianas, y cómo ha cambiado esa relación en los últimos 10 años?
2. ¿Qué variables (área, ciudad, tipo de inmueble, inflación, tasa hipotecaria, desempleo) tienen mayor poder predictivo sobre el precio de una propiedad?
3. ¿Es posible clasificar objetivamente los mercados de vivienda urbana en segmentos diferenciables de accesibilidad mediante clustering no supervisado?
4. ¿En qué ciudades la cuota hipotecaria mensual supera el 30% del ingreso mínimo, comprometiendo la viabilidad financiera de los hogares?

---

## 3. Objetivos del Proyecto

**Objetivo general:**
Desarrollar un sistema de análisis y predicción de accesibilidad habitacional en Colombia, integrando todos los datos inmobiliarios y macroeconómicos disponibles, para identificar patrones nacionales y diferencias espaciales de inequidad en el acceso a la vivienda entre 2015 y 2024.

**Objetivos específicos:**

1. Construir y validar un Índice de Accesibilidad Habitacional (IAH) para las ciudades con cobertura de datos, comparándolo con el estándar PIR de la OCDE a nivel nacional y por ciudad.
2. Entrenar y comparar modelos de regresión para predecir el precio de una propiedad con base en sus características físicas y el contexto macroeconómico del año y ciudad correspondientes.
3. Segmentar los mercados de vivienda urbana mediante clustering no supervisado para identificar grupos de ciudades con comportamientos similares de accesibilidad.
4. Desplegar los resultados en un dashboard interactivo público (Streamlit) que permita exploración a nivel nacional y por ciudad, año y tipo de inmueble, incluyendo un predictor de precio.

---

## 4. Alcance Geográfico — Estrategia Nacional + Ciudades Focales

### Nivel 1 — Análisis Nacional (todo el país)
El análisis de tendencias macroeconómicas (evolución del salario mínimo vs. inflación de vivienda, PIR nacional) cubre **todo el territorio colombiano** como referencia de contexto. Esto es posible porque las variables macro del DANE y BanRep son de cobertura nacional.

### Nivel 2 — Ciudades Focales (análisis profundo con datos de precios)
El análisis de precios, modelos predictivos y clustering se realizará sobre las ciudades con suficiente representación en los datasets. La selección sigue el marco de las **13 áreas metropolitanas del DANE** (referencia estándar del mercado laboral) y la disponibilidad real de datos en Kaggle:

| # | Ciudad focal | Región | Tamaño | Presencia en datasets | Prioridad |
|---|---|---|---|---|---|
| 1 | **Bogotá D.C.** | Centro-Oriente | Metrópoli (+7M hab) | A1, A2, A3, A4, A5, A6 | 🔴 Alta |
| 2 | **Medellín** | Occidente | Metrópoli (+2.5M hab) | A1, A4, A5, A7 | 🔴 Alta |
| 3 | **Cali** | Occidente | Metrópoli (+2M hab) | A1, A4, A5 | 🔴 Alta |
| 4 | **Barranquilla** | Caribe | Grande (+1.2M hab) | A1, A4, A5 | 🔴 Alta |
| 5 | **Bucaramanga** | Nororiente | Intermedia (+600K hab) | A1, A4, A5 | 🟡 Media |
| 6 | **Cartagena** | Caribe | Grande (+900K hab) | A1, A4, A5 | 🟡 Media |
| 7 | **Pereira** | Eje Cafetero | Intermedia (+450K hab) | A1, A4, A5 | 🟡 Media |
| 8 | **Cúcuta** | Nororiente | Intermedia (+700K hab) | A1, A4 | 🟡 Media |
| 9 | **Manizales** | Eje Cafetero | Intermedia (+400K hab) | A1, A4 | 🟡 Media |
| 10 | **Ibagué** | Centro-Oriente | Intermedia (+550K hab) | A1, A4 | 🟢 Baja |
| 11 | **Santa Marta** | Caribe | Intermedia (+500K hab) | A4, A5 | 🟢 Baja |
| 12 | **Villavicencio** | Orinoquia | Intermedia (+500K hab) | A1, A4, A9 (scraping) | 🟡 Media |

> **Decisión metodológica:** Se incluirán en el análisis final solo las ciudades con ≥ 500 registros de vivienda en el dataset integrado. Las demás quedarán documentadas como "cobertura limitada" en el reporte de calidad de datos (Fase 2).

### Por qué esta estrategia es correcta
- **Cobertura real:** El 47% de la población colombiana vive en ciudades capitales (DANE 2023). Las 12 ciudades focales cubren más del 35% de la población nacional.
- **Contraste útil:** Incluir ciudades grandes (Bogotá, Medellín, Cali), intermedias (Pereira, Bucaramanga, Manizales) y costeras (Cartagena, Barranquilla, Santa Marta) permite responder si la crisis de accesibilidad es un fenómeno de grandes capitales o se extiende a ciudades menores.
- **Rigor académico:** El IPVU del BanRep ya cubre exactamente estas ciudades, lo que permite validación cruzada con datos oficiales.

---

## 5. Criterios de Éxito

| # | Criterio | Métrica | Umbral mínimo aceptable |
|---|---|---|---|
| 1 | Precisión del modelo de regresión | RMSE relativo (% del precio mediano) | < 15% |
| 2 | Bondad de ajuste | R² en conjunto de prueba | ≥ 0.75 |
| 3 | Calidad del clustering | Coeficiente de silueta | ≥ 0.45 |
| 4 | Separabilidad de clusters | Segmentos diferenciables | ≥ 3 |
| 5 | Cobertura geográfica | Ciudades con análisis completo | ≥ 8 ciudades |
| 6 | Cobertura temporal | Años cubiertos por los datos | 2015 – 2024 |
| 7 | Funcionalidad del dashboard | Filtros operativos implementados | Ciudad, año, tipo inmueble |
| 8 | Respuesta a preguntas de investigación | Preguntas respondidas con evidencia cuantitativa | 4 de 4 |

---

## 6. Stakeholders

| Stakeholder | Qué quiere | Cómo impacta el proyecto |
|---|---|---|
| Jurado / Profesor | Rigor metodológico, claridad en la presentación, conclusiones válidas con evidencia | Determina la calificación final |
| Potencial comprador de vivienda | Saber si puede costear una vivienda en su ciudad con su ingreso actual | Define la usabilidad del dashboard y el predictor |
| Investigador / tomador de decisión pública | Identificar en qué ciudades se requiere intervención prioritaria para política de vivienda | Valida la relevancia social de los hallazgos |
| Entidad financiera / sector inmobiliario | Entender riesgo de impago hipotecario y tendencias de precios por ciudad | Valida la precisión y cobertura del modelo predictivo |

---

## 7. Supuestos y Restricciones

**Supuestos:**
- Los precios en los datasets de Kaggle son representativos del mercado formal de vivienda urbana en listados digitales (FincaRaiz, Properati, Metro Cuadrado).
- El salario mínimo legal mensual se usa como proxy del ingreso de referencia para hogares de bajos y medianos ingresos; no reemplaza el ingreso mediano real pero es la serie más consistente y comparable disponible.
- Las ciudades con menos de 500 registros en el dataset integrado serán excluidas del análisis de clustering y del modelo predictivo, pero se mencionarán como limitación de cobertura.

**Restricciones:**
- El dataset Properati (A4) cubre hasta 2021; se complementa con A1, A2 y A5 para los años 2022–2024.
- No se dispone de datos catastrales georreferenciados a nivel de predio para todas las ciudades.
- El análisis se limita a vivienda urbana; la vivienda rural queda fuera del alcance.
- Los datasets de Kaggle solo cubren vivienda en venta listada en plataformas digitales; las transacciones informales o no publicadas no están representadas.

---

## 8. Herramientas Confirmadas

| Propósito | Herramienta | Responsable | Estado |
|---|---|---|---|
| Descarga de datos Kaggle | Kaggle API (`kaggle.json`) | **Steve** | ✅ Cuenta activa confirmada |
| Notebooks interactivos | Jupyter / Google Colab | Steve | ✅ Disponible |
| Análisis y manipulación de datos | pandas, numpy | Steve | ✅ Disponible |
| Visualización exploratoria | matplotlib, seaborn, plotly | Steve | ✅ Disponible |
| Modelado supervisado | scikit-learn (Random Forest, Ridge) | Steve | ✅ Disponible |
| Modelado no supervisado | scikit-learn (KMeans, DBSCAN) | Kukis | ✅ Disponible |
| Web scraping datos vivienda | BeautifulSoup + requests | Steve / Sofía | ✅ Disponible — refuerzo Villavicencio |
| Dashboard interactivo | Streamlit | Kukis | ✅ Disponible |
| Control de versiones | GitHub (rama por fase CRISP-DM) | Sofía | ✅ Disponible |

---

## 9. Inventario Completo de Datasets — TODOS los disponibles

### Filosofía de uso: usar TODO lo que existe y tiene calidad suficiente

> Se usarán **todos los datasets** identificados. En la Fase 2 (EDA) Steve evaluará la calidad de cada uno y decidirá cuáles se integran al modelo final vs. cuáles se reservan como validación cruzada. No se descarta ningún dataset en Fase 1.

---

### GRUPO A — Datasets de Precios de Vivienda (Kaggle)

| ID | Dataset | Link verificado | Registros aprox. | Ciudades cubiertas | Período |
|---|---|---|---|---|---|
| **A1** | Colombia Housing Properties Price | [kaggle.com/datasets/julianusugaortiz/colombia-housing-properties-price](https://www.kaggle.com/datasets/julianusugaortiz/colombia-housing-properties-price) | ~120.000 | Nacional (multiciudad) | 2018–2022 |
| **A2** | Colombian Properties 2023 | [kaggle.com/datasets/lauramartinezortiz/colombian-properties](https://www.kaggle.com/datasets/lauramartinezortiz/colombian-properties) | ~50.000 | Nacional (multiciudad) | 2023 |
| **A3** | Real Estate Bogotá — análisis por barrio | [kaggle.com/datasets/pablobravo73/real-estate-bogota](https://www.kaggle.com/datasets/pablobravo73/real-estate-bogota) | ~30.000 | Bogotá (granular) | 2019–2022 |
| **A4** | Properati Latinoamérica (filtrar Colombia) | [kaggle.com/datasets/properati-data/properties](https://www.kaggle.com/datasets/properati-data/properties) | ~1.500.000 | Nacional (histórico más amplio) | 2015–2021 |
| **A5** | Properties for sale in Colombia — FincaRaiz | [kaggle.com/datasets/diegomedinaflores/properties-for-sale-in-colombia-fincaraiz](https://www.kaggle.com/datasets/diegomedinaflores/properties-for-sale-in-colombia-fincaraiz) | ~80.000 | Nacional (multiciudad) | 2023–2024 |
| **A6** | Real Estate / Housing Colombia Bogotá 2023 | [kaggle.com/datasets/juandavsnchez/real-estatehousing-colombia-bogota](https://www.kaggle.com/datasets/juandavsnchez/real-estatehousing-colombia-bogota) | ~20.000 | Bogotá | 2023 |
| **A7** | Medellín Properties 2023 | [kaggle.com/datasets/cesaregr/medelln-properties](https://www.kaggle.com/datasets/cesaregr/medelln-properties) | ~15.000 | Medellín | 2023 |
| **A8** | Colombia House Prediction | [kaggle.com/datasets/danieleduardofajardo/colombia-house-prediction](https://www.kaggle.com/datasets/danieleduardofajardo/colombia-house-prediction) | ~10.000 | Nacional | 2019–2020 |
| **A9** | Scraping FincaRaiz Villavicencio | Scraping propio (BeautifulSoup) | ~3.000–6.000 | Villavicencio | 2024–2025 |

**Total registros brutos de precios (antes de limpiar): ~1.828.000 filas**

#### Cobertura temporal combinada de los datasets A:

```
2015 ──── 2016 ──── 2017 ──── 2018 ──── 2019 ──── 2020 ──── 2021 ──── 2022 ──── 2023 ──── 2024
│                            │                            │            │            │
A4 (Properati) ──────────────────────────────────────────┤            │            │
                             A1 (Colombia Housing) ───────────────────┤            │
                                              A8 (House Pred) ────────┤            │
                                                          A3 (Bogotá) ────────────────
                                                                       A2 (2023) ───┤
                                                                       A6 (Bogotá 2023)
                                                                       A7 (Medellín 2023)
                                                                       A5 (FincaRaiz) ────┤
                                                                       A9 (Scraping Vcio) ──┤
```

> El dataset A4 (Properati) es la columna vertebral histórica 2015–2021. Los datasets A1, A2, A3, A5, A6, A7 y A9 (scraping Villavicencio) complementan y extienden hasta 2024. Juntos, cubren el período completo requerido.

---

### GRUPO B — Variables Macroeconómicas (DANE + BanRep)

| ID | Variable | Fuente | Link verificado | Frecuencia | Período |
|---|---|---|---|---|---|
| **B1** | Salario mínimo mensual histórico | DANE + Consultor Contable | [consultorcontable.com/datos-historicos/salario-minimo-historico](https://www.consultorcontable.com/datos-hist%C3%B3ricos/salario-m%C3%ADnimo-historico/) | Anual | 1984–2025 |
| **B2** | IPC — Índice de Precios al Consumidor (histórico) | DANE | [dane.gov.co → IPC Histórico](https://www.dane.gov.co/index.php/estadisticas-por-tema/precios-y-costos/indice-de-precios-al-consumidor-ipc/ipc-historico) | Mensual | 2000–presente |
| **B3** | Tasas de interés crédito hipotecario (VIS y No VIS) | Banco de la República | [banrep.gov.co → Tasas de crédito por modalidades](https://www.banrep.gov.co/es/estadisticas/tasas-credito-modalidades) | Mensual | 1998–presente |
| **B4** | Tasa de desempleo por ciudad — 13 áreas metropolitanas | DANE (GEIH) | [dane.gov.co → Empleo y desempleo](https://www.dane.gov.co/index.php/estadisticas-por-tema/mercado-laboral/empleo-y-desempleo) | Trimestral | 2006–presente |
| **B5** | IPVU — Índice de Precios de Vivienda Usada | BanRep / datos.gov.co | [datos.gov.co/d/msis-zzf8](https://www.datos.gov.co/Econom-a-y-Finanzas/IPVU-ndice-de-precios-de-la-vivienda-usada/msis-zzf8) | Trimestral | 2010–presente |
| **B6** | IPVN — Índice de Precios de Vivienda Nueva | DANE | [dane.gov.co → IPVN](https://www.dane.gov.co/index.php/estadisticas-por-tema/precios-y-costos/indice-de-precios-de-la-vivienda-nueva-ipvn) | Trimestral | 2015–presente |

---

### Tabla resumen: archivos a tener en `/data/raw/`

| # | Archivo | Tipo | Fuente | ¿Obligatorio? |
|---|---|---|---|---|
| 1 | `properati_colombia.csv` | CSV | Kaggle A4 | ✅ Sí — histórico base |
| 2 | `colombia_housing_price.csv` | CSV | Kaggle A1 | ✅ Sí |
| 3 | `colombian_properties_2023.csv` | CSV | Kaggle A2 | ✅ Sí |
| 4 | `fincaraiz_properties.csv` | CSV | Kaggle A5 | ✅ Sí — cierre 2023-24 |
| 5 | `real_estate_bogota.csv` | CSV | Kaggle A3 | ✅ Sí — análisis granular Bogotá |
| 6 | `real_estate_bogota_2023.csv` | CSV | Kaggle A6 | ✅ Sí — amplía cobertura Bogotá |
| 7 | `medellin_properties_2023.csv` | CSV | Kaggle A7 | ✅ Sí — amplía cobertura Medellín |
| 8 | `colombia_house_prediction.csv` | CSV | Kaggle A8 | ✅ Sí — agrega 2019-20 |
| 9 | `fincaraiz_villavicencio_scraping.csv` | CSV | Scraping propio A9 | ✅ Sí — refuerza cobertura Villavicencio |
| 10 | `salario_minimo_historico.xlsx` | **XLSX** | DANE | ✅ Sí |
| 10 | `ipc_colombia_mensual.xlsx` | **XLSX** | DANE | ✅ Sí |
| 11 | `tasa_hipotecaria_mensual.xlsx` | **XLSX** | BanRep | ✅ Sí |
| 12 | `desempleo_ciudades_trimestral.xlsx` | **XLSX** | DANE GEIH | ✅ Sí |
| 13 | `ipvu_trimestral.xlsx` | **XLSX** | BanRep / datos.gov.co | ✅ Sí |
| 15 | `ipvn_trimestral.xlsx` | **XLSX** | DANE | ✅ Sí |

**Total: 9 archivos CSV de precios + 6 archivos XLSX macro = 15 archivos en `/data/raw/`**

> **Nota:** El archivo A9 (`fincaraiz_villavicencio_scraping.csv`) se genera mediante scraping automático (ver Sección 9-bis de Fase 2) para reforzar la cobertura de Villavicencio, que es la ciudad focal con menos representación en los datasets Kaggle.

> **¿Por qué usar TODOS los datasets?** Más registros = modelo más robusto, menos sesgo de fuente, mayor representación geográfica. En Fase 3 (limpieza) se normalizan los esquemas de columnas y se eliminan duplicados antes de integrar. El esfuerzo extra vale porque pasa de ~300.000 registros (solo los 3 principales) a ~1.8M registros (todos).

---

## 10. Riesgos Identificados y Mitigaciones

| # | Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|---|
| R1 | Datos incompletos (valores nulos en precio, área, ciudad) | Alta | Medio | Imputación y filtros en Fase 3; documentar tasa de missings por dataset y variable |
| R2 | Esquemas de columnas diferentes entre datasets | Alta | Alto | Fase 3 define esquema canónico; script de mapeo de columnas por dataset |
| R3 | Duplicados entre datasets (mismo inmueble en A1 y A2) | Media | Medio | Deduplicación por hash de (ciudad, precio, área, tipo); registrar registros eliminados |
| R4 | Series temporales macroeconómicas desalineadas con precios | Media | Alto | Resampleo a frecuencia anual; interpolación lineal donde sea válido |
| R5 | Multicolinealidad entre variables macro (IPC, tasa hipotecaria) | Media | Medio | Calcular VIF; usar feature_importances_ para selección de features |
| R6 | Ciudades intermedias con < 500 registros tras limpieza | Media | Medio | Documentar como limitación; excluir del modelo pero incluir en análisis descriptivo. Villavicencio reforzado con scraping A9 |
| R7 | Clusters no diferenciables (silueta < 0.45) | Baja | Alto | Probar KMeans, DBSCAN y clustering jerárquico; variar número de features |
| R8 | Properati A4 requiere filtrar ~1.4M filas no-Colombia | Alta | Bajo | Script de filtrado por campo `l1 == 'Colombia'` en carga inicial |
| R9 | Dashboard lento con dataset grande | Media | Bajo | Usar datos agregados (mediana por ciudad/año); caché de Streamlit |

---

## 11. Cronograma General del Proyecto

| Semana | Actividad | Responsable |
|---|---|---|
| 1–2 | **Fase 1:** Comprensión del negocio. Documento de planificación aprobado. | Steve |
| 3–4 | **Fase 2:** Descarga de los 14 archivos, EDA inicial, reporte de calidad por dataset. | Sofía |
| 5–6 | **Fase 3:** Normalización de esquemas, deduplicación, integración y construcción del IAH. | Kukis |
| 7–8 | **Fase 4:** Entrenamiento de modelos de regresión y clustering. | Steve |
| 9 | **Fase 5:** Evaluación, gráficas de residuos, conclusiones cuantitativas. | Sofía |
| 10–11 | **Fase 6:** Dashboard Streamlit con vistas nacional y por ciudad. Despliegue URL pública. | Kukis |
| 12 | Preparación de presentación final. Ensayo general. | Todos |
| 13 | **Presentación final ante jurado.** | Todos |

---

## Checklist Final — Fase 1 Completada

### Entregables de contenido

- [x] **1. Contexto y justificación** — incluye cifras reales de déficit habitacional, PIR, datos DANE 2025
- [x] **2. Pregunta central** (1) + **4 preguntas derivadas** — específicas, medibles, relevantes
- [x] **3. Objetivo general** (1) + **4 objetivos específicos** — redacción evaluable por el jurado
- [x] **4. Criterios de éxito** (8) — cada uno con métrica y umbral numérico concreto
- [x] **5. Alcance geográfico definido** — análisis nacional + 12 ciudades focales con justificación
- [x] **6. Tabla de stakeholders** (4) — con interés y modo de impacto
- [x] **7. Supuestos y restricciones** — documentados explícitamente

### Herramientas y entorno

- [x] **Python + Jupyter/Colab** confirmados (Steve)
- [x] **pandas, numpy, matplotlib, seaborn, plotly** disponibles
- [x] **scikit-learn** disponible (Random Forest, Ridge, KMeans, DBSCAN)
- [x] **Streamlit** disponible (Kukis)
- [x] **GitHub** con repositorio creado y estructura de ramas por fase (Sofía)
- [x] **Cuenta Kaggle de Steve** activa — confirmar token `kaggle.json` configurado en equipo

### Fuentes de datos — todos los links verificados

**Datasets de precios (Kaggle):**
- [x] A1 — Colombia Housing Properties Price ✅
- [x] A2 — Colombian Properties 2023 ✅
- [x] A3 — Real Estate Bogotá ✅
- [x] A4 — Properati Latinoamérica ✅
- [x] A5 — FincaRaiz Colombia ✅
- [x] A6 — Real Estate / Housing Colombia Bogotá 2023 ✅
- [x] A7 — Medellín Properties 2023 ✅
- [x] A8 — Colombia House Prediction ✅

**Variables macroeconómicas (DANE + BanRep):**
- [x] B1 — Salario mínimo histórico ✅
- [x] B2 — IPC histórico DANE ✅
- [x] B3 — Tasa hipotecaria BanRep ✅
- [x] B4 — Desempleo por ciudad GEIH DANE ✅
- [x] B5 — IPVU datos.gov.co / BanRep ✅
- [x] B6 — IPVN DANE ✅

**Pendientes de ejecución (tarea Sofía + Kukis, Sesión 2):**
- [ ] Descargar los 8 CSV de Kaggle y guardar en `/data/raw/`
- [ ] Descargar los 6 XLSX macro y guardar en `/data/raw/`
- [ ] Verificar que todos los archivos abren correctamente con `pandas.read_csv()` / `read_excel()`
- [ ] Ejecutar scraping FincaRaiz Villavicencio (`python scripts/scraping_fincaraiz_villavicencio.py`) para generar A9
- [ ] Escribir `data/raw/README.md` con origen, URL y estructura de cada archivo
- [ ] Hacer primer commit al repositorio GitHub con la rama `fase-2-datos`

### Riesgos

- [x] 9 riesgos identificados con probabilidad, impacto y mitigación concreta
- [ ] Riesgos revisados y aprobados por todo el equipo en sesión conjunta

### Documento final

- [x] Cronograma completo (Fases 1–6 + presentación) con responsables y semanas
- [x] Documento integrado en un solo `.md`
- [ ] **Revisión y visto bueno del profesor/jurado** — pendiente entrega Semana 2

---

## Guía Rápida de Descarga para Sofía — Sesión 2

### 8 datasets Kaggle (con CLI, cuenta de Steve)

```bash
# Configurar API (solo primera vez)
# Descargar kaggle.json desde kaggle.com → Account → API → Create New Token
# Colocar en ~/.kaggle/kaggle.json

# Descargar todos los datasets en /data/raw/
mkdir -p data/raw

# A4 — Properati (histórico más grande, filtrar Colombia después)
kaggle datasets download -d properati-data/properties -p data/raw/ --unzip

# A1 — Colombia Housing Properties Price
kaggle datasets download -d julianusugaortiz/colombia-housing-properties-price -p data/raw/ --unzip

# A2 — Colombian Properties 2023
kaggle datasets download -d lauramartinezortiz/colombian-properties -p data/raw/ --unzip

# A5 — FincaRaiz Colombia 2023-2024
kaggle datasets download -d diegomedinaflores/properties-for-sale-in-colombia-fincaraiz -p data/raw/ --unzip

# A3 — Real Estate Bogotá
kaggle datasets download -d pablobravo73/real-estate-bogota -p data/raw/ --unzip

# A6 — Real Estate Bogotá 2023
kaggle datasets download -d juandavsnchez/real-estatehousing-colombia-bogota -p data/raw/ --unzip

# A7 — Medellín Properties 2023
kaggle datasets download -d cesaregr/medelln-properties -p data/raw/ --unzip

# A8 — Colombia House Prediction
kaggle datasets download -d danieleduardofajardo/colombia-house-prediction -p data/raw/ --unzip
```

### 6 archivos XLSX macro (descarga manual — Kukis)

| Archivo destino | Pasos |
|---|---|
| `salario_minimo_historico.xlsx` | consultorcontable.com → "Salario mínimo histórico" → Descargar Excel |
| `ipc_colombia_mensual.xlsx` | dane.gov.co → Precios y costos → IPC Histórico → Descargar Excel |
| `tasa_hipotecaria_mensual.xlsx` | banrep.gov.co → Estadísticas → Tasas de crédito por modalidades → Serie hipotecaria VIS y No VIS |
| `desempleo_ciudades_trimestral.xlsx` | dane.gov.co → Mercado laboral → Empleo y desempleo → Tabla 13 ciudades → Descargar |
| `ipvu_trimestral.xlsx` | datos.gov.co/d/msis-zzf8 → Exportar → Excel |
| `ipvn_trimestral.xlsx` | dane.gov.co → Construcción → IPVN → Descargar Excel |

---

*Documento de Fase 1 · CRISP-DM 2025-I · Proyecto Accesibilidad Habitacional Colombia*
*Steve · Sofía · Kukis — Repositorio: github.com/[usuario]/proyecto-vivienda-colombia*
