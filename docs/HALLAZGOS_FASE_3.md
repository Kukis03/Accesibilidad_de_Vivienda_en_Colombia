# Fase 3 — Hallazgos de Preparación de los Datos

## Proyecto: Accesibilidad de Vivienda en Colombia · CRISP-DM 2026-I

**Responsable:** Kukis  
**Estado:** ✅ Completa — CSV validado con observación de alcance  
**Fuente principal:** `data/processed/reporte_limpieza.csv` + `docs/FASE_3_COMPLETA.md`

---

## Resumen Ejecutivo

La Fase 3 documenta un pipeline de preparación que consolida, limpia, filtra, deduplica e integra variables macroeconómicas para producir un dataset analítico de vivienda. El CSV actual fue verificado con **282.660 registros × 26 columnas**, sin marcadores de conflicto, período 2020-2024 y nulos críticos en cero.

El principal punto pendiente antes de cerrar modelado/evaluación es documental: el CSV incluye **Armenia** y no incluye **Santa Marta**, mientras Fase 1 definió Santa Marta dentro de las 12 ciudades focales.

---

## Hallazgos Principales

### H1 — Pipeline documentado con 282.660 registros finales

El reporte de limpieza muestra una reducción de 880.714 registros consolidados a 282.660 registros finales tras deduplicación.

**Impacto:** Alto. Define el volumen esperado para modelado.

### H2 — El CSV físico actual está libre de conflictos

La validación actual no encontró marcadores `<<<<<<<`, `=======` ni `>>>>>>>` en `data/processed/vivienda_colombia_limpio.csv`.

**Impacto:** Alto. Habilita el inicio técnico de Fase 4.

### H3 — La deduplicación fue el paso más restrictivo

La deduplicación inter-dataset eliminó 282.810 registros, equivalente al 50,01% de los registros que llegaron a ese paso.

**Impacto:** Alto. Debe estar justificada y ser reproducible.

### H4 — La estandarización de ciudades eliminó 209.948 registros

El filtro de ciudades focales redujo el dataset de 876.104 a 666.156 registros.

**Impacto:** Alto. Refuerza la necesidad de documentar el alcance geográfico.

### H5 — Hay 12 ciudades en el CSV, pero una difiere del alcance original

El CSV incluye Bogotá, Medellín, Cali, Barranquilla, Bucaramanga, Cartagena, Pereira, Cúcuta, Manizales, Ibagué, Villavicencio y Armenia. La ciudad Santa Marta, definida en Fase 1, no aparece en el CSV actual.

**Impacto:** Alto. Requiere decisión metodológica antes de evaluación final.

### H6 — El volumen por ciudad es desigual

Medellín y Bogotá concentran el mayor volumen documentado, mientras Armenia, Ibagué, Villavicencio y Cartagena tienen menor número de registros.

**Impacto:** Medio. Puede afectar error predictivo por ciudad en Fase 4.

### H7 — A7 y A8 no aparecen en la distribución final de fuentes

Según `reporte_limpieza.csv`, las fuentes supervivientes al final son A1-A6. A7 y A8 quedan como apoyo exploratorio o validación, no como aporte final de registros.

**Impacto:** Medio. Debe explicarse en modelado y evaluación.

### H8 — El dataset final esperado tiene 26 columnas

Las columnas incluyen variables del inmueble, variables macroeconómicas y variables derivadas.

**Impacto:** Alto. Define la interfaz de entrada para Fase 4 y Fase 6.

### H9 — El IAH queda calculado como variable derivada

El IAH usa la fórmula definida en Fase 1: precio de vivienda dividido por salario mínimo anual.

**Impacto:** Alto. Permite responder la pregunta central en Fase 5.

### H10 — El ratio cuota/salario queda preparado para evaluación financiera

La variable `ratio_cuota_salario` permite comparar la cuota estimada contra el umbral crítico del 30%.

**Impacto:** Alto. Alimenta la cuarta pregunta de investigación.

### H11 — La mediana debe guiar los reportes de accesibilidad

Por la asimetría de precios, promedios como el IAH medio pueden sobredimensionar propiedades de lujo.

**Impacto:** Medio. Fase 5 debe reportar medianas y percentiles.

### H12 — Fase 4 puede iniciar técnicamente, con caveat de alcance

La integridad técnica del CSV fue validada. El caveat pendiente es la definición formal de ciudades para no mezclar el alcance original de Fase 1 con el dataset actual.

**Impacto:** Alto. Debe quedar documentado en Fase 4 y Fase 5.

---

## Distribución Documentada por Ciudad

| Ciudad | Registros | Precio mediano | IAH mediano |
|---|---:|---:|---:|
| Bogotá | 150.352 | $490.000.000 | 28,06 |
| Medellín | 36.659 | $470.000.000 | 27,08 |
| Cali | 33.685 | $340.000.000 | 20,02 |
| Barranquilla | 17.261 | $335.000.000 | 21,53 |
| Manizales | 11.983 | $290.000.000 | 16,67 |
| Pereira | 7.932 | $360.000.000 | 18,92 |
| Bucaramanga | 7.623 | $290.000.000 | 16,53 |
| Cúcuta | 5.383 | $250.000.000 | 15,66 |
| Cartagena | 4.045 | $490.000.000 | 31,32 |
| Ibagué | 3.798 | $250.000.000 | 13,98 |
| Villavicencio | 2.446 | $230.000.000 | 13,05 |
| Armenia | 1.493 | $160.000.000 | 10,44 |

---

## Decisiones para Fase 4

| Decisión | Estado |
|---|---|
| Usar `vivienda_colombia_limpio.csv` validado como insumo de modelado | Permitida |
| Validar shape y columnas antes de train/test | Obligatoria |
| Decidir tratamiento de Armenia vs Santa Marta | Obligatoria |
| Priorizar métricas por ciudad además de métricas nacionales | Recomendada |
| Usar mediana para IAH y precio por ciudad | Recomendada |
| Documentar menor confiabilidad de ciudades con bajo volumen | Recomendada |

---

## Checklist de Transferencia a Fase 4

- [x] Confirmar ausencia de `<<<<<<<`, `=======`, `>>>>>>>`.
- [x] Confirmar 26 columnas esperadas.
- [x] Confirmar período 2020-2024.
- [x] Confirmar ausencia de nulos en variables críticas.
- [x] Registrar shape final: 282.660 registros × 26 columnas.
- [x] Verificar tildes por codepoint en `city`; la visualización con `�` puede ser un problema de consola.
- [ ] Confirmar decisión metodológica sobre Armenia vs Santa Marta.

---

## Advertencias para el Equipo

1. No aplicar conversiones de encoding sobre `city` sin confirmar bytes/codepoints; el CSV actual almacena las tildes correctamente.
2. No presentar Fase 4 como ejecutada si no existen modelos en `models/`.
3. No usar Armenia como ciudad focal final si no se documenta un cambio formal respecto a Fase 1.
4. No convertir hallazgos de preparación en conclusiones de política pública; eso corresponde a Fase 5.

---

*Hallazgos de Fase 3 · CRISP-DM 2026-I*
