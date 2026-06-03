# Dataset de Vivienda en Colombia (Procesado)

Este directorio contiene el dataset final procesado, listo para su uso en los modelos predictivos de la Fase 4 y en el dashboard interactivo de Streamlit.

## Archivos
* `vivienda_colombia_limpio.csv`: El dataset principal con todos los datos integrados.
* `reporte_limpieza.csv`: El reporte de métricas que indica el número de registros en cada etapa de la Fase 3.

## Diccionario de Datos (`vivienda_colombia_limpio.csv`)

| Columna | Tipo | Descripción |
|---|---|---|
| `price` | float | Precio de venta del inmueble en COP |
| `area` | float | Área total del inmueble en m² |
| `rooms` | int | Número de habitaciones (mínimo 1) |
| `bathrooms` | int | Número de baños (mínimo 1) |
| `property_type` | str | Tipo de propiedad (`Apartamento` o `Casa`) |
| `city` | str | Ciudad estandarizada (12 ciudades principales) |
| `lat` | float | Latitud (imputada con centroide de ciudad — sin nulos) |
| `lon` | float | Longitud (imputada con centroide de ciudad — sin nulos) |
| `created_on` | datetime | Fecha de publicación o extracción del registro |
| `estrato` | int | Estrato socioeconómico (1-6) |
| `fuente` | str | Origen de los datos (A1-A8) |
| `year` | int | Año de análisis (2019-2024) |
| `salario_mensual` | float | Salario mínimo legal vigente mensual (COP) para ese año |
| `ipc_var_anual` | float | Variación anual del IPC (%) |
| `ipc_base2018` | float | Índice de Precios al Consumidor (Base 2018=100) |
| `tasa_hipotecaria_anual` | float | Tasa de interés hipotecaria promedio (%) |
| `tasa_desempleo` | float | Tasa de desempleo nacional anual (%) |
| `ipvu_variacion_anual` | float | Variación del IPVU (Vivienda Usada) (%) |
| `ipvn_variacion_anual` | float | Variación del IPVN (Vivienda Nueva) (%) |
| `salario_anual` | float | Salario anual acumulado (COP) |
| `IAH` | float | Índice de Accesibilidad a la Vivienda (Años de salario necesarios para comprar) |
| `precio_real` | float | Precio ajustado por inflación (Base 2018) |
| `precio_m2` | float | Precio por metro cuadrado (COP/m²) |
| `cuota_mensual` | float | Cuota mensual estimada (Crédito a 15 años, 70% LTV) |
| `ratio_cuota_salario` | float | Proporción de la cuota mensual sobre el salario mínimo |
| `nivel_accesibilidad` | str | Clasificación de asequibilidad (`Accesible`, `Moderado`, `Elevado`, `Crítico`) |
