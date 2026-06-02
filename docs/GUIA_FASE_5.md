# Fase 5 — Evaluación
## Notebook: `notebooks/04_evaluacion.ipynb`
**Responsable:** Sofía · **Apoyo:** Steve  
**Insumos:** `data/processed/vivienda_colombia_limpio.csv`, `models/modelo_random_forest.pkl`, `models/kmeans_segmentacion.pkl`, `data/processed/ciudades_clusters.csv`  
**Semana:** 9

---

## Sección 1: Setup y Carga de Recursos
**Celdas 1–6: Importaciones y carga**
- [ ] Importar pandas, numpy, matplotlib, seaborn, plotly, joblib
- [ ] Importar métricas de scikit-learn: `mean_absolute_error`, `mean_squared_error`, `r2_score`, `silhouette_score`, `davies_bouldin_score`
- [ ] Cargar dataset limpio: `data/processed/vivienda_colombia_limpio.csv`
- [ ] Cargar modelo RF: `joblib.load('models/modelo_random_forest.pkl')`
- [ ] Cargar modelo KMeans: `joblib.load('models/kmeans_segmentacion.pkl')`
- [ ] Cargar tabla de clusters: `data/processed/ciudades_clusters.csv`
- [ ] Recrear la misma división train/test de Fase 4 (usar `random_state=42`, `test_size=0.20`) para evaluación sobre el mismo conjunto de prueba

---

## Sección 2: Verificación de Criterios de Éxito (Fase 1)
**Celdas 7–12: Tabla de criterios cumplidos**
- [ ] Calcular R² del modelo Random Forest en X_test
- [ ] Calcular RMSE relativo (RMSE / precio mediano × 100)
- [ ] Calcular desviación estándar del R² en validación cruzada 5-fold
- [ ] Cargar coeficiente de silueta calculado en Fase 4
- [ ] Contar ciudades incluidas en el análisis final (esperado ≥ 8)
- [ ] Confirmar rango temporal del dataset (2019–2024)
- [ ] Construir tabla con 7 filas: criterio | umbral Fase 1 | valor obtenido | ¿cumple?
- [ ] Documentar en celda Markdown cualquier criterio marginal con justificación

---

## Sección 3: Evaluación Detallada del Modelo de Regresión
**Celdas 13–20: Métricas completas en conjunto de prueba**
- [ ] Calcular MAE sobre X_test
- [ ] Calcular RMSE sobre X_test
- [ ] Calcular MAPE (Mean Absolute Percentage Error) sobre X_test
- [ ] Calcular R² sobre X_test
- [ ] Calcular RMSE relativo (%)
- [ ] Crear tabla de métricas: métrica | valor | interpretación de negocio
- [ ] Exportar tabla a `docs/tabla_metricas_finales.csv`

**Celdas 21–28: Análisis de residuos**
- [ ] Calcular residuos = `y_test − y_pred`
- [ ] Crear scatter plot `y_pred vs y_test` con línea diagonal de predicción perfecta
- [ ] Crear gráfico de residuos vs valores predichos — verificar homocedasticidad
- [ ] Crear histograma de residuos — verificar aproximación a distribución normal
- [ ] Crear Q-Q plot de residuos
- [ ] Calcular residuos absolutos medianos por ciudad — identificar sesgo geográfico
- [ ] Crear boxplot de residuos por ciudad
- [ ] Documentar si alguna ciudad presenta sesgo sistemático y posible causa

**Celdas 29–33: Importancia de variables (interpretabilidad)**
- [ ] Extraer `feature_importances_` del modelo entrenado
- [ ] Recuperar nombres de features (incluyendo dummies generadas por OneHotEncoder)
- [ ] Crear gráfico de barras horizontal con las 15 variables más influyentes
- [ ] Calcular importancia acumulada del top 5 de variables
- [ ] Documentar el hallazgo: ¿qué pesa más, las características físicas o el contexto macro?

---

## Sección 4: Evaluación del Modelo de Clustering
**Celdas 34–42: Métricas de calidad de clusters**
- [ ] Reconstruir el dataset de clustering: mediana de IAH, precio_m2, ratio_cuota_salario, tasa_desempleo por `(city, year)`
- [ ] Escalar con el `scaler_cluster.pkl` guardado en Fase 4
- [ ] Calcular coeficiente de silueta — verificar que supera 0.45
- [ ] Calcular índice Davies-Bouldin (menor = mejor separación)
- [ ] Calcular índice Calinski-Harabasz
- [ ] Crear gráfico de silueta por muestra (silhouette plot por cluster)
- [ ] Crear scatter plot PC1 vs PC2 (PCA) con puntos coloreados por cluster y etiquetados por ciudad
- [ ] Documentar si los 4 clusters son interpretables y diferenciables

**Celdas 43–48: Perfil y descripción de clusters**
- [ ] Calcular media de `IAH`, `precio_m2`, `ratio_cuota_salario`, `tasa_desempleo` por cluster
- [ ] Asignar nombre cualitativo a cada cluster (ej. "Mercado Inaccesible", "Accesible Relativo")
- [ ] Identificar qué ciudades pertenecen a qué cluster en 2024
- [ ] Crear heatmap ciudad × año con color del cluster asignado
- [ ] Documentar transiciones de cluster entre 2019 y 2024 (¿alguna ciudad empeoró?)

---

## Sección 5: Respuesta a las 4 Preguntas de Investigación
**Celdas 49–75: Evidencia cuantitativa por pregunta**

### Pregunta 1 — ¿Cuántos años de salario mínimo equivale el precio mediano de vivienda?
- [ ] Calcular IAH mediano nacional por año (2019–2024)
- [ ] Calcular IAH mediano por ciudad focal por año
- [ ] Crear tabla: ciudad | IAH 2019 | IAH 2021 | IAH 2024 | variación (%)
- [ ] Crear gráfico de líneas: evolución del IAH por ciudad con líneas de referencia OCDE (5 y 10 años)
- [ ] Redactar hallazgo principal: ¿qué ciudad es la más y menos accesible en 2024?

### Pregunta 2 — ¿Qué variables tienen mayor poder predictivo sobre el precio?
- [ ] Usar la tabla de importancias de la Sección 3
- [ ] Identificar el top 5 de variables con mayor importancia
- [ ] Calcular correlación de Pearson entre cada variable numérica y el precio (en escala log)
- [ ] Crear tabla: variable | importancia RF | correlación Pearson | interpretación
- [ ] Redactar hallazgo: ¿qué factores estructurales dominan la determinación del precio?

### Pregunta 3 — ¿Es posible segmentar ciudades en grupos diferenciables?
- [ ] Resumir los K clusters identificados con su nombre y ciudades asignadas en 2024
- [ ] Crear mapa conceptual de los clusters (scatter IAH vs precio_m2)
- [ ] Calcular diferencia de IAH promedio entre el cluster más accesible y el más costoso
- [ ] Redactar hallazgo: ¿la crisis de accesibilidad es uniforme o hay segmentación clara?

### Pregunta 4 — ¿En qué ciudades la cuota hipotecaria supera el 30% del salario mínimo?
- [ ] Calcular `ratio_cuota_salario` mediano por ciudad y año
- [ ] Identificar ciudades y años donde el ratio supera 0.30 (umbral financiero crítico)
- [ ] Crear heatmap: ciudad × año con semáforo (verde < 0.30, amarillo 0.30–0.50, rojo > 0.50)
- [ ] Calcular % de registros del dataset con ratio > 0.30 a nivel nacional
- [ ] Redactar hallazgo: ¿qué porcentaje del mercado resulta financieramente inviable para un hogar de salario mínimo?

---

## Sección 6: Análisis Complementario del IAH
**Celdas 76–84: Análisis descriptivo de accesibilidad**
- [ ] Calcular distribución de `nivel_accesibilidad` (Accesible / Moderado / Elevado / Crítico) a nivel nacional
- [ ] Calcular distribución de `nivel_accesibilidad` por ciudad
- [ ] Crear gráfico de barras apiladas: ciudad vs composición de niveles de accesibilidad
- [ ] Calcular % de vivienda "Crítica" (IAH > 20) por ciudad en 2024
- [ ] Calcular evolución del % de vivienda "Accesible" (IAH ≤ 5) entre 2019 y 2024
- [ ] Calcular precio real (ajustado por inflación) mediano por ciudad y año — ¿creció el precio en términos reales?
- [ ] Crear gráfico comparativo: precio nominal vs precio real por año

---

## Sección 7: Validación Final del Proyecto
**Celdas 85–90: Consistencia interna**
- [ ] Verificar que las 4 preguntas de investigación tienen respuesta cuantitativa y gráfica
- [ ] Verificar que los 4 objetivos específicos de Fase 1 están cumplidos
- [ ] Comparar la tabla de criterios de éxito (Sección 2) con el estado final — todos deben estar marcados
- [ ] Redactar limitaciones del proyecto (tipos de vivienda excluidos, cobertura de Kaggle, uso del salario mínimo como proxy)
- [ ] Redactar recomendaciones de política pública basadas en los hallazgos

---

## Sección 8: Guardado de Outputs y Figuras
**Celdas 91–97: Exportación**
- [ ] Crear carpeta `docs/figures/` si no existe
- [ ] Guardar todas las figuras en `docs/figures/` con nombres descriptivos (ej. `fig_IAH_por_ciudad.png`) a 150 dpi
- [ ] Exportar tabla de métricas finales a `docs/tabla_metricas_finales.csv`
- [ ] Exportar tabla de criterios de éxito a `docs/tabla_criterios_exito.csv`
- [ ] Exportar tabla de respuestas a preguntas de investigación a `docs/respuestas_preguntas.csv`

---

## Sección 9: Preparación para GitHub
**Celdas 98–104: Verificación y commit**
- [ ] Ejecutar todas las celdas en kernel limpio (Restart & Run All) sin errores
- [ ] Verificar que NOT hay rutas absolutas en el notebook
- [ ] Confirmar que todas las figuras se guardaron en `docs/figures/`
- [ ] `git add notebooks/04_evaluacion.ipynb docs/figures/ docs/tabla_metricas_finales.csv docs/tabla_criterios_exito.csv`
- [ ] Commit: `"feat: Fase 5 - evaluación completa y respuestas a preguntas de investigación"`
- [ ] Push a rama `development`
- [ ] Actualizar `README.md`: marcar Fase 5 como completada
- [ ] Crear `docs/FASE_5_COMPLETA.md` con hallazgos consolidados y conclusiones

---

## Entregables de Fase 5

| Archivo | Ruta | Descripción |
|---|---|---|
| Notebook de evaluación | `notebooks/04_evaluacion.ipynb` | Análisis completo de métricas y respuestas de negocio |
| Tabla de métricas | `docs/tabla_metricas_finales.csv` | R², MAE, RMSE, MAPE del modelo final |
| Tabla de criterios | `docs/tabla_criterios_exito.csv` | Umbral Fase 1 vs valor obtenido por criterio |
| Tabla de respuestas | `docs/respuestas_preguntas.csv` | Respuesta cuantitativa a las 4 preguntas de investigación |
| Figuras | `docs/figures/` | Todas las gráficas generadas (PNG 150 dpi) |
| Documento de fase | `docs/FASE_5_COMPLETA.md` | Resumen ejecutivo de hallazgos, limitaciones y recomendaciones |
