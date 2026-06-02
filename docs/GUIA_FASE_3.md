# Fase 3 — Preparación de los Datos
## Notebook: `notebooks/02_preparacion_datos.ipynb`
**Responsable:** Kukis · **Apoyo:** Steve  
**Insumo:** `data/raw/` (16 CSVs) + hallazgos de Fase 2  
**Entregable principal:** `data/processed/vivienda_colombia_limpio.csv`  
**Semanas:** 5 – 6

---

## Sección 1: Setup y Carga de Datos
**Celdas 1–5: Importaciones y rutas**
- [ ] Importar pandas, numpy, os, re, joblib
- [ ] Definir rutas base: `DIR_RAW = "data/raw"`, `DIR_PROCESSED = "data/processed"`
- [ ] Crear carpeta `data/processed/` si no existe (`os.makedirs(..., exist_ok=True)`)
- [ ] Definir `COLS_CANONICAS`: `['price', 'area', 'rooms', 'bathrooms', 'property_type', 'city', 'lat', 'lon', 'created_on', 'barrio', 'parking', 'estrato', 'fuente']`
- [ ] Definir TRM histórica por año (2015–2024) para conversión USD → COP

**Celdas 6–14: Carga y canonización de los 8 datasets**
- [ ] Cargar A1 (Properati) — filtrar `l1 == 'Colombia'` y `operation_type == 'Venta'`; renombrar columnas al esquema canónico; agregar `fuente = 'A1_Properati'`
- [ ] Cargar A2 (FincaRaiz Kaggle) — renombrar columnas; escalar precio (`× 1_000_000` si viene en millones); agregar `fuente = 'A2_FincaRaiz_Kaggle'`
- [ ] Cargar A3 (Colombia House Prediction) — verificar nombres de columnas; agregar `fuente = 'A3_Kaggle'`
- [ ] Cargar A4 (Real Estate Bogotá) — asignar `city = 'Bogotá'`; agregar `fuente = 'A4_Bogota_Kaggle'`
- [ ] Cargar A5 (Medellín Properties) — asignar `city = 'Medellín'`; agregar `fuente = 'A5_Medellin_Kaggle'`
- [ ] Cargar A6 (Real Estate Bogotá 2023) — asignar `city = 'Bogotá'`; agregar `fuente = 'A6_Bogota2023_Kaggle'`
- [ ] Cargar A7 (Scraping Villavicencio) — verificar que el archivo existe; agregar `fuente = 'A7_Scraping_Villavicencio'`
- [ ] Cargar A8 (Vivienda nueva Bogotá UPZ) — agregar `fuente = 'A8_CaracPreVivNueva'`
- [ ] Agregar columnas faltantes como `NaN` a cada dataset antes de concatenar
- [ ] Concatenar los 8 DataFrames con `pd.concat(..., ignore_index=True)` usando solo `COLS_CANONICAS`
- [ ] Imprimir: `Total registros cargados antes de limpieza: {N:,}`

---

## Sección 2: Limpieza de Precios y Monedas
**Celdas 15–20: Conversión y filtros de precio**
- [ ] Extraer año temporal desde `created_on` (para aplicar TRM correcta por año)
- [ ] Convertir precios en USD de Properati (A1) a COP usando TRM histórica por año
- [ ] Detectar y corregir registros con precio en COP/m² (precio < 1_000_000 y area > 10): multiplicar por área
- [ ] Eliminar registros con `price` nulo
- [ ] Eliminar registros con `price < 10_000_000` (menos de $10M COP — probables errores)
- [ ] Eliminar registros con `price > 10_000_000_000` (más de $10,000M COP — outliers extremos)
- [ ] Imprimir registros restantes tras limpieza de precios

---

## Sección 3: Estandarización de Ciudades
**Celdas 21–25: Mapeo canónico de ciudades**
- [ ] Definir diccionario `MAPA_CIUDADES` con todas las variantes conocidas (minúsculas, sin tildes, alias) → nombre canónico para las 12 ciudades focales
- [ ] Normalizar columna `city`: convertir a minúsculas, strip, remover tildes para el matching
- [ ] Aplicar el mapa de ciudades
- [ ] Filtrar y conservar **solo** los registros de las 12 ciudades canónicas (descartar todo lo demás)
- [ ] Renombrar columna limpia a `city`
- [ ] Imprimir: `Registros en 12 ciudades focales: {N:,}` y distribución por ciudad

---

## Sección 4: Filtro Temporal (2019–2024)
**Celdas 26–30: Extracción y validación de año**
- [ ] Convertir `created_on` a datetime con `errors='coerce'`
- [ ] Extraer columna `year` (entero)
- [ ] Imputar `year` nulo usando año de publicación típico por fuente (diccionario `año_fuente`)
- [ ] Filtrar registros con `year` entre 2019 y 2024
- [ ] Imprimir distribución de registros por año

---

## Sección 5: Estandarización de Tipo de Propiedad
**Celdas 31–35: Mapeo a Casa / Apartamento**
- [ ] Definir diccionario `MAPA_PROPIEDADES`: todas las variantes de "apartamento" y "casa" → categorías canónicas
- [ ] Normalizar columna `property_type`: minúsculas, strip
- [ ] Aplicar el mapa; conservar **solo** `'Casa'` y `'Apartamento'`
- [ ] Imprimir distribución por tipo de propiedad

---

## Sección 6: Eliminación de Outliers por Grupo
**Celdas 36–42: IQR por ciudad × año × tipo**
- [ ] Agrupar el dataset por `['city', 'year', 'property_type']`
- [ ] Para grupos con ≥ 10 registros: calcular percentiles 2.5 y 97.5 de `price`; eliminar fuera del rango
- [ ] Para grupos con ≥ 10 registros: calcular percentiles 1 y 99 de `area`; eliminar fuera del rango (solo donde `area` no sea nulo)
- [ ] Conservar grupos con < 10 registros sin filtrar (para no perder datos históricos escasos)
- [ ] Imprimir registros restantes tras eliminación de outliers

---

## Sección 7: Deduplicación Inter-Dataset
**Celdas 43–48: Hash lógico por propiedad**
- [ ] Construir columna `dup_key`: concatenación de `city + round(price/1M) + round(area) + property_type + year`
- [ ] Definir orden de prioridad de fuentes: A7 > A2 > A1 > A6 > A5 > A4 > A3 > A8
- [ ] Ordenar por prioridad; aplicar `drop_duplicates(subset='dup_key', keep='first')`
- [ ] Eliminar columnas temporales (`dup_key`, `fuente_priority`)
- [ ] Imprimir registros finales tras deduplicación
- [ ] Crear tabla resumen del pipeline de limpieza (registros entrada → salida en cada paso)

---

## Sección 8: Imputación de Valores Faltantes
**Celdas 49–55: Imputación jerárquica**
- [ ] Imputar `area` nulo: mediana de grupo `(city, year, property_type)`; fallback con mediana global de `property_type`
- [ ] Imputar `rooms` nulo: mediana de grupo `(city, property_type)`; fallback = 3
- [ ] Imputar `bathrooms` nulo: mediana de grupo `(city, property_type)`; fallback = 2
- [ ] Imputar `estrato` nulo: primero por mediana de `(city, barrio)` si existe; luego por mediana de `city`; fallback = 3
- [ ] Aplicar `clip(1, 6)` sobre `estrato` y convertir a entero
- [ ] Verificar que el DataFrame no tiene nulos en las 6 columnas críticas: `price`, `area`, `rooms`, `bathrooms`, `city`, `property_type`
- [ ] Imprimir tabla de nulos antes y después de la imputación

---

## Sección 9: Integración de Variables Macroeconómicas
**Celdas 56–65: Carga y merge con Grupo B**
- [ ] Cargar B3 — `salario_mensual` por año (columnas esperadas: `year`, `salario_mensual`)
- [ ] Cargar B4 — agregar IPC a nivel anual: columnas `ipc_var_anual` e `ipc_base2018` (base 2018 = 100)
- [ ] Cargar B2 — extraer año de `Fecha`; calcular promedio anual de `tasa_hipotecaria_anual`
- [ ] Cargar B1 — separar IPVU e IPVN; calcular `ipvu_variacion_anual` e `ipvn_variacion_anual` por año
- [ ] Cargar B5 — estandarizar `city` con `MAPA_CIUDADES`; calcular `tasa_desempleo` promedio anual por `(year, city)`
- [ ] Construir `df_macro`: merge de B3 + B4 + B2 + B1 (cruce por `year`)
- [ ] Merge principal: `df_inmuebles` + `df_macro` por `year` (left join)
- [ ] Merge específico: resultado anterior + desempleo por `(year, city)` (left join)
- [ ] Imputar `tasa_desempleo` nula restante con el promedio nacional del año
- [ ] Verificar cobertura del merge: imprimir `% de registros con macro completa`

---

## Sección 10: Construcción de Variables Derivadas
**Celdas 66–72: Cálculo del IAH y métricas financieras**
- [ ] Calcular `salario_anual = salario_mensual × 12`
- [ ] Calcular `IAH = price / salario_anual` (años de salario mínimo para comprar)
- [ ] Calcular `precio_real = price / (ipc_base2018 / 100)` (COP constantes, base 2018)
- [ ] Calcular `precio_m2 = price / area`
- [ ] Implementar función `calcular_cuota_mensual(price, tasa_anual, meses=180, financia=0.70)` usando amortización francesa y conversión de tasa EA mensual: `r = (1 + tasa/100)^(1/12) − 1`
- [ ] Calcular `cuota_mensual` aplicando la función por fila
- [ ] Calcular `ratio_cuota_salario = cuota_mensual / salario_mensual`
- [ ] Calcular `nivel_accesibilidad`: `'Accesible'` (IAH ≤ 5), `'Moderado'` (5 < IAH ≤ 10), `'Elevado'` (10 < IAH ≤ 20), `'Crítico'` (IAH > 20)
- [ ] Imprimir estadísticas descriptivas de IAH, precio_real, precio_m2, cuota_mensual, ratio_cuota_salario

---

## Sección 11: Validación del Dataset Final
**Celdas 73–78: Assertions de integridad**
- [ ] Verificar 0 nulos en el dataset completo
- [ ] Verificar `price > 0` en todos los registros
- [ ] Verificar `area > 0` en todos los registros
- [ ] Verificar `rooms >= 1` y `bathrooms >= 1`
- [ ] Verificar `city` en las 12 ciudades canónicas
- [ ] Verificar `year` entre 2019 y 2024
- [ ] Verificar `estrato` entre 1 y 6
- [ ] Imprimir: `Validación de integridad aprobada. Shape final: (N filas, M columnas)`

**Celdas 79–82: Validación cruzada con IPVN DANE**
- [ ] Calcular variación anual del `precio_m2` promedio por ciudad
- [ ] Comparar contra `ipvn_variacion_anual` del dataset B1
- [ ] Documentar diferencia entre variación propia vs oficial (esperado < 0.5 pp para Bogotá y Medellín)

---

## Sección 12: Exportación y Documentación
**Celdas 83–88: Guardar outputs**
- [ ] Exportar dataset a `data/processed/vivienda_colombia_limpio.csv` (encoding UTF-8, sin índice)
- [ ] Crear `data/processed/README.md` con diccionario de columnas (descripción de cada campo)
- [ ] Guardar tabla de métricas del pipeline de limpieza en `data/processed/reporte_limpieza.csv`
- [ ] Imprimir confirmación: nombre del archivo y shape exportado

---

## Sección 13: Preparación para GitHub
**Celdas 89–95: Verificación y commit**
- [ ] Verificar que NO hay rutas absolutas en el notebook (`C:\Users\...`)
- [ ] Ejecutar todas las celdas en kernel limpio (Restart & Run All) sin errores
- [ ] Confirmar que `data/processed/vivienda_colombia_limpio.csv` se generó correctamente
- [ ] Confirmar que `.gitignore` excluye `data/raw/` (CSVs pesados no se suben)
- [ ] Confirmar que `data/processed/` sí está incluida en el repo
- [ ] `git add notebooks/02_preparacion_datos.ipynb data/processed/`
- [ ] Commit: `"feat: Fase 3 - pipeline de limpieza e integración macro completo"`
- [ ] Push a rama `development`
- [ ] Actualizar `README.md`: marcar Fase 3 como completada
- [ ] Crear `docs/FASE_3_COMPLETA.md` con hallazgos resumidos

---

## Entregables de Fase 3

| Archivo | Ruta | Descripción |
|---|---|---|
| Notebook de preparación | `notebooks/02_preparacion_datos.ipynb` | Pipeline completo de limpieza e integración |
| Dataset limpio | `data/processed/vivienda_colombia_limpio.csv` | Dataset consolidado con ~315K registros listos para modelado |
| Metadatos | `data/processed/README.md` | Diccionario de todas las columnas del dataset |
| Reporte de limpieza | `data/processed/reporte_limpieza.csv` | Tabla con registros entrada/salida por cada paso del pipeline |
| Documento de fase | `docs/FASE_3_COMPLETA.md` | Resumen de hallazgos y decisiones metodológicas |
