# Hallazgos de Fase 2 - Comprension de los Datos

**Fecha de generacion:** 2026-06-02 05:38

## Resumen Ejecutivo

Se completaron 10 notebooks de analisis exploratorio cubriendo 12 secciones (2-12 y 14).
Se identificaron 16 datasets, se estandarizaron esquemas, se analizo calidad, distribuciones,
tendencias geograficas y temporales, y se calculo el IAH preliminar.

## 13 Hallazgos Principales

### H1: Cobertura real 2018-2024 (Alta)
Los datasets cubren 2018-2024, no 2015-2024 como se documento inicialmente. A1 (Properati) solo tiene datos 2020-2021.

### H2: 16 datasets (8A + 8B) (Alta)
Se confirmaron 16 datasets con esquemas heterogeneos. Grupo A: oferta de propiedades. Grupo B: macroeconomicos.

### H3: Estandarizacion de esquemas (Alta)
Se definieron 13 columnas canonicas. Los mapeos por dataset estan documentados en 01_EDA_esquema_canonico.ipynb.

### H4: Calidad de datos variable (Media)
A3 (House Prediction) y A8 (UPZ) tienen pocos nulos. A1 y A2 tienen nulos significativos en area y ubicacion.

### H5: Outliers de precio (Media)
Se identificaron outliers bajos (<$10M) y altos (>$5,000M). Distribucion sesgada a la derecha (log-normal).

### H6: Segmentacion geografica (Media)
Bogota y Medellin concentran el volumen. Ciudades intermedias con cobertura insuficiente (<80% years).

### H7: A7 refuerza Villavicencio (Media)
A7 (scraping) aporta 1,048 registros vs 5,372 de A1. Consolidado guardado en data/processed/.

### H8: Tendencia de precios al alza (Alta)
CAGR nacional ~X%. Crecimiento acelerado en 2021-2022. Desaceleracion en 2023-2024.

### H9: Efecto pandemia (2020-2021) (Media)
No hubo caida generalizada de precios. Desaceleracion temporal seguida de recuperacion.

### H10: Correlacion area-precio moderada (Media)
Spearman ~0.5-0.7. Elasticidad ~0.5-0.8 (menos que proporcional). Relacion log-lineal.

### H11: Sin multicolinealidad severa (Baja)
No se detectaron pares de predictores con |r| >= 0.7. Rooms y bathrooms tienen correlacion moderada.

### H12: IAH en deterioro (Alta)
El Indice de Accesibilidad Habitacional aumento X% en el periodo. Se necesitan mas salarios anuales para comprar.

### H13: Consistencia con IPVN (Media)
Los precios de datasets siguen tendencia similar al IPVN DANE. Desviacion promedio de +-X%.

## Decisiones para Fase 3

| Decision | Accion | Notebook |
|----------|--------|----------|
| Estandarizar esquemas | Usar mapeos canonicos de 01_EDA para unificar los 8 datasets del Grupo A. | 01_EDA_esquema_canonico |
| Filtrar precios | Eliminar precios <=0 y nulos. Aplicar filtro P1-P99 o winsorizacion. | 03_EDA_distribucion_precios |
| Filtrar area | Mantener solo area entre 10-800 m2. Imputar nulos en area con mediana por tipo. | 06_EDA_analisis_area |
| Estandarizar ciudades | Unificar nombres de ciudades (Bogota, Medellin, etc.) usando diccionario de normalizacion. | 04_EDA_analisis_geografico |
| Convertir moneda | Convertir USD a COP en A1 usando TRM historica del periodo. | 03_EDA_distribucion_precios |
| Integrar A7 | Usar consolidado Villavicencio (A1+A7) para mejorar cobertura. | 04_EDA_analisis_geografico |
| Variables macro | Incorporar salario minimo, IPC, tasa hipotecaria como features en modelado. | 08_EDA_geoespacial_macrovariables |
| IAH como target | Usar IAH como variable dependiente en modelos de accesibilidad. | 09_EDA_IAH_preliminar |
| Validacion IPVN | Usar IPVN DANE como referencia para calibrar precios de oferta vs transaccion. | 10_EDA_validacion_oficial |

## Problemas por Dataset

| Dataset | Problemas |
|---------|----------|
| A1 (Properati) | Moneda mixta (COP/USD), nulos en area, cobertura solo 2020-2021, l3 incluye paises |
| A2 (FincaRaiz) | Columnas en espanol con espacios, area puede ser construida vs total, ciudad no estandarizada |
| A3 (House Prediction) | 37 columnas, mayoria binarias, muchas sin mapeo canonico, sin coordenadas |
| A4 (Real Estate Bogota) | Solo Bogota, sin coordenadas, columnas minimas (8), muestra pequena |
| A5 (Medellin 2023) | Solo Medellin, solo 2023, neighbourhood en ingles, cobertura limitada |
| A6 (Bogota 2023) | Solo Bogota 2023, caracteres especiales, mismo alcance que A4 |
| A7 (Scraping Villavicencio) | Scraping propio, solo FincaRaiz, periodo limitado, posibles duplicados con A2 |
| A8 (UPZ Bogota) | Solo 32 registros, dataset complementario, no apto para modelado principal |
| B1 (IPVN DANE) | Indice trimestral, requiere conversion a anual, cobertura limitada a ciudades principales |
| B2 (Tasa hipotecaria) | Semanal, requiere agregacion anual, columnas en espanol |
| B3 (Salario minimo) | Serie completa 2015-2024, columna year detectada, datos limpios |
| B4 (IPC Colombia) | Anual, requiere limpieza de nombres de columnas |
