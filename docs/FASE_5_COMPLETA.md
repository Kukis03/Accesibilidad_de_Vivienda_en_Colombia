# Fase 5 — Evaluación
## Proyecto: Accesibilidad de Vivienda en Colombia · CRISP-DM 2025-I
**Responsable principal:** Sofía · **Apoyo:** Steve  
**Estado:** ⏳ Pendiente — requiere resultados reales de Fase 4  
**Notebook asociado:** `notebooks/04_evaluacion.ipynb` *(por ejecutar)*  
**Semana:** 9

> ⚠️ **Aviso de auditoría:** Esta fase **no ha sido ejecutada**. El documento describe el plan de evaluación y el código a implementar. Todos los resultados, métricas, tablas de verificación de criterios y respuestas a preguntas de investigación están marcados como `[PENDIENTE]` y deberán completarse con los datos reales producidos por Fase 4. No contiene datos inventados.

---

## Introducción

La Fase 5 de la metodología CRISP-DM corresponde a la Evaluación. Su propósito no es evaluar el ajuste matemático de los algoritmos (realizado preliminarmente en Fase 4), sino **validar el proyecto desde la perspectiva del negocio**: constatar si los entregables técnicos cumplen los criterios de éxito planteados en la Fase 1, traducir las métricas técnicas a implicaciones socioeconómicas reales y proveer respuestas cuantitativas a las 4 preguntas de investigación.

**Prerrequisito bloqueante:** Fase 4 debe estar completamente ejecutada y sus entregables generados (`modelo_random_forest.pkl`, `segmentos_mercado.csv`, métricas reales documentadas).

---

## 1. Verificación de Criterios de Aceptación

> ⚠️ Los valores de la columna "Valor Obtenido" se completarán con los datos reales producidos por Fase 4. No completar con estimaciones.

| Criterio de Éxito | Dimensión | Umbral Definido (Fase 1) | Valor Obtenido | ¿Cumple? |
|---|---|---|---|---|
| **R² Regresión** | Capacidad Predictiva | R² ≥ 0.75 | `[PENDIENTE]` | `[PENDIENTE]` |
| **RMSE relativo** | Precisión Predictiva | < 15.0% del precio mediano | `[PENDIENTE]` | `[PENDIENTE]` |
| **Estabilidad Regresión** | Validación Cruzada | CV R² std < 0.05 | `[PENDIENTE]` | `[PENDIENTE]` |
| **Separabilidad Clustering** | Calidad de Agrupación | Coef. Silueta ≥ 0.45 | `[PENDIENTE]` | `[PENDIENTE]` |
| **Resolución del Modelo** | Cobertura Territorial | ≥ 8 ciudades | `[PENDIENTE]` | `[PENDIENTE]` |
| **Resolución Temporal** | Historial de Datos | Período 2020–2024 | `[PENDIENTE]` | `[PENDIENTE]` |
| **Preguntas de Investigación** | Transferencia de Negocio | 4 de 4 preguntas resueltas | `[PENDIENTE]` | `[PENDIENTE]` |

---

## 2. Evaluación Completa del Modelo de Regresión

### 2.1 Métricas Finales sobre el Conjunto de Pruebas

```python
import pandas as pd
import numpy as np
import joblib
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Cargar modelo entrenado en Fase 4
pipeline_rf = joblib.load("models/modelo_random_forest.pkl")
df = pd.read_csv("data/processed/vivienda_colombia_limpio.csv")

FEATURES_NUM = ['area', 'rooms', 'bathrooms', 'estrato', 'year', 'ipc_var_anual',
                'tasa_hipotecaria_anual', 'tasa_desempleo', 'ipvu_variacion_anual']
FEATURES_CAT = ['city', 'property_type']
TARGET = 'price'

# Reproducir la misma división train/test de Fase 4 (random_state=42)
from sklearn.model_selection import train_test_split
X = df[FEATURES_NUM + FEATURES_CAT]
y = df[TARGET]
_, X_test, _, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

y_pred = pipeline_rf.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)
mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100
rmse_relativo = (rmse / y_test.mean()) * 100

print(f"R²:            {r2:.4f}")
print(f"MAE:           ${mae:,.0f} COP")
print(f"RMSE:          ${rmse:,.0f} COP")
print(f"MAPE:          {mape:.2f}%")
print(f"RMSE Relativo: {rmse_relativo:.2f}%")
```

| Métrica | Valor Obtenido | Interpretación |
|---|---|---|
| **R² (Coef. de Determinación)** | `[PENDIENTE]` | `[PENDIENTE]` |
| **MAE (Error Absoluto Medio)** | `[PENDIENTE]` COP | `[PENDIENTE]` |
| **MAPE** | `[PENDIENTE]`% | `[PENDIENTE]` |
| **RMSE** | `[PENDIENTE]` COP | `[PENDIENTE]` |
| **RMSE Relativo** | `[PENDIENTE]`% | `[PENDIENTE]` |

### 2.2 Validación Cruzada (Estabilidad del Modelo)

```python
from sklearn.model_selection import cross_val_score

scores = cross_val_score(pipeline_rf, X, y, cv=5, scoring='r2', n_jobs=-1)
print(f"R² por partición: {scores}")
print(f"R² Promedio: {scores.mean():.4f} +/- {scores.std():.4f}")
```

**R² por partición (5-Fold CV):** `[PENDIENTE]`  
**R² Promedio:** `[PENDIENTE]` ± `[PENDIENTE]`

### 2.3 Curva de Aprendizaje

```python
import matplotlib.pyplot as plt
from sklearn.model_selection import learning_curve

train_sizes, train_scores, test_scores = learning_curve(
    pipeline_rf, X, y, train_sizes=np.linspace(0.1, 1.0, 5),
    cv=3, scoring='r2', n_jobs=-1, random_state=42
)

plt.figure(figsize=(8, 4))
plt.plot(train_sizes, np.mean(train_scores, axis=1), 'o-', color="r", label="Entrenamiento")
plt.plot(train_sizes, np.mean(test_scores, axis=1), 'o-', color="g", label="Validación")
plt.title("Curva de Aprendizaje - Random Forest Regressor")
plt.xlabel("Tamaño del Conjunto de Entrenamiento")
plt.ylabel("R²")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("docs/figures/10_curva_aprendizaje.png", dpi=150)
plt.close()
```

**Figura generada:** `docs/figures/10_curva_aprendizaje.png` `[PENDIENTE]`  
**Interpretación (sobreajuste / underfitting):** `[PENDIENTE — completar tras ejecutar]`

---

## 3. Evaluación del Modelo de Clustering

### 3.1 Métricas de Cohesión y Separabilidad

```python
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score

df_sub = pd.read_csv("data/processed/segmentos_mercado.csv")
VARS_CLUSTER = ['precio_mediano', 'IAH_promedio', 'ratio_cuota_promedio',
                'precio_m2_mediano', 'tasa_desempleo']

scaler = StandardScaler()
X_c = scaler.fit_transform(df_sub[VARS_CLUSTER])
labels = df_sub['cluster']

sil_global = silhouette_score(X_c, labels)
db_global = davies_bouldin_score(X_c, labels)
ch_global = calinski_harabasz_score(X_c, labels)

print(f"Coeficiente de Silueta Global: {sil_global:.4f}")
print(f"Índice Davies-Bouldin:         {db_global:.4f}")
print(f"Índice Calinski-Harabasz:      {ch_global:.4f}")
```

**Coeficiente de Silueta:** `[PENDIENTE]`  
**Índice Davies-Bouldin:** `[PENDIENTE]`  
**Índice Calinski-Harabasz:** `[PENDIENTE]`

> **Umbrales de aceptación:** Silueta ≥ 0.45 y Davies-Bouldin < 1.0 confirmarán estructura de agrupación válida.

### 3.2 Prueba Estadística de Separabilidad de Grupos (Kruskal-Wallis)

```python
import scipy.stats as stats

# Obtener los nombres reales de los segmentos una vez ejecutado el clustering
segmentos = df_sub['segmento'].unique().tolist()  # [PENDIENTE — nombres reales]
grupos_iah = [df_sub[df_sub['segmento'] == s]['IAH_promedio'] for s in segmentos]
h_stat, p_value = stats.kruskal(*grupos_iah)
print(f"Estadístico H de Kruskal-Wallis: {h_stat:.2f} | p-valor: {p_value:.3e}")
```

**Estadístico H:** `[PENDIENTE]`  
**p-valor:** `[PENDIENTE]`  
**Conclusión:** `[PENDIENTE — completar tras ejecutar prueba]`

---

## 4. Interpretación del Modelo con Importancia de Variables

```python
# Extraer feature_importances_ del pipeline cargado
rf_step = pipeline_rf.named_steps['regressor']
prep_step = pipeline_rf.named_steps['preprocessor']
cat_encoder = prep_step.named_transformers_['cat'].named_steps['onehot']
cat_cols = list(cat_encoder.get_feature_names_out(FEATURES_CAT))
all_features = FEATURES_NUM + cat_cols

importances = rf_step.feature_importances_
ranking = sorted(zip(all_features, importances), key=lambda x: x[1], reverse=True)
for i, (feat, imp) in enumerate(ranking, 1):
    print(f"{i}. {feat}: {imp:.4f} ({imp*100:.1f}%)")
```

**Ranking completo de importancia de variables:** `[PENDIENTE — completar tras ejecutar]`

**Variable física con mayor poder predictivo:** `[PENDIENTE]`  
**Variable macroeconómica con mayor impacto:** `[PENDIENTE]`

---

## 5. Respuesta a las Preguntas de Investigación

> ⚠️ Las respuestas cuantitativas se completan **después de ejecutar las fases 3 y 4** con datos reales. No completar con estimaciones.

### 5.1 Pregunta 1: ¿Cuántos años de salario mínimo cuesta una vivienda mediana en Colombia y cómo varía por ciudad?

**Respuesta:** `[PENDIENTE — calcular con dataset corregido de Fase 3]`

| Ciudad | IAH Mediano `[AÑO MÁS RECIENTE]` (Años de Salario) | Clasificación de Accesibilidad (OCDE) |
|---|---|---|
| Bogotá | `[PENDIENTE]` | `[PENDIENTE]` |
| Medellín | `[PENDIENTE]` | `[PENDIENTE]` |
| Cali | `[PENDIENTE]` | `[PENDIENTE]` |
| Barranquilla | `[PENDIENTE]` | `[PENDIENTE]` |
| Cartagena | `[PENDIENTE]` | `[PENDIENTE]` |
| Bucaramanga | `[PENDIENTE]` | `[PENDIENTE]` |
| Manizales | `[PENDIENTE]` | `[PENDIENTE]` |
| Pereira | `[PENDIENTE]` | `[PENDIENTE]` |
| Armenia | `[PENDIENTE]` | `[PENDIENTE]` |
| Ibagué | `[PENDIENTE]` | `[PENDIENTE]` |
| Cúcuta | `[PENDIENTE]` | `[PENDIENTE]` |
| Villavicencio | `[PENDIENTE]` | `[PENDIENTE]` |

*Clasificación OCDE: Accesible (IAH ≤ 5) | Moderado (5–10) | Elevado (10–20) | Crítico (> 20)*

**Conclusión:** `[PENDIENTE]`

---

### 5.2 Pregunta 2: ¿Qué variables del inmueble y del entorno macroeconómico tienen el mayor poder explicativo sobre el precio?

**Variable inmobiliaria más importante:** `[PENDIENTE — ver importancia de variables, sección 4]`  
**Variable macroeconómica más importante:** `[PENDIENTE]`

*Evidencia cuantitativa (feature_importances_):*

| Rango | Variable | Importancia (%) |
|---|---|---|
| 1 | `[PENDIENTE]` | `[PENDIENTE]` |
| 2 | `[PENDIENTE]` | `[PENDIENTE]` |
| 3 | `[PENDIENTE]` | `[PENDIENTE]` |
| 4 | `[PENDIENTE]` | `[PENDIENTE]` |
| 5 | `[PENDIENTE]` | `[PENDIENTE]` |

**Conclusión:** `[PENDIENTE]`

---

### 5.3 Pregunta 3: ¿Es posible identificar y segmentar submercados urbanos homogéneos según accesibilidad?

**Respuesta:** `[PENDIENTE — depende de K óptimo y clustering ejecutado en Fase 4]`

*Número de segmentos identificados:* `[PENDIENTE]`  
*Validación (Silueta / Davies-Bouldin):* `[PENDIENTE]`

**Conclusión:** `[PENDIENTE]`

---

### 5.4 Pregunta 4: ¿En qué ciudades de Colombia la cuota hipotecaria promedio supera el 30% del salario mínimo mensual?

```python
# Calcular por ciudad el porcentaje de propiedades con ratio_cuota_salario > 0.30
df_inviable = df.groupby('city').apply(
    lambda x: (x['ratio_cuota_salario'] > 0.30).mean() * 100
).reset_index()
df_inviable.columns = ['city', 'pct_inviable']
print(df_inviable.sort_values('pct_inviable', ascending=False).round(1))
```

**Porcentaje de oferta inviable (cuota > 30% salario mínimo) por ciudad:** `[PENDIENTE]`

**Conclusión:** `[PENDIENTE]`

---

## 6. Conclusiones en Lenguaje de Negocio

> ⚠️ Las conclusiones se redactarán con base en los resultados reales obtenidos en las secciones anteriores. Los siguientes ítems representan el marco de análisis; el contenido específico se completa tras la ejecución.

1. **Viabilidad del crédito hipotecario para el salario mínimo:** `[PENDIENTE — redactar con porcentajes reales de ratio cuota/salario]`
2. **Brecha entre precios de oferta y capacidad de pago real:** `[PENDIENTE]`
3. **Impacto de las tasas de interés en la accesibilidad:** `[PENDIENTE — cuantificar con datos del período 2020–2024]`
4. **Dinámicas de mercado específicas por ciudad:** `[PENDIENTE — completar con hallazgos del clustering]`
5. **Recomendación de política pública:** `[PENDIENTE — derivar de los segmentos identificados]`

---

## 7. Limitaciones Identificadas

> Las siguientes limitaciones son inherentes al diseño del proyecto y son conocidas antes de la ejecución. Los detalles cuantitativos se completarán con datos reales.

- **Sesgo de formalidad:** El dataset representa únicamente la oferta publicada en portales digitales. No incluye vivienda informal ni mercado de segunda mano fuera de internet.
- **Ausencia del mercado de arriendos:** El estudio se centra en el acceso a la compra. La mayoría de los hogares de salario mínimo recurre al arrendamiento.
- **Cobertura desigual entre ciudades:** Bogotá y Medellín tendrán mayor volumen de registros que ciudades intermedias como Villavicencio o Armenia. El impacto exacto en las métricas se evaluará tras la ejecución.
- **Período con alta variabilidad macroeconómica:** El período 2020–2024 incluye la pandemia y el ciclo de tasas de interés más agresivo en décadas, lo que puede introducir ruido en las relaciones precio–características físicas.

---

## 8. Hallazgos de la Fase 5

> ⚠️ Esta sección se completa **únicamente después de ejecutar la fase** con datos reales.

| ID | Hallazgo Clave | Evidencia Numérica | Relevancia para Fase 6 |
|---|---|---|---|
| **H5.1** | Cumplimiento umbral R² | `[PENDIENTE]` | `[PENDIENTE]` |
| **H5.2** | MAPE vs umbral del 15% | `[PENDIENTE]` | `[PENDIENTE]` |
| **H5.3** | Estabilidad de validación cruzada | σ CV R² = `[PENDIENTE]` | `[PENDIENTE]` |
| **H5.4** | Validación estadística de clústeres | p-valor Kruskal-Wallis = `[PENDIENTE]` | `[PENDIENTE]` |
| **H5.5** | IAH en ciudad con mayor inaccesibilidad | `[PENDIENTE]` años | `[PENDIENTE]` |
| **H5.6** | IAH en ciudad con menor inaccesibilidad | `[PENDIENTE]` años | `[PENDIENTE]` |
| **H5.7** | Ciudad(es) con mercado atípico detectado por DBSCAN | `[PENDIENTE]` | `[PENDIENTE]` |

---

## 9. Entregables de la Fase 5

| Archivo | Ruta | Estado |
|---------|------|--------|
| Notebook | `notebooks/04_evaluacion.ipynb` | ⏳ Pendiente de ejecución |
| Tabla métricas finales | `docs/tabla_metricas_finales.csv` | ⏳ Pendiente de generación |
| Figura curva de aprendizaje | `docs/figures/10_curva_aprendizaje.png` | ⏳ Pendiente |

---

## 10. Checklist — Fase 5

- [ ] Ejecutar Fase 4 y verificar que todos sus entregables existen
- [ ] Cargar modelo entrenado y reproducir métricas en test set
- [ ] Ejecutar validación cruzada 5-Fold y graficar curva de aprendizaje
- [ ] Calcular métricas de clustering (Silueta, Davies-Bouldin, Calinski-Harabasz)
- [ ] Ejecutar prueba Kruskal-Wallis sobre IAH por segmento
- [ ] Completar tabla de verificación de criterios de aceptación
- [ ] Extraer y documentar importancia de variables del modelo
- [ ] Calcular IAH mediano por ciudad para el período más reciente disponible
- [ ] Calcular porcentaje de oferta con cuota > 30% salario mínimo por ciudad
- [ ] Redactar conclusiones de negocio con datos reales
- [ ] Completar sección de hallazgos con datos reales obtenidos
- [ ] Actualizar estado del documento de "Pendiente" a "Completa"

---

## 11. Notas para el Equipo

- **Para Kukis (Fase 6):** El dashboard usará directamente las métricas y segmentos validados en esta fase. El semáforo de accesibilidad se calibrará con los umbrales confirmados aquí (IAH y ratio cuota/salario reales).
- **Criterio de aceptación del modelo para producción:** Si R² < 0.75 o Silueta < 0.45, no se debe desplegar el dashboard con esos modelos; se deben revisar el pipeline de datos o explorar modelos alternativos.

---

*Documento de Fase 5 · CRISP-DM 2025-I · Proyecto Accesibilidad Habitacional Colombia*  
*Estado: PLANTILLA — completar con datos reales tras ejecutar la fase*
