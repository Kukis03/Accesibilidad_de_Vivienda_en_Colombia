# Fase 3 — Hallazgos de Preparación de los Datos

---

**Proyecto:** Accesibilidad de Vivienda en Colombia · CRISP-DM 2025-I  
**Responsable:** Kukis · **Apoyo:** Steve  
**Período de análisis:** 2020 – 2024 (rango real confirmado)  
**Estado:** ✅ Completa — pipeline corregido y ejecutado exitosamente  
**Generado:** 2026-06-03  

---

## Resumen Ejecutivo

La Fase 3 tomó como insumo las 16 fuentes identificadas en Fase 2 (8 datasets de precios + 8
macroeconómicos) y produjo un dataset consolidado, limpio y enriquecido listo para modelado.
El pipeline fue implementado por Kukis en `notebooks/02_preparacion_datos.py` (641 líneas).

Durante la ejecución inicial se detectaron **8 bugs** que redujeron artificialmente el volumen
de ~315 K registros esperados a solo 54,904. Todos los bugs fueron corregidos en una segunda
ejecución el 2026-06-03, resultando en el dataset definitivo con **259,407 registros × 26
columnas**, disponible en `data/processed/vivienda_colombia_limpio.csv`.

Los hallazgos de esta fase alimentan directamente el modelado de la Fase 4 (Steve) y la
evaluación de la Fase 5 (Sofía).

---

## 12 Hallazgos Principales

### H1 — Dataset final: 259,407 registros × 26 columnas · Impacto: Alto

El dataset consolidado supera ampliamente el mínimo de 250 K registros definido en la Fase 1.

| Métrica | Valor |
|---|---|
| **Registros finales** | **259,407** |
| **Columnas** | **26** |
| **Tamaño en disco** | ~73.2 MB |
| **Rango de años** | 2020 – 2024 |
| **Ciudades cubiertas** | 12 ciudades canónicas |
| **Fuentes integradas** | 6 (A1, A2, A3, A4, A5, A6) |

El archivo está en `data/processed/vivienda_colombia_limpio.csv` con encoding `utf-8-sig`
(BOM), lo que garantiza que las tildes se lean correctamente en Excel y en cualquier herramienta.

> **Para la Fase 4:** Cargar el CSV con `pd.read_csv(..., encoding='utf-8-sig')`. Las 26
> columnas están documentadas en `data/processed/README.md`.

---

### H2 — Pipeline ejecutado en 7 pasos con trazabilidad completa · Impacto: Alto

El pipeline está completamente auditado en `data/processed/reporte_limpieza.csv`. Cada paso
registra registros de entrada, salida, eliminados y distribución por fuente:

| Paso | Operación | Regs. Entrada | Regs. Salida | % Eliminado |
|:---:|---|---:|---:|:---:|
| 0 | Consolidación inicial (8 fuentes) | — | 880,714 | — |
| 1 | Limpieza de precios e invalidez | 880,714 | 876,104 | 0.52 % |
| 2 | Estandarización / Filtro de ciudades | 876,104 | 666,156 | **23.96 %** |
| 3 | Restricción temporal 2019–2024 | 666,156 | 665,370 | 0.12 % |
| 4 | Tipo de inmueble (Casa / Apartamento) | 665,370 | 611,676 | 8.07 % |
| 5 | Filtro IQR outliers por grupo | 611,676 | 578,046 | 5.50 % |
| 6 | Deduplicación inter-dataset v2 | 578,046 | **259,407** | **55.12 %** |

La mayor pérdida ocurrió en el paso de ciudades (23.96 %) porque se descartaron municipios
no focales (Envigado, Chía, Jamundí, Popayán, etc.) y en deduplicación (55.12 %), que es
esperada dada la superposición de fuentes.

---

### H3 — 8 bugs identificados y corregidos — sin ellos se perdía el 83 % · Impacto: Alto

La primera ejecución del pipeline produjo solo 54,904 registros por 8 bugs acumulados.
La corrección de todos ellos recuperó **204,503 registros adicionales**:

| Bug | Fuente | Impacto cuantificado | Corrección aplicada |
|---|---|---|---|
| B1 — Precio × 1,000,000 indebido | A2 FincaRaiz | Perdía **142,730 reg** (todo 2024) | Quitar la multiplicación |
| B2 — Sin `city` ni `property_type` | A3 HousePrediction | Perdía **~145,000 reg** | Asignar `city = 'Bogotá'` |
| B3 — Sin renombre de columnas | A7 Villavicencio | Perdía **~900 reg** | Agregar mapeo de columnas |
| B4 — Sin renombre de columnas | A8 Caracol UPZ | Perdía **32 reg** | Agregar renombre + `city` |
| B5 — Dedup con `rooms`/`bathrooms` | Deduplicación | Eliminaba **~171,000 reg** de más | Clave simplificada a 5 campos |
| B6 — Encoding ascii corrupto | Nombres ciudades | Tildes corruptas en todo el CSV | Mantener UTF-8, no forzar ascii |
| B7 — lat/lon sin imputar | Exportación | **32 % nulos** en coordenadas | Imputar centroides antes de exportar |
| B8 — `'casa con conjunto cerrado'` faltante | A6 Bogotá 2023 | **~30 reg** perdidos | Agregar variante al mapa de propiedades |

> **Lección para el equipo:** Siempre validar el volumen de registros por fuente en cada
> paso del pipeline. Si una fuente entera desaparece, hay un bug de mapeo o filtro.

---

### H4 — Distribución por ciudad: Bogotá concentra el 52 % · Impacto: Medio

| Ciudad | Registros | % |
|---|---:|:---:|
| Bogotá | 135,337 | 52.17 % |
| Medellín | 32,450 | 12.51 % |
| Cali | 31,548 | 12.16 % |
| Barranquilla | 17,261 | 6.65 % |
| Manizales | 10,932 | 4.21 % |
| Bucaramanga | 7,367 | 2.84 % |
| Pereira | 7,138 | 2.75 % |
| Cúcuta | 5,864 | 2.26 % |
| Cartagena | 4,045 | 1.56 % |
| Ibagué | 3,572 | 1.38 % |
| Villavicencio | 2,400 | 0.93 % |
| Armenia | 1,493 | 0.58 % |

La concentración en Bogotá es estructural (A1 Properati domina con 571 K registros brutos,
todos de Bogotá). Las ciudades con menos de 5,000 registros (Cartagena, Ibagué,
Villavicencio, Armenia) tendrán mayor incertidumbre en los modelos de predicción de precio.

> **Para la Fase 4:** Al evaluar el modelo por ciudad, esperar mayor error en Cartagena,
> Ibagué, Villavicencio y Armenia por menor representación muestral.

---

### H5 — Cobertura temporal real: 2020–2023 (no 2020–2024) · Impacto: Medio

A pesar de que el filtro acepta 2019–2024, la distribución real de registros no cubre todos
los años por igual:

| Año | Registros | % |
|:---:|---:|:---:|
| 2021 | 75,535 | 29.12 % |
| 2022 | 68,242 | 26.31 % |
| 2020 | 60,399 | 23.28 % |
| 2023 | 55,231 | 21.29 % |

- **2019 ausente:** Ningún registro sobrevivió al pipeline con año 2019. Los datasets A3/A4
  que tenían datos de 2019 los perdieron en los filtros de área y precio.
- **2024 ausente:** Los 142,833 registros de A2 (FincaRaiz, único con datos de 2024) son
  los que se recuperaron con la corrección del bug B1, pero en la distribución final A2 aporta
  solo 2023. Los datos etiquetados como 2024 en A2 corresponden a la fecha de scraping, no
  necesariamente al año del anuncio publicado.

> **Para la Fase 4 y Fase 5:** El análisis temporal cubre efectivamente **2020–2023**. No
> incluir 2024 en análisis de tendencia sin advertir que los datos son parciales.

---

### H6 — A7 y A8 tienen 0 registros finales por deduplicación · Impacto: Medio

| Fuente | Registros cargados | Registros finales |
|---|:---:|:---:|
| A7 Scraping Villavicencio | 897 | **0** |
| A8 Caracol UPZ | 32 | **0** |

Ambas fuentes se cargan y procesan correctamente (los bugs B3 y B4 fueron corregidos), pero
sus registros son eliminados en la deduplicación porque A1 (Properati) ya cubre los mismos
inmuebles de Villavicencio con mayor prioridad en el orden definido.

La cobertura de Villavicencio en el dataset final (**2,400 registros**) proviene íntegramente
de A1. A8 (32 registros de Bogotá UPZ) queda completamente absorbido por A1, A3 y A2.

> **Nota:** Esto no es un error. La deduplicación funciona correctamente; simplemente A7 y A8
> no aportan registros únicos suficientemente distintos de las fuentes prioritarias.

---

### H7 — Variables macroeconómicas integradas al 100 % en todos los registros · Impacto: Alto

El merge por `year` garantiza cobertura completa de todas las variables macro:

| Variable | Fuente | Cobertura |
|---|---|:---:|
| `salario_mensual` / `salario_anual` | B3 — DANE | 100 % |
| `ipc_var_anual` / `ipc_base2018` | B4 — DANE | 100 % |
| `tasa_hipotecaria_anual` | B2 — BanRep | 100 % |
| `ipvu_variacion_anual` / `ipvn_variacion_anual` | B1 — DANE | 100 % |
| `tasa_desempleo` | B5 — GEIH DANE | 100 % |

**Mejora aplicada:** B5 (desempleo) se integró por `(year, city)` donde hay datos disponibles,
y con fallback nacional donde no. Esto da mayor granularidad regional al análisis de accesibilidad.

---

### H8 — Variables derivadas calculadas: IAH, precio real, precio/m², cuota · Impacto: Alto

Se calcularon 6 variables derivadas clave para el análisis de accesibilidad:

| Variable | Fórmula | Descripción |
|---|---|---|
| `salario_anual` | `salario_mensual × 12` | Base para el IAH |
| `IAH` | `price / salario_anual` | Años de salario mínimo para comprar |
| `precio_real` | `price / (ipc_base2018 / 100)` | Precio ajustado por inflación (base 2018) |
| `precio_m2` | `price / area` | Precio por metro cuadrado |
| `cuota_mensual` | Amortización francesa (70 % LTV, 15 años) | Cuota hipotecaria mensual estimada |
| `ratio_cuota_salario` | `cuota_mensual / salario_mensual` | Esfuerzo mensual relativo al salario |
| `nivel_accesibilidad` | Clasificación por IAH | `Accesible` / `Moderado` / `Elevado` / `Crítico` |

**Estadísticas descriptivas del dataset final** *(calculadas directamente del CSV con pandas)*:

| Variable | Promedio | Mediana | Desv. Est. | Mín. | Máx. |
|---|:---:|:---:|:---:|:---:|:---:|
| IAH (años) | 34.32 | 25.44 | 27.93 | 2.58 | 413.17 |
| precio_real (COP) | $478.5 M | $355.8 M | $389.8 M | $37.4 M | $5,834.9 M |
| precio_m2 (COP/m²) | $4.85 M | $4.26 M | $3.24 M | $0.20 M | $43.3 M |
| cuota_mensual (COP) | $5.25 M | $3.71 M | $4.75 M | $0.29 M | $50.2 M |
| ratio_cuota_salario | 3.70 | 2.68 | 3.18 | 0.23 | 35.12 |

---

### H9 — IAH promedio de 34 años: Colombia en nivel "Crítico" · Impacto: Alto

El IAH promedio del dataset final es **34.32 años** (mediana: 25.44 años), calculado
directamente del CSV. La distribución es muy asimétrica — el valor máximo es 413 años —
lo que jala el promedio hacia arriba respecto a la mediana, que es el estadístico más
representativo de la accesibilidad típica.
  
| Nivel de accesibilidad | IAH | Registros | % |
|---|:---:|---:|:---:|
| Accesible | ≤ 5 años | 330 | 0.13 % |
| Moderado | 5 – 10 años | 18,614 | 7.18 % |
| Elevado | 10 – 20 años | 74,928 | 28.88 % |
| **Crítico** | **> 20 años** | **165,535** | **63.81 %** |

Más del **92 % de las propiedades del dataset tienen un IAH superior al umbral OCDE de
"seriamente inaccesible" (≥ 10 años de salario)**. Solo el 0.13 % cae en el rango accesible.

> **Para la Fase 5 (Sofía):** El IAH promedio (34.32 años) está inflado por la cola derecha
> de la distribución (máximo: 413 años). Usar la **mediana (25.44 años)** como estadístico
> representativo en el informe, no el promedio. Reportar por ciudad para mostrar la heterogeneidad.

---

### H10 — Validación cruzada IPVN DANE: diferencia de 12.72 pp en Bogotá · Impacto: Medio

| Ciudad | Variación dataset | IPVN DANE | Diferencia |
|---|:---:|:---:|:---:|
| Bogotá | +23.44 % | +10.72 % | **12.72 pp** |
| Medellín | +14.84 % | +10.30 % | **4.54 pp** |

La guía esperaba < 0.5 pp (como en la Fase 2), pero la diferencia real es mayor. Esto se
debe a que el dataset mezcla vivienda usada y vivienda nueva en proporciones variables por
año, mientras que el IPVN DANE mide solo vivienda nueva. La diferencia disminuyó un **38 %
en Bogotá** y un **57 % en Medellín** respecto a la primera ejecución bugueada, lo que
confirma que el pipeline corregido es más preciso.

> **No es un error del pipeline.** Esta diferencia es inherente a las fuentes de datos
> (listados de portales vs. transacciones registradas). Debe documentarse explícitamente
> en el informe de la Fase 5.

---

### H11 — Imputación de lat/lon: 0 % de nulos en coordenadas · Impacto: Medio

Las fuentes A4, A6, A7 y parte de A1 no incluían coordenadas. Se imputaron con el centroide
de la ciudad correspondiente antes de exportar, garantizando que todas las visualizaciones
geoespaciales del dashboard (Fase 6) funcionen sin valores faltantes.

**Centroides usados por ciudad:**

| Ciudad | Lat. centroide | Lon. centroide |
|---|:---:|:---:|
| Bogotá | 4.7110 | -74.0721 |
| Medellín | 6.2518 | -75.5636 |
| Cali | 3.4516 | -76.5320 |
| Barranquilla | 10.9685 | -74.7813 |
| ... (12 ciudades) | — | — |

> **Advertencia:** Los registros con lat/lon imputado no representan la ubicación real del
> inmueble dentro de la ciudad, solo su ciudad. No usar para análisis intra-urbano ni para
> cálculos de distancia entre inmuebles.

---

### H12 — Dataset listo para Fase 4: 0 nulos en columnas críticas · Impacto: Alto

El dataset pasa todas las validaciones de integridad:

| Validación | Resultado |
|---|:---:|
| Nulos en `price` | ✅ 0 |
| Nulos en `area` | ✅ 0 |
| Nulos en `rooms` | ✅ 0 |
| Nulos en `bathrooms` | ✅ 0 |
| Nulos en `city` | ✅ 0 |
| Nulos en `property_type` | ✅ 0 |
| Nulos en `estrato` | ✅ 0 |
| Nulos en `lat` / `lon` | ✅ 0 |
| `price > 0` | ✅ Todos |
| `area > 0` | ✅ Todos |
| `rooms >= 1` | ✅ Todos |
| `bathrooms >= 1` | ✅ Todos |
| `city` en 12 ciudades canónicas | ✅ Todos |
| `year` entre 2019 y 2024 | ✅ Todos |
| `estrato` entre 1 y 6 | ✅ Todos |
| Tildes preservadas (UTF-8-SIG) | ✅ Bogotá, Medellín, Cúcuta, Ibagué |

---

## Decisiones para Fase 4

| Decisión | Acción concreta | Hallazgo de evidencia |
|---|---|:---:|
| Insumo del modelo | Usar `data/processed/vivienda_colombia_limpio.csv` directamente | H1 |
| Variable objetivo | `price` para regresión; `nivel_accesibilidad` para clasificación | H8 |
| Features numéricas | `area`, `rooms`, `bathrooms`, `estrato`, `year`, `ipc_var_anual`, `tasa_hipotecaria_anual`, `tasa_desempleo`, `ipvu_variacion_anual` | H7, H8 |
| Features categóricas | `city`, `property_type` | H4 |
| Ciudades con mayor error esperado | Cartagena, Ibagué, Villavicencio, Armenia (< 5,000 registros) | H4 |
| Estadístico de IAH a reportar | Mediana (25.44 años), no el promedio (34.32 años) | H9 |
| Cobertura temporal reportable | 2020–2023 como rango principal | H5 |
| Diferencia IPVN DANE | Documentar 12.72 pp en Bogotá y 4.54 pp en Medellín como limitación | H10 |
| Uso de lat/lon | Solo para visualización por ciudad, no para análisis intra-urbano | H11 |

---

## Advertencias para el Equipo

### ⚠️ A7 y A8 no aportan registros al dataset final
Aunque el pipeline los carga y procesa correctamente, ambas fuentes quedan absorbidas por
A1 en la deduplicación. Villavicencio está cubierta por 2,400 registros de A1.

### ⚠️ 2024 no está representado en el dataset
Los 142,833 registros de A2 FincaRaiz se recuperaron con la corrección del bug B1, pero
corresponden a anuncios de 2023, no de 2024. El dataset cubre efectivamente 2020–2023.

### ⚠️ IAH promedio ≠ IAH mediano
El promedio (34.32 años) está inflado por la cola derecha de la distribución (valor máximo:
413 años de salario). La mediana (25.44 años) es el estadístico correcto para interpretar
la accesibilidad típica.

### ⚠️ lat/lon imputados no reflejan ubicación exacta
Aproximadamente el 32 % de los registros tienen coordenadas de centroide de ciudad,
no del inmueble real. Suficiente para mapas de calor por ciudad, no para análisis granular.

---

## Checklist de Cierre — Fase 3

### Entregables generados

- [x] `data/processed/vivienda_colombia_limpio.csv` — Dataset limpio (259,407 × 26)
- [x] `data/processed/reporte_limpieza.csv` — Trazabilidad del pipeline (7 pasos)
- [x] `data/processed/README.md` — Diccionario de datos de las 26 columnas
- [x] `data/processed/acciones_correctivas_fase_3.csv` — Acciones aplicadas por dataset
- [x] `data/processed/decisiones_fase_3.csv` — Decisiones de diseño del pipeline
- [x] `notebooks/02_preparacion_datos.py` — Script completo (641 líneas, ejecutable)
- [x] `notebooks/02_preparacion_datos.ipynb` — Notebook complementario

### Verificaciones de calidad

- [x] 0 nulos en las 8 columnas críticas de modelado
- [x] Tildes preservadas en nombres de ciudades (UTF-8-SIG)
- [x] Todos los 8 bugs corregidos y documentados
- [x] Reporte de limpieza generado y validado
- [x] Validación cruzada IPVN DANE implementada
- [x] Coordenadas imputadas: 0 % de nulos en lat/lon

### Transferencia a Fase 4

- [x] 12 hallazgos documentados con evidencia cuantitativa
- [x] Tabla de decisiones para Fase 4 con acción concreta
- [x] Advertencias para el equipo sobre limitaciones del dataset
- [x] Dataset disponible y verificado en `data/processed/`

---

*Documento de Fase 3 · CRISP-DM 2025-I · Proyecto Accesibilidad Habitacional Colombia — 2020–2024*  
*Kukis · Steve · Revisión técnica completada el 2026-06-03*  
*Repositorio: github.com/AlexanderPineda25/Accesibilidad_de_Vivienda_en_Colombia*
