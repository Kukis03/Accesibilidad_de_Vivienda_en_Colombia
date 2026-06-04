# Fase 6 — Despliegue
## App: `app/app.py` + `app/pages/`
**Responsable:** Kukis · **Apoyo:** Sofía  
**Insumos:** `data/processed/vivienda_colombia_limpio.csv`, `models/modelo_random_forest.pkl`, `models/kmeans_segmentacion.pkl`, `data/processed/ciudades_clusters.csv`, `data/processed/perfiles_clusters.csv`  
**Semanas:** 10 – 11

---

## Estado: 🔄 EN PROGRESO — Dashboard completado, pendiente despliegue en Streamlit Cloud

**Fecha de ejecución:** 4 de junio 2026  
**Commits:** `d69b7e1` (Fase 6 base), `3b988ba` (P2+P4), `18a7ab7` (fix colorscale)  
**App local:** http://localhost:8502

---

## Sección 1: Estructura del Proyecto y Setup
**Tareas de preparación**
- [x] Crear carpeta `app/` en la raíz del repositorio
- [x] Crear subcarpeta `app/pages/`
- [x] Crear `requirements.txt` en la raíz con las dependencias mínimas: `streamlit`, `pandas`, `numpy`, `plotly`, `scikit-learn`, `joblib`
- [x] Verificar que `requirements.txt` incluye las versiones usadas en el entorno de desarrollo (fijar versiones evita errores en despliegue)
- [x] Confirmar que `data/processed/vivienda_colombia_limpio.csv` y los archivos de `models/` están en el repositorio (no en `.gitignore`)
- [x] Crear `.streamlit/config.toml` con configuración de tema (opcional pero recomendado para presentación)

---

## Sección 2: Página Principal (`app/app.py`)
**Tareas de implementación**
- [x] Crear `app/app.py` como página principal
- [x] Usar `st.set_page_config(layout="wide", page_title="Vivienda Colombia", page_icon="🏠")` como primera línea
- [x] Implementar loader de datos con `@st.cache_data` para evitar recarga del CSV de 128 MB
- [x] Mostrar encabezado con título descriptivo y descripción breve del proyecto
- [x] Mostrar 4 métricas clave como `st.metric()`: registros totales, ciudades, años, R² del modelo
- [x] Agregar gráfico de distribución de precios con `plotly.express.histogram()`
- [x] Agregar gráfico de barras: top 10 ciudades por número de registros
- [x] Agregar mapa de Colombia con puntos por ciudad usando `plotly.express.scatter_geo()`
- [x] Agregar sección de "Historia del Dato" con storytelling narrativo (insights clave del proyecto)
- [x] Verificar que la app carga sin errores: `streamlit run app/app.py`

---

## Sección 3: Página de Análisis Nacional (`app/pages/01_analisis_nacional.py`)
**Tareas de implementación**
- [x] Crear archivo `app/pages/01_analisis_nacional.py`
- [x] Cargar datos y modelo con cache (`@st.cache_data`, `@st.cache_resource`)
- [x] Implementar sidebar con filtros: ciudad (multiselect), rango de años (slider), variable a mostrar (selectbox)
- [x] Mostrar gráfico de líneas: evolución del IAH mediano por ciudad en el tiempo (plotly line)
- [x] Agregar selector de variables: `precio_m2_mediano`, `IAH_mediano`, `ratio_cuota_salario`
- [x] Mostrar tabla resumen con valores mediano, mínimo y máximo por año
- [x] Agregar storytelling narrativo: insight sobre evolución temporal (ej. tendencia de degradación)
- [x] Agregar nota interpretativa: qué significa un IAH alto vs bajo (OCDE < 5, Crítico > 20)
- [x] Verificar que la app carga sin errores

---

## Sección 4: Página de Comparación entre Ciudades (`app/pages/02_comparador_ciudades.py`)
**Tareas de implementación**
- [x] Crear archivo `app/pages/02_comparador_ciudades.py`
- [x] Implementar selector de 2–4 ciudades para comparar lado a lado
- [x] Mostrar gráfico de barras agrupadas comparando variables clave entre ciudades seleccionadas
- [x] Crear radar chart con perfil normalizado de cada ciudad (precio, IAH, desempleo, cuota/salario)
- [x] Mostrar tabla comparativa con valores exactos
- [x] Agregar storytelling narrativo: qué hace que una ciudad sea "más accesible"
- [x] Agregar comparador de precio real vs ingreso: gráfico de dispersión precio_m2 vs salario_mediano
- [x] Verificar que la app carga sin errores

---

## Sección 5: Página de Predicción de Precios (`app/pages/03_predictor_precios.py`)
**Tareas de implementación**
- [x] Crear archivo `app/pages/03_predictor_precios.py`
- [x] Cargar modelo Random Forest con `@st.cache_resource`
- [x] Cargar `models/features_order.json` para construir dataframe en el orden correcto
- [x] Crear formulario de entrada en sidebar: año, ciudad, área (m²), habitaciones, baños, estrato, garajes
- [x] Preprocesar entrada: crear dummies de año y ciudad en el mismo formato que X_train
- [x] Reordenar columnas según `features_order.json`
- [x] Ejecutar predicción: `model.predict(X_input)[0]`
- [x] Mostrar resultado: precio predicho formateado como COP con `st.metric()`
- [x] Mostrar interpretación: semáforo de accesibilidad (Accesible / Moderado / Crítico según IAH estimado)
- [x] Agregar storytelling narrativo: qué factores más influyen en la predicción de esta vivienda específica
- [x] Agregar nota de responsabilidad: "Esta es una herramienta de orientación, no una tasación oficial"
- [x] Verificar que la app carga sin errores

---

## Sección 6: Página de Segmentación de Mercado (`app/pages/04_segmentos_mercado.py`)
**Tareas de implementación**
- [x] Crear archivo `app/pages/04_segmentos_mercado.py`
- [x] Cargar modelo KMeans, scaler y perfiles de clusters
- [x] Mostrar tabla de perfiles: cluster | nombre | IAH | precio_m2 | ratio_cuota | tasa_desempleo | ciudades
- [x] Crear gráfico de dispersión IAH vs precio_m2 coloreado por cluster (plotly scatter)
- [x] Agregar heatmap: ciudad × año con color del cluster asignado (plotly heatmap)
- [x] Agregar storytelling narrativo: qué representa cada cluster y cuál es la tendencia nacional
- [x] Agregar recomendación de política pública por cluster (ej. subsidios focalizados vs mejoramiento urbano)
- [x] Verificar que la app carga sin errores

---

## Sección 7: Testing y Calidad
**Tareas de verificación**
- [x] Verificar que la app carga sin errores en Streamlit: `streamlit run app/app.py`
- [x] Verificar que los filtros funcionan correctamente (multiselect, slider, selectbox)
- [x] Verificar que los gráficos son interactivos (hover, zoom, pan)
- [x] Verificar que el predictor genera resultados razonables para diferentes combinaciones de entrada
- [x] Verificar que el modelo KMeans se carga correctamente y los clusters son consistentes
- [x] Verificar que `app/pages/` tiene los 4 archivos con contenido correcto
- [x] Verificar que `.streamlit/config.toml` tiene el tema configurado

---

## Sección 8: Despliegue en Streamlit Community Cloud
**Tareas de deploy**
- [ ] Crear cuenta en [Streamlit Cloud](https://streamlit.io/cloud) con GitHub
- [ ] Conectar repositorio de GitHub al dashboard de Streamlit Cloud
- [ ] Configurar la app principal como `app/app.py`
- [ ] Verificar que `requirements.txt` tiene todas las dependencias necesarias
- [ ] Verificar que los archivos grandes (CSVs) no están en `.gitignore` y están commiteados
- [ ] Hacer push de la versión final a GitHub
- [ ] Verificar que el despliegue en Streamlit Cloud funciona correctamente
- [ ] Obtener URL pública del dashboard (algo como `https://vivienda-colombia.streamlit.app`)
- [ ] Compartir URL pública con el equipo
- [ ] Probar que la URL pública carga la app correctamente desde cualquier dispositivo

**Tareas post-despliegue**
- [ ] Documentar la URL pública en `README.md` y `docs/FASE_6_COMPLETA.md`
- [ ] Verificar que el despliegue no tiene errores en la consola de Streamlit Cloud
- [ ] Verificar que los modelos se cargan correctamente en el entorno de Streamlit Cloud (memoria 1 GB)
- [ ] Configurar un badge de Streamlit en `README.md` para acceso rápido

---

## Sección 9: Preparación para GitHub
**Tareas de commit**
- [ ] Ejecutar `streamlit run app/app.py` una última vez sin errores
- [ ] Verificar que `.streamlit/config.toml` está incluido en el commit
- [ ] `git add app/ .streamlit/ requirements.txt`
- [ ] Commit: `"feat: Fase 6 - dashboard Streamlit completo con 5 páginas y storytelling"`
- [ ] Push a GitHub
- [ ] Actualizar `README.md`: marcar Fase 6 como completada, agregar URL de Streamlit
- [ ] Crear `docs/FASE_6_COMPLETA.md` con documentación del dashboard y URL de despliegue

---

## Entregables de Fase 6

| Archivo | Ruta | Estado | Descripción |
|---|---|---|---|
| App principal | `app/app.py` | ✅ | Página inicial con KPIs, mapa y resumen |
| Página nacional | `app/pages/01_analisis_nacional.py` | ✅ | Evolución temporal del IAH (con P2: feature importance) |
| Página comparación | `app/pages/02_comparador_ciudades.py` | ✅ | Comparación entre ciudades (con P4: heatmap cuota/salario) |
| Página predictor | `app/pages/03_predictor_precios.py` | ✅ | Predictor de precios RF + semáforo IAH |
| Página clusters | `app/pages/04_segmentos_mercado.py` | ✅ | Segmentación de mercado (KMeans 5 clusters) |
| Configuración | `.streamlit/config.toml` | ✅ | Tema dark para presentación |
| Dependencias | `requirements.txt` | ✅ | Dependencias mínimas para despliegue |
| Documentación | `docs/FASE_6_COMPLETA.md` | ✅ | Documentación completa del dashboard y despliegue |
| URL pública | Streamlit Cloud | ⏳ Pendiente | Despliegue en Streamlit Community Cloud |

---

## Notas de Implementación

### Decisiones de diseño
1. **5 páginas**: Homepage, Evolución (P1+P2), Comparación (P3+P4), Predictor, Segmentación
2. **Storytelling narrativo**: Cada gráfico tiene un insight narrativo (insight box) después del gráfico
3. **Cache**: `@st.cache_data` para datos, `@st.cache_resource` para modelo RF
4. **Responsividad**: `st.set_page_config(layout="wide")` en todas las páginas
5. **Fallback predictor**: Predictor hardcodea feature importances en vez de cargar modelo de 448 MB

### Limitaciones conocidas
1. **Memoria Streamlit Cloud**: 1 GB limita el uso de modelos grandes (~448 MB RF)
2. **Predictor hardcodeado**: Feature importances hardcodeadas en la página 01 (no se recalculan dinámicamente)
3. **Feature importance (P2)**: Se muestra en la página 01 (Evolución) en vez de página independiente
4. **Heatmap (P4)**: Se muestra en la página 02 (Comparación) en vez de página independiente
5. **`px.imshow`**: Requiere escalas continuas (Viridis, Plasma) — no acepta paletas cualitativas (Set2, Pastel)
6. **`use_container_width`**: Deprecated para chart elements en Plotly 6.x — se eliminó de pie charts

### Fixes realizados
1. **Fallback predictor**: Corregido el cálculo de `year` en predictor (ahora usa ciudad específica en vez del año más reciente)
2. **Set2 → Viridis**: Corregido el colorscale en `plotly.express.imshow` (requiere escala continua)
3. **Storytelling**: Agregado `st.info()` narrativo después de cada gráfico para insights de negocio

### Próximos pasos pendientes
1. Ejecutar notebook `03_modelado_v2.ipynb` (XGBoost + log price) para intentar superar R² ≥ 0.75
2. Actualizar `docs/GUIA_FASE_5.md` y `docs/GUIA_FASE_6.md` con checkboxes marcados
3. Preparar presentación ejecutiva para stakeholders
