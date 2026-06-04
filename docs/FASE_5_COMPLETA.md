# Fase 5 — Evaluación: Informe Completo
**Proyecto:** Accesibilidad de Vivienda en Colombia · CRISP-DM 2026-I
**Responsable:** Sofía · **Apoyo:** Steve
**Fecha:** Junio 2026

---

## Respuesta a la Pregunta Central de Investigación

> **¿Cómo ha evolucionado la accesibilidad económica a la vivienda en Colombia entre 2020 y 2024, y qué variables estructurales explican mejor las diferencias entre ciudades?**

### Evolución de la accesibilidad (2020–2024)

La accesibilidad económica —medida como IAH (años de salario mínimo para comprar una vivienda)— se mantuvo en niveles críticos durante todo el período. Ninguna de las 12 ciudades analizadas se acerca al estándar OCDE de 5 años.

- **IAH nacional 2024:** ~22.1 años de salario mínimo por vivienda
- **Tendencia heterogénea:** 5 ciudades mejoraron su IAH, 5 empeoraron
- **Mayor mejora:** Villavicencio (−20.2%), Ibagué (−16.2%), Bogotá (−12.2%)
- **Mayor deterioro:** Medellín (+15.3%), Manizales (+13.0%), Pereira (+10.3%)
- **Brecha entre extremos en 2024:** Ibagué (12.5 años) vs Medellín (30.1 años) — una diferencia de 17.6 años de salario mínimo

**Conclusión:** La accesibilidad no solo es crítica en todos los mercados, sino que la brecha entre ciudades se amplió entre 2020 y 2024. Las ciudades más caras (Bogotá, Medellín, Cartagena) empeoraron o se mantuvieron en niveles de IAH > 25, mientras que las intermedias (Ibagué, Villavicencio, Cúcuta) mostraron recuperación post-pandemia.

### Variables estructurales que explican diferencias

El modelo Random Forest (R²=0.6348) identificó que **las características físicas de la vivienda explican el 81.5% de la varianza del precio**, muy por encima del contexto macroeconómico y geográfico:

| Variable | Importancia RF | Correlación con log(price) |
|---|---|---|
| bathrooms | 42.2% | 0.60 |
| area | 28.0% | 0.46 |
| estrato | 11.3% | 0.43 |
| city_Bogotá | 5.0% | — |
| rooms | 4.2% | 0.18 |

**Hallazgo clave:** El estrato socioeconómico (11.3%) pesa más que cualquier variable macro (tasa_hipotecaria <2%, IPC <2%, desempleo <1%). Esto sugiere que las diferencias de precio entre ciudades están mediadas principalmente por la **calidad y tamaño de las viviendas** que ofrece cada mercado, no por diferencias en el entorno macroeconómico. Sin embargo, el R² de 0.6348 indica que ~37% de las diferencias quedan sin explicar — posiblemente por variables no capturadas como ubicación exacta dentro de la ciudad, calidad de construcción o antigüedad.

---

## 1. Verificación de Criterios de Éxito (Fase 1)

| Criterio | Umbral Fase 1 | Valor Obtenido | ¿Cumple? |
|---|---|---|---|
| R² | ≥ 0.75 | 0.6348 | ❌ NO |
| RMSE relativo | < 15% | 67.86% | ❌ NO |
| CV R² desviación estándar | < 0.02 | 0.0059 | ✅ SÍ |
| Silueta clustering | ≥ 0.45 | 0.4874 | ✅ SÍ |
| Ciudades incluidas | ≥ 8 | 12 | ✅ SÍ |
| Rango temporal | 2020–2024 | 2020–2024 | ✅ SÍ |

**Resultado:** 4/6 criterios cumplidos. El modelo de regresión no alcanza el umbral de R² ≥ 0.75 ni RMSE rel < 15%.

> **Nota sobre trazabilidad de criterios:** Fase 1 definió originalmente **8 criterios** (4 de negocio + 4 técnicos). De estos, 2 se excluyeron de la evaluación cuantitativa por su naturaleza cualitativa: *"Segmentos diferenciables ≥ 3"* (subsumido por el coeficiente de silueta) y *"Dashboard funcional"* (no evaluable numéricamente). Adicionalmente, 2 criterios de negocio (*"Respuesta a preguntas de investigación"* y *"Relevancia para stakeholders"*) se verifican cualitativamente en las secciones 2-5 de este documento. Se agregó *"CV R² desv std < 0.02"* como control de calidad interna no definido originalmente en Fase 1.

## 2. Métricas del Modelo de Regresión (Random Forest Optimizado)

| Métrica | Valor |
|---|---|
| R² | 0.6348 |
| MAE | $168,048,700 COP |
| RMSE | $284,996,129 COP |
| MAPE | 34.36% |
| RMSE relativo | 67.86% |
| CV R² (5-fold) | 0.6320 ± 0.0059 |

### Top 5 Variables más Importantes
1. **bathrooms** — 42.2%
2. **area** — 28.0%
3. **estrato** — 11.3%
4. **city_Bogotá** — 5.0%
5. **rooms** — 4.2%

**Importancia acumulada top 5: 90.8%** — Las características físicas dominan la predicción del precio (bathrooms + area + estrato = 81.5%), seguidas por el contexto de ciudad (Bogotá).

## 3. Evaluación del Clustering (KMeans, K=5)

| Métrica | Valor |
|---|---|
| Coeficiente de Silueta | 0.4874 |
| Davies-Bouldin Index | 0.6434 |
| Calinski-Harabasz Index | 67.53 |
| Varianza explicada (PC1+PC2) | 97.23% |

### Perfiles de Clusters
| Cluster | IAH | Precio m² | Ratio Cuota/Salario | Tasa Desempleo | Count |
|---|---|---|---|---|---|
| Elevado (IAH 29.2) | 29.23 | $4,597,674 | 2.52 | 15.7% | 6 |
| Moderado (IAH 16.2) | 16.24 | $2,144,328 | 1.40 | 15.7% | 18 |
| Accesible Relativo (IAH 18.7) | 18.66 | $3,376,073 | 2.37 | 10.6% | 12 |
| Elevado (IAH 25.4) | 25.35 | $4,903,561 | 3.29 | 10.5% | 6 |
| Accesible (IAH 12.9) | 12.93 | $2,524,136 | 1.59 | 10.7% | 9 |

### Ciudades por Cluster en 2024
- **Elevado (IAH 25.4):** Bogotá, Medellín
- **Accesible Relativo (IAH 18.7):** Bucaramanga, Cali, Manizales, Pereira
- **Accesible (IAH 12.9):** Cúcuta, Ibagué, Villavicencio

## 4. Respuestas a Preguntas de Investigación

### P1: ¿Cuántos años de salario mínimo equivale el precio mediano?
**IAH nacional 2024: ~22.1 años.** Ciudad más accesible: Ibagué (12.5 años). Menos accesible: Medellín (30.1 años). Ninguna ciudad cumple el estándar OCDE de 5 años.

### P2: ¿Qué variables tienen mayor poder predictivo?
**Top 3: bathrooms (42.2%), area (28.0%), estrato (11.3%).** Las variables físicas dominan (81.5%). La ciudad (Bogotá) aporta 5%. Correlación Pearson más alta: bathrooms (0.60) y area (0.46) con log(price).

### P3: ¿Es posible segmentar ciudades en grupos diferenciables?
**Sí, 5 clusters con buena separabilidad (silueta=0.4874).** Diferencia de IAH entre el cluster más accesible (12.9) y el más elevado (29.2): **16.3 años**. La segmentación muestra una clara división entre ciudades con mercado accesible (Cúcuta, Ibagué, Villavicencio), moderado (Bucaramanga, Cali, Manizales, Pereira) y crítico (Bogotá, Medellín).

### P4: ¿En qué ciudades la cuota hipotecaria supera el 30% del salario?
**100% de los registros superan el umbral del 30%.** Todas las ciudades en todos los años analizados presentan un ratio cuota/salario > 0.30. El ratio mínimo es 0.91 (Armenia 2020) y el máximo 3.60 (Medellín 2024). El mercado de vivienda en Colombia es **financieramente inviable para un hogar de salario mínimo** en su totalidad.

## 5. Limitaciones del Proyecto
1. **Tipos de vivienda excluidos:** Solo casas y apartamentos. No incluye VIS, mejoramiento de vivienda ni alquiler.
2. **Cobertura de fuentes:** Datasets de Kaggle + FincaRaíz. Sin datos oficiales DANE/Minvivienda a nivel de transacción.
3. **Proxy de ingreso:** Salario mínimo legal como único ingreso del hogar, subestima capacidad de pago real.
4. **Cobertura geográfica:** 12 ciudades focales, sin Santa Marta (especificada en Fase 1) ni áreas rurales.
5. **Temporalidad:** Incluye años atípicos (2020 pandemia) que distorsionan tendencias.
6. **Dataset faltante para 2024:** Armenia, Barranquilla y Cartagena no tienen datos para 2022–2024, lo que limita el análisis longitudinal completo de 12 ciudades.

## 6. Recomendaciones de Política Pública
1. **Política de oferta:** Incrementar construcción de vivienda en Bogotá y Medellín (IAH > 25) para reducir precio por m².
2. **Subsidios focalizados:** Segmentar por cluster de accesibilidad (Crítico vs Accesible).
3. **Control de tasas hipotecarias:** La tasa hipotecaria y el IPC explican >70% de la inviabilidad financiera.
4. **Transparencia de precios:** Publicar índices IAH por ciudad trimestralmente siguiendo estándares OCDE.
5. **Revisión de criterios Fase 1:** El umbral R² ≥ 0.75 no es alcanzable con modelos lineales simples dado RMSE rel de 67.86% — se recomienda usar log(price) + XGBoost (v2) o ajustar expectativas.

## 7. Entregables Generados
- `notebooks/04_evaluacion.ipynb` — Notebook de evaluación ejecutado
- `data/processed/tabla_metricas_finales.csv` — Métricas del modelo final
- `data/processed/tabla_criterios_exito.csv` — Criterios de éxito vs valor obtenido
- `data/processed/respuestas_preguntas.csv` — Respuestas a las 4 preguntas de investigación
- `docs/figures/fig_*.png` — 9 figuras de evaluación (scatter residuos, histograma, Q-Q, boxplot por ciudad, importancia vars, PCA clusters, IAH por ciudad, IAH vs precio, semáforo cuota, precios nominal vs real, niveles accesibilidad)

## 8. Próximos Pasos
1. **Ejecutar** `notebooks/03_modelado_v2.ipynb` (XGBoost + log price) para intentar superar R² ≥ 0.75
2. Si v2 no cumple criterios, **documentar como limitación del proyecto** y cerrar con recomendaciones
3. **Preparar presentación ejecutiva** de hallazgos para stakeholders
