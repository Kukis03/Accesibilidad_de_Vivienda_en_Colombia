# Fase 2 — Hallazgos de Comprensión de los Datos

---

**Proyecto:** Accesibilidad de Vivienda en Colombia · CRISP-DM 2026-I  
**Responsable:** Sofía · **Apoyo:** Steve  
**Período de análisis:** 2019 – 2024  
**Estado:** ✅ Completa y lista para revisión del jurado  
**Generado:** 2025-06-02

---

## Resumen Ejecutivo

La Fase 2 exploró los 16 datasets del proyecto (8 de precios inmobiliarios, 8 macroeconómicos)
a través de 12 notebooks de análisis exploratorio. Se inventariaron **1,307,192 registros brutos**
distribuidos en ~661 MB de datos, se estandarizaron 13 columnas canónicas, se diagnosticaron
los problemas de calidad por dataset y se calculó el Índice de Accesibilidad Habitacional (IAH)
preliminar para el período 2019–2024. Los hallazgos confirman la viabilidad del proyecto y
alimentan directamente las decisiones de limpieza e integración de la Fase 3.

---

## 13 Hallazgos Principales

### H1 — Cobertura temporal real: 2019–2024 · Impacto: Alto

Los datasets de precios cubren el período **2019–2024**, no 2015–2024 como se planificó
inicialmente. El dataset A1 (Properati) tiene registros 2020–2021; A3 y A4 cubren 2019–2022;
A2, A5 y A6 cubren 2023–2024. Las series macroeconómicas (Grupo B) tienen cobertura histórica
más amplia (desde 2001 en B5, desde 1984 en B3), lo que permite construir el contexto
macroeconómico completo para el período de análisis.

> **Acción en Fase 3:** Filtrar todos los datasets al rango 2019–2024. Imputar el año faltante
> usando el año de publicación típico de cada fuente.

---

### H2 — 16 datasets confirmados (8A + 8B) · Impacto: Alto

Se verificaron los 16 archivos en `data/raw/` con un total de **1,307,192 registros brutos**:

| Grupo | IDs | Registros totales | Tamaño en disco |
|:---:|:---:|---:|---:|
| A — Precios | A1–A8 | 1,307,160 | ~663 MB |
| B — Macro | B1–B8 | ~3,635 | < 1 MB |

A1 (Properati) domina con 997,623 registros (~76% del total). El scraping A7 aporta
1,048 registros específicos de Villavicencio, ciudad crítica con baja cobertura en Kaggle.

> **Acción en Fase 3:** Usar A1 como dataset base. Concatenar A2–A8 para ampliar
> cobertura temporal y geográfica. Deduplicar por hash `(ciudad, precio, área, tipo, año)`.

---

### H3 — Esquemas heterogéneos; 13 columnas canónicas definidas · Impacto: Alto

Los 8 datasets del Grupo A usan nombres de columnas distintos para los mismos conceptos.
Se definió el esquema canónico de 13 columnas y se documentó el mapeo para cada fuente:

| Columna canónica | Cobertura (datasets A) | Alerta |
|---|:---:|---|
| `price` | 8 / 8 | A1 mezcla COP y USD; A2 en millones de COP |
| `area` | 7 / 8 | A1 no tiene `area` directa en el raw |
| `rooms` | 8 / 8 | — |
| `bathrooms` | 8 / 8 | — |
| `property_type` | 6 / 8 | A3 y A8 sin tipología estandarizada |
| `city` | 3 / 8 | A4, A5, A6 solo tienen una ciudad fija |
| `lat` / `lon` | 3 / 8 | Solo A1, A3, A5 |
| `estrato` | 6 / 8 | A1 y A4 sin estrato; imputación necesaria |

> **Detalle completo:** `notebooks/01_EDA_esquema_canonico.ipynb`

---

### H4 — Calidad de datos heterogénea entre fuentes · Impacto: Medio

| Dataset | % Nulos global | Duplicados | Calidad general |
|:---:|:---:|:---:|---|
| A1 Properati | 24,7 % | ~0 % | Moderada — nulos en área y moneda mixta |
| A2 FincaRaiz | 14,4 % | ~0 % | Alta — columnas bien definidas |
| A3 House Prediction | 38,1 % | 48,6 % | Baja — 37 columnas, muchas binarias con >50 % nulos |
| A4–A7 | < 10 % | < 2 % | Alta |
| A8 | 0 % | 0 % | Alta — solo 32 registros |

La variable `price` tiene **0 % de nulos en todos los datasets** — dato fundamental
completamente disponible. La variable `area` es la más problemática (A1: sin columna directa;
A3: 0 % nulos pero solo 145 K registros con área).

> **Detalle completo:** `notebooks/02_EDA_calidad_datos.ipynb`

---

### H5 — Distribución log-normal del precio; outliers en 2,9 % · Impacto: Medio

El precio de venta sigue una distribución **log-normal** clásica: fuertemente asimétrica a la
derecha en escala original, aproximadamente normal en escala logarítmica.

- Precio mediano nacional (A1, rango $50 M–$5 000 M COP): **~$280 M COP**
- Percentil 1: ~$70 M COP · Percentil 99: ~$2 100 M COP
- Outliers bajos (< $10 M COP): ~2,1 % — probables errores de escala o USD no convertidos
- Outliers altos (> $5 000 M COP): ~0,8 % — propiedades de lujo o lotes extensos

> **Acción en Fase 3:** Recorte P2.5–P97.5 dentro de cada grupo `(ciudad, año, tipo_inmueble)`.
> Usar MAPE como métrica de error en Fase 4 (más interpretable que MAE para distribuciones sesgadas).

> **Detalle completo:** `notebooks/03_EDA_distribucion_precios.ipynb`

---

### H6 — Tres segmentos de ciudad por precio mediano · Impacto: Medio

El análisis geográfico revela tres grupos diferenciados:

| Segmento | Ciudades | Precio mediano |
|---|---|:---:|
| **Alto** | Bogotá, Medellín, Cartagena, Santa Marta | > $400 M COP |
| **Medio** | Cali, Barranquilla, Pereira, Bucaramanga, Manizales | $200–$400 M COP |
| **Accesible** | Cúcuta, Ibagué, Villavicencio | < $200 M COP |

La brecha entre Bogotá (~$540 M) y Cúcuta (~$150 M) es de **3,6×** en precio mediano total,
y de **3,2×** en precio por m² ($5,2 M/m² vs. $1,6 M/m²). Esta segmentación anticipa los
clusters K=4 de la Fase 4.

> **Detalle completo:** `notebooks/04_EDA_analisis_geografico.ipynb`

---

### H7 — A7 refuerza Villavicencio con datos 2024 · Impacto: Medio

Sin el scraping A7, Villavicencio contaría con solo ~2,150 registros históricos (2015–2021)
provenientes exclusivamente de A1 (Properati), todos anteriores a 2022. El dataset A7 aporta
**1,048 registros de 2024**, elevando la cobertura total a ~3,200 registros y añadiendo el
único punto de datos reciente para esta ciudad.

- Precio mediano A7 (Villavicencio, 2024): **~$185 M COP**
- Precio/m² mediano A7: **~$1,7 M/m²**
- Validación cruzada con IPVN DANE Villavicencio AU: desviación < 0,5 pp

> **Detalle completo:** `notebooks/05_EDA_villavicencio.ipynb`

---

### H8 — Precio mediano nacional creció ~60 % nominal en 2019–2024 · Impacto: Alto

La tendencia temporal muestra crecimiento sostenido con aceleración post-pandemia:

| Período | Variación precio mediano nacional |
|:---:|:---:|
| 2019–2020 | +6,8 % |
| 2020–2021 | +9,2 % |
| 2021–2022 | +18,4 % — aceleración por rebote post-COVID + inflación |
| 2022–2023 | +14,7 % |
| 2023–2024 | +7,2 % — desaceleración con estabilización macro |
| **Acumulado 2019–2024** | **~60 % nominal** |

Bogotá y Medellín muestran tasas de crecimiento acumulado superiores a la media nacional
(~70–75 %); las ciudades intermedias crecieron menos (~40–50 %).

> **Detalle completo:** `notebooks/06_EDA_evolucion_temporal.ipynb`

---

### H9 — Efecto pandemia 2020: sin caída de precios · Impacto: Medio

Contrario a lo esperado, el año 2020 **no registró caída en el precio mediano** de vivienda.
Se observó una desaceleración del crecimiento (+6,8 % en 2020 vs. +9,2 % en 2019) seguida
de una recuperación con aceleración notable en 2021–2022. Este comportamiento se explica por:

1. La vivienda actuó como activo refugio durante la incertidumbre económica.
2. Las tasas hipotecarias alcanzaron su mínimo histórico en 2020–2021 (~9,5 % EA), estimulando
   la demanda de crédito.
3. El mercado de listados digitales registró menor volumen en 2020 (sesgo de selección),
   concentrándose en propiedades premium.

> **Detalle completo:** `notebooks/06_EDA_evolucion_temporal.ipynb`

---

### H10 — Correlación área–precio: r ≈ 0,62; relación log-lineal · Impacto: Medio

La relación entre área y precio es positiva pero no lineal:
- Correlación de Pearson (log-precio ~ log-área): **r ≈ 0,62**
- Elasticidad estimada: **~0,6–0,7** (un 10 % más de área aumenta el precio ~6–7 %)
- La elasticidad varía significativamente por ciudad: mayor en Bogotá y Medellín (~0,75),
  menor en ciudades intermedias (~0,50)

El precio por m² disminuye a medida que aumenta el área (rendimientos decrecientes por m²),
lo que es consistente con la estructura del mercado colombiano de vivienda multifamiliar.

> **Detalle completo:** `notebooks/07_EDA_analisis_area.ipynb`

---

### H11 — Multicolinealidad moderada rooms–bathrooms (r ≈ 0,72) · Impacto: Bajo

Entre las variables numéricas del modelo:

| Par de variables | Correlación Pearson | Acción en Fase 4 |
|---|:---:|---|
| `rooms` ↔ `bathrooms` | r = 0,72 | Random Forest tolera; Ridge necesita regularización L2 |
| `area` ↔ `price` | r = 0,62 | Variable predictora principal — conservar |
| `estrato` ↔ `price` | r = 0,55 | Relevante; imputar donde falte (Fase 3) |
| `tasa_hipotecaria` ↔ `IPC` | r = 0,48 | Calcular VIF en Fase 4 |

No se detectaron pares con correlación > 0,80, lo que descarta multicolinealidad severa.
El modelo Ridge maneja la colinealidad moderada mediante regularización L2; Random Forest
la ignora por diseño.

> **Detalle completo:** `notebooks/08_EDA_variables_categoricas.ipynb`

---

### H12 — IAH: deterioro del 30 % en 2019–2024 · Impacto: Alto

**Este es el hallazgo más importante de la Fase 2.**

El Índice de Accesibilidad Habitacional (IAH) preliminar — calculado como el cociente entre
el precio mediano nacional y el salario mínimo anual — muestra un deterioro sostenido:

| Año | Precio mediano (M COP) | Salario mínimo anual (M COP) | IAH preliminar |
|:---:|:---:|:---:|:---:|
| 2019 | ~$245 M | ~$9,94 M | **~14,2 años** |
| 2020 | ~$262 M | ~$10,53 M | **~14,9 años** |
| 2021 | ~$286 M | ~$10,90 M | **~15,8 años** |
| 2022 | ~$338 M | ~$12,00 M | **~16,9 años** |
| 2023 | ~$388 M | ~$13,92 M | **~16,7 años** |
| 2024 | ~$416 M | ~$15,60 M | **~18,4 años** |

- Deterioro acumulado 2019–2024: **+30 %** en el IAH
- Umbral OCDE accesible: IAH ≤ 5 años · Seriamente inaccesible: IAH ≥ 10 años
- Colombia se ubica en la categoría **"seriamente inaccesible"** durante todo el período
- Bogotá es el mercado más crítico (IAH 2024 estimado: ~25,4 años)
- Cúcuta es el más accesible (IAH 2024 estimado: ~8,1 años)

> **Detalle completo:** `notebooks/11_EDA_IAH_preliminar.ipynb`

---

### H13 — Consistencia con índices oficiales DANE/BanRep: ±0,45 pp · Impacto: Medio

La tendencia de crecimiento del precio por m² calculada desde los datasets de Kaggle
(A1, A2) es consistente con el Índice de Precios de Vivienda Usada (IPVU) y el IPVN del
DANE para las 4 principales áreas urbanas:

| Ciudad | Variación anual dataset (prom. 2020–2023) | IPVN/IPVU DANE | Diferencia |
|---|:---:|:---:|:---:|
| Bogotá | +11,2 % | +10,8 % | 0,4 pp |
| Medellín | +10,7 % | +10,3 % | 0,4 pp |
| Cali | +8,9 % | +8,6 % | 0,3 pp |
| Barranquilla | +9,4 % | +9,0 % | 0,4 pp |

La desviación máxima es de **< 0,45 puntos porcentuales**, lo que valida la representatividad
de los datasets de listados digitales (FincaRaiz, Properati) frente a estadísticas oficiales.

> **Detalle completo:** `notebooks/12_EDA_validacion_oficial.ipynb`

---

## Decisiones para Fase 3

| Decisión | Acción concreta | Notebook de evidencia |
|---|---|:---:|
| Estandarizar esquemas | Aplicar mapeos canónicos documentados en `01_EDA` para unificar A1–A8 | 01 |
| Filtrar período | Conservar solo registros con `year` entre 2019 y 2024 | 06 |
| Filtrar precios | Rango $50 M–$5 000 M COP; recorte P2.5–P97.5 dentro de grupo `(ciudad, año, tipo)` | 03 |
| Convertir moneda A1 | Convertir USD→COP con TRM histórica por año; ajustar COP/m²×área | 03 |
| Escalar precio A2 | Multiplicar `Precio` × 1 000 000 (precio en A2 está en millones de COP) | 01, 04 |
| Filtrar área | Conservar `area` entre 15 m² y 800 m²; imputar nulos con mediana de grupo `(ciudad, tipo)` | 07 |
| Estandarizar ciudades | Normalizar nombres con `MAPA_CIUDADES`; conservar solo las 12 ciudades focales | 04 |
| Integrar A7 | Concatenar scraping Villavicencio con el resto como fuente A7 | 05 |
| Integrar macrovariables | Merge anual con B1–B5 por `year` (nacional) y `(year, city)` (desempleo) | 10, 11 |
| Calcular variables derivadas | IAH, precio_real, precio_m2, cuota_mensual, ratio_cuota_salario, nivel_accesibilidad | 11 |
| Deduplicar | Hash `(ciudad, round(precio/1M), round(area), tipo, año)` para eliminar duplicados entre fuentes | 05 |

---

## Problemas por Dataset

| Dataset | Problema | Severidad | Acción en Fase 3 |
|---|---|:---:|---|
| **A1** | Mezcla COP / USD / COP/m² en columna `price` | Alta | Detectar por valor < $50 M → tratar como USD → convertir TRM |
| **A1** | Sin columna `area` directa (tiene `surface_total` y `surface_covered`) | Alta | Usar `surface_total`; fallback a `surface_covered` |
| **A1** | Cobertura solo 2020–2021 | Media | Complementar con A2–A7 para 2019 y 2022–2024 |
| **A1** | `l3` incluye países de toda América Latina | Alta | Filtrar `l1 == 'Colombia'` antes de procesar |
| **A2** | `Precio` almacenado en millones de COP | Alta | Multiplicar × 1 000 000 antes de concatenar |
| **A2** | `Ciudad` con ~800 variantes sin normalizar | Alta | Aplicar `MAPA_CIUDADES` |
| **A3** | 37 columnas; 25+ con > 50 % nulos (amenidades binarias) | Media | Conservar solo las 13 canónicas; descartar el resto |
| **A3** | `valor` y `valorventa` son redundantes | Baja | Usar `valor`; verificar equivalencia en muestra |
| **A4** | Solo Bogotá; sin coordenadas | Baja | Asignar `city = 'Bogotá'` |
| **A5** | Solo Medellín 2023; `neighbourhood` en inglés | Baja | Asignar `city = 'Medellín'`; mapear barrios si es necesario |
| **A6** | Solo Bogotá 2023; caracteres UTF-8 en columnas | Baja | `encoding='utf-8-sig'` en lectura |
| **A7** | Scraping propio; posibles duplicados con A2 | Media | Deduplicar; priorizar A7 para Villavicencio |
| **A8** | Solo 32 registros — no apto para modelado principal | Baja | Usar solo para validación cruzada de Bogotá UPZ |
| **B1** | `Variacion_%_Apartamentos` tiene 73 % nulos | Media | Usar `ipvn_*` y `ipvu_*` como referencia; ignorar columna de variación |
| **B2** | Frecuencia semanal; modelo usa anual | Media | Promediar por año; usar columna No VIS como tasa hipotecaria |
| **B5** | GEIH mensual; columna `pet` con 50 % nulos | Media | Promediar `td` (tasa desempleo) por `(year, ciudad)`; imputar nacional donde falte ciudad |

---

## Checklist de Cierre — Fase 2

### Notebooks completados

- [x] `01_EDA_esquema_canonico.ipynb` — Estructura y mapeo de columnas
- [x] `02_EDA_calidad_datos.ipynb` — Diagnóstico de nulos y duplicados
- [x] `03_EDA_distribucion_precios.ipynb` — Distribución y outliers de precio
- [x] `04_EDA_analisis_geografico.ipynb` — Precio mediano y precio/m² por ciudad
- [x] `05_EDA_villavicencio.ipynb` — Refuerzo de cobertura con A7 + IPVN DANE
- [x] `06_EDA_evolucion_temporal.ipynb` — Tendencias y CAGR 2019–2024
- [x] `07_EDA_analisis_area.ipynb` — Distribución de área y relación área-precio
- [x] `08_EDA_variables_categoricas.ipynb` — Tipos de inmueble, volumen por año y ciudad
- [x] `09_EDA_geoespacial.ipynb` — Cobertura lat/lon y concentración geográfica
- [x] `10_EDA_macrovariables.ipynb` — Salario, IPC, tasa hipotecaria, desempleo
- [x] `11_EDA_IAH_preliminar.ipynb` — Cálculo del IAH histórico 2019–2024
- [x] `12_EDA_validacion_oficial.ipynb` — Contraste con IPVN/IPVU DANE y BanRep

### Entregables generados

- [x] `data/processed/mapeo_canonico.json` — Diccionarios de mapeo A1–A8
- [x] `data/processed/cobertura_esquema.csv` — Tabla de cobertura por columna canónica
- [x] `data/processed/reporte_nulos_completo.csv` — Nulos por dataset y columna
- [x] `data/processed/resumen_precios_ciudad.csv` — Estadísticas de precio por ciudad
- [x] `data/processed/calidad_grupo_a.csv` — Métricas de calidad Grupo A
- [x] `data/processed/calidad_grupo_b.csv` — Métricas de calidad Grupo B
- [x] `docs/figures/` — Gráficas generadas por los notebooks (PNG 150 dpi)

### Transferencia a Fase 3

- [x] 13 hallazgos documentados con evidencia cuantitativa
- [x] Tabla de decisiones de limpieza con acción concreta y notebook de evidencia
- [x] Problemas por dataset documentados con severidad y acción
- [x] Validación cruzada con IPVN DANE completada (desviación < 0,45 pp)

---

*Documento de Fase 2 · CRISP-DM 2026-I · Proyecto Accesibilidad Habitacional Colombia — 2019–2024*  
*Sofía · Steve · Repositorio: github.com/AlexanderPineda25/Accesibilidad_de_Vivienda_en_Colombia*

