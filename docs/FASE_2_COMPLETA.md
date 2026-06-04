# Fase 2 — Comprensión de los Datos

## Proyecto: Accesibilidad de Vivienda en Colombia · CRISP-DM 2026-I

**Responsable principal:** Sofía · **Equipo:** Steve · Kukis  
**Período objetivo del proyecto:** 2020-2024  
**Estado:** ✅ Completa  
**Semanas:** 3-4

---

## Resumen Ejecutivo

La Fase 2 verificó la disponibilidad, estructura y calidad inicial de las **16 fuentes de datos** definidas en Fase 1: ocho fuentes de precios de vivienda (A1-A8) y ocho fuentes macroeconómicas/geográficas (B1-B8). El trabajo se concentró en conocer los datos antes de transformarlos: inventario, perfil de calidad, mapeo de columnas, nulos, duplicados, cobertura geográfica, cobertura temporal, outliers y consistencia preliminar con fuentes oficiales.

El resultado principal de esta fase es un conjunto de artefactos de diagnóstico en `data/processed/` y una lista de decisiones para Fase 3. No se entrenaron modelos ni se generaron conclusiones finales de negocio; esos resultados pertenecen a Fases 4 y 5.

---

## Contexto dentro de CRISP-DM

| Relación en el ciclo | Descripción |
|---|---|
| Entrada desde Fase 1 | Inventario de 16 fuentes, 12 ciudades focales, variables críticas y criterios de éxito. |
| Rol de Fase 2 | Comprender estructura, calidad y cobertura real de los datos disponibles. |
| Salida hacia Fase 3 | Mapeo canónico, problemas de esquema, acciones correctivas y reportes de calidad. |
| Salida indirecta hacia Fase 4 | Identificación de variables candidatas y riesgos para modelado. |

---

## Objetivos de la Fase

1. Verificar que los 16 archivos definidos en Fase 1 existen y pueden cargarse.
2. Documentar tamaño, columnas, tipos de dato, nulos y duplicados por fuente.
3. Definir un esquema canónico común para los datasets de vivienda.
4. Identificar problemas que deben corregirse en Fase 3.
5. Producir hallazgos preliminares sin convertirlos en conclusiones finales.

---

## Alcance Ejecutado

| Elemento | Resultado |
|---|---|
| Fuentes verificadas | 16 archivos en `data/raw/` |
| Grupo A | 8 datasets de precios inmobiliarios |
| Grupo B | 8 fuentes macroeconómicas/geográficas |
| Notebooks de EDA | 11 notebooks registrados en `metadatos_fase_2.json` |
| Hallazgos documentados | 13 hallazgos principales |
| Decisiones para Fase 3 | 9 decisiones documentadas |
| Acciones correctivas | 8 acciones documentadas |

---

## Actividades Realizadas

1. Inventario físico de archivos crudos A1-A8 y B1-B8.
2. Perfil de calidad por dataset: filas, columnas, tamaño, nulos y duplicados.
3. Definición del esquema canónico para vivienda: `price`, `area`, `rooms`, `bathrooms`, `property_type`, `city`, `lat`, `lon`, `created_on`, `barrio`, `parking`, `estrato`, `fuente`.
4. Exploración de precios, áreas, ciudades, tipos de propiedad y cobertura temporal.
5. Revisión inicial de variables macroeconómicas: salario mínimo, IPC, tasas hipotecarias, empleo, IPVU/IPVN y fuentes complementarias.
6. Documentación de problemas por dataset y decisiones requeridas para Fase 3.
7. Generación de figuras exploratorias y reportes CSV/JSON en `data/processed/`.

---

## Correspondencia con GUIA_FASE_2.md

| Actividad planificada | Estado | Evidencia | Sección |
|---|---|---|---|
| Inventario de fuentes y carga inicial | ✅ Completo | `reporte_calidad_datasets.csv` contiene 16 fuentes | Inventario |
| Esquema canónico | ✅ Completo | `mapeo_canonico.json` define 13 columnas canónicas | Metodología |
| Calidad de datos | ✅ Completo | `calidad_grupo_a.csv`, `calidad_grupo_b.csv`, `reporte_nulos_completo.csv` | Resultados |
| Distribución de precios | ✅ Completo | `estadisticas_precio.csv` y figuras en `docs/figures/` | Resultados |
| Análisis geográfico | ✅ Completo | `resumen_precios_ciudad.csv` | Hallazgos |
| Refuerzo Villavicencio A7 | ✅ Completo | `A7_fincaraiz_villavicencio_scraping.csv`, `villavicencio_consolidado.csv` | Hallazgos |
| Variables macroeconómicas | ✅ Completo | `macrovariables_consolidadas.csv` | Resultados |
| IAH preliminar | ✅ Completo | Notebooks y figuras de EDA; cálculo definitivo queda para Fase 3 | Limitaciones |
| Validación oficial | ⚠️ Parcial | Comparaciones preliminares; validación final depende de Fase 3 | Validaciones |
| Preparación para GitHub | ⚠️ Parcial | Hay documentación y artefactos, pero Fase 3 detectó problemas posteriores | Riesgos |

---

## Metodología Aplicada

La metodología fue exploratoria y documental. Se trabajó con lectura de archivos, perfiles de calidad, tablas de resumen y visualizaciones. El objetivo no fue limpiar ni modelar, sino levantar evidencia para decidir cómo preparar los datos.

La Fase 2 separó tres niveles de análisis:

| Nivel | Propósito |
|---|---|
| Inventario | Confirmar existencia, tamaño y columnas reales de cada fuente. |
| Calidad | Detectar nulos, duplicados, outliers y problemas de formato. |
| Integrabilidad | Determinar qué columnas pueden mapearse al esquema canónico de Fase 3. |

---

## Resultados Obtenidos

### Inventario físico de fuentes

| Grupo | Fuentes | Filas crudas documentadas | Observación |
|---|---:|---:|---|
| A — Precios de vivienda | 8 | 3.005.876 | A1 incluye datos multi-país; el subconjunto colombiano relevante se perfiló aparte. |
| B — Macro/geografía | 8 | 3.435 | Series oficiales o complementarias de menor volumen. |
| Total | 16 | 3.009.311 | Inventario físico post-descarga. |

### Calidad del Grupo A

| Dataset | Filas perfiladas | Columnas | Nulos totales | Duplicados | Observación |
|---|---:|---:|---:|---:|---|
| A1 | 997.623 | 17 | 12,18% | 0 | Principal fuente histórica tras filtrar Colombia. |
| A2 | 142.833 | 28 | 14,41% | 0 | Fuente clave para 2023-2024. |
| A3 | 145.552 | 37 | 38,13% | 70.794 | Alta duplicidad y muchas columnas de amenities. |
| A4 | 9.520 | 8 | 0,06% | 3.575 | Bogotá por barrio; requiere deduplicación. |
| A5 | 9.999 | 12 | 5,02% | 100 | Medellín 2023. |
| A6 | 585 | 21 | 0,28% | 0 | Bogotá 2023, bajo volumen. |
| A7 | 1.048 | 24 | 2,64% | 0 | Scraping propio Villavicencio. |
| A8 | 32 | 14 | 0,00% | 0 | Referencia oficial Bogotá UPZ, no apta para entrenar. |

### Calidad del Grupo B

| Dataset | Filas | Columnas | Nulos totales | Duplicados | Uso esperado |
|---|---:|---:|---:|---:|---|
| B1 | 332 | 16 | 23,40% | 0 | IPVN/IPVU para contexto y validación. |
| B2 | 1.255 | 7 | 0,00% | 0 | Tasa hipotecaria semanal. |
| B3 | 43 | 5 | 7,44% | 0 | Salario mínimo histórico. |
| B4 | 10 | 2 | 0,00% | 0 | IPC anual. |
| B5 | 1.202 | 6 | 8,37% | 0 | GEIH/desempleo. |
| B6 | 148 | 2 | 0,00% | 0 | Confianza constructora. |
| B7 | 152 | 2 | 0,00% | 0 | Licencias de construcción. |
| B8 | 293 | 2 | 0,00% | 0 | Referencias geográficas. |

---

## Métricas y Estadísticas Relevantes

| Métrica | Valor |
|---|---:|
| Fuentes confirmadas | 16 |
| Columnas canónicas definidas | 13 |
| Figuras exploratorias generadas | 31 según `GUIA_FASE_2.md` |
| Hallazgos principales documentados | 13 |
| Decisiones para Fase 3 | 9 |
| Acciones correctivas para Fase 3 | 8 |
| Datasets con duplicados relevantes | A3, A4, A5 |
| Dataset con mayor tasa de nulos en Grupo A | A3, 38,13% |
| Dataset macro con mayor tasa de nulos | B1, 23,40% |

---

## Hallazgos Clave

1. Las 16 fuentes existen y son utilizables, pero no tienen estructura homogénea.
2. A1 es la fuente principal, pero requiere filtrado geográfico estricto para quedarse con Colombia.
3. A2 es crítico para cubrir 2023-2024.
4. A3 aporta volumen, pero también duplicados y columnas de baja completitud.
5. A7 refuerza Villavicencio, aunque su aporte final debe validarse en Fase 3.
6. A8 es útil como referencia oficial, no como fuente de entrenamiento.
7. La distribución de precios es asimétrica y requiere tratamiento robusto de outliers.
8. La integración de macrovariables debe hacerse por año y, cuando sea posible, por ciudad.
9. El IAH calculado en Fase 2 es preliminar; el cálculo definitivo pertenece a Fase 3.
10. El período operativo del proyecto debe mantenerse en 2020-2024, según la Fase 1 y la confirmación posterior de Fase 3.

---

## Problemas Encontrados y Resolución

| Problema | Impacto | Resolución/traslado |
|---|---|---|
| Esquemas heterogéneos entre A1-A8 | Alto | Crear `mapeo_canonico.json`. |
| A1 contiene registros fuera de Colombia | Alto | Filtrar por ubicación colombiana en Fase 3. |
| Duplicados en A3 y A4 | Alto | Diseñar deduplicación inter-dataset en Fase 3. |
| Diferentes formatos de precio y moneda | Alto | Normalizar precios y revisar COP/USD en Fase 3. |
| Cobertura irregular por ciudad | Medio | Aplicar umbral de cobertura y documentar ciudades limitadas. |
| A8 tiene solo 32 registros | Bajo para modelado, medio para validación | Usar como referencia, no como entrenamiento. |

---

## Validaciones Realizadas

- Confirmación de presencia de los 16 archivos crudos.
- Confirmación de columnas reales por dataset.
- Revisión de nulos y duplicados.
- Revisión de rangos de precios y áreas.
- Revisión preliminar de consistencia macroeconómica.
- Generación de reportes procesados reproducibles para alimentar Fase 3.

---

## Entregables Generados

| Entregable | Ubicación | Estado |
|---|---|---|
| Reporte de Fase 2 | `docs/FASE_2_COMPLETA.md` | ✅ Actualizado |
| Hallazgos de Fase 2 | `docs/HALLAZGOS_FASE_2.md` | ✅ Actualizado |
| Guía de ejecución | `docs/GUIA_FASE_2.md` | ✅ Disponible |
| Inventario de datasets | `data/processed/reporte_calidad_datasets.csv` | ✅ Disponible |
| Calidad Grupo A | `data/processed/calidad_grupo_a.csv` | ✅ Disponible |
| Calidad Grupo B | `data/processed/calidad_grupo_b.csv` | ✅ Disponible |
| Reporte de nulos | `data/processed/reporte_nulos_completo.csv` | ✅ Disponible |
| Mapeo canónico | `data/processed/mapeo_canonico.json` | ✅ Disponible |
| Problemas de esquema | `data/processed/problemas_esquema.json` | ✅ Disponible |
| Metadatos | `data/processed/metadatos_fase_2.json` | ✅ Disponible |

---

## Riesgos o Limitaciones Detectadas

1. **No inferir resultados finales desde EDA:** los hallazgos de Fase 2 son diagnósticos, no conclusiones de negocio.
2. **No mezclar período exploratorio con período objetivo:** puede haber datos fuera de 2020-2024, pero el proyecto está acotado a 2020-2024.
3. **No usar A8 como dataset de entrenamiento:** su volumen es insuficiente.
4. **Controlar duplicados antes del modelado:** la duplicación afecta métricas y sesga modelos.
5. **Validar el dataset final antes de Fase 4:** Fase 4 debe partir de un CSV limpio, sin marcadores de conflicto ni inconsistencias.

---

## Conclusiones

La Fase 2 cumplió su propósito CRISP-DM: transformar el inventario conceptual de Fase 1 en conocimiento técnico de los datos reales. Se confirmaron las fuentes, se identificaron los problemas principales y se dejaron insumos concretos para preparar el dataset analítico.

La fase no produce modelos, métricas de desempeño, respuestas finales a las preguntas de investigación ni dashboard. Esos resultados se deben completar en Fases 4, 5 y 6.

---

## Preparación para la Siguiente Fase

### Prerrequisitos técnicos para Fase 3

1. Usar `mapeo_canonico.json` como guía de normalización.
2. Aplicar filtros de país, ciudad, tipo de propiedad y período 2020-2024.
3. Resolver duplicados inter-dataset con reglas documentadas.
4. Integrar macrovariables por año y ciudad cuando exista granularidad.
5. Exportar un dataset final con esquema documentado y validaciones de integridad.

### Riesgos heredados hacia Fase 3

| Riesgo | Acción requerida |
|---|---|
| Duplicados y solapamiento temporal | Diseñar deduplicación reproducible. |
| Precios en formatos inconsistentes | Normalizar unidades y moneda. |
| Ciudades con baja cobertura | Documentar exclusiones o incertidumbre. |
| Variables macro con granularidad nacional | Explicitar cuándo se usa fallback nacional. |

---

*Documento de Fase 2 · CRISP-DM 2026-I · Accesibilidad Habitacional Colombia*
