# Fase 2 — Comprensión de los Datos
## Estado: ✅ COMPLETADA
**Notebooks ejecutados:**
- `notebooks/01_EDA_esquema_canonico.ipynb` — Esquema canónico y mapeo de columnas
- `notebooks/02_EDA_calidad_datos.ipynb` — Calidad de datos y diagnóstico de nulos
- `notebooks/03_EDA_distribucion_precios.ipynb` — Distribución de precios y outliers
- `notebooks/04_EDA_analisis_geografico.ipynb` — Análisis geográfico por ciudad
- `notebooks/05_EDA_evolucion_temporal.ipynb` — Evolución temporal de precios
- `notebooks/06_EDA_analisis_area.ipynb` — Análisis de área construida
- `notebooks/07_EDA_variables_categoricas.ipynb` — Variables categóricas
- `notebooks/08_EDA_geoespacial_macrovariables.ipynb` — Geoespacial y macrovariables
- `notebooks/09_EDA_IAH_preliminar.ipynb` — Cálculo del IAH preliminar
- `notebooks/10_EDA_validacion_oficial.ipynb` — Validación cruzada con datos oficiales
- `notebooks/11_EDA_reporte_consolidado.ipynb` — Reporte consolidado de hallazgos

**Documentos generados:**
- `docs/FASE_2_COMPLETA.md` — Documentación completa de Fase 2
- `docs/HALLAZGOS_FASE_2.md` — 13 hallazgos principales documentados
- `docs/figures/` — 31 figuras generadas (PNG/HTML)
- `data/processed/` — 11 archivos procesados (CSV/JSON)

---

## Sección 1: Inventario de Fuentes y Carga Inicial
**Importaciones y setup**
- [x] Importar pandas, numpy, matplotlib, seaborn, plotly
- [x] Configurar estilo de gráficos y opciones de visualización
- [x] Definir rutas relativas: `data/raw/`, `data/processed/`, `docs/figures/`
- [x] Verificar que las carpetas existen; crearlas si es necesario
- [x] Configurar logging para documentar operaciones

**Carga y verificación de datasets Grupo A**
- [x] Cargar A1 (A1_colombia_housing_properties.csv) — Properati Colombia (fuente principal, ~998K registros)
- [x] Cargar A2 (A2_fincaraiz_colombia.csv) — FincaRaiz Colombia 2023-2024
- [x] Cargar A3 (A3_colombia_house_prediction.csv) — Colombia House Prediction
- [x] Cargar A4 (A4_real_estate_bogota.csv) — Real Estate Bogotá por barrio
- [x] Cargar A5 (A5_medellin_properties_2023.csv) — Medellín Properties 2023
- [x] Cargar A6 (A6_real_estate_bogota_2023.csv) — Real Estate Bogotá 2023
- [x] Cargar A7 (A7_fincaraiz_villavicencio_scraping.csv) — Scraping FincaRaiz Villavicencio
- [x] Cargar A8 (A8_carac_pre_viv_nueva.csv) — Características precios vivienda nueva Bogotá UPZ
- [x] Registrar tamaño y número de registros de cada dataset (incluir A7)

**Carga y verificación de datasets Grupo B**
- [x] Cargar B1 (B1_indices_precios_vivienda.csv) — IPVN+IPVU unificado (BanRep + DANE)
- [x] Cargar B2 (B2_tasa_hipotecaria_semanal.csv) — Tasa hipotecaria semanal (BanRep)
- [x] Cargar B3 (B3_salario_minimo_historico.csv) — Salario mínimo histórico (DANE)
- [x] Cargar B4 (B4_ipc_colombia_anual.csv) — IPC anual (DANE)
- [x] Cargar B5 (B5_geih_empleo_colombia.csv) — GEIH empleo mensual (DANE)
- [x] Cargar B6 (B6_qcon_confianza_constructora.csv) — Confianza constructora (Fedesarollo)
- [x] Cargar B7 (B7_qcon_licencias_construccion.csv) — Licencias construcción (Fedesarollo)
- [x] Cargar B8 (B8_geo_estados_localidades.csv) — Estados/localidades geográficas
- [x] Crear tabla resumen de inventario (filas, columnas, período)
- [x] Guardar reporte de inventario en CSV (`data/processed/reporte_calidad_datasets.csv`)

---

## Sección 2: Estructura de Columnas — Esquema Canónico
**Notebook:** `notebooks/01_EDA_esquema_canonico.ipynb`

**Exploración de columnas por dataset**
- [x] Listar columnas reales de A1
- [x] Listar columnas reales de A4
- [x] Listar columnas reales de A5
- [x] Listar tipos de datos de cada dataset
- [x] Crear diccionario de mapeo canónico (nombre original → nombre estándar)

**Documentación de esquemas**
- [x] Crear tabla de esquema para A1 (columna, tipo, descripción, mapeo)
- [x] Crear tabla de esquema para A4 (Properati)
- [x] Crear tabla de esquema para A5 (FincaRaiz)
- [x] Crear tabla de esquema consolidada para A2, A3, A6, A7, A8
- [x] Identificar columnas problemáticas (inconsistencias de nombres, tipos)

---

## Sección 3: Calidad de Datos — Diagnóstico Inicial
**Notebook:** `notebooks/02_EDA_calidad_datos.ipynb`

**Estadísticas de calidad por dataset**
- [x] Calcular filas, columnas y tamaño en memoria para cada dataset
- [x] Calcular % de valores nulos por columna
- [x] Calcular número de duplicados exactos
- [x] Calcular % de registros con precio nulo
- [x] Calcular % de registros con área nula
- [x] Crear tabla resumen de calidad (Grupo A y B)

**Análisis de nulos**
- [x] Visualizar mapa de calor de nulos (muestra)
- [x] Calcular porcentaje de nulos por columna (gráfico barras)
- [x] Verificar si nulos en 'área' están correlacionados con ciudad/año
- [x] Documentar patrones de nulos por ciudad
- [x] Guardar reporte de nulos en CSV (`data/processed/reporte_nulos_completo.csv`)

---

## Sección 4: Distribución de Precios
**Notebook:** `notebooks/03_EDA_distribucion_precios.ipynb`

**Estadísticas descriptivas de precio**
- [x] Calcular min, Q1, mediana, Q3, max, mean de precio (A1)
- [x] Calcular P1 y P99
- [x] Identificar registros con precio <= 0 o nulo
- [x] Visualizar distribución en escala original (histograma)
- [x] Visualizar distribución en escala log (histograma)
- [x] Crear boxplot de precio

**Outliers de precio**
- [x] Identificar precios < $10M COP (outliers bajos)
- [x] Identificar precios > $5.000M COP (outliers altos)
- [x] Calcular % de outliers
- [x] Mostrar 5 registros con precio más bajo
- [x] Mostrar 5 registros con precio más alto
- [x] Documentar hallazgos sobre outliers

---

## Sección 5: Análisis Geográfico — Precios por Ciudad
**Notebook:** `notebooks/04_EDA_analisis_geografico.ipynb`

**Precio mediano por ciudad**
- [x] Calcular precio mediano por ciudad (top 15 por volumen)
- [x] Crear tabla: ciudad, precio_mediano, Q1, Q3, N_registros
- [x] Crear gráfico barras horizontal (precio por ciudad)
- [x] Ranking de ciudades por precio
- [x] Documentar segmentación de ciudades (alta, media, baja)

**Precio por m² por ciudad**
- [x] Calcular precio/m² por registro
- [x] Filtrar outliers en precio/m² (< $500K o > $20M COP/m²)
- [x] Calcular mediana de precio/m² por ciudad
- [x] Crear tabla: ciudad, precio_mediano_m2, precio_medio_m2
- [x] Visualizar precio/m² por ciudad (gráfico comparativo)

---

## Sección 5-bis: Refuerzo de Cobertura — Villavicencio (Dataset A7)
**Notebook:** `notebooks/04_EDA_analisis_geografico.ipynb`

**Cargar y explorar datos de scraping de Villavicencio**
- [x] Cargar dataset A7 (A7_fincaraiz_villavicencio_scraping.csv)
- [x] Explorar estructura de columnas de A7
- [x] Calcular volumen de registros en A7 (~1.048 registros)
- [x] Documentar período cubierto por scraping (fecha inicio-fin)
- [x] Comparar volumen A7 vs cobertura de Villavicencio en A1

**Integración de fuentes complementarias para Villavicencio**
- [x] Cargar IPVN DANE trimestral (incluye Villavicencio AU)
- [ ] Cargar boletines CENAC si están disponibles (no disponibles)
- [x] Convertir IPVN trimestral a anual
- [x] Relacionar precios de scraping con índices oficiales IPVN
- [x] Validar consistencia de precios A7 vs IPVN DANE

**Análisis especial de Villavicencio**
- [x] Calcular estadísticas descriptivas de precio para Villavicencio (A1 + A7 consolidados)
- [x] Precio mediano de Villavicencio en cada año (2015–2024)
- [x] Comparar precio/m² de Villavicencio vs ciudades similares (Ibagué, Cúcuta)
- [x] Distribución de tipos de propiedad en Villavicencio
- [x] Documentar calidad de datos A7 (completitud, nulos, duplicados)
- [x] Guardar figura: `docs/figures/villavicencio_contexto_nacional.png`
- [x] Crear visualización de Villavicencio en contexto nacional

**Documentación de estrategia A7**
- [x] Documentar que A7 es dataset generado internamente (scraping)
- [x] Especificar fechas de scraping y fuente (FincaRaiz)
- [x] Documentar metodología de scraping (script: `scripts/scraping_fincaraiz_villavicencio.py`)
- [x] Explicar por qué Villavicencio requiere refuerzo (cobertura insuficiente en A1)
- [x] Guardar subset de Villavicencio consolidado en `data/processed/villavicencio_consolidado.csv`

---

## Sección 6: Evolución Temporal de Precios
**Notebook:** `notebooks/05_EDA_evolucion_temporal.ipynb`

**Crear columna de año y filtrar período**
- [x] Extraer año de columna de fecha
- [x] Filtrar registros con año entre 2015–2024
- [x] Calcular volumen de registros por año
- [x] Documentar cobertura temporal por dataset

**Tendencia nacional**
- [x] Calcular precio mediano nacional por año
- [x] Calcular precio mediano por año y ciudad (principales)
- [x] Visualizar línea de tendencia nacional (2015–2024)
- [x] Visualizar líneas de tendencia por ciudad focal
- [x] Documentar crecimiento porcentual acumulado

**Hallazgos temporales**
- [x] Calcular CAGR (tasa de crecimiento anual) nacional
- [x] Calcular CAGR por ciudad
- [x] Comparar crecimiento entre ciudades
- [x] Identificar años con mayor/menor crecimiento
- [x] Documentar efecto pandemia (2020–2021)

---

## Sección 7: Análisis de Área Construida
**Notebook:** `notebooks/06_EDA_analisis_area.ipynb`

**Distribución de área**
- [x] Filtrar área válida (> 10 m², < 800 m²)
- [x] Calcular estadísticas descriptivas (min, Q1, mediana, Q3, max)
- [x] Visualizar histograma de distribución de área
- [x] Identificar valores atípicos en área
- [x] Calcular % de registros sin área

**Área por tipo de propiedad**
- [x] Calcular área mediana por tipo (Apartamento, Casa, Lote, etc.)
- [x] Crear boxplot área × tipo de propiedad
- [x] Calcular área mediana por ciudad focal
- [x] Crear gráfico comparativo de área por ciudad
- [x] Documentar diferencias entre tipos

**Relación área-precio**
- [x] Calcular correlación área-precio
- [x] Crear scatterplot área vs precio (muestra)
- [x] Scatterplot facetado por tipo de propiedad
- [x] Analizar relación por ciudad (¿lineal?, ¿log-lineal?)
- [x] Documentar hallazgos de elasticidad precio-área

---

## Sección 8: Variables Categóricas
**Notebook:** `notebooks/07_EDA_variables_categoricas.ipynb`

**Tipo de propiedad**
- [x] Calcular distribución de tipos de propiedad
- [x] Crear gráfico barras de top 8 tipos
- [x] Calcular % por tipo
- [x] Documentar tipos minoritarios

**Volumen temporal y geográfico**
- [x] Calcular registros por año (gráfico barras)
- [x] Calcular registros por ciudad top 12 (gráfico barras)
- [x] Crear tabla cruzada ciudad × año
- [x] Identificar ciudades con cobertura insuficiente
- [x] Documentar períodos con baja cobertura

---

## Sección 9: Matriz de Correlaciones
**Notebook:** `notebooks/07_EDA_variables_categoricas.ipynb`

**Correlaciones de variables numéricas**
- [x] Seleccionar variables numéricas (price, area, rooms, bathrooms, parking, estrato)
- [x] Calcular matriz de correlación
- [x] Visualizar heatmap de correlaciones (triangular)
- [x] Rankear variables por correlación con precio
- [x] Documentar multicolinealidad entre predictores

---

## Sección 10: Análisis Geoespacial (si lat/lon disponibles)
**Notebook:** `notebooks/08_EDA_geoespacial_macrovariables.ipynb`

**Validación de coordenadas**
- [x] Verificar rango válido de lat/lon para Colombia
- [x] Calcular % de registros con coordenadas válidas (~61%)
- [x] Identificar ciudades con mejor cobertura geoespacial
- [x] Crear mapa interactivo de distribución de puntos
- [x] Documentar limitaciones geoespaciales

---

## Sección 11: Variables Macroeconómicas
**Notebook:** `notebooks/08_EDA_geoespacial_macrovariables.ipynb`

**Cargar y limpiar macrovariables**
- [x] Cargar salario mínimo histórico
- [x] Limpiar nombres de columnas (convertir a inglés/estándar)
- [x] Filtrar años 2015–2024
- [x] Crear series anuales de IPC, tasa hipotecaria
- [x] Crear tabla consolidada de macrovariables (`data/processed/macrovariables_consolidadas.csv`)

**Visualización de tendencias macro**
- [x] Gráfico de salario mínimo por año
- [x] Gráfico de inflación anual (IPC %)
- [x] Gráfico de tasa hipotecaria por año
- [x] Comparar crecimiento nominal vs real del salario
- [x] Documentar períodos de estrés (2022–2023)

---

## Sección 12: Índice de Accesibilidad Habitacional (IAH) Preliminar
**Notebook:** `notebooks/09_EDA_IAH_preliminar.ipynb`

**Cálculo del IAH**
- [x] Calcular precio mediano nacional por año
- [x] Obtener salario mínimo anual del dataset B
- [x] Calcular IAH = precio_mediano / (salario_anual)
- [x] Crear serie histórica de IAH (2015–2024)
- [x] Calcular IAH por ciudad focal

**Análisis y visualización de IAH**
- [x] Graficar IAH nacional con línea de tendencia
- [x] Agregar líneas de referencia (5, 10, 20 años)
- [x] Calcular crecimiento porcentual del IAH
- [x] Graficar IAH por ciudad (líneas múltiples)
- [x] Documentar hallazgo principal: deterioro de accesibilidad

---

## Sección 13: Análisis de Desempleo por Ciudad
**Notebook:** `notebooks/08_EDA_geoespacial_macrovariables.ipynb`

**Preparación de datos de desempleo**
- [x] Cargar datos de desempleo GEIH (B5)
- [x] Limpiar nombres de ciudades (estandarizar)
- [x] Agregar a desempleo anual por ciudad
- [x] Filtrar años 2015–2024

**Visualización de desempleo**
- [x] Crear heatmap desempleo × ciudad × año
- [x] Ranking de ciudades por desempleo promedio
- [x] Líneas de tendencia de desempleo por ciudad
- [x] Calcular correlación entre desempleo y precio
- [x] Documentar relación desempleo-accesibilidad

---

## Sección 14: Validación Cruzada con Datos Oficiales
**Notebook:** `notebooks/10_EDA_validacion_oficial.ipynb`

**Comparar contra IPVU/IPVN DANE**
- [x] Cargar IPVU trimestral oficial
- [x] Cargar IPVN trimestral oficial
- [x] Convertir a series anuales
- [x] Comparar precios derivados de datasets vs IPVU/IPVN
- [x] Documentar desviaciones y causas

---

## Sección 15: Reporte Consolidado de Hallazgos
**Notebook:** `notebooks/11_EDA_reporte_consolidado.ipynb`

**Resumen ejecutivo**
- [x] Listar 13 hallazgos principales (H1–H13)
- [x] Crear tabla resumen de decisiones para Fase 3
- [x] Documentar problemas identificados por dataset
- [x] Proponer acciones correctivas

**Guardado de resultados**
- [x] Guardar todas las figuras en `docs/figures/` (formato PNG 150 dpi / HTML)
- [x] Guardar tablas intermedias en `data/processed/` (formato CSV con encoding UTF-8)
- [x] Crear archivo de hallazgos en Markdown (`docs/HALLAZGOS_FASE_2.md`)
- [x] Exportar reporte de calidad en CSV (`data/processed/reporte_calidad_datasets.csv`)
- [x] Actualizar metadatos del proyecto(`data/processed/metadatos_fase_2.json`)

---

## Sección 16: Preparación para GitHub

**Documentación y versionado**
- [x] Documentar todas las decisiones metodológicas en FASE_2_COMPLETA.md
- [x] Verificar que todas las rutas sean **relativas** (no rutas absolutas con usuario)
- [ ] Revisar que NO hay archivos sensibles (contraseñas, tokens, API keys)

**Validación pre-push a GitHub**
- [x] Verificar que NO hay rutas absolutas de usuario (p.ej. `C:\Users\...`)
- [x] Verificar que el notebook no referencia directorios que no existen en el repo
- [x] Confirmar que todas las figuras se guardaron en `docs/figures/` (31 figuras)
- [x] Confirmar que todos los CSV se guardaron en `data/processed/` (11 archivos)

**Git workflow**
- [x] Adicionar cambios generales

**Actualización de documentación del repo**
- [x] Actualizar `README.md` con referencia a Fase 2
- [x] Actualizar tabla de fases en `README.md` (marcar Fase 2 como completada)
- [x] Crear `docs/FASE_2_COMPLETA.md` con hallazgos resumidos (incluir análisis A7 Villavicencio)

---

## Sección 17: .gitignore y configuración de archivos
**ANTES de push — Verificar .gitignore**
- [x] `.gitignore` incluye `data/raw/` (los CSV/XLSX no se suben)
- [x] `.gitignore` incluye `.ipynb_checkpoints/`
- [x] `.gitignore` incluye `*.pyc` y `__pycache__/`
- [x] `.gitignore` incluye archivos temporales (`.tmp`, `*.log`)
- [x] Confirmar que `notebooks/*.ipynb` NO están en gitignore
- [x] Confirmar que `docs/figures/` NO está en gitignore
- [x] Confirmar que `data/processed/` NO está en gitignore
