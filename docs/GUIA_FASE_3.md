# Fase 3 — Preparación de los Datos
## Notebook: `notebooks/02_preparacion_datos.ipynb` / Script: `notebooks/02_preparacion_datos.py`
**Responsable:** Kukis · **Apoyo:** Steve  
**Insumo:** `data/raw/` (16 CSVs) + hallazgos de Fase 2  
**Entregable principal:** `data/processed/vivienda_colombia_limpio.csv`  
**Objetivo:** Dataset consolidado ~250K–370K registros (2020–2024), 0 nulos en variables críticas  
**Semanas:** 5 – 6

---

> ⚠️ **Lección aprendida:** La primera ejecución perdió el 94% por 5 bugs. Esta guía los corrige.
> Los cambios clave respecto a la versión anterior están marcados con **⚠️**.

---

## Sección 1: Setup y Carga de Datos
**Importaciones y rutas**
- [ ] Importar pandas, numpy, os, re
- [ ] Definir `DIR_RAW = "data/raw"`, `DIR_PROCESSED = "data/processed"`
- [ ] Crear `data/processed/` con `os.makedirs(..., exist_ok=True)`
- [ ] Definir `COLS_CANONICAS`: `['price', 'area', 'rooms', 'bathrooms', 'property_type', 'city', 'lat', 'lon', 'created_on', 'barrio', 'parking', 'estrato', 'fuente']`
- [ ] Definir `TRM_HISTORICA` por año (2015–2024)
- [ ] Crear función `registrar_metrica()` para el reporte de limpieza

**Carga de los 8 datasets — aplicar mapeo al esquema canónico:**

- [ ] **A1 Properati** — Filtrar `operation_type == 'Venta'`. Renombrar: `bedrooms→rooms`, `bathrooms→bathrooms`, `property_type→property_type`, `l3→city`, `start_date→created_on`, `surface_total→area`. Agregar `fuente = 'A1_Properati'`
- [ ] **⚠️ A2 FincaRaiz** — Renombrar: `Precio→price`, `Area Construida→area`, `Habitaciones→rooms`, `Banos→bathrooms`, `Tipo Propiedad→property_type`, `Ciudad→city`, `Estrato→estrato`. Limpiar precio con regex. **NO multiplicar por 1,000,000** (el precio ya está en COP completos). Agregar `fuente = 'A2_FincaRaiz_Kaggle'`
- [ ] **⚠️ A3 HousePrediction** — Renombrar: `valor→price`, `area→area`, `habitaciones→rooms`, `banos→bathrooms`, `estrato→estrato`. **Asignar `city = 'Bogotá'`** (coordenadas corresponden a Bogotá). Si no existe `property_type`, dejar NaN (se mapea después). Agregar `fuente = 'A3_Kaggle'`
- [ ] **A4 Bogotá** — Mapeo difuso de columnas. Asignar `city = 'Bogotá'`. Agregar `fuente = 'A4_Bogota_Kaggle'`
- [ ] **A5 Medellín** — Renombrar: `price→price`, `area→area`, `rooms→rooms`, `baths→bathrooms`, `property_type→property_type`, `neighbourhood→barrio`, `stratum→estrato`. Asignar `city = 'Medellín'`. Agregar `fuente = 'A5_Medellin_Kaggle'`
- [ ] **A6 Bogotá 2023** — Mapeo difuso de columnas. Asignar `city = 'Bogotá'`. Agregar `fuente = 'A6_Bogota2023_Kaggle'`
- [ ] **⚠️ A7 Villavicencio** — **Agregar renombre** (no estaba en la versión anterior): `precio_cop→price`, `area_m2→area`, `habitaciones→rooms`, `banos→bathrooms`, `tipo_inmueble→property_type`, `ciudad→city`, `fecha_scraping→created_on`. Filtrar `tipo_operacion == 'Venta'`. Filtrar solo `city == 'Villavicencio'`. Agregar `fuente = 'A7_Scraping_Villavicencio'`
- [ ] **⚠️ A8 Caracol UPZ** — **Agregar renombre**: `precios→price`, `area→area`, `alcobas→rooms`, `baños→bathrooms`. Asignar `city = 'Bogotá'`, `property_type = 'Apartamento'`. Agregar `fuente = 'A8_CaracPreVivNueva'`

- [ ] Agregar columnas faltantes como NaN a cada dataset antes de concatenar
- [ ] Concatenar con `pd.concat(..., ignore_index=True)` usando solo `COLS_CANONICAS`
- [ ] Imprimir total registros (esperado: ~880,000)
- [ ] Registrar métrica en reporte_limpieza.csv

---

## Sección 2: Limpieza de Precios y Monedas
- [ ] Extraer año temporal desde `created_on` para aplicar TRM
- [ ] Convertir precios USD → COP en Properati A1 si existe columna `currency`
- [ ] Detectar y corregir precios en COP/m² (precio < 1,000,000 y area > 10): multiplicar por área
- [ ] Eliminar registros con `price` nulo
- [ ] Eliminar registros con `price < 10,000,000` (errores)
- [ ] Eliminar registros con `price > 10,000,000,000` (outliers extremos)
- [ ] Imprimir registros restantes
- [ ] Registrar métrica

---

## Sección 3: Estandarización de Ciudades ⚠️ CORREGIDO
- [ ] Definir `MAPA_CIUDADES` con todas las variantes conocidas → 12 ciudades focales
- [ ] **⚠️ NO usar `normalize('NFKD').encode('ascii', errors='ignore')`** — eso corrompe las tildes en el CSV
- [ ] Normalizar solo con `.str.lower().str.strip()` — mantener UTF-8
- [ ] Aplicar el mapa de ciudades
- [ ] Filtrar y conservar solo las 12 ciudades canónicas
- [ ] Renombrar columna limpia a `city`
- [ ] Imprimir distribución por ciudad
- [ ] Registrar métrica

---

## Sección 4: Filtro Temporal (2019–2024)
**Nota:** No hay datos de 2019 en ninguna fuente. El rango real comienza en 2020.
- [ ] Convertir `created_on` a datetime con `errors='coerce'`
- [ ] Extraer columna `year`
- [ ] Imputar `year` nulo usando año típico por fuente
- [ ] Filtrar registros con `year` entre 2019 y 2024
- [ ] Imprimir distribución por año
- [ ] Registrar métrica

---

## Sección 5: Estandarización de Tipo de Propiedad
- [ ] Definir `MAPA_PROPIEDADES`: variantes de "apartamento" / "casa" → categorías canónicas
- [ ] **⚠️ Incluir variantes adicionales:** `'casa con conjunto cerrado': 'Casa'` (existe en A6)
- [ ] Normalizar columna: minúsculas, strip
- [ ] Aplicar mapa; conservar solo `'Casa'` y `'Apartamento'`
- [ ] Imprimir distribución por tipo
- [ ] Registrar métrica

---

## Sección 6: Eliminación de Outliers por Grupo (IQR)
- [ ] Agrupar por `['city', 'year', 'property_type']`
- [ ] Para grupos ≥ 10 registros: percentiles 2.5 y 97.5 de `price`; eliminar fuera del rango
- [ ] Para grupos ≥ 10 registros: percentiles 1 y 99 de `area`; eliminar fuera del rango (solo donde `area` no sea nulo)
- [ ] Conservar grupos < 10 registros sin filtrar
- [ ] Imprimir registros restantes
- [ ] Registrar métrica

---

## Sección 7: Deduplicación Inter-Dataset ⚠️ CORREGIDO
**La versión anterior incluía `rooms` y `bathrooms` en la clave, eliminando el 79.8% de los datos.**
- [ ] **⚠️ Construir `dup_key` SOLO con:** `city + "_" + round(price/1M) + "_" + round(area) + "_" + property_type + "_" + year`
- [ ] **⚠️ NO incluir `rooms` ni `bathrooms`** en la clave
- [ ] Definir orden de prioridad: A2 > A7 > A1 > A5 > A6 > A4 > A3 > A8
- [ ] Ordenar por prioridad; `drop_duplicates(subset='dup_key', keep='first')`
- [ ] Eliminar columnas temporales
- [ ] Imprimir registros finales (esperado: ~250K–370K)
- [ ] Registrar métrica

---

## Sección 8: Imputación de Valores Faltantes
- [ ] `area` — mediana de `(city, year, property_type)`; fallback mediana global de `property_type`
- [ ] `rooms` — mediana de `(city, property_type)`; fallback = 3; `clip(lower=1)`
- [ ] `bathrooms` — mediana de `(city, property_type)`; fallback = 2; `clip(lower=1)`
- [ ] `estrato` — mediana `(city, barrio)` → mediana `city` → fallback = 3; `clip(1, 6)`
- [ ] **⚠️ `lat`/`lon`** — imputar por centroide de ciudad ANTES de exportar (antes quedaban 32% nulos)
- [ ] Verificar 0 nulos en columnas críticas
- [ ] Imprimir tabla de nulos antes/después

---

## Sección 9: Integración de Variables Macroeconómicas
- [ ] Cargar B3 — salario mínimo por año (columnas: `Ano`, `Salario_minimo_mensual`)
- [ ] Cargar B4 — IPC anual: `ipc_var_anual`, `ipc_base2018` (base 2018 = 100, calculado iterativamente)
- [ ] Cargar B2 — tasa hipotecaria: extraer año de fecha, promedio anual de tasa de colocación
- [ ] Cargar B1 — IPVU/IPVN: variación anual por año
- [ ] **⚠️ Cargar B5** — intentar merge por `(year, city)`; fallback nacional (antes era solo nacional)
- [ ] Construir `df_macro`: merge B3 + B4 + B2 + B1 + B5 por `year`
- [ ] Merge principal: `df_inmuebles` + `df_macro` por `year` (left join)
- [ ] Si B5 tiene datos por ciudad, merge adicional por `(year, city)`
- [ ] Imputar `tasa_desempleo` nula con promedio del año
- [ ] Verificar cobertura del merge e imprimir %

---

## Sección 10: Construcción de Variables Derivadas
- [ ] `salario_anual = salario_mensual × 12`
- [ ] `IAH = price / salario_anual`
- [ ] `precio_real = price / (ipc_base2018 / 100)`
- [ ] `precio_m2 = price / area`
- [ ] Implementar `calcular_cuota_mensual(price, tasa_anual, meses=180, financia=0.70)` con amortización francesa: `r = (1 + tasa/100)^(1/12) - 1`
- [ ] Calcular `cuota_mensual` aplicando la función por fila
- [ ] `ratio_cuota_salario = cuota_mensual / salario_mensual`
- [ ] `nivel_accesibilidad`: `'Accesible'` (IAH ≤ 5), `'Moderado'` (5–10), `'Elevado'` (10–20), `'Crítico'` (>20)
- [ ] Imprimir estadísticas descriptivas de IAH, precio_real, precio_m2, cuota_mensual, ratio_cuota_salario

---

## Sección 11: Validación del Dataset Final
**Assertions de integridad**
- [ ] Verificar 0 nulos en columnas críticas
- [ ] Verificar `price > 0`
- [ ] Verificar `area > 0`
- [ ] Verificar `rooms >= 1` y `bathrooms >= 1`
- [ ] Verificar `city` en las 12 ciudades canónicas
- [ ] Verificar `year` entre 2019 y 2024
- [ ] Verificar `estrato` entre 1 y 6
- [ ] Imprimir validación aprobada con shape final

**Validación cruzada IPVN DANE**
- [ ] Calcular variación anual del `precio_m2` promedio por ciudad
- [ ] Comparar contra `ipvn_variacion_anual` del dataset B1
- [ ] Documentar diferencia (esperado < 0.5 pp para Bogotá y Medellín)

---

## Sección 12: Exportación
- [ ] **⚠️** Exportar dataset con `encoding='utf-8-sig'` (con BOM) para preservar tildes
- [ ] Crear `data/processed/README.md` con diccionario de columnas
- [ ] Guardar `data/processed/reporte_limpieza.csv`
- [ ] Imprimir confirmación: nombre del archivo y shape exportado

---

## Sección 13: Preparación para GitHub
- [ ] Verificar que NO hay rutas absolutas
- [ ] Ejecutar el script completo sin errores
- [ ] Verificar que el CSV generado tenga las 26 columnas y sin nulos en críticas
- [ ] Verificar encoding: tildes preservadas (Bogotá, Cúcuta, Ibagué, Medellín)
- [ ] Verificar que 2024 esté presente en el rango de años
- [ ] Confirmar `.gitignore` excluye `data/raw/` (o LFS)
- [ ] `git add notebooks/02_preparacion_datos.ipynb notebooks/02_preparacion_datos.py data/processed/`
- [ ] Commit: `"fix: Fase 3 - pipeline corregido"`
- [ ] Push a rama `development`
- [ ] Actualizar `docs/FASE_3_COMPLETA.md` con los resultados reales de la ejecución

---

## Resumen de Correcciones Clave

| # | Bug | Cambio | Impacto |
|---|-----|--------|---------|
| 1 | A2 precio × 1,000,000 | Quitar multiplicación | +142K registros (incluye 2024) |
| 2 | A3 sin city | Asignar `city = 'Bogotá'` | +145K registros |
| 3 | A7 sin renombre | Agregar mapeo de columnas | +900 registros |
| 4 | A8 sin renombre | Agregar mapeo + city | +32 registros |
| 5 | Dedup con rooms/bath | Clave simplificada a 5 campos | ~171K registros retenidos |
| 6 | Encoding corrupto | No forzar ascii; mantener UTF-8 | Tildes preservadas |
| 7 | lat/lon nulos | Imputar centroides antes de exportar | 0 nulos en coordenadas |
| 8 | 'casa c/ conjunto' faltante | Agregar a MAPA_PROPIEDADES | ~30 registros de A6 retenidos |

---

## Resultados Esperados

| Métrica | Versión anterior (bugs) | Versión corregida |
|---------|------------------------|-------------------|
| Registros finales | 54,904 | ~250,000–370,000 |
| Rango años | 2020–2023 | 2020–2024 |
| Año 2024 presente | ❌ | ✅ (de A2) |
| Fuentes supervivientes | 4 (A1, A4, A5, A6) | 7 (A1–A7 excepto A8) |
| IAH promedio | 33.3 años (sesgado) | ~18–22 años |
| Tildes en ciudades | Corruptas | Preservadas |
| Nulos en lat/lon | 32% | 0% |

---

## Entregables

| Archivo | Ruta |
|---------|------|
| Notebook | `notebooks/02_preparacion_datos.ipynb` |
| Script | `notebooks/02_preparacion_datos.py` |
| Dataset limpio | `data/processed/vivienda_colombia_limpio.csv` |
| Metadatos | `data/processed/README.md` |
| Reporte limpieza | `data/processed/reporte_limpieza.csv` |
| Documento de fase | `docs/FASE_3_COMPLETA.md` (actualizar tras ejecución) |
