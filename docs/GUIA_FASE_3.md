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
- [x] Importar pandas, numpy, os, re
- [x] Definir `DIR_RAW = "data/raw"`, `DIR_PROCESSED = "data/processed"`
- [x] Crear `data/processed/` con `os.makedirs(..., exist_ok=True)`
- [x] Definir `COLS_CANONICAS`: `['price', 'area', 'rooms', 'bathrooms', 'property_type', 'city', 'lat', 'lon', 'created_on', 'barrio', 'parking', 'estrato', 'fuente']`
- [x] Definir `TRM_HISTORICA` por año para el período operativo 2020–2024 y años fuente necesarios para conversión
- [x] Crear función `registrar_metrica()` para el reporte de limpieza

**Carga de los 8 datasets — aplicar mapeo al esquema canónico:**

- [x] **A1 Properati** — Filtrar `operation_type == 'Venta'`. Renombrar: `bedrooms→rooms`, `bathrooms→bathrooms`, `property_type→property_type`, `l3→city`, `start_date→created_on`, `surface_total→area`. Agregar `fuente = 'A1_Properati'`
- [x] **⚠️ A2 FincaRaiz** — Renombrar: `Precio→price`, `Area Construida→area`, `Habitaciones→rooms`, `Banos→bathrooms`, `Tipo Propiedad→property_type`, `Ciudad→city`, `Estrato→estrato`. Limpiar precio con regex. **NO multiplicar por 1,000,000** (el precio ya está en COP completos). Agregar `fuente = 'A2_FincaRaiz_Kaggle'`
- [x] **⚠️ A3 HousePrediction** — Renombrar: `valor→price`, `area→area`, `habitaciones→rooms`, `banos→bathrooms`, `estrato→estrato`. **Asignar `city = 'Bogotá'`** (coordenadas corresponden a Bogotá). Si no existe `property_type`, dejar NaN (se mapea después). Agregar `fuente = 'A3_Kaggle'`
- [x] **A4 Bogotá** — Mapeo difuso de columnas. Asignar `city = 'Bogotá'`. Agregar `fuente = 'A4_Bogota_Kaggle'`
- [x] **A5 Medellín** — Renombrar: `price→price`, `area→area`, `rooms→rooms`, `baths→bathrooms`, `property_type→property_type`, `neighbourhood→barrio`, `stratum→estrato`. Asignar `city = 'Medellín'`. Agregar `fuente = 'A5_Medellin_Kaggle'`
- [x] **A6 Bogotá 2023** — Mapeo difuso de columnas. Asignar `city = 'Bogotá'`. Agregar `fuente = 'A6_Bogota2023_Kaggle'`
- [x] **⚠️ A7 Villavicencio** — **Agregar renombre** (no estaba en la versión anterior): `precio_cop→price`, `area_m2→area`, `habitaciones→rooms`, `banos→bathrooms`, `tipo_inmueble→property_type`, `ciudad→city`, `fecha_scraping→created_on`. Filtrar `tipo_operacion == 'Venta'`. Filtrar solo `city == 'Villavicencio'`. Agregar `fuente = 'A7_Scraping_Villavicencio'`
- [x] **⚠️ A8 Caracol UPZ** — **Agregar renombre**: `precios→price`, `area→area`, `alcobas→rooms`, `baños→bathrooms`. Asignar `city = 'Bogotá'`, `property_type = 'Apartamento'`. Agregar `fuente = 'A8_CaracPreVivNueva'`

- [x] Agregar columnas faltantes como NaN a cada dataset antes de concatenar
- [x] Concatenar con `pd.concat(..., ignore_index=True)` usando solo `COLS_CANONICAS`
- [x] Imprimir total registros (resultado: 880.714)
- [x] Registrar métrica en reporte_limpieza.csv

---

## Sección 2: Limpieza de Precios y Monedas
- [x] Extraer año temporal desde `created_on` para aplicar TRM
- [x] Convertir precios USD → COP en Properati A1 si existe columna `currency`
- [x] Detectar y corregir precios en COP/m² (precio < 1,000,000 y area > 10): multiplicar por área
- [x] Eliminar registros con `price` nulo
- [x] Eliminar registros con `price < 10,000,000` (errores)
- [x] Eliminar registros con `price > 10,000,000,000` (outliers extremos)
- [x] Imprimir registros restantes (resultado: 876.104)
- [x] Registrar métrica

---

## Sección 3: Estandarización de Ciudades ⚠️ CORREGIDO
- [x] Definir `MAPA_CIUDADES` con variantes conocidas
- [x] **⚠️ NO usar `normalize('NFKD').encode('ascii', errors='ignore')`** — eso corrompe las tildes en el CSV
- [x] Normalizar solo con `.str.lower().str.strip()` — mantener UTF-8
- [x] Aplicar el mapa de ciudades
- [x] Filtrar y conservar 12 ciudades en el CSV final
- [x] Renombrar columna limpia a `city`
- [x] Imprimir distribución por ciudad
- [x] Registrar métrica

> **Nota de alcance:** el CSV final contiene 12 ciudades, pero son 11 ciudades del alcance original más Armenia; Santa Marta no aparece. Esta decisión debe formalizarse en Fase 4/Fase 5 o regenerarse el dataset.

---

## Sección 4: Filtro Temporal (2020–2024)
**Nota:** El alcance operativo confirmado por Fase 1 y Fase 3 es 2020–2024.
- [x] Convertir `created_on` a datetime con `errors='coerce'`
- [x] Extraer columna `year`
- [x] Imputar `year` nulo usando año típico por fuente
- [x] Filtrar registros con `year` entre 2020 y 2024
- [x] Imprimir distribución por año
- [x] Registrar métrica

---

## Sección 5: Estandarización de Tipo de Propiedad
- [x] Definir `MAPA_PROPIEDADES`: variantes de "apartamento" / "casa" → categorías canónicas
- [x] **⚠️ Incluir variantes adicionales:** `'casa con conjunto cerrado': 'Casa'` (existe en A6)
- [x] Normalizar columna: minúsculas, strip
- [x] Aplicar mapa; conservar solo `'Casa'` y `'Apartamento'`
- [x] Imprimir distribución por tipo
- [x] Registrar métrica

---

## Sección 6: Eliminación de Outliers por Grupo (IQR)
- [x] Agrupar por `['city', 'year', 'property_type']`
- [x] Para grupos ≥ 10 registros: percentiles 2.5 y 97.5 de `price`; eliminar fuera del rango
- [x] Para grupos ≥ 10 registros: percentiles 1 y 99 de `area`; eliminar fuera del rango (solo donde `area` no sea nulo)
- [x] Conservar grupos < 10 registros sin filtrar
- [x] Imprimir registros restantes (resultado: 565.470)
- [x] Registrar métrica

---

## Sección 7: Deduplicación Inter-Dataset ⚠️ CORREGIDO
**La versión anterior incluía `rooms` y `bathrooms` en la clave, eliminando el 79.8% de los datos.**
- [x] **⚠️ Construir `dup_key` SOLO con:** `city + "_" + round(price/1M) + "_" + round(area) + "_" + property_type + "_" + year`
- [x] **⚠️ NO incluir `rooms` ni `bathrooms`** en la clave
- [x] Definir orden de prioridad: A2 > A7 > A1 > A5 > A6 > A4 > A3 > A8
- [x] Ordenar por prioridad; `drop_duplicates(subset='dup_key', keep='first')`
- [x] Eliminar columnas temporales
- [x] Imprimir registros finales (resultado: 282.660)
- [x] Registrar métrica

---

## Sección 8: Imputación de Valores Faltantes
- [x] `area` — mediana de `(city, year, property_type)`; fallback mediana global de `property_type`
- [x] `rooms` — mediana de `(city, property_type)`; fallback = 3; `clip(lower=1)`
- [x] `bathrooms` — mediana de `(city, property_type)`; fallback = 2; `clip(lower=1)`
- [x] `estrato` — mediana `(city, barrio)` → mediana `city` → fallback = 3; `clip(1, 6)`
- [x] **⚠️ `lat`/`lon`** — imputar por centroide de ciudad ANTES de exportar (antes quedaban 32% nulos)
- [x] Verificar 0 nulos en columnas críticas
- [x] Imprimir tabla de nulos antes/después

---

## Sección 9: Integración de Variables Macroeconómicas
- [x] Cargar B3 — salario mínimo por año (columnas: `Ano`, `Salario_minimo_mensual`)
- [x] Cargar B4 — IPC anual: `ipc_var_anual`, `ipc_base2018` (base 2018 = 100, calculado iterativamente)
- [x] Cargar B2 — tasa hipotecaria: extraer año de fecha, promedio anual de tasa de colocación
- [x] Cargar B1 — IPVU/IPVN: variación anual por año
- [x] **⚠️ Cargar B5** — intentar merge por `(year, city)`; fallback nacional (antes era solo nacional)
- [x] Construir `df_macro`: merge B3 + B4 + B2 + B1 + B5 por `year`
- [x] Merge principal: `df_inmuebles` + `df_macro` por `year` (left join)
- [x] Si B5 tiene datos por ciudad, merge adicional por `(year, city)`
- [x] Imputar `tasa_desempleo` nula con promedio del año
- [x] Verificar cobertura del merge e imprimir %

---

## Sección 10: Construcción de Variables Derivadas
- [x] `salario_anual = salario_mensual × 12`
- [x] `IAH = price / salario_anual`
- [x] `precio_real = price / (ipc_base2018 / 100)`
- [x] `precio_m2 = price / area`
- [x] Implementar `calcular_cuota_mensual(price, tasa_anual, meses=180, financia=0.70)` con amortización francesa: `r = (1 + tasa/100)^(1/12) - 1`
- [x] Calcular `cuota_mensual` aplicando la función por fila
- [x] `ratio_cuota_salario = cuota_mensual / salario_mensual`
- [x] `nivel_accesibilidad`: `'Accesible'` (IAH ≤ 5), `'Moderado'` (5–10), `'Elevado'` (10–20), `'Crítico'` (>20)
- [x] Imprimir estadísticas descriptivas de IAH, precio_real, precio_m2, cuota_mensual, ratio_cuota_salario

---

## Sección 11: Validación del Dataset Final
**Assertions de integridad**
- [x] Verificar 0 nulos en columnas críticas
- [x] Verificar `price > 0`
- [x] Verificar `area > 0`
- [x] Verificar `rooms >= 1` y `bathrooms >= 1`
- [x] Verificar `city` en 12 ciudades del CSV; queda caveat Armenia vs Santa Marta
- [x] Verificar `year` entre 2020 y 2024
- [x] Verificar `estrato` entre 1 y 6
- [x] Imprimir validación aprobada con shape final (282.660 × 26)

**Validación cruzada IPVN DANE**
- [x] Calcular variación anual del `precio_m2` promedio por ciudad
- [x] Comparar contra `ipvn_variacion_anual` del dataset B1
- [x] Documentar diferencia en `docs/FASE_3_COMPLETA.md`

---

## Sección 12: Exportación
- [x] **⚠️** Exportar dataset con `encoding='utf-8-sig'` (con BOM) para preservar tildes
- [x] Crear `data/processed/README.md` con diccionario de columnas
- [x] Guardar `data/processed/reporte_limpieza.csv`
- [x] Imprimir confirmación: nombre del archivo y shape exportado

---

## Sección 13: Preparación para GitHub
- [x] Verificar que NO hay rutas absolutas
- [x] Ejecutar el script completo sin errores
- [x] Verificar que el CSV generado tenga las 26 columnas y sin nulos en críticas
- [x] Verificar encoding: tildes preservadas (Bogotá, Cúcuta, Ibagué, Medellín)
- [x] Verificar que 2024 esté presente en el rango de años
- [x] Confirmar `.gitignore` excluye `data/raw/` (o LFS)
- [ ] `git add notebooks/02_preparacion_datos.ipynb notebooks/02_preparacion_datos.py data/processed/`
- [ ] Commit: `"fix: Fase 3 - pipeline corregido"`
- [ ] Push a rama `development`
- [x] Actualizar `docs/FASE_3_COMPLETA.md` con los resultados reales de la ejecución

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

## Resultados Verificados

| Métrica | Valor final |
|---|---:|
| Registros finales | 282.660 |
| Columnas finales | 26 |
| Rango años | 2020–2024 |
| Nulos en variables críticas | 0 |
| Marcadores de conflicto en CSV | 0 |
| Ciudades en el CSV | 12 (11 del alcance original + Armenia; Santa Marta ausente) |

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
