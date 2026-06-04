# Fase 6 — Despliegue
## App: `app/app.py` + `app/pages/`
**Responsable:** Kukis · **Apoyo:** Sofía  
**Insumos:** `data/processed/vivienda_colombia_limpio.csv`, `models/modelo_random_forest.pkl`, `models/kmeans_segmentacion.pkl`, `data/processed/ciudades_clusters.csv`, `data/processed/perfiles_clusters.csv`  
**Semanas:** 10 – 11

---

## Sección 1: Estructura del Proyecto y Setup
**Tareas de preparación**
- [ ] Crear carpeta `app/` en la raíz del repositorio
- [ ] Crear subcarpeta `app/pages/`
- [ ] Crear `requirements.txt` en la raíz con las dependencias mínimas: `streamlit`, `pandas`, `numpy`, `plotly`, `scikit-learn`, `joblib`
- [ ] Verificar que `requirements.txt` incluye las versiones usadas en el entorno de desarrollo (fijar versiones evita errores en despliegue)
- [ ] Confirmar que `data/processed/vivienda_colombia_limpio.csv` y los archivos de `models/` están en el repositorio (no en `.gitignore`)
- [ ] Crear `.streamlit/config.toml` con configuración de tema (opcional pero recomendado para presentación)

---

## Sección 2: Página Principal (`app/app.py`)
**Tareas de implementación**
- [ ] Configurar `st.set_page_config`: título, ícono, layout="wide", sidebar expandido
- [ ] Implementar función `@st.cache_data` para cargar `vivienda_colombia_limpio.csv` — sin caché el dashboard será lento
- [ ] Implementar función `@st.cache_resource` para cargar el modelo RF con `joblib.load`
- [ ] Crear sidebar con filtros globales: `st.sidebar.selectbox` para ciudad (+ opción "Todas"), `st.sidebar.slider` para rango de años (2020–2024), `st.sidebar.radio` para tipo de propiedad
- [ ] Aplicar filtros al DataFrame cargado y almacenar como variable de sesión o pasar a las páginas
- [ ] Mostrar 3 KPI cards en la fila principal: precio mediano nacional (COP), IAH mediano nacional (años), % de mercado con ratio cuota/salario > 0.30
- [ ] Agregar texto de bienvenida con descripción breve del proyecto y metodología CRISP-DM
- [ ] Verificar que la página carga correctamente en navegador local (`streamlit run app/app.py`)

---

## Sección 3: Página de Análisis Nacional (`app/pages/01_analisis_nacional.py`)
**Tareas de implementación**
- [ ] Cargar datos usando la misma función `@st.cache_data` definida en `app.py` (o importar desde módulo común)
- [ ] Crear gráfico de líneas: evolución del IAH mediano nacional por año (2020–2024) con líneas de referencia horizontales en IAH = 5 (verde, "Accesible OCDE") y IAH = 10 (naranja, "Moderado")
- [ ] Crear gráfico de líneas: salario mínimo nominal vs precio mediano de vivienda por año (doble eje Y)
- [ ] Crear gráfico de barras apiladas: distribución de `nivel_accesibilidad` por año (% de Accesible / Moderado / Elevado / Crítico)
- [ ] Crear tabla resumen anual: año | precio mediano | salario mínimo | IAH | tasa hipotecaria | IPC
- [ ] Agregar selector de ciudad para mostrar análisis temporal de una ciudad específica
- [ ] Verificar que todos los gráficos son interactivos (Plotly, no matplotlib estático)

---

## Sección 4: Página Comparador de Ciudades (`app/pages/02_comparador_ciudades.py`)
**Tareas de implementación**
- [ ] Agregar `st.multiselect` para seleccionar 2 o más ciudades a comparar (máximo 4 recomendado)
- [ ] Agregar `st.slider` para seleccionar año de comparación (2020–2024)
- [ ] Crear tabla comparativa: ciudad | precio mediano | precio/m² | IAH | ratio cuota/salario | tasa desempleo | cluster
- [ ] Crear gráfico de barras agrupadas: precio mediano y IAH por ciudad seleccionada
- [ ] Crear gráfico de líneas: evolución del IAH por ciudad seleccionada en el período completo
- [ ] Crear boxplot de distribución de precios por ciudad seleccionada (para el año elegido)
- [ ] Mostrar mensaje de advertencia si alguna ciudad tiene < 500 registros en el año seleccionado

---

## Sección 5: Página Predictor de Precios (`app/pages/03_predictor_precios.py`)
**Tareas de implementación**
- [ ] Cargar modelo RF y el `features_order.json` con `@st.cache_resource`
- [ ] Crear formulario de entrada con `st.form`:
  - `st.selectbox` para ciudad (12 ciudades canónicas)
  - `st.selectbox` para tipo de propiedad (Casa / Apartamento)
  - `st.number_input` para área (m²) — rango sugerido 20–500
  - `st.number_input` para habitaciones — rango 1–10
  - `st.number_input` para baños — rango 1–8
  - `st.selectbox` para estrato (1–6)
  - `st.selectbox` para año (2020–2024)
- [ ] Al enviar el formulario: recuperar macro variables del año seleccionado (tasa hipotecaria, IPC, desempleo por ciudad) desde el dataset
- [ ] Construir DataFrame de 1 fila con todas las features en el orden correcto (`features_order.json`)
- [ ] Llamar `pipeline_rf.predict(X_input)` y mostrar el precio predicho en COP
- [ ] Calcular IAH = precio predicho / salario anual del año seleccionado
- [ ] Calcular cuota mensual estimada (70% financiación, 15 años, tasa del año)
- [ ] Calcular ratio cuota/salario
- [ ] Mostrar semáforo de accesibilidad: verde (IAH ≤ 5), amarillo (5 < IAH ≤ 10), naranja (10 < IAH ≤ 20), rojo (IAH > 20)
- [ ] Mostrar comparación: "esta vivienda está en el percentil X de precios en [ciudad] para [año]"
- [ ] Agregar nota aclaratoria sobre las limitaciones del predictor (vivienda listada en plataformas digitales)

---

## Sección 6: Página Segmentos de Mercado (`app/pages/04_segmentos_mercado.py`)
**Tareas de implementación**
- [ ] Cargar `data/processed/ciudades_clusters.csv` y `data/processed/perfiles_clusters.csv`
- [ ] Crear scatter plot interactivo: IAH mediano vs precio_m2 mediano, un punto por ciudad-año, coloreado por cluster, con tooltip que muestre ciudad y año
- [ ] Crear heatmap: ciudad (filas) × año (columnas), con celda coloreada según cluster asignado
- [ ] Mostrar tabla de perfiles de clusters: nombre del cluster | IAH promedio | precio/m² promedio | ratio cuota/salario | ciudades en 2024
- [ ] Crear gráfico de área o Sankey que muestre si ciudades cambiaron de cluster entre 2020 y 2024
- [ ] Agregar explicación textual de cada cluster (accesible, moderado, elevado, crítico) con las ciudades que lo componen
- [ ] Agregar nota metodológica sobre KMeans: número de clusters, coeficiente de silueta obtenido

---

## Sección 7: Pruebas Locales Completas
**Verificación antes del despliegue**
- [ ] Ejecutar `streamlit run app/app.py` localmente y navegar por las 4 páginas
- [ ] Probar el predictor con al menos 3 combinaciones diferentes (Bogotá apartamento / Cúcuta casa / Medellín apartamento)
- [ ] Verificar que los filtros del sidebar funcionan correctamente en todas las páginas
- [ ] Verificar que los gráficos de Plotly son interactivos (hover, zoom, filtros de leyenda)
- [ ] Verificar que la app no lanza errores en la consola de Streamlit
- [ ] Verificar que la app carga en menos de 10 segundos (si es más lenta, revisar el caché de datos)
- [ ] Probar en resolución de pantalla 1366×768 (portátil estándar) para verificar que no hay desbordamiento de layout

---

## Sección 8: Despliegue en Streamlit Community Cloud
**Tareas de despliegue**
- [ ] Hacer push de todos los cambios a la rama `main` (Streamlit Cloud despliega desde `main` por defecto)
- [ ] Ingresar a [share.streamlit.io](https://share.streamlit.io) con la cuenta GitHub del equipo
- [ ] Crear nueva app: seleccionar repositorio, rama `main`, archivo principal `app/app.py`
- [ ] Verificar que `requirements.txt` está en la raíz del repositorio (Streamlit Cloud lo detecta automáticamente)
- [ ] Esperar a que el build termine sin errores (revisar logs de Streamlit Cloud)
- [ ] Abrir la URL pública generada y probar las 4 páginas en el entorno de producción
- [ ] Copiar la URL pública y agregarla al `README.md` del repositorio
- [ ] Si el build falla por falta de memoria (dataset pesado): agregar `@st.cache_data(max_entries=1)` y considerar usar datos pre-agregados (`mediana por ciudad-año`) en lugar del dataset completo

---

## Sección 9: Preparación para la Presentación Final
**Tareas de documentación y ensayo**
- [ ] Actualizar `README.md` con: descripción del proyecto, URL del dashboard, instrucciones de instalación local, estructura de carpetas, equipo
- [ ] Crear `docs/FASE_6_COMPLETA.md` con descripción de la arquitectura, requerimientos funcionales y URL de despliegue
- [ ] Preparar demo de 3 minutos del dashboard para la presentación ante jurado: recorrido por las 4 páginas + predictor con un caso real
- [ ] Documentar en el notebook o en el doc de fase cuáles datos se usan agregados (mediana) vs registro completo, para responder preguntas del jurado
- [ ] Actualizar `README.md`: marcar Fase 6 como completada con link al dashboard

---

## Sección 10: Preparación para GitHub — Commit Final
- [ ] Confirmar que `data/raw/` está en `.gitignore` (no subir los 16 CSVs pesados)
- [ ] Confirmar que `models/` NO está en `.gitignore` (los `.pkl` deben subirse)
- [ ] Confirmar que `app/` NO está en `.gitignore`
- [ ] `git add app/ requirements.txt .streamlit/ README.md docs/FASE_6_COMPLETA.md`
- [ ] Commit: `"feat: Fase 6 - dashboard Streamlit completo y desplegado"`
- [ ] Push a rama `main`
- [ ] Verificar que el despliegue en Streamlit Cloud se actualiza automáticamente

---

## Entregables de Fase 6

| Archivo / URL | Ruta | Descripción |
|---|---|---|
| Página principal | `app/app.py` | Contenedor, KPIs y filtros globales |
| Análisis nacional | `app/pages/01_analisis_nacional.py` | Evolución temporal del IAH y macro Colombia |
| Comparador de ciudades | `app/pages/02_comparador_ciudades.py` | Contraste estadístico entre ciudades |
| Predictor de precios | `app/pages/03_predictor_precios.py` | Formulario + modelo RF + semáforo de accesibilidad |
| Segmentos de mercado | `app/pages/04_segmentos_mercado.py` | Visualización de clusters KMeans |
| Dependencias | `requirements.txt` | Versiones fijas de todas las librerías |
| Configuración Streamlit | `.streamlit/config.toml` | Tema y configuración visual |
| Dashboard público | URL Streamlit Cloud | Aplicación desplegada y accesible desde cualquier navegador |
| Documento de fase | `docs/FASE_6_COMPLETA.md` | Arquitectura, requerimientos y URL de despliegue |
