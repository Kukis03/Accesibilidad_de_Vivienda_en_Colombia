# Fase 5 — Evaluación
## Notebook: `notebooks/04_evaluacion.ipynb`
**Responsable:** Sofía · **Apoyo:** Steve  
**Insumos:** `data/processed/vivienda_colombia_limpio.csv`, `models/modelo_random_forest.pkl`, `models/kmeans_segmentacion.pkl`, `data/processed/ciudades_clusters.csv`  
**Semana:** 9

---

## Estado: ✅ COMPLETADA

**Fecha de ejecución:** 4 de junio 2026  
**Commits:** `1a779b7` (evaluación), `b068a7d` (respuesta pregunta central)

---

## Sección 1: Setup y Carga de Recursos
**Celdas 1–6: Importaciones y carga**
- [x] Importar pandas, numpy, matplotlib, seaborn, plotly, joblib
- [x] Importar métricas de scikit-learn: `mean_absolute_error`, `mean_squared_error`, `r2_score`, `silhouette_score`, `davies_bouldin_score`
- [x] Cargar dataset limpio: `data/processed/vivienda_colombia_limpio.csv`
- [x] Cargar modelo RF: `joblib.load('models/modelo_random_forest.pkl')`
- [x] Cargar modelo KMeans: `joblib.load('models/kmeans_segmentacion.pkl')`
- [x] Cargar tabla de clusters: `data/processed/ciudades_clusters.csv`
- [x] Recrear la misma división train/test de Fase 4 (usar `random_state=42`, `test_size=0.20`) para evaluación sobre el mismo conjunto de prueba

---

## Sección 2: Verificación de Criterios de Éxito (Fase 1)
**Celdas 7–12: Tabla de criterios cumplidos**
- [x] Calcular R² del modelo Random Forest en X_test
- [x] Calcular RMSE relativo (RMSE / precio mediano × 100)
- [x] Calcular desviación estándar del R² en validación cruzada 5-fold
- [x] Cargar coeficiente de silueta calculado en Fase 4
- [x] Contar ciudades incluidas en el análisis final (esperado ≥ 8)
- [x] Confirmar rango temporal del dataset (2020–2024)
- [x] Construir tabla con 7 filas: criterio | umbral Fase 1 | valor obtenido | ¿cumple?
- [x] Documentar en celda Markdown cualquier criterio marginal con justificación

**Resultados:**

| Criterio | Umbral | Valor | ¿Cumple? |
|---|---|---|---|
| R² | ≥ 0.75 | 0.6348 | ❌ NO |
| RMSE relativo | < 15% | 67.86% | ❌ NO |
| CV R² desv std | < 0.02 | 0.0059 | ✅ SÍ |
| Silueta clustering | ≥ 0.45 | 0.4874 | ✅ SÍ |
| Ciudades incluidas | ≥ 8 | 12 | ✅ SÍ |
| Rango temporal | 2020–2024 | 2020–2024 | ✅ SÍ |

---

## Sección 3: Evaluación Detallada del Modelo de Regresión
**Celdas 13–20: Métricas completas en conjunto de prueba**
- [x] Calcular MAE sobre X_test ($168,048,700 COP)
- [x] Calcular RMSE sobre X_test ($284,996,129 COP)
- [x] Calcular MAPE (Mean Absolute Percentage Error) sobre X_test (34.36%)
- [x] Calcular R² sobre X_test (0.6348)
- [x] Calcular RMSE relativo (%) (67.86%)
- [x] Crear tabla de métricas: métrica | valor | interpretación de negocio
- [x] Exportar tabla a `data/processed/tabla_metricas_finales.csv`

**Celdas 21–28: Análisis de residuos**
- [x] Calcular residuos = `y_test − y_pred`
- [x] Crear scatter plot `y_pred vs y_test` con línea diagonal de predicción perfecta
- [x] Crear gráfico de residuos vs valores predichos — verificar homocedasticidad
- [x] Crear histograma de residuos — verificar aproximación a distribución normal
- [x] Crear Q-Q plot de residuos
- [x] Calcular residuos absolutos medianos por ciudad — identificar sesgo geográfico
- [x] Crear boxplot de residuos por ciudad
- [x] Documentar si alguna ciudad presenta sesgo sistemático y posible causa

**Celdas 29–33: Importancia de variables (interpretabilidad)**
- [x] Extraer `feature_importances_` del modelo entrenado
- [x] Recuperar nombres de features (incluyendo dummies generadas por OneHotEncoder)
- [x] Crear gráfico de barras horizontal con las 15 variables más influyentes
- [x] Calcular importancia acumulada del top 5 de variables (90.8%)
- [x] Documentar el hallazgo: ¿qué pesa más, las características físicas o el contexto macro?

**Hallazgo:** Las características físicas dominan (bathrooms 42.2%, area 28.0%, estrato 11.3% = 81.5%). El contexto macro aporta <10%.

---

## Sección 4: Evaluación del Modelo de Clustering
**Celdas 34–42: Métricas de calidad de clusters**
- [x] Reconstruir el dataset de clustering: mediana de IAH, precio_m2, ratio_cuota_salario, tasa_desempleo por `(city, year)`
- [x] Escalar con el `scaler_cluster.pkl` guardado en Fase 4
- [x] Calcular coeficiente de silueta — verificar que supera 0.45 (0.4874 ✅)
- [x] Calcular índice Davies-Bouldin (menor = mejor separación) → 0.6434
- [x] Calcular índice Calinski-Harabasz → 67.53
- [x] Crear gráfico de silueta por muestra (silhouette plot por cluster)
- [x] Crear scatter plot PC1 vs PC2 (PCA) con puntos coloreados por cluster y etiquetados por ciudad
- [x] Documentar si los 4 clusters son interpretables y diferenciables

**Celdas 43–48: Perfil y descripción de clusters**
- [x] Calcular media de `IAH`, `precio_m2`, `ratio_cuota_salario`, `tasa_desempleo` por cluster
- [x] Asignar nombre cualitativo a cada cluster (ej. "Mercado Inaccesible", "Accesible Relativo")
- [x] Identificar qué ciudades pertenecen a qué cluster en 2024
- [x] Crear heatmap ciudad × año con color del cluster asignado
- [x] Documentar transiciones de cluster entre 2020 y 2024 (¿alguna ciudad empeoró?)

---

## Sección 5: Respuesta a las 4 Preguntas de Investigación
**Celdas 49–75: Evidencia cuantitativa por pregunta**

### Pregunta 1 — ¿Cuántos años de salario mínimo equivale el precio mediano de vivienda?
- [x] Calcular IAH mediano nacional por año (2020–2024)
- [x] Calcular IAH mediano por ciudad focal por año
- [x] Crear tabla: ciudad | IAH 2020 | IAH 2022 | IAH 2024 | variación (%)
- [x] Crear gráfico de líneas: evolución del IAH por ciudad con líneas de referencia OCDE (5 y 10 años)
- [x] Redactar hallazgo principal: ¿qué ciudad es la más y menos accesible en 2024?

**Hallazgo:** Ibagué más accesible (12.5 años), Medellín menos accesible (30.1 años). Ninguna cumple OCDE <5.

### Pregunta 2 — ¿Qué variables tienen mayor poder predictivo sobre el precio?
- [x] Usar la tabla de importancias de la Sección 3
- [x] Identificar el top 5 de variables con mayor importancia
- [x] Calcular correlación de Pearson entre cada variable numérica y el precio (en escala log)
- [x] Crear tabla: variable | importancia RF | correlación Pearson | interpretación
- [x] Redactar hallazgo: ¿qué factores estructurales dominan la determinación del precio?

**Hallazgo:** Top 3: bathrooms (42.2%), area (28.0%), estrato (11.3%) = 81.5% combinado. Variables físicas >> contexto macro.

### Pregunta 3 — ¿Es posible segmentar ciudades en grupos diferenciables?
- [x] Resumir los K clusters identificados con su nombre y ciudades asignadas en 2024
- [x] Crear mapa conceptual de los clusters (scatter IAH vs precio_m2)
- [x] Calcular diferencia de IAH promedio entre el cluster más accesible y el más costoso (16.3 años)
- [x] Redactar hallazgo: ¿la crisis de accesibilidad es uniforme o hay segmentación clara?

**Hallazgo:** 5 clusters con silueta 0.4874. Segmentación clara: ciudades accesibles (Cúcuta, Ibagué, Villavicencio), moderadas (Bucaramanga, Cali, Manizales, Pereira), y críticas (Bogotá, Medellín).

### Pregunta 4 — ¿En qué ciudades la cuota hipotecaria supera el 30% del salario mínimo?
- [x] Calcular `ratio_cuota_salario` mediano por ciudad y año
- [x] Identificar ciudades y años donde el ratio supera 0.30 (umbral financiero crítico)
- [x] Crear heatmap: ciudad × año con semáforo (verde < 0.30, amarillo 0.30–0.50, rojo > 0.50)
- [x] Calcular % de registros del dataset con ratio > 0.30 a nivel nacional
- [x] Redactar hallazgo: ¿qué porcentaje del mercado resulta financieramente inviable para un hogar de salario mínimo?

**Hallazgo:** 100% del mercado supera el umbral del 30%. El mercado es financieramente inviable para un hogar de salario mínimo en su totalidad.

---

## Sección 6: Análisis Complementario del IAH
**Celdas 76–84: Análisis descriptivo de accesibilidad**
- [x] Calcular distribución de `nivel_accesibilidad` (Accesible / Moderado / Elevado / Crítico) a nivel nacional
- [x] Calcular distribución de `nivel_accesibilidad` por ciudad
- [x] Crear gráfico de barras apiladas: ciudad vs composición de niveles de accesibilidad
- [x] Calcular % de vivienda "Crítica" (IAH > 20) por ciudad en 2024
- [x] Calcular evolución del % de vivienda "Accesible" (IAH ≤ 5) entre 2020 y 2024
- [x] Calcular precio real (ajustado por inflación) mediano por ciudad y año — ¿creció el precio en términos reales?
- [x] Crear gráfico comparativo: precio nominal vs precio real por año

---

## Sección 7: Validación Final del Proyecto
**Celdas 85–90: Consistencia interna**
- [x] Verificar que las 4 preguntas de investigación tienen respuesta cuantitativa y gráfica
- [x] Verificar que los 4 objetivos específicos de Fase 1 están cumplidos
- [x] Comparar la tabla de criterios de éxito (Sección 2) con el estado final — todos deben estar marcados
- [x] Redactar limitaciones del proyecto (tipos de vivienda excluidos, cobertura de Kaggle, uso del salario mínimo como proxy)
- [x] Redactar recomendaciones de política pública basadas en los hallazgos

**Limitaciones documentadas:**
1. Tipos de vivienda excluidos: VIS, mejoramiento, alquiler
2. Cobertura: Datasets Kaggle/FincaRaíz, no DANE/Minvivienda
3. Proxy: Salario mínimo como único ingreso del hogar
4. Geografía: 12 ciudades, sin Santa Marta
5. Temporalidad: Incluye años atípicos (2020 pandemia)
6. Datos faltantes: Armenia/Barranquilla/Cartagena 2022-2024

---

## Sección 8: Guardado de Outputs y Figuras
**Celdas 91–97: Exportación**
- [x] Crear carpeta `docs/figures/` si no existe
- [x] Guardar todas las figuras en `docs/figures/` con nombres descriptivos (ej. `fig_IAH_por_ciudad.png`) a 150 dpi
- [x] Exportar tabla de métricas finales a `data/processed/tabla_metricas_finales.csv`
- [x] Exportar tabla de criterios de éxito a `data/processed/tabla_criterios_exito.csv`
- [x] Exportar tabla de respuestas a preguntas de investigación a `data/processed/respuestas_preguntas.csv`

---

## Sección 9: Preparación para GitHub
**Celdas 98–104: Verificación y commit**
- [x] Ejecutar todas las celdas en kernel limpio (Restart & Run All) sin errores
- [x] Verificar que NOT hay rutas absolutas en el notebook
- [x] Confirmar que todas las figuras se guardaron en `docs/figures/`
- [x] `git add notebooks/04_evaluacion.ipynb docs/figures/ data/processed/tabla_metricas_finales.csv data/processed/tabla_criterios_exito.csv`
- [x] Commit: `"feat: Fase 5 - evaluación completa y respuestas a preguntas de investigación"`
- [x] Actualizar `README.md`: marcar Fase 5 como completada
- [x] Crear `docs/FASE_5_COMPLETA.md` con hallazgos consolidados y conclusiones

---

## Entregables de Fase 5

| Archivo | Ruta | Estado | Descripción |
|---|---|---|---|
| Notebook de evaluación | `notebooks/04_evaluacion.ipynb` | ✅ | Análisis completo de métricas y respuestas de negocio |
| Tabla de métricas | `data/processed/tabla_metricas_finales.csv` | ✅ | R², MAE, RMSE, MAPE del modelo final |
| Tabla de criterios | `data/processed/tabla_criterios_exito.csv` | ✅ | Umbral Fase 1 vs valor obtenido por criterio |
| Tabla de respuestas | `data/processed/respuestas_preguntas.csv` | ✅ | Respuesta cuantitativa a las 4 preguntas de investigación |
| Figuras | `docs/figures/fig_*.png` | ✅ | 11 figuras de evaluación (PNG 150 dpi) |
| Documento de fase | `docs/FASE_5_COMPLETA.md` | ✅ | Resumen ejecutivo de hallazgos, limitaciones y recomendaciones |
