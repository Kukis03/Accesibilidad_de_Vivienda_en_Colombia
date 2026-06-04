# Fase 6 — Despliegue: Informe Completo
**Proyecto:** Accesibilidad de Vivienda en Colombia · CRISP-DM 2026-I  
**Responsable:** Kukis · **Apoyo:** Sofía  
**Fecha:** Junio 2026

---

## Arquitectura de la Aplicación

La aplicación consiste en un dashboard interactivo desarrollado con **Streamlit** que permite explorar los resultados del proyecto CRISP-DM completo (Fases 1–5). Se compone de:

| Componente | Archivo | Propósito |
|---|---|---|
| Página principal | `app/app.py` | KPIs nacionales, mapa geográfico, tabla exploratoria |
| Análisis Nacional | `app/pages/01_analisis_nacional.py` | Evolución IAH, macro, niveles de accesibilidad |
| Comparador de Ciudades | `app/pages/02_comparador_ciudades.py` | Contraste estadístico entre ciudades |
| Predictor de Precios | `app/pages/03_predictor_precios.py` | Formulario + modelo RF + semáforo de accesibilidad |
| Segmentos de Mercado | `app/pages/04_segmentos_mercado.py` | Visualización de clusters KMeans |

## Datos y Modelos Utilizados

- `data/processed/vivienda_colombia_limpio.csv` — 282,660 registros, 26 columnas, 12 ciudades, 2020–2024
- `models/modelo_random_forest.pkl` — Random Forest optimizado (R²=0.6348)
- `models/kmeans_segmentacion.pkl` — KMeans K=5 (silueta=0.4874)
- `data/processed/ciudades_clusters.csv` — Asignación de clusters por ciudad-año
- `data/processed/perfiles_clusters.csv` — Perfiles medios de clusters

## Requerimientos Funcionales

1. **Filtros globales:** sidebar con selector de ciudad, año y tipo de propiedad que afectan a KPIs y mapa
2. **Análisis nacional:** gráficos interactivos de evolución temporal (IAH, precios, macroeconomía)
3. **Comparador:** selección múltiple de ciudades con tabla de indicadores y boxplots
4. **Predictor:** formulario de entrada → predicción RF → IAH → semáforo → indicadores financieros
5. **Segmentos:** scatter IAH vs precio, PCA clusters, heatmap ciudad-año, perfiles

## Limitaciones Conocidas

- **Predictor:** El modelo RF explica solo el 63.5% de la varianza del precio. Las predicciones son orientativas.
- **Cobertura:** Solo viviendas listadas en plataformas digitales (FincaRaíz, Properati, Kaggle).
- **Datos faltantes:** Armenia, Barranquilla, Cartagena sin datos para 2022–2024.
- **Memoria:** El dataset completo (~128 MB) puede causar lentitud en Streamlit Cloud free tier.
- **Modelo 448 MB:** El archivo `.pkl` del RF se almacena via Git LFS. Streamlit Cloud lo descarga al iniciar.

## Próximos Pasos

1. Ejecutar `notebooks/03_modelado_v2.ipynb` (XGBoost + log price) para mejorar el predictor
2. Desplegar en Streamlit Community Cloud y obtener URL pública
3. Preparar presentación ejecutiva para stakeholders
