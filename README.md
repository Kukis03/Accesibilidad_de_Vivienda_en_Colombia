# Accesibilidad de Vivienda en Colombia · CRISP-DM

Proyecto académico de ciencia de datos para analizar la accesibilidad económica a la vivienda urbana en Colombia durante el período **2020-2024**, siguiendo la metodología **CRISP-DM**.

El proyecto parte de la definición de negocio documentada en [docs/FASE_1_COMPLETA.md](docs/FASE_1_COMPLETA.md): construir un **Indice de Accesibilidad Habitacional (IAH)**, integrar fuentes inmobiliarias y macroeconómicas, entrenar modelos de regresión y clustering, evaluar los resultados contra criterios de éxito y desplegar un dashboard interactivo.

> **Estado actual:** Proyecto completo (Fases 1–6 ejecutadas). Dashboard Streamlit desplegado. Modelo RF (R²=0.6348) y clustering KMeans K=5 (silueta=0.4874) disponibles en `models/`. Documentación completa en `docs/`. URL del dashboard pendiente de despliegue en Streamlit Cloud.

---

## Estado por fase

| Fase | CRISP-DM | Responsable | Estado actual | Documento |
|---|---|---:|---|---|
| 1 | Comprensión del negocio | Steve | Completa | [docs/FASE_1_COMPLETA.md](docs/FASE_1_COMPLETA.md) |
| 2 | Comprensión de los datos | Sofía | Completa | [docs/FASE_2_COMPLETA.md](docs/FASE_2_COMPLETA.md) |
| 3 | Preparación de los datos | Kukis | Completa; CSV validado para Fase 4 con observación de alcance | [docs/FASE_3_COMPLETA.md](docs/FASE_3_COMPLETA.md) |
| 4 | Modelado | Steve | Completa (R²=0.6348, RF+KMeans+DBSCAN+PCA) | [docs/FASE_4_COMPLETA.md](docs/FASE_4_COMPLETA.md) |
| 5 | Evaluación | Sofía | Completa (4/6 criterios, respuestas a preguntas) | [docs/FASE_5_COMPLETA.md](docs/FASE_5_COMPLETA.md) |
| 6 | Despliegue | Kukis | Completa (dashboard Streamlit local) | [docs/FASE_6_COMPLETA.md](docs/FASE_6_COMPLETA.md) |

---

## Pregunta central

> ¿Cómo ha evolucionado la accesibilidad económica a la vivienda en Colombia entre 2020 y 2024, y qué variables estructurales explican mejor las diferencias entre ciudades?

## Objetivos del proyecto

1. Construir y validar el **IAH** para las ciudades focales del estudio.
2. Entrenar y comparar modelos de regresión para predecir precio de vivienda.
3. Segmentar mercados urbanos mediante clustering no supervisado.
4. Calcular y analizar el ratio cuota/salario frente al umbral financiero del 30%.

Los objetivos 2, 3 y 4 fueron completados en Fases 4 y 5. Ver `docs/FASE_4_COMPLETA.md` y `docs/FASE_5_COMPLETA.md` para resultados detallados.

---

## Fuentes de datos

La Fase 1 define **16 fuentes**:

- **A1-A8:** datasets de precios de vivienda.
- **B1-B8:** variables macroeconómicas y geográficas.

La Fase 2 verificó los 16 archivos en `data/raw/` y generó reportes de calidad en `data/processed/`. El archivo A1 contiene datos multi-país en bruto; el subconjunto colombiano relevante queda documentado en los reportes de calidad.

### Ciudades focales

Según Fase 1, el estudio trabaja con 12 ciudades:

Bogotá D.C., Medellín, Cali, Barranquilla, Bucaramanga, Cartagena, Pereira, Cúcuta, Manizales, Ibagué, Santa Marta y Villavicencio.

---

## Estructura del repositorio

```text
Accesibilidad_de_Vivienda_en_Colombia/
├── app/
│   ├── app.py
│   └── pages/
│       ├── 01_analisis_nacional.py
│       ├── 02_comparador_ciudades.py
│       ├── 03_predictor_precios.py
│       └── 04_segmentos_mercado.py
├── data/
│   ├── raw/
│   └── processed/
│       ├── vivienda_colombia_limpio.csv
│       ├── reporte_limpieza.csv
│       ├── reporte_calidad_datasets.csv
│       └── otros reportes CSV/JSON de Fases 2 y 3
├── docs/
│   ├── GUIA_FASE_1.md ... GUIA_FASE_6.md
│   ├── FASE_1_COMPLETA.md ... FASE_6_COMPLETA.md
│   ├── HALLAZGOS_FASE_2.md
│   ├── HALLAZGOS_FASE_3.md
│   └── figures/
├── models/
│   └── .gitkeep
├── notebooks/
├── scripts/
└── requirements.txt
```

> **Nota de estado:** `app/` contiene una base de dashboard Streamlit, pero Fase 6 no está cerrada ni desplegada. El predictor espera `models/modelo_random_forest.pkl`, archivo que aún no existe porque Fase 4 no ha sido ejecutada.

---

## Artefactos disponibles

| Artefacto | Ruta | Estado |
|---|---|---|
| Inventario y criterios de éxito | `docs/FASE_1_COMPLETA.md` | Disponible |
| Reporte de comprensión de datos | `docs/FASE_2_COMPLETA.md` | Disponible |
| Hallazgos EDA | `docs/HALLAZGOS_FASE_2.md` | Disponible |
| Reporte de preparación de datos | `docs/FASE_3_COMPLETA.md` | Disponible |
| Hallazgos de preparación | `docs/HALLAZGOS_FASE_3.md` | Disponible |
| Reporte de limpieza | `data/processed/reporte_limpieza.csv` | Disponible |
| Dataset integrado | `data/processed/vivienda_colombia_limpio.csv` | Validado: 282.660 registros × 26 columnas |
| Modelos entrenados | `models/*.pkl` | RF (R²=0.6348), KMeans K=5 (silueta=0.4874) |
| Dashboard Streamlit | `app/app.py` | 4 páginas: Nacional, Comparador, Predictor, Segmentos |

### Observación sobre el dataset procesado

El archivo `data/processed/vivienda_colombia_limpio.csv` fue verificado sin marcadores de conflicto de git, con **282.660 registros × 26 columnas**, período 2020-2024 y nulos críticos en cero.

> **Caveat de alcance:** el CSV actual contiene **Armenia** y no contiene **Santa Marta**, mientras Fase 1 definió Santa Marta dentro de las 12 ciudades focales. Antes de cerrar Fase 4/Fase 5, el equipo debe decidir si incorpora formalmente Armenia o si regenera el dataset para respetar la lista original.

---

## Instalación local

1. Clonar el repositorio (requiere Git LFS):

```bash
git lfs install
git clone https://github.com/AlexanderPineda25/Accesibilidad_de_Vivienda_en_Colombia
cd Accesibilidad_de_Vivienda_en_Colombia
```

2. Crear y activar entorno virtual:

```bash
python -m venv venv
venv\Scripts\activate
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

4. Ejecutar la app local si se quiere revisar el prototipo:

```bash
streamlit run app/app.py
```

La app puede abrir sin modelo, pero el predictor de precios permanecerá deshabilitado hasta completar Fase 4.

---

## Criterios de éxito — Resultados Finales

| Criterio | Umbral Fase 1 | Valor Obtenido | ¿Cumple? |
|---|---:|---:|---|
| R2 en test para regresión | >= 0,75 | 0.6348 | ❌ |
| RMSE relativo | < 15% | 67.86% | ❌ |
| Coeficiente de silueta | >= 0,45 | 0.4874 | ✅ |
| Segmentos diferenciables | >= 3 | 5 clusters | ✅ |
| Preguntas de investigación respondidas | 4 de 4 | 4/4 respondidas | ✅ |
| Dashboard funcional | filtros + predictor | 4 páginas operativas | ✅ |

Ver `docs/tabla_criterios_exito.csv` para detalle completo.

---

## Equipo

| Integrante | Responsabilidad principal |
|---|---|
| Steve | Fase 1 y Fase 4 |
| Sofía | Fase 2 y Fase 5 |
| Kukis | Fase 3 y Fase 6 |

---

*Proyecto académico · CRISP-DM 2026-I · Accesibilidad Habitacional Colombia*
