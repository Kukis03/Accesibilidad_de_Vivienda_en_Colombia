# Fase 2 — Comprensión de los Datos
## Notebook: `notebooks/01_EDA.ipynb`
**Tareas por hacer en el notebook** (sin ejemplos implementados)

---

## Sección 1: Inventario de Fuentes y Carga Inicial
**Celdas 1–5: Importaciones y setup**
- [ ] Importar pandas, numpy, matplotlib, seaborn, plotly
- [ ] Configurar estilo de gráficos y opciones de visualización
- [ ] Definir rutas relativas: `data/raw/`, `data/processed/`, `docs/figures/`
- [ ] Verificar que las carpetas existen; crearlas si es necesario
- [ ] Configurar logging para documentar operaciones

**Celdas 6–10: Carga y verificación de datasets Grupo A**
- [ ] Cargar A1 (A1_colombia_housing_properties.csv) — Properati Colombia (fuente principal, ~998K registros)
- [ ] Cargar A2 (A2_fincaraiz_colombia.csv) — FincaRaiz Colombia 2023-2024
- [ ] Cargar A3 (A3_colombia_house_prediction.csv) — Colombia House Prediction
- [ ] Cargar A4 (A4_real_estate_bogota.csv) — Real Estate Bogotá por barrio
- [ ] Cargar A5 (A5_medellin_properties_2023.csv) — Medellín Properties 2023
- [ ] Cargar A6 (A6_real_estate_bogota_2023.csv) — Real Estate Bogotá 2023
- [ ] Cargar A7 (A7_fincaraiz_villavicencio_scraping.csv) — Scraping FincaRaiz Villavicencio
- [ ] Cargar A8 (A8_carac_pre_viv_nueva.csv) — Características precios vivienda nueva Bogotá UPZ
- [ ] Registrar tamaño y número de registros de cada dataset (incluir A7)

**Celdas 11–15: Carga y verificación de datasets Grupo B**
- [ ] Cargar B1 (B1_indices_precios_vivienda.csv) — IPVN+IPVU unificado (BanRep + DANE)
- [ ] Cargar B2 (B2_tasa_hipotecaria_semanal.csv) — Tasa hipotecaria semanal (BanRep)
- [ ] Cargar B3 (B3_salario_minimo_historico.csv) — Salario mínimo histórico (DANE)
- [ ] Cargar B4 (B4_ipc_colombia_anual.csv) — IPC anual (DANE)
- [ ] Cargar B5 (B5_geih_empleo_colombia.csv) — GEIH empleo mensual (DANE)
- [ ] Cargar B6 (B6_qcon_confianza_constructora.csv) — Confianza constructora (Fedesarollo)
- [ ] Cargar B7 (B7_qcon_licencias_construccion.csv) — Licencias construcción (Fedesarollo)
- [ ] Cargar B8 (B8_geo_estados_localidades.csv) — Estados/localidades geográficas
- [ ] Crear tabla resumen de inventario (filas, columnas, período)
- [ ] Guardar reporte de inventario en CSV

---

## Sección 2: Estructura de Columnas — Esquema Canónico
**Celdas 16–20: Exploración de columnas por dataset**
- [ ] Listar columnas reales de A1
- [ ] Listar columnas reales de A4
- [ ] Listar columnas reales de A5
- [ ] Listar tipos de datos de cada dataset
- [ ] Crear diccionario de mapeo canónico (nombre original → nombre estándar)

**Celdas 21–25: Documentación de esquemas**
- [ ] Crear tabla de esquema para A1 (columna, tipo, descripción, mapeo)
- [ ] Crear tabla de esquema para A4 (Properati)
- [ ] Crear tabla de esquema para A5 (FincaRaiz)
- [ ] Crear tabla de esquema consolidada para A2, A3, A6, A7, A8
- [ ] Identificar columnas problemáticas (inconsistencias de nombres, tipos)

---

## Sección 3: Calidad de Datos — Diagnóstico Inicial
**Celdas 26–30: Estadísticas de calidad por dataset**
- [ ] Calcular filas, columnas y tamaño en memoria para cada dataset
- [ ] Calcular % de valores nulos por columna
- [ ] Calcular número de duplicados exactos
- [ ] Calcular % de registros con precio nulo
- [ ] Calcular % de registros con área nula
- [ ] Crear tabla resumen de calidad (Grupo A y B)

**Celdas 31–35: Análisis de nulos**
- [ ] Visualizar mapa de calor de nulos (muestra)
- [ ] Calcular porcentaje de nulos por columna (gráfico barras)
- [ ] Verificar si nulos en 'área' están correlacionados con ciudad/año
- [ ] Documentar patrones de nulos por ciudad
- [ ] Guardar reporte de nulos en CSV

---

## Sección 4: Distribución de Precios
**Celdas 36–40: Estadísticas descriptivas de precio**
- [ ] Calcular min, Q1, mediana, Q3, max, mean de precio (A1)
- [ ] Calcular P1 y P99
- [ ] Identificar registros con precio <= 0 o nulo
- [ ] Visualizar distribución en escala original (histograma)
- [ ] Visualizar distribución en escala log (histograma)
- [ ] Crear boxplot de precio

**Celdas 41–45: Outliers de precio**
- [ ] Identificar precios < $10M COP (outliers bajos)
- [ ] Identificar precios > $5.000M COP (outliers altos)
- [ ] Calcular % de outliers
- [ ] Mostrar 5 registros con precio más bajo
- [ ] Mostrar 5 registros con precio más alto
- [ ] Documentar hallazgos sobre outliers

---

## Sección 5: Análisis Geográfico — Precios por Ciudad
**Celdas 46–50: Precio mediano por ciudad**
- [ ] Calcular precio mediano por ciudad (top 15 por volumen)
- [ ] Crear tabla: ciudad, precio_mediano, Q1, Q3, N_registros
- [ ] Crear gráfico barras horizontal (precio por ciudad)
- [ ] Ranking de ciudades por precio
- [ ] Documentar segmentación de ciudades (alta, media, baja)

**Celdas 51–55: Precio por m² por ciudad**
- [ ] Calcular precio/m² por registro
- [ ] Filtrar outliers en precio/m² (< $500K o > $20M COP/m²)
- [ ] Calcular mediana de precio/m² por ciudad
- [ ] Crear tabla: ciudad, precio_mediano_m2, precio_medio_m2
- [ ] Visualizar precio/m² por ciudad (gráfico comparativo)

---

## Sección 5-bis: Refuerzo de Cobertura — Villavicencio (Dataset A7)
**Celdas 56–58: Cargar y explorar datos de scraping de Villavicencio**
- [ ] Cargar dataset A7 (A7_fincaraiz_villavicencio_scraping.csv)
- [ ] Explorar estructura de columnas de A7
- [ ] Calcular volumen de registros en A7
- [ ] Documentar período cubierto por scraping (fecha inicio-fin)
- [ ] Comparar volumen A7 vs cobertura de Villavicencio en A1

**Celdas 59–61: Integración de fuentes complementarias para Villavicencio**
- [ ] Cargar IPVN DANE trimestral (incluye Villavicencio AU)
- [ ] Cargar boletines CENAC si están disponibles
- [ ] Convertir IPVN trimestral a anual
- [ ] Relacionar precios de scraping con índices oficiales IPVN
- [ ] Validar consistencia de precios A7 vs IPVN DANE

**Celdas 62–64: Análisis especial de Villavicencio**
- [ ] Calcular estadísticas descriptivas de precio para Villavicencio (A1 + A7 consolidados)
- [ ] Precio mediano de Villavicencio en cada año (2015–2024)
- [ ] Comparar precio/m² de Villavicencio vs ciudades similares (Ibagué, Cúcuta)
- [ ] Distribución de tipos de propiedad en Villavicencio
- [ ] Documentar calidad de datos A7 (completitud, nulos, duplicados)
- [ ] Crear visualización de Villavicencio en contexto nacional

**Celdas 65–67: Documentación de estrategia A7**
- [ ] Documentar que A7 es dataset generado internamente (scraping)
- [ ] Especificar fechas de scraping y fuente (FincaRaiz)
- [ ] Documentar metodología de scraping (en notebook o linked script)
- [ ] Explicar por qué Villavicencio requiere refuerzo (cobertura insuficiente en A1)
- [ ] Guardar subset de Villavicencio consolidado en `data/processed/villavicencio_consolidado.csv`

---

## Sección 6: Evolución Temporal de Precios
**Celdas 56–60: Crear columna de año y filtrar período**
- [ ] Extraer año de columna de fecha
- [ ] Filtrar registros con año entre 2015–2024
- [ ] Calcular volumen de registros por año
- [ ] Documentar cobertura temporal por dataset

**Celdas 61–65: Tendencia nacional**
- [ ] Calcular precio mediano nacional por año
- [ ] Calcular precio mediano por año y ciudad (principales)
- [ ] Visualizar línea de tendencia nacional (2015–2024)
- [ ] Visualizar líneas de tendencia por ciudad focal
- [ ] Documentar crecimiento porcentual acumulado

**Celdas 66–70: Hallazgos temporales**
- [ ] Calcular CAGR (tasa de crecimiento anual) nacional
- [ ] Calcular CAGR por ciudad
- [ ] Comparar crecimiento entre ciudades
- [ ] Identificar años con mayor/menor crecimiento
- [ ] Documentar efecto pandemia (2020–2021)

---

## Sección 7: Análisis de Área Construida
**Celdas 70–74: Distribución de área**
- [ ] Filtrar área válida (> 10 m², < 800 m²)
- [ ] Calcular estadísticas descriptivas (min, Q1, mediana, Q3, max)
- [ ] Visualizar histograma de distribución de área
- [ ] Identificar valores atípicos en área
- [ ] Calcular % de registros sin área

**Celdas 73–77: Área por tipo de propiedad**
- [ ] Calcular área mediana por tipo (Apartamento, Casa, Lote, etc.)
- [ ] Crear boxplot área × tipo de propiedad
- [ ] Calcular área mediana por ciudad focal
- [ ] Crear gráfico comparativo de área por ciudad
- [ ] Documentar diferencias entre tipos

**Celdas 78–82: Relación área-precio**
- [ ] Calcular correlación área-precio
- [ ] Crear scatterplot área vs precio (muestra)
- [ ] Scatterplot facetado por tipo de propiedad
- [ ] Analizar relación por ciudad (¿lineal?, ¿log-lineal?)
- [ ] Documentar hallazgos de elasticidad precio-área

---

## Sección 8: Variables Categóricas
**Celdas 83–87: Tipo de propiedad**
- [ ] Calcular distribución de tipos de propiedad
- [ ] Crear gráfico barras de top 8 tipos
- [ ] Calcular % por tipo
- [ ] Documentar tipos minoritarios

**Celdas 88–92: Volumen temporal y geográfico**
- [ ] Calcular registros por año (gráfico barras)
- [ ] Calcular registros por ciudad top 12 (gráfico barras)
- [ ] Crear tabla cruzada ciudad × año
- [ ] Identificar ciudades con cobertura insuficiente
- [ ] Documentar períodos con baja cobertura

---

## Sección 9: Matriz de Correlaciones
**Celdas 93–97: Correlaciones de variables numéricas**
- [ ] Seleccionar variables numéricas (price, area, rooms, bathrooms, parking, estrato)
- [ ] Calcular matriz de correlación
- [ ] Visualizar heatmap de correlaciones (triangular)
- [ ] Rankear variables por correlación con precio
- [ ] Documentar multicolinealidad entre predictores

---

## Sección 10: Análisis Geoespacial (si lat/lon disponibles)
**Celdas 98–102: Validación de coordenadas**
- [ ] Verificar rango válido de lat/lon para Colombia
- [ ] Calcular % de registros con coordenadas válidas
- [ ] Identificar ciudades con mejor cobertura geoespacial
- [ ] Crear mapa interactivo de distribución de puntos
- [ ] Documentar limitaciones geoespaciales

---

## Sección 11: Variables Macroeconómicas
**Celdas 103–107: Cargar y limpiar macrovariables**
- [ ] Cargar salario mínimo histórico
- [ ] Limpiar nombres de columnas (convertir a inglés/estándar)
- [ ] Filtrar años 2015–2024
- [ ] Crear series anuales de IPC, tasa hipotecaria
- [ ] Crear table consolidada de macrovariables

**Celdas 108–112: Visualización de tendencias macro**
- [ ] Gráfico de salario mínimo por año
- [ ] Gráfico de inflación anual (IPC %)
- [ ] Gráfico de tasa hipotecaria por año
- [ ] Comparar crecimiento nominal vs real del salario
- [ ] Documentar períodos de estrés (2022–2023)

---

## Sección 12: Índice de Accesibilidad Habitacional (IAH) Preliminar
**Celdas 113–117: Cálculo del IAH**
- [ ] Calcular precio mediano nacional por año
- [ ] Obtener salario mínimo anual del dataset B
- [ ] Calcular IAH = precio_mediano / (salario_anual)
- [ ] Crear serie histórica de IAH (2015–2024)
- [ ] Calcular IAH por ciudad focal

**Celdas 118–122: Análisis y visualización de IAH**
- [ ] Graficar IAH nacional con línea de tendencia
- [ ] Agregar líneas de referencia (5, 10, 20 años)
- [ ] Calcular crecimiento porcentual del IAH
- [ ] Graficar IAH por ciudad (líneas múltiples)
- [ ] Documentar hallazgo principal: deterioro de accesibilidad

---

## Sección 13: Análisis de Desempleo por Ciudad
**Celdas 123–127: Preparación de datos de desempleo**
- [ ] Cargar datos de desempleo trimestral
- [ ] Limpiar nombres de ciudades (estandarizar)
- [ ] Agregar a desempleo anual por ciudad
- [ ] Filtrar años 2015–2024

**Celdas 128–132: Visualización de desempleo**
- [ ] Crear heatmap desempleo × ciudad × año
- [ ] Ranking de ciudades por desempleo promedio
- [ ] Líneas de tendencia de desempleo por ciudad
- [ ] Calcular correlación entre desempleo y precio
- [ ] Documentar relación desempleo-accesibilidad

---

## Sección 14: Validación Cruzada con Datos Oficiales
**Celdas 133–137: Comparar contra IPVU/IPVN DANE**
- [ ] Cargar IPVU trimestral oficial
- [ ] Cargar IPVN trimestral oficial
- [ ] Convertir a series anuales
- [ ] Comparar precios derivados de datasets vs IPVU/IPVN
- [ ] Documentar desviaciones y causas

---

## Sección 15: Reporte Consolidado de Hallazgos
**Celdas 138–142: Resumen ejecutivo**
- [ ] Listar 13 hallazgos principales (H1–H13)
- [ ] Crear tabla resumen de decisiones para Fase 3
- [ ] Documentar problemas identificados por dataset
- [ ] Proponer acciones correctivas

**Celdas 143–147: Guardado de resultados**
- [ ] Guardar todas las figuras en `docs/figures/` (formato PNG 150 dpi)
- [ ] Guardar tablas intermedias en `data/processed/` (formato CSV con encoding UTF-8)
- [ ] Crear archivo de hallazgos en Markdown (`docs/HALLAZGOS_FASE_2.md`)
- [ ] Exportar reporte de calidad en CSV (`data/processed/reporte_calidad_datasets.csv`)
- [ ] Actualizar metadatos del proyecto (versión del notebook, fecha)

---

## Sección 16: Preparación para GitHub
**Celdas 148–152: Documentación y versionado**
- [ ] Crear celda Markdown con metadatos del notebook (autor, fecha, versión)
- [ ] Documentar todas las decisiones metodológicas en el notebook
- [ ] Verificar que todas las rutas sean **relativas** (no rutas absolutas con usuario)
- [ ] Agregar comentarios en código explicando transformaciones clave
- [ ] Crear celda de resumen: "Este notebook genera X figuras y Y tablas en..."

**Celdas 153–157: Validación pre-push a GitHub**
- [ ] Ejecutar todas las celdas en kernel limpio (Restart & Run All)
- [ ] Verificar que NO hay rutas absolutas de usuario (p.ej. `C:\Users\...`)
- [ ] Verificar que el notebook no referencia directorios que no existen en el repo
- [ ] Confirmar que todas las figuras se guardaron en `docs/figures/`
- [ ] Confirmar que todos los CSV se guardaron en `data/processed/`
- [ ] Revisar que NO hay archivos sensibles (contraseñas, tokens, API keys)

**Celdas 158–162: Git workflow**
- [ ] Adicionar cambios: `git add notebooks/01_EDA.ipynb`
- [ ] Adicionar figuras: `git add docs/figures/`
- [ ] Adicionar archivos procesados: `git add data/processed/`
- [ ] Escribir commit message descriptivo (p.ej. "feat: Fase 2 - EDA completo con Villavicencio")
- [ ] Push a rama development: `git push origin development`

**Celdas 163–167: Actualización de documentación del repo**
- [ ] Actualizar `README.md` con referencia al notebook (enlace a `notebooks/01_EDA.ipynb`)
- [ ] Actualizar tabla de fases en `README.md` (marcar Fase 2 como completada)
- [ ] Agregar lista de outputs en `data/processed/README.md` (incluir villavicencio_consolidado.csv)
- [ ] Agregar lista de figuras en `docs/figures/README.md`
- [ ] Crear o actualizar `docs/FASE_2_COMPLETA.md` con hallazgos resumidos (incluir análisis A7 Villavicencio)

---

## Sección 17: .gitignore y configuración de archivos
**ANTES de push — Verificar .gitignore**
- [ ] `.gitignore` incluye `data/raw/` (los CSV/XLSX no se suben)
- [ ] `.gitignore` incluye `.ipynb_checkpoints/`
- [ ] `.gitignore` incluye `*.pyc` y `__pycache__/`
- [ ] `.gitignore` incluye archivos temporales (`.tmp`, `*.log`)
- [ ] Confirmar que `notebooks/01_EDA.ipynb` NO está en gitignore (sí debe subirse)
- [ ] Confirmar que `docs/figures/` NO está en gitignore (figuras generadas deben subirse)
- [ ] Confirmar que `data/processed/` NO está en gitignore (outputs procesados deben subirse)
- [ ] Cargar y limpiar datos de tasa hipotecaria mensual (1998–2025)
- [ ] Cargar y limpiar datos de desempleo por ciudad (trimestral) — dataset GEIH DANE pendiente de re-descarga
- [ ] Cargar y limpiar datos de IPVU trimestral
- [ ] Cargar y limpiar datos de IPVN trimestral

## 13. Visualización de la Evolución Macroeconómica
- [ ] Graficar evolución del salario mínimo (2015–2024)
- [ ] Graficar evolución del IPC/inflación anual
- [ ] Graficar evolución de la tasa hipotecaria
- [ ] Comparar crecimiento nominal vs real del salario
- [ ] Documentar períodos de estrés financiero (2022–2023)

## 14. Cálculo Preliminar del IAH (Índice de Accesibilidad Habitacional)
- [ ] Calcular IAH preliminar nacional (precio mediano / salario anual)
- [ ] Calcular serie histórica de IAH (2015–2024)
- [ ] Comparar IAH nacional contra umbral OCDE (5 años accesible)
- [ ] Documentar deterioro de accesibilidad
- [ ] Graficar IAH histórico con umbrales de referencia

## 15. Análisis de Desempleo por Ciudad
- [ ] Calcular tasa promedio de desempleo por ciudad (2015–2024)
- [ ] Crear heatmap desempleo × ciudad × año
- [ ] Identificar ciudades con mayor/menor desempleo
- [ ] Analizar correlación entre desempleo y precio de vivienda
- [ ] Documentar ciudades con mayor volatilidad de empleo

## 16. Reporte Consolidado de Calidad de Datos
- [ ] Generar reporte de calidad completo por dataset (A1–A8, B1–B8)
- [ ] Documentar problemas identificados en cada dataset
- [ ] Proponer acciones correctivas para Fase 3
- [ ] Crear tabla de decisiones por dataset
- [ ] Estimar pérdida de datos por limpieza

## 17. Tabla de Cobertura Ciudad–Año
- [ ] Crear tabla cruzada ciudad × año (2015–2024)
- [ ] Registrar número de observaciones por ciudad-año
- [ ] Identificar ciudades con cobertura insuficiente (< 500 registros)
- [ ] Documentar períodos con mayor/menor volumen de datos

## 18. Estrategia de Integración de Datasets para Fase 3
- [ ] Definir dataset base (probablemente A1)
- [ ] Definir orden de concatenación con datasets complementarios (A2–A8)
- [ ] Definir estrategia de deduplicación
- [ ] Documentar cambios esperados en volumen de datos
- [ ] Proponer cálculos de Fase 3 basados en hallazgos

## 19. Validación Cruzada con Datos Oficiales
- [ ] Comparar precios medios contra IPVU del DANE (disponibles por ciudad)
- [ ] Verificar consistencia de tendencias
- [ ] Documentar desviaciones significativas
- [ ] Explicar causas de divergencias (si existen)

## 20. Reporte Final de Fase 2
- [ ] Documentar todos los hallazgos principales (H1–H13)
- [ ] Crear documento ejecutivo (1–2 páginas)
- [ ] Guardar todas las figuras en `docs/figures/`
- [ ] Guardar datos intermedios en `data/processed/`
- [ ] Transferir decisiones a documento de preparación (Fase 3)
- [ ] Actualizar README del proyecto con hallazgos clave