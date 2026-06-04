# Fase 3 — Preparación de los Datos

## Proyecto: Accesibilidad de Vivienda en Colombia · CRISP-DM 2026-I

**Responsable principal:** Kukis · **Apoyo:** Steve · Sofía
**Período objetivo del proyecto:** 2020–2024
**Estado:** ✅ Completa — dataset listo para Fase 4
**Semanas:** 5–6

---

## Resumen Ejecutivo

La Fase 3 transformó los diagnósticos de Fase 2 en un pipeline de preparación de datos para producir un dataset integrado de vivienda y macrovariables. El pipeline pasó de **880.714 registros consolidados** a **282.660 registros finales** después de limpieza, filtrado, estandarización, eliminación de outliers y deduplicación.

El dataset final tiene **26 columnas** e incluye variables estructurales del inmueble (`price`, `area`, `rooms`, `bathrooms`, `property_type`, `city`, `lat`, `lon`), variables macroeconómicas (`salario_mensual`, `ipc_var_anual`, `tasa_hipotecaria_anual`, `tasa_desempleo`, etc.) y variables derivadas de accesibilidad: **IAH**, `precio_real`, `precio_m2`, `cuota_mensual`, `ratio_cuota_salario` y `nivel_accesibilidad`.

> El archivo `data/processed/vivienda_colombia_limpio.csv` está limpio, sin marcadores de conflicto, y listo para modelado.

---

## Contexto dentro de CRISP-DM

| Relación en el ciclo | Descripción |
|---|---|
| Entrada desde Fase 2 | Mapeo canónico, reportes de calidad, acciones correctivas y problemas por dataset. |
| Rol de Fase 3 | Limpiar, estandarizar, deduplicar, integrar macrovariables y construir variables derivadas. |
| Salida hacia Fase 4 | Dataset limpio, validado y listo para entrenamiento de modelos. |

---

## Objetivos de la Fase

1. Integrar los datasets inmobiliarios A1–A8 bajo un esquema común.
2. Estandarizar precios, ciudades, tipos de propiedad y años.
3. Filtrar el período operativo 2020–2024.
4. Eliminar outliers y duplicados inter-dataset con reglas reproducibles.
5. Integrar variables macroeconómicas B1–B8 y derivadas necesarias para IAH.
6. Exportar un dataset final documentado para modelado.

---

## Alcance Ejecutado

| Elemento | Resultado |
|---:|---:|
| Registros consolidados iniciales | 880.714 |
| Registros tras limpieza de precios | 876.104 |
| Registros tras filtro de ciudades | 666.156 |
| Registros tras filtro temporal | 652.047 |
| Registros tras tipo de inmueble | 598.353 |
| Registros tras outliers IQR | 565.470 |
| Registros finales tras deduplicación | **282.660** |
| Columnas finales | **26** |
| Tamaño en disco | ~85 MB |

---

## Pipeline de Limpieza

| Paso | Operación | Entrada | Salida | Eliminados | % |
|---:|---|---:|---:|---:|---:|
| 0 | Consolidación inicial | 0 | 880.714 | — | — |
| 1 | Limpieza precios e invalidez | 880.714 | 876.104 | 4.610 | 0,52 % |
| 2 | Estandarización / filtro ciudades | 876.104 | 666.156 | 209.948 | 23,96 % |
| 3 | Restricción temporal | 666.156 | 652.047 | 14.109 | 2,12 % |
| 4 | Tipo de inmueble | 652.047 | 598.353 | 53.694 | 8,23 % |
| 5 | Filtro IQR outliers por grupo | 598.353 | 565.470 | 32.883 | 5,50 % |
| 6 | Deduplicación inter-dataset v2 | 565.470 | 282.660 | 282.810 | 50,01 % |

---

## Distribución por Ciudad

| Ciudad | Registros | % | Precio Mediano | IAH Mediano |
|---|---:|---:|---:|---:|
| Bogotá | 150.352 | 53,19 % | $ 490.000.000 | 28,06 |
| Medellín | 36.659 | 12,97 % | $ 470.000.000 | 27,08 |
| Cali | 33.685 | 11,92 % | $ 340.000.000 | 20,02 |
| Barranquilla | 17.261 | 6,11 % | $ 335.000.000 | 21,53 |
| Manizales | 11.983 | 4,24 % | $ 290.000.000 | 16,67 |
| Pereira | 7.932 | 2,81 % | $ 360.000.000 | 18,92 |
| Bucaramanga | 7.623 | 2,70 % | $ 290.000.000 | 16,53 |
| Cúcuta | 5.383 | 1,90 % | $ 250.000.000 | 15,66 |
| Cartagena | 4.045 | 1,43 % | $ 490.000.000 | 31,32 |
| Ibagué | 3.798 | 1,34 % | $ 250.000.000 | 13,98 |
| Villavicencio | 2.446 | 0,87 % | $ 230.000.000 | 13,05 |
| Armenia | 1.493 | 0,53 % | $ 160.000.000 | 10,44 |
| **Total** | **282.660** | **100 %** | **$ 430.000.000** | **24,40** |

---

## Distribución por Fuente

| Fuente | Descripción | Registros | % |
|---|---:|---:|---:|
| A1_Properati | Properati (Bogotá) | 135.934 | 48,09 % |
| A2_FincaRaiz_Kaggle | FincaRaiz (nacional) | 72.393 | 25,61 % |
| A3_Kaggle | Kaggle House Prediction | 63.950 | 22,62 % |
| A5_Medellin_Kaggle | Medellín Kaggle | 5.557 | 1,97 % |
| A4_Bogota_Kaggle | Bogotá Kaggle | 4.312 | 1,53 % |
| A6_Bogota2023_Kaggle | Bogotá 2023 Kaggle | 514 | 0,18 % |
| **Total** | | **282.660** | **100 %** |

---

## Distribución por Año

| Año | Registros | % |
|---:|---:|---:|
| 2020 | 60.399 | 21,37 % |
| 2021 | 75.535 | 26,72 % |
| 2022 | 69.993 | 24,76 % |
| 2023 | 8.014 | 2,84 % |
| 2024 | 68.719 | 24,31 % |
| **Total** | **282.660** | **100 %** |

El volumen bajo de 2023 se debe a la corrección B9: los registros A2 con `Fecha Actualizacion` en 2024 se reclasificaron correctamente de 2023 a 2024.

---

## Variables Derivadas

| Variable | Descripción |
|---|---|
| `salario_anual` | `salario_mensual × 12` |
| `IAH` | `price / salario_anual` (años de salario para comprar) |
| `precio_real` | `price × (ipc_base2018 / ipc_base2018_del_año)` |
| `precio_m2` | `price / area` |
| `cuota_mensual` | Cuota bajo tasa hipotecaria a 15 años (180 meses), con 70 % financiado |
| `ratio_cuota_salario` | `cuota_mensual / salario_mensual` |
| `nivel_accesibilidad` | Categorías de Fase 1: Accesible (IAH ≤ 5), Moderado (5–10), Elevado (10–20), Crítico (>20) |

---

## Calidad del Dataset

| Verificación | Resultado |
|---|---|
| Registros totales | 282.660 |
| Columnas | 26 |
| Nulos en columnas críticas (`price`, `area`, `rooms`, `bathrooms`, `property_type`, `city`, `lat`, `lon`, `estrato`, `year`) | **0** |
| Nulos en `created_on` (esperado) | 74.333 (26,3 %) |
| Merge conflicts | **0** — archivo limpio |
| Ciudades en el CSV | 12; incluye Armenia y no incluye Santa Marta frente al alcance original |
| Rango de años | 2020–2024 |

---

## Hallazgos Clave

1. La deduplicación inter-dataset fue el paso más restrictivo: eliminó 282.810 registros (50,01 %).
2. Bogotá concentra el 53,19 % del dataset — cualquier modelo de regresión estará dominado por su mercado.
3. 2023 tiene solo 8.014 registros por la corrección B9 (A2 reclasificado a 2024); esto debe considerarse en validación temporal.
4. A7 (Villavicencio) y A8 (Caracol UPZ) no aportan registros finales; su utilidad queda como exploración.
5. El IAH promedio es 32,85 y el IAH mediano es 24,40; ambos clasifican como "Crítico" según el umbral de Fase 1 (>20).
6. `created_on` tiene 26,3 % de nulos (fuentes A3–A6 sin fecha de publicación), pero el año se imputa correctamente desde la fuente.
7. Las variables macroeconómicas están integradas al 100 % en todos los registros.

---

## Problemas y Correcciones (8 Bugs)

| Bug | Descripción | Impacto | Corrección |
|---|---|---|---|
| B1 | A2 precio multiplicado por 1.000.000 (ya estaba en COP) | 142.833 registros perdidos | Eliminar multiplicación |
| B2 | A2 sin coordenadas | Modelos geoespaciales degradados | Extraer lat/lon desde Link Google Maps |
| B3 | A2 sin enlace `created_on` | Fecha de publicación ausente | Mapear `Fecha Actualizacion` → `created_on` |
| B4 | A3 sin ciudad asignada | 2.766 registros sin geografía | Asignar Bogotá por fuente |
| B5 | A4 sin ciudad asignada | 7.003 registros sin geografía | Asignar Bogotá por fuente |
| B6 | A5 con `bathrooms` como string | Tipo de dato incorrecto | Convertir a numérico |
| B7 | A6 sin ciudad asignada | 407 registros sin geografía | Asignar Bogotá por fuente |
| B9 | `año_fuente['A2']` hardcodeado en 2023 | 117.664 registros etiquetados como 2023 en vez de 2024 | Cambiar a 2024 |

> Tras la corrección de todos los bugs, el dataset pasó de 54.904 a 282.660 registros (recuperación de ~227.756 registros).

---

## Entregables

| Entregable | Ruta | Estado |
|---|---|---|
| Reporte de Fase 3 | `docs/FASE_3_COMPLETA.md` | ✅ Actualizado |
| Hallazgos de Fase 3 | `docs/HALLAZGOS_FASE_3.md` | ✅ Actualizado |
| Guía de Fase 3 | `docs/GUIA_FASE_3.md` | ✅ Disponible |
| Script de preparación | `notebooks/02_preparacion_datos.py` | ✅ Actualizado |
| Notebook de preparación | `notebooks/02_preparacion_datos.ipynb` | ✅ Disponible |
| Reporte de limpieza | `data/processed/reporte_limpieza.csv` | ✅ Disponible |
| Dataset integrado | `data/processed/vivienda_colombia_limpio.csv` | ✅ Listo para Fase 4 |
| Diccionario de datos | `data/processed/README.md` | ✅ Disponible |
| Decisiones de fase | `data/processed/decisiones_fase_3.csv` | ✅ Disponible |
| Acciones correctivas | `data/processed/acciones_correctivas_fase_3.csv` | ✅ Disponible |

---

## Preparación para Fase 4

### Prerrequisitos cumplidos

1. ✅ `vivienda_colombia_limpio.csv` sin marcadores de conflicto
2. ✅ 282.660 registros × 26 columnas
3. ✅ 0 nulos en columnas críticas para modelado
4. ✅ 12 ciudades presentes; queda pendiente decisión formal sobre Armenia vs Santa Marta
5. ✅ Reportes de limpieza y trazabilidad disponibles

### Artefactos que Fase 4 debe consumir

| Artefacto | Uso |
|---|---|
| `vivienda_colombia_limpio.csv` | Entrenamiento de regresión y clustering |
| `reporte_limpieza.csv` | Trazabilidad de preparación |
| `data/processed/README.md` | Diccionario de columnas |
| `decisiones_fase_3.csv` | Justificación metodológica |

---

*Documento de Fase 3 · CRISP-DM 2026-I · Accesibilidad Habitacional Colombia*
