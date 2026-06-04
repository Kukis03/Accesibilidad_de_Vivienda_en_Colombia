# Fase 2 — Hallazgos de Comprensión de los Datos

## Proyecto: Accesibilidad de Vivienda en Colombia · CRISP-DM 2026-I

**Responsable:** Sofía  
**Estado:** ✅ Completa  
**Fuente principal:** `data/processed/` + `docs/FASE_2_COMPLETA.md`

---

## Resumen Ejecutivo

La Fase 2 confirmó que el proyecto cuenta con las **16 fuentes de datos** definidas en Fase 1, pero también evidenció que las fuentes no están listas para modelado directo. Los principales retos son heterogeneidad de esquemas, duplicados, nulos, diferencias de cobertura temporal/geográfica y necesidad de estandarización antes de entrenar modelos.

Estos hallazgos son diagnósticos. No deben leerse como conclusiones finales del negocio ni como resultados de modelado.

---

## Hallazgos Principales

### H1 — Las 16 fuentes definidas en Fase 1 están presentes

Se verificaron 8 fuentes inmobiliarias (A1-A8) y 8 fuentes macroeconómicas/geográficas (B1-B8). El inventario físico suma 3.009.311 filas crudas, aunque A1 contiene datos multi-país y requiere filtrado colombiano.

**Impacto:** Alto. Confirma viabilidad de continuar a Fase 3.

### H2 — A1 es la fuente principal, pero requiere filtrado geográfico

A1 tiene 2.695.508 filas en el archivo crudo, pero el perfil colombiano relevante documentado en Fase 2 queda en 997.623 filas.

**Impacto:** Alto. Sin filtro de país, el dataset final mezclaría mercados no colombianos.

### H3 — El esquema de vivienda no es homogéneo entre A1-A8

Se definieron 13 columnas canónicas para preparar la integración: precio, área, habitaciones, baños, tipo, ciudad, coordenadas, fecha, barrio, parqueadero, estrato y fuente.

**Impacto:** Alto. Fase 3 depende de `mapeo_canonico.json`.

### H4 — A3 tiene el mayor problema de nulos y duplicados

A3 registra 38,13% de nulos totales y 70.794 duplicados. Sus columnas de amenities no deben incorporarse automáticamente al modelo.

**Impacto:** Medio-alto. Requiere limpieza y selección de variables.

### H5 — A4 también tiene duplicados relevantes

A4 contiene 3.575 duplicados sobre 9.520 filas perfiladas.

**Impacto:** Medio. Debe entrar a deduplicación inter-dataset.

### H6 — A8 es útil para validación, no para entrenamiento

A8 tiene 32 registros de precios de vivienda nueva por UPZ en Bogotá. Su volumen es insuficiente para modelado.

**Impacto:** Medio. Se recomienda usarlo como referencia o contraste oficial.

### H7 — A7 documenta refuerzo de Villavicencio

A7 contiene datos de scraping de Villavicencio y mejora la comprensión exploratoria de esa ciudad. Su aporte final debe confirmarse en el pipeline de Fase 3.

**Impacto:** Medio. Apoya cobertura de ciudad intermedia.

### H8 — Las variables macro son de bajo volumen, pero suficientes como contexto anual

B1-B8 tienen menor volumen que los datasets inmobiliarios. Su función principal es enriquecer el dataset con salario, IPC, tasa hipotecaria, desempleo y referencias oficiales.

**Impacto:** Alto. Permiten calcular IAH y ratio cuota/salario.

### H9 — La distribución de precios exige tratamiento robusto

La exploración confirmó fuerte asimetría y presencia de outliers. Para reportes de negocio se debe priorizar la mediana sobre el promedio.

**Impacto:** Alto. Afecta IAH, modelos y conclusiones.

### H10 — La cobertura temporal debe alinearse a 2020-2024

Aunque algunos archivos pueden contener años fuera del alcance operativo, Fase 1 fija el período del proyecto en 2020-2024.

**Impacto:** Alto. Evita conclusiones fuera de alcance.

### H11 — Las ciudades deben alinearse con las 12 focales de Fase 1

La documentación y la app deben usar la misma lista: Bogotá, Medellín, Cali, Barranquilla, Bucaramanga, Cartagena, Pereira, Cúcuta, Manizales, Ibagué, Santa Marta y Villavicencio.

**Impacto:** Alto. Evita inconsistencias entre análisis, modelos y dashboard.

### H12 — El IAH de Fase 2 es preliminar

El cálculo definitivo del IAH corresponde a Fase 3, después de limpiar, deduplicar e integrar macrovariables.

**Impacto:** Medio. No usar cifras preliminares como conclusión final.

### H13 — Fase 3 debe resolver calidad antes de modelar

Las decisiones de preparación están registradas en `decisiones_fase_3.csv` y `acciones_correctivas_fase_3.csv`.

**Impacto:** Alto. Fase 4 depende de un dataset limpio.

---

## Decisiones para Fase 3

| Decisión | Justificación |
|---|---|
| Usar esquema canónico | Permite integrar A1-A8 sin perder trazabilidad. |
| Filtrar país y ciudades focales | Alinea datos con el alcance de Fase 1. |
| Normalizar precios y moneda | Evita errores de escala. |
| Deduplicar inter-dataset | Reduce sesgo por registros repetidos. |
| Usar A8 como validación | Evita sobrerrepresentar 32 registros oficiales. |
| Calcular IAH solo tras limpieza | Evita indicadores sesgados por outliers o duplicados. |

---

## Advertencias

1. No reportar métricas de modelo desde Fase 2.
2. No afirmar que el dashboard está desplegado desde hallazgos EDA.
3. No extender el período final más allá de 2020-2024 sin justificarlo.
4. No usar ciudades fuera de las 12 focales de Fase 1 sin documentar el cambio.

---

## Transferencia a Fase 3

| Artefacto | Uso |
|---|---|
| `mapeo_canonico.json` | Normalización de columnas. |
| `problemas_esquema.json` | Lista de problemas por fuente. |
| `reporte_calidad_datasets.csv` | Inventario y tamaños. |
| `calidad_grupo_a.csv` | Calidad de datasets inmobiliarios. |
| `calidad_grupo_b.csv` | Calidad de macrovariables. |
| `reporte_nulos_completo.csv` | Tratamiento de nulos. |
| `acciones_correctivas_fase_3.csv` | Cambios requeridos en preparación. |

---

*Hallazgos de Fase 2 · CRISP-DM 2026-I*
