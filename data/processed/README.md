# Datos Procesados — Accesibilidad de Vivienda en Colombia

Este directorio contiene artefactos generados durante las Fases 2 y 3 del proyecto CRISP-DM.

> **Estado actual:** `vivienda_colombia_limpio.csv` fue validado sin marcadores de conflicto, con **282.660 registros × 26 columnas** y período 2020-2024. **Decisión:** Armenia se incorporó al alcance (datos 2020-2021). Santa Marta se excluyó por falta de datos en las fuentes utilizadas.

---

## Archivos principales

| Archivo | Fase | Descripción | Estado |
|---|---:|---|---|
| `reporte_calidad_datasets.csv` | 2 | Inventario de las 16 fuentes crudas. | Disponible |
| `calidad_grupo_a.csv` | 2 | Calidad de datasets inmobiliarios A1-A8. | Disponible |
| `calidad_grupo_b.csv` | 2 | Calidad de fuentes macro/geográficas B1-B8. | Disponible |
| `reporte_nulos_completo.csv` | 2 | Nulos por columna y dataset. | Disponible |
| `mapeo_canonico.json` | 2 | Mapeo de columnas originales al esquema canónico. | Disponible |
| `problemas_esquema.json` | 2 | Problemas detectados por fuente. | Disponible |
| `metadatos_fase_2.json` | 2 | Metadatos de notebooks, hallazgos y decisiones. | Disponible |
| `reporte_limpieza.csv` | 3 | Trazabilidad del pipeline de limpieza. | Disponible |
| `decisiones_fase_3.csv` | 3 | Decisiones metodológicas aplicadas en preparación. | Disponible |
| `acciones_correctivas_fase_3.csv` | 3 | Acciones requeridas/corregidas por problema. | Disponible |
| `resumen_precios_ciudad.csv` | 3 | Resumen de registros y precios por ciudad. | Disponible |
| `vivienda_colombia_limpio.csv` | 3 | Dataset integrado para modelado. | Validado con caveat de alcance |

---

## Salida esperada de Fase 3

Según la validación actual del CSV y `reporte_limpieza.csv`, la salida final del pipeline es:

| Métrica | Valor |
|---|---:|
| Registros finales | 282.660 |
| Columnas finales | 26 |
| Período objetivo | 2020-2024 |
| Ciudades en el CSV | 12 |

Decisión final: **Armenia se incorporó** al alcance (datos disponibles 2020-2021). **Santa Marta no se incluyó** por falta de datos en las fuentes utilizadas. El dataset final tiene 12 ciudades: las 11 originales + Armenia.

---

## Diccionario de Datos Esperado

| Columna | Tipo esperado | Descripción |
|---|---|---|
| `price` | float | Precio de venta del inmueble en COP. |
| `area` | float | Área del inmueble en metros cuadrados. |
| `rooms` | int/float | Número de habitaciones. |
| `bathrooms` | int/float | Número de baños. |
| `property_type` | str | Tipo de propiedad, principalmente `Casa` o `Apartamento`. |
| `city` | str | Ciudad estandarizada. 12 ciudades: Bogotá, Medellín, Cali, Barranquilla, Bucaramanga, Cartagena, Pereira, Cúcuta, Manizales, Ibagué, Villavicencio, Armenia. Santa Marta no aparece por falta de datos. |
| `lat` | float | Latitud; puede estar imputada por centroide de ciudad. |
| `lon` | float | Longitud; puede estar imputada por centroide de ciudad. |
| `created_on` | datetime/str | Fecha de publicación o extracción cuando existe. |
| `estrato` | int/float | Estrato socioeconómico estimado o reportado. |
| `fuente` | str | Fuente de origen del registro. |
| `year` | int | Año de análisis. |
| `salario_mensual` | float | Salario mínimo mensual vigente para el año. |
| `ipc_var_anual` | float | Variación anual del IPC. |
| `ipc_base2018` | float | Índice IPC con base 2018. |
| `tasa_hipotecaria_anual` | float | Tasa hipotecaria anual promedio. |
| `tasa_desempleo` | float | Tasa de desempleo usada como contexto macro. |
| `ipvu_variacion_anual` | float | Variación anual del IPVU. |
| `ipvn_variacion_anual` | float | Variación anual del IPVN. |
| `salario_anual` | float | Salario mínimo anual (`salario_mensual × 12`). |
| `IAH` | float | Indice de Accesibilidad Habitacional (`price / salario_anual`). |
| `precio_real` | float | Precio ajustado por inflación. |
| `precio_m2` | float | Precio por metro cuadrado. |
| `cuota_mensual` | float | Cuota estimada con supuestos de financiación documentados. |
| `ratio_cuota_salario` | float | Relación entre cuota mensual y salario mínimo mensual. |
| `nivel_accesibilidad` | str | Clasificación: `Accesible`, `Moderado`, `Elevado` o `Crítico`. |

---

## Validaciones requeridas antes de Fase 4

- [x] El archivo no contiene `<<<<<<<`, `=======` ni `>>>>>>>`.
- [x] El shape final queda registrado: 282.660 × 26.
- [x] Las 26 columnas esperadas existen.
- [x] El período operativo queda acotado a 2020-2024.
- [x] Las variables críticas para modelado no contienen nulos.
- [x] Las tildes de ciudades están almacenadas con codepoints correctos; algunas consolas pueden renderizarlas como `�`.
- [x] Decisión: Armenia se incorporó (datos 2020-2021); Santa Marta excluida por falta de datos.

---

*Datos procesados · CRISP-DM Fases 2-3*
