# Fase 3 — Preparación de los Datos
## Proyecto: Accesibilidad de Vivienda en Colombia · CRISP-DM 2025-I
**Responsable principal:** Kukis · **Apoyo:** Steve  
**Estado:** ⚠️ En corrección — pipeline implementado con bugs identificados (ver sección 8)  
**Notebook asociado:** `notebooks/02_preparacion_datos.ipynb` · `notebooks/02_preparacion_datos.py`  
**Semanas:** 5 – 6

---

## Introducción

La Fase 3 de la metodología CRISP-DM se enfoca en la preparación de los datos. Toma como insumo las 16 fuentes identificadas en Fase 2 (8 datasets de precios de vivienda y 8 macroeconómicos) y produce un dataset consolidado, limpio y enriquecido listo para modelado.

Esta fase fue implementada por Kukis con apoyo de Steve. Durante la revisión posterior se identificaron **8 bugs** que redujeron artificialmente el volumen del dataset final de ~315K esperados a 54,904 registros. Este documento registra el estado actual y las correcciones necesarias.

> ⚠️ **Nota de auditoría:** Las cifras de las secciones 1–14 son datos **reales obtenidos** del pipeline ejecutado (aún con bugs). La sección 16 contiene **proyecciones estimadas**, no datos obtenidos, y está marcada explícitamente como tal. No iniciar Fase 4 hasta corregir los bugs y re-ejecutar el pipeline.

---

## 1. Carga y Unificación de los 8 Datasets de Precios (A1–A8)

Se definió el esquema canónico de unificación:

```python
COLS_CANONICAS = [
    'price', 'area', 'rooms', 'bathrooms', 'property_type', 
    'city', 'lat', 'lon', 'created_on', 'barrio', 'parking', 'estrato', 'fuente'
]
```

- [x] A1 Properati — filtrado por `operation_type == 'Venta'`, renombrado al esquema canónico
- [x] A2 FincaRaiz — renombrado con columnas reales (`Precio`, `Area Construida`, `Habitaciones`, etc.)
- [x] A3 HousePrediction — renombrado desde `valor`, `area`, `habitaciones`, `banos`
- [x] A4 Bogotá — mapeo difuso de columnas, asignada `city = 'Bogotá'`
- [x] A5 Medellín — renombrado desde `price`, `baths`, `neighbourhood`, `stratum`
- [x] A6 Bogotá 2023 — mapeo difuso de columnas, asignada `city = 'Bogotá'`
- [ ] ⚠️ A7 Villavicencio — **pendiente: agregar renombre de columnas** (no se mapearon sus columnas reales)
- [ ] ⚠️ A8 Caracol UPZ — **pendiente: agregar renombre de columnas y asignar city**
- [x] Columnas faltantes completadas como NaN y datasets concatenados

**Resultado:** 880,865 registros consolidados.

---

## 2. Limpieza de Precios y Monedas

- [x] Extracción de año temporal desde `created_on`
- [x] Conversión USD → COP en Properati (A1) usando TRM histórica
- [x] Detección y corrección de precios en COP/m²
- [ ] ⚠️ **Bug detectado:** A2 FincaRaiz — precio multiplicado por 1,000,000 cuando ya estaba en COP completos. Esto elevó todos los precios de A2 por encima del límite de $10,000M, eliminando los 142,833 registros de esta fuente.
- [x] Eliminación de `price` nulo, `price < 10M` y `price > 10,000M`

**Registros tras limpieza:** 734,258

---

## 3. Estandarización de Ciudades

- [x] Diccionario `MAPA_CIUDADES` con 24 variantes → 12 ciudades canónicas
- [ ] ⚠️ **Bug detectado:** La normalización usó `normalize('NFKD').encode('ascii', errors='ignore')`, lo que corrompió caracteres acentuados en el CSV exportado (Cúcuta, Ibagué, Medellín, Bogotá aparecen con caracteres corruptos).
- [x] Filtro: solo registros en las 12 ciudades focales

**Registros tras filtro de ciudades:** 325,554  
**Pérdida:** 55.7% (municipios no focales como Envigado, Chía, Jamundí, Popayán, etc.)

---

## 4. Filtro Temporal

- [x] Conversión de `created_on` a datetime
- [x] Imputación de año faltante por fuente
- [x] Filtro 2019–2024

**Registros tras filtro temporal:** 325,554 (0 registros eliminados — todos estaban dentro del rango)  
**Nota:** No se encontraron registros de 2019 ni de 2024 en el dataset final. 2024 existe en A2 pero se perdió por el bug de precio.

---

## 5. Estandarización de Tipo de Propiedad

- [x] Diccionario `MAPA_PROPIEDADES` → solo `'Casa'` y `'Apartamento'`
- [ ] ⚠️ Variante `'casa con conjunto cerrado'` de A6 no estaba en el mapa — 30 registros perdidos

**Registros tras filtro de tipo:** 285,705

---

## 6. Eliminación de Outliers por Grupo (IQR)

- [x] Agrupación por `(city, year, property_type)`
- [x] Percentiles 2.5–97.5 para `price`
- [x] Percentiles 1–99 para `area` (solo donde no es nulo)
- [x] Grupos < 10 registros conservados sin filtrar

**Registros tras IQR:** 272,044

---

## 7. Deduplicación Inter-Dataset

- [ ] ⚠️ **Bug detectado:** La clave `dup_key` incluyó `rooms` y `bathrooms` además de los campos previstos (`city + price_round + area_round + property_type + year`). Esto sobre-especificó el matching, eliminando el **79.8%** de los registros (217,140 de 272,044) en lugar del ~15–20% esperado.
- [x] Prioridad de fuentes definida: A7 > A2 > A1 > A6 > A5 > A4 > A3 > A8

**Registros tras deduplicación:** **54,904** (vs ~250K esperados)

---

## 8. Resumen de Bugs y Correcciones Pendientes

| # | Bug | Fuente | Impacto | Corrección |
|---|-----|--------|---------|------------|
| **B1** | Precio × 1,000,000 | A2 (línea 78) | Pierde **142,730 reg** (incluye 2024) | Quitar `* 1000000` |
| **B2** | Sin city ni property_type | A3 (línea 83–91) | Pierde **~145,000 reg** | Asignar `city = 'Bogotá'`, definir property_type |
| **B3** | Sin renombre de columnas | A7 (línea 141–145) | Pierde **~900 reg** de Villavicencio | Agregar diccionario de renombre |
| **B4** | Sin renombre de columnas | A8 (línea 147–151) | Pierde **32 reg** | Agregar renombre + `city = 'Bogotá'` |
| **B5** | Dedup con rooms/bathrooms | Dedup (línea 293–315) | Elimina **~171,000 reg** de más | Clave solo: city+price+area+type+year |
| **B6** | Encoding ascii corrompe tildes | Ciudades (línea 236) | Nombres de ciudad ilegibles | No forzar ascii; mantener UTF-8 |
| **B7** | lat/lon sin imputar | Exportación | **32% nulos** en coordenadas | Imputar centroides antes de exportar |
| **B8** | 'casa con conjunto cerrado' faltante | A6 (MAPA_PROPIEDADES) | **~30 reg** perdidos | Agregar variante al mapa |

---

## 9. Imputación de Valores Faltantes

- [x] `area` — mediana de `(city, year, property_type)`; fallback mediana global
- [x] `rooms` — mediana de `(city, property_type)`; fallback = 3; `clip(lower=1)`
- [x] `bathrooms` — mediana de `(city, property_type)`; fallback = 2; `clip(lower=1)`
- [x] `estrato` — mediana `(city, barrio)` → mediana `city` → fallback = 3; `clip(1, 6)`
- [ ] ⚠️ `lat`/`lon` — la imputación por centroide está definida pero no se ejecuta antes de la exportación; persisten 17,628 nulos (32%)

**Resultado:** 0 nulos en columnas críticas de modelado (`price`, `area`, `rooms`, `bathrooms`, `city`, `property_type`, `estrato`).

---

## 10. Integración de Variables Macroeconómicas

- [x] B3 — salario mínimo por año
- [x] B4 — IPC anual con `ipc_base2018` calculado iterativamente
- [x] B2 — tasa hipotecaria (promedio anual de tasa de colocación)
- [x] B1 — IPVU e IPVN con variación anual
- [x] B5 — desempleo (merge a nivel nacional)
- [ ] ⚠️ B5 podría integrarse por `(year, city)` para mayor granularidad

**Cobertura:** 100% de registros con variables macroeconómicas.

---

## 11. Construcción de Variables Derivadas

- [x] `salario_anual = salario_mensual × 12`
- [x] `IAH = price / salario_anual`
- [x] `precio_real = price / (ipc_base2018 / 100)`
- [x] `precio_m2 = price / area`
- [x] `cuota_mensual` — amortización francesa (70% financiado, 15 años, tasa EA→mensual)
- [x] `ratio_cuota_salario = cuota_mensual / salario_mensual`
- [x] `nivel_accesibilidad` — 'Accesible', 'Moderado', 'Elevado', 'Crítico'

### Estadísticas Descriptivas (dataset actual con bugs)

| Variable | Promedio | Mediana | Desv. Est. |
|----------|----------|---------|------------|
| IAH (años) | 33.3 | 24.5 | 29.3 |
| precio_real (COP) | 470.9M | 346.1M | 415.0M |
| precio_m2 (COP/m²) | 4.52M | 3.78M | 3.31M |
| cuota_mensual (COP) | 4.37M | 3.19M | 4.26M |
| ratio_cuota_salario | 3.20 | 2.37 | 2.96 |

> **Nota:** Estas cifras están sesgadas porque solo sobrevive A1 Properati (77.7% de los registros), que lista propiedades de mayor valor. Se espera que al corregir los bugs, el IAH promedio baje a ~18–22 años.

---

## 12. Validación del Dataset Final

- [x] Sin nulos en columnas críticas
- [x] `price > 0`, `area > 0`
- [x] `rooms >= 1`, `bathrooms >= 1`
- [x] `city` en 12 ciudades canónicas
- [x] `year` entre 2019 y 2024
- [x] `estrato` entre 1 y 6
- [ ] ❌ Validación cruzada con IPVN DANE — no implementada en el código

---

## 13. Exportación

- [x] Dataset exportado a `data/processed/vivienda_colombia_limpio.csv`
- [x] Reporte de limpieza `data/processed/reporte_limpieza.csv`
- [x] Metadatos `data/processed/README.md`

### Shape final del dataset actual: **54,904 filas × 26 columnas** (16 MB)

**Columnas:** `price`, `area`, `rooms`, `bathrooms`, `property_type`, `city`, `lat`, `lon`, `created_on`, `estrato`, `fuente`, `year`, `salario_mensual`, `ipc_var_anual`, `ipc_base2018`, `tasa_hipotecaria_anual`, `tasa_desempleo`, `ipvu_variacion_anual`, `ipvn_variacion_anual`, `salario_anual`, `IAH`, `precio_real`, `precio_m2`, `cuota_mensual`, `ratio_cuota_salario`, `nivel_accesibilidad`

---

## 14. Resultados del Dataset Actual (pre-corrección)

### Distribución por ciudad

| Ciudad | Registros | % | IAH Promedio |
|--------|-----------|---|-------------|
| Medellín | 15,134 | 27.6% | 37.6 |
| Cali | 10,096 | 18.4% | 35.8 |
| Barranquilla | 7,790 | 14.2% | 32.1 |
| Bogotá | 5,490 | 10.0% | 32.0 |
| Cartagena | 2,916 | 5.3% | 46.3 |
| Bucaramanga | 2,694 | 4.9% | 25.3 |
| Manizales | 2,658 | 4.8% | 23.7 |
| Cúcuta | 2,276 | 4.1% | 25.3 |
| Pereira | 2,188 | 4.0% | 31.5 |
| Ibagué | 1,388 | 2.5% | 25.7 |
| Villavicencio | 1,254 | 2.3% | 18.5 |
| Armenia | 1,020 | 1.9% | 17.8 |

### Distribución por año

| Año | Registros | % |
|-----|-----------|---|
| 2020 | 18,391 | 33.5% |
| 2021 | 24,289 | 44.2% |
| 2022 | 4,999 | 9.1% |
| 2023 | 7,225 | 13.2% |
| 2024 | 0 | 0% |

### Distribución de accesibilidad

| Nivel | Registros | % |
|-------|-----------|---|
| Crítico (IAH > 20) | 33,388 | 60.8% |
| Elevado (10–20) | 15,884 | 28.9% |
| Moderado (5–10) | 5,368 | 9.8% |
| Accesible (≤5) | 264 | 0.5% |

### Fuentes supervivientes

| Fuente | Registros | % |
|--------|-----------|---|
| A1 Properati | 42,680 | 77.7% |
| A5 Medellín Kaggle | 6,734 | 12.3% |
| A4 Bogotá Kaggle | 4,999 | 9.1% |
| A6 Bogotá 2023 Kaggle | 491 | 0.9% |
| A2, A3, A7, A8 | 0 | 0% |

---

## 15. Checklist de Correcciones Pendientes

- [ ] **B1** — Quitar `* 1,000,000` en carga de A2
- [ ] **B2** — Asignar `city = 'Bogotá'` y `property_type` a A3
- [ ] **B3** — Agregar renombre de columnas para A7
- [ ] **B4** — Agregar renombre de columnas para A8
- [ ] **B5** — Simplificar `dup_key`: solo `city + price + area + type + year`
- [ ] **B6** — Cambiar normalización de ciudades: no forzar ascii
- [ ] **B7** — Imputar `lat`/`lon` por centroide antes de la exportación
- [ ] **B8** — Agregar `'casa con conjunto cerrado': 'Casa'` a MAPA_PROPIEDADES
- [ ] **B5 mejorado** — Integrar B5 por `(year, city)` en lugar de solo nacional
- [ ] **Validación IPVN** — Implementar validación cruzada contra DANE

---

## 16. Proyecciones Post-Corrección *(estimaciones — no son datos obtenidos)*

> ⚠️ **Aviso:** Esta sección contiene estimaciones derivadas del análisis de impacto de los bugs. Los valores de la columna "Esperado (corregido)" **no son datos reales obtenidos**; son proyecciones basadas en el recuento de registros perdidos por cada bug. Esta tabla deberá reemplazarse con los valores reales tras re-ejecutar el pipeline con los 8 fixes aplicados.

| Métrica | Actual — run con bugs (real) | Proyección post-corrección (estimada) |
|---------|------------------------------|---------------------------------------|
| Registros finales | 54,904 | ~250,000–370,000 (estimado) |
| Rango años | 2020–2023 | 2020–2024 (si B1 se corrige, A2 aporta 2024) |
| Año 2024 presente | ❌ | ✅ esperado (de A2, si se quita ×1,000,000) |
| Fuentes supervivientes | 4 (A1, A4, A5, A6) | 7 (A1–A7) si se corrigen B2, B3 y B4 |
| IAH promedio | 33.3 años | ~18–22 años (estimado; sesgo de Properati eliminado) |
| % Crítico | 60.8% | ~35–45% (estimado) |
| Tildes en ciudades | Corruptas (bug B6) | Preservadas si se usa UTF-8 |
| Nulos en lat/lon | 32% (17,628 nulos) | 0% si se aplica imputación por centroide (B7) |

**⟶ Acción requerida:** Aplicar los 8 fixes, re-ejecutar `02_preparacion_datos.py` y actualizar esta sección con los valores reales obtenidos.

---

## 17. Entregables

| Archivo | Ruta | Estado |
|---------|------|--------|
| Notebook | `notebooks/02_preparacion_datos.ipynb` | ✅ Implementado (requiere correcciones) |
| Script | `notebooks/02_preparacion_datos.py` | ✅ Implementado (490 líneas) |
| Dataset limpio | `data/processed/vivienda_colombia_limpio.csv` | ⚠️ Generado con bugs — 54,904 reg |
| Reporte limpieza | `data/processed/reporte_limpieza.csv` | ✅ Generado |
| Metadatos | `data/processed/README.md` | ✅ Generado |
| Documento de fase | `docs/FASE_3_COMPLETA.md` | ✅ Actualizado con diagnóstico |

---

## 18. Notas para el Equipo

- **Para Steve (Modelado - Fase 4):** No iniciar modelado sobre el dataset actual. Esperar a que se apliquen las correcciones de los 8 bugs documentados. El dataset corregido tendrá ~250K–370K registros con cobertura 2020–2024 e IAH más representativo.
- **Para Sofía (Evaluación - Fase 5):** Las cifras de accesibilidad actuales (60.8% crítico, IAH promedio 33.3) están artificialmente infladas por el sesgo de A1 Properati. Recalcular después de la corrección.
- **Próximo paso:** Aplicar los 8 fixes en `02_preparacion_datos.py`, re-ejecutar el pipeline completo, verificar que el CSV resultante tenga las 26 columnas con 0 nulos y tildes preservadas, luego actualizar este documento.

---

*Documento de Fase 3 · CRISP-DM 2025-I · Proyecto Accesibilidad Habitacional Colombia*  
*Pendiente de corrección de 8 bugs identificados — actualizar tras re-ejecución*
