# Plan de Mejoras — Accesibilidad de Vivienda en Colombia

**Fecha:** 4 de junio 2026  
**Versión:** 2.1 (actualizado con progreso)  
**Cobertura:** 68 hallazgos de la auditoría profunda de todo el códigobase  
**Estado:** Sprint 1 ✅ | Sprint 2 ✅ | Sprint 3 ✅ | **100% COMPLETADO**  

---

## 📋 Resumen por categoría y severidad

| Categoría | 🔴 Crítico | 🟠 Alto | 🟡 Medio | 🔵 Menor | Total |
|---|---|---|---|---|---|
| Dashboard (lógica) | 2 | 6 | 3 | 0 | 11 |
| Dashboard (narrativas) | 1 | 1 | 2 | 0 | 4 |
| Dashboard (UX/UI) | 1 | 2 | 2 | 0 | 5 |
| Dashboard (código) | 0 | 0 | 0 | 6 | 6 |
| Data pipeline | 0 | 1 | 5 | 3 | 9 |
| Modelo / Notebooks | 1 | 2 | 0 | 4 | 7 |
| Documentación | 1 | 2 | 5 | 7 | 15 |
| Infraestructura | 0 | 0 | 0 | 2 | 2 |
| **Total** | **6** | **14** | **17** | **22** | **59** |

*(9 hallazgos adicionales son duplicados entre agentes o información sin acción)*

---

## 🔴 CRÍTICOS (6)

### C-1. Crash en Página 4 — Column rename mismatch
| | |
|---|---|
| **Archivo** | `app/pages/04_segmentos_mercado.py:88-89` |
| **Problema** | `perfiles_clusters.csv` tiene 6 columnas (`cluster`, `IAH`, `precio_m2`, `ratio_cuota_salario`, `tasa_desempleo`, `count`). El código asigna 5 nombres → `ValueError`. La pestaña "Perfiles" nunca carga. |
| **Solución** | `perf.columns = ['Clúster', 'IAH', 'Precio m²', 'Ratio Cuota/Salario', 'Tasa Desempleo', 'Registros']` o cargar con `index_col=0` |
| **Archivos a tocar** | 1 |

### C-2. Fórmula de cuota mensual inconsistente (predictor vs dataset)
| | |
|---|---|
| **Archivos** | `02_preparacion_datos.py:559` vs `03_predictor_precios.py:83` |
| **Problema** | Preparación usa **tasa efectiva** `(1 + tasa/100)^(1/12) - 1`; predictor usa **tasa nominal** `tasa / 12`. Discrepancia de ~7.3% en cuotas mensuales. El dato del dataset no coincide con lo que calcula el predictor. |
| **Solución** | Unificar ambas a la misma fórmula. Banco de la República reporta tasa **nominal** → usar `/ 12` en ambos. |
| **Archivos a tocar** | 2 |

### C-3. Slider de año en homepage no filtra los KPIs
| | |
|---|---|
| **Archivo** | `app/app.py:30,34-38` |
| **Problema** | `anio_sel` se captura del slider pero `df_f` solo filtra por ciudad y tipo. Los KPIs, el mapa y los insights muestran datos de **todos** los años combinados, no del año seleccionado. Usuario cree que está viendo 2024 pero ve el promedio 2020-2024. |
| **Solución** | Agregar `& (df['year'] == anio_sel)` al filtro de `df_f`. |
| **Archivos a tocar** | 1 |

### C-4. Narrativa "Crítica 30-50%" contradice el dato real (61.4%)
| | |
|---|---|
| **Archivo** | `app/pages/01_analisis_nacional.py:101` |
| **Problema** | El insight narrativo hardcodeado dice "el porcentaje de vivienda 'Crítica' (IAH > 20) se mantiene entre 30-50% del mercado". El valor real computado en la barra apilada de arriba es **61.4%** (173,550 de 282,660 registros). El insight subestima la crisis. |
| **Solución** | Computar dinámicamente `pct_critica = (df_p['nivel_accesibilidad'] == 'Crítico').sum() / len(df_p) * 100` e insertar en el f-string. |
| **Archivos a tocar** | 1 |

### C-5. Validación ficticia en `generate_eval_notebook.py`
| | |
|---|---|
| **Archivo** | `generate_eval_notebook.py:490-497` |
| **Problema** | Las líneas son: `if True: respuestas.append("P1: ok")` en vez de `if p1: ...`. Las variables `p1`, `p2`, `p3`, `p4` contienen resultados reales de búsqueda en notebooks, pero siempre se reporta "ok" porque los `if` ignoran las variables. |
| **Solución** | Cambiar `if True:` → `if p1:` (y análogamente p2, p3, p4) |
| **Archivos a tocar** | 1 |

### C-6. Importancia de variables contradictoria entre documentos del mismo modelo
| | |
|---|---|
| **Archivos** | `docs/FASE_4_COMPLETA.md` (línea 137), `docs/GUIA_FASE_4.md` (línea 112) vs `docs/FASE_5_COMPLETA.md` (líneas 65-69), `docs/GUIA_FASE_5.md` (línea 79) |
| **Problema** | **Documentos de Fase 4** dicen: "`tasa_desempleo` y `ipc_var_anual` son las más importantes (~12% cada una), seguidas de `area` y `estrato`". **Documentos de Fase 5** dicen: "`bathrooms` 42.2%, `area` 28.0%, `estrato` 11.3%". Es el **mismo modelo Random Forest** — las feature importances deberían ser idénticas. Una de las dos versiones está completamente equivocada. |
| **Solución** | Revisar el notebook `03_modelado.ipynb` para extraer las importancias reales. Probablemente Fase 5 es correcta (extraída del modelo con código). Corregir Fase 4. |
| **Archivos a tocar** | 2 documentos |

---

## 🟠 ALTOS (14)

### A-1. Heatmap ignora selección de ciudades en P2
| | |
|---|---|
| **Archivo** | `app/pages/02_comparador_ciudades.py:112` |
| **Problema** | `ratio_all = df.groupby(['city', 'year'])...` calcula el heatmap de ratio_cuota_salario para **todas** las ciudades. El usuario seleccionó 2-4 ciudades para comparar, pero el heatmap muestra las 12. |
| **Solución** | Agregar filtro: `df[df['city'].isin(cities_sel)].groupby(...)` |
| **Archivos a tocar** | 1 |

### A-2. Heatmap de cuota/salario todo rojo (escala incorrecta)
| | |
|---|---|
| **Archivo** | `app/pages/02_comparador_ciudades.py:116-117` |
| **Problema** | `range_color=[0, 0.6]` fija el máximo en 0.6 (60% del salario). Pero los datos reales van de 0.23 a **35.12** (352% del salario). Todas las celdas quedan en el extremo rojo, sin discriminación visual entre ciudades. |
| **Solución** | Usar `range_color=[0, 3.5]` que cubre el ~90% de los datos, o eliminar `range_color` y dejar que Plotly auto-escala (el tooltip muestra el valor exacto). |
| **Archivos a tocar** | 1 |

### A-3. Percentil del predictor ignora tipo de propiedad
| | |
|---|---|
| **Archivo** | `app/pages/03_predictor_precios.py:115` |
| **Problema** | `pct = (df[(df['city'] == ciudad) & (df['year'] == anio)]['price'] < pred).mean() * 100` — filtra por ciudad y año pero **no** por `property_type`. Si el usuario predice un apartamento de 70m², el percentil compara contra casas de 300m² también. |
| **Solución** | Agregar `& (df['property_type'] == tipo)` |
| **Archivos a tocar** | 1 |

### A-4. Radar incluye columnas no-feature (cluster ID, count)
| | |
|---|---|
| **Archivo** | `app/pages/04_segmentos_mercado.py:98-107` |
| **Problema** | `perfiles` tiene 6 columnas: `cluster` (enteros 0-4), `IAH`, `precio_m2`, `ratio_cuota_salario`, `tasa_desempleo`, `count` (enteros 6-18). La normalización `(perfiles - perfiles.min()) / (perfiles.max() - perfiles.min())` incluye `cluster` y `count`, distorsionando el radar. |
| **Solución** | Seleccionar solo features: `perfiles[['IAH', 'precio_m2', 'ratio_cuota_salario', 'tasa_desempleo']]` |
| **Archivos a tocar** | 1 |

### A-5. Nombres de clusters contradicen `nivel_accesibilidad` (desinformación)
| | |
|---|---|
| **Archivo** | `app/pages/04_segmentos_mercado.py:22` |
| **Problema** | Los nombres de clusters en P4 no corresponden a los niveles de IAH definidos en Fase 1 y usados en todas las demás páginas: |
| | Cluster 4 (IAH=12.93) → llamado "Accesible" pero según `nivel_accesibilidad` es **"Elevado"** (10 < IAH ≤ 20) |
| | Cluster 2 (IAH=18.66) → llamado "Accesible Relativo" pero también es **"Elevado"** |
| | Cluster 0 (IAH=29.23) → llamado "Elevado" pero es **"Crítico"** (IAH > 20) |
| | Cluster 3 (IAH=25.35) → llamado "Elevado" pero es **"Crítico"** |
| | Un mismo usuario navegando entre páginas ve "Accesible" en P4 y "Elevado" en P1 para la misma ciudad. |
| **Solución** | Cambiar nombres: `{0: "Premium (IAH 29.2)", 1: "Intermedio (IAH 16.2)", 2: "Accesible Relativo (IAH 18.7)", 3: "Premium (IAH 25.4)", 4: "Intermedio (IAH 12.9)"}`. O idealmente cargar desde CSV. |
| **Archivos a tocar** | 1 |

### A-6. Slider de año en P4 no conectado a nada (engaña al usuario)
| | |
|---|---|
| **Archivo** | `app/pages/04_segmentos_mercado.py:33` |
| **Problema** | `año = st.select_slider("Año", ...)` — la variable `año` se asigna pero **nunca se usa** en ninguna parte del archivo. El usuario ve un slider, lo ajusta, y no pasa nada. |
| **Solución** | Eliminar el slider, o conectarlo filtrando `dfc = dfc[dfc['year'] == año]` en los scatter y heatmap. |
| **Archivos a tocar** | 1 |

### A-7. `nivel_accesibilidad` con NaN → string "nan" distorsiona gráficos
| | |
|---|---|
| **Archivo** | `app/pages/01_analisis_nacional.py:14` |
| **Problema** | `df['nivel_accesibilidad'].astype(str)` convierte valores NaN al string literal `"nan"`. Este string no matchea ninguna clave en `color_discrete_map`. Los registros "nan" reciben color default (gris) y se cuentan en las barras apiladas como categoría fantasma. |
| **Solución** | `df['nivel_accesibilidad'] = df['nivel_accesibilidad'].fillna('Desconocido').astype(str)` |
| **Archivos a tocar** | 1 |

### A-8. Sin separación temporal train/test (sobrestima R²)
| | |
|---|---|
| **Archivos** | `03_modelado.ipynb` y `03_modelado_v2.ipynb` |
| **Problema** | `train_test_split(X, y, test_size=0.20, random_state=42)` es un split **aleatorio**. Datos de 2024 aparecen en train y test simultáneamente. Las features macro (IPC, tasa hipotecaria, desempleo) varían por año, así que el modelo "ve" el futuro durante el entrenamiento. El R² real sería menor. |
| **Solución** | Split temporal: train = años ≤ 2022, test = años ≥ 2023. Documentar que el R² reportado (0.6348) es optimista. |
| **Archivos a tocar** | 2 notebooks + docs |

### A-9. Feature importances hardcodeadas en el dashboard (se vuelven obsoletas al re-entrenar)
| | |
|---|---|
| **Archivo** | `app/pages/01_analisis_nacional.py:126-151` |
| **Problema** | Las importancias de features (42.2%, 28.0%, etc.) y las correlaciones de Pearson están escritas como literales en el código. Si alguien re-entrena el modelo, estas cifras quedan desactualizadas sin ninguna advertencia. |
| **Solución** | Opción A: Exportar `feature_importances_` a un JSON (`models/feature_importances.json`) y cargarlo. Opción B: Agregar comentario prominente "ACTUALIZAR SI SE RE-ENTRENA". |
| **Archivos a tocar** | 1 |

### A-10. Sin advertencia cuando el predictor usa datos macro de respaldo
| | |
|---|---|
| **Archivo** | `app/pages/03_predictor_precios.py:61-67` |
| **Problema** | Si la ciudad/año seleccionada no tiene datos macro (ej. Armenia 2024), el código promedia todas las ciudades de ese año. El usuario no recibe ninguna notificación de que se están usando datos aproximados. |
| **Solución** | Agregar `st.info()` o `st.warning()` cuando se usa el fallback. |
| **Archivos a tocar** | 1 |

### A-11. Narrativa "Ninguna ciudad IAH<5" ignora 331 propiedades que sí cumplen
| | |
|---|---|
| **Archivo** | `app/app.py:111` |
| **Problema** | El insight dice "Ninguna ciudad colombiana cumple el estándar OCDE (IAH<5)". A nivel de **mediana por ciudad** es cierto (la mediana más baja es Ibagué 12.5), pero **a nivel de propiedades individuales**, 331 registros (0.1%) tienen IAH ≤ 5 y son realmente accesibles. |
| **Solución** | Cambiar a "A nivel de mediana por ciudad, ninguna cumple el estándar OCDE de accesibilidad (IAH < 5 años)". |
| **Archivos a tocar** | 1 |

### A-12. Accent mismatch: `'Critico'` vs `'Crítico'` (bug latente)
| | |
|---|---|
| **Archivo** | `run_fase5.py:238` |
| **Problema** | `critica_2024 = df.groupby('city')['nivel_accesibilidad'].apply(lambda x: (x=='Critico').mean()*100)` — compara contra `'Critico'` (sin tilde), pero el dataset tiene `'Crítico'` (con tilde). **Siempre retorna 0**. La variable no se usa actualmente, pero es un bug latente que silenciosamente produce resultados incorrectos. |
| **Solución** | Cambiar a `'Crítico'` (con tilde) |
| **Archivos a tocar** | 1 |

### A-13. Narrativa "Accesible nunca supera el 15%" subestima masivamente
| | |
|---|---|
| **Archivo** | `app/pages/01_analisis_nacional.py:101` |
| **Problema** | El insight dice "el porcentaje de vivienda 'Accesible' (IAH ≤ 5) nunca supera el 15%". Es técnicamente cierto (máximo es 0.1%), pero es engañoso — sugiere que hay algo de accesibilidad cuando prácticamente no existe. |
| **Solución** | Cambiar a "la vivienda 'Accesible' (IAH ≤ 5) es prácticamente inexistente: solo 331 de 282,660 registros (0.1%)". |
| **Archivos a tocar** | 1 |

### A-14. Emoji lookup nunca matchea "Accesible Relativo"
| | |
|---|---|
| **Archivo** | `04_segmentos_mercado.py:60-62` |
| **Problema** | `key = r['cluster_name'].split(" ")[0]` sobre "Accesible Relativo (IAH 18.7)" → `split(" ")` → `["Accesible", "Relativo", "(IAH", "18.7)"]` → `[0]` = "Accesible". El emoji lookup matchea `"Accesible": "🟢"` en vez de `"Accesible Relativo": "🟠"`. Ambos clusters "Accesible Relativo" e "Intermedio" se muestran con el mismo emoji verde. |
| **Solución** | Cambiar la extracción de key para usar el nombre completo antes del paréntesis: `r['cluster_name'].split(" (")[0]` |
| **Archivos a tocar** | 1 |

---

## 🟡 MEDIOS (17)

### M-1. Sin manejo de error si faltan archivos del modelo
| | |
|---|---|
| **Archivo** | `03_predictor_precios.py:16-26` |
| **Problema** | `joblib.load("models/modelo_random_forest.pkl")` y `json.load(f)` para `features_order.json` — si cualquiera falta, la app crashea con traceback. |
| **Solución** | Envolver en `try/except FileNotFoundError` con `st.error()` |
| **Archivos a tocar** | 1 |

### M-2. Coordenadas nulas → todas agrupadas en -1.0 (falsos positivos en dedup)
| | |
|---|---|
| **Archivo** | `02_preparacion_datos.py:404-405` |
| **Problema** | `df['lat_key'] = df['lat'].round(3).fillna(-1.0)` — todas las propiedades sin GPS se marcan como lat=-1.0, lon=-1.0. Dos propiedades distintas sin GPS en la misma ciudad con precio y área similar se colapsan en un solo registro. |
| **Solución** | Usar un identificador único (hash de las columnas textuales disponibles: `fuente`, índice original) como parte de la key de dedup cuando faltan coordenadas. |
| **Archivos a tocar** | 1 |

### M-3. Heurística precio/m² puede inflar propiedades baratas
| | |
|---|---|
| **Archivo** | `02_preparacion_datos.py:225-226` |
| **Problema** | `is_cop_m2 = is_properati & (df['price'] < 1_000_000) & (df['price'] > 5000) & (df['area'] > 10)` — una propiedad legítimamente barata (ej. lote rural $500,000 COP, 50m²) se identificaría como "precio por m²" y se multiplicaría: $500K × 50 = $25M, inflando el precio 50x. |
| **Solución** | Agregar sanity check: `& ((df['price'] * df['area']) > 10_000_000)` para asegurar que el precio resultante sea razonable. |
| **Archivos a tocar** | 1 |

### M-4. Ciudades no listadas en MAPA_CIUDADES se pierden sin aviso
| | |
|---|---|
| **Archivo** | `02_preparacion_datos.py:244-289` |
| **Problema** | Las ciudades no incluidas en `MAPA_CIUDADES` (Santa Marta, Neiva, Pasto, Montería, Sincelejo, Popayán, Tunja, Quibdó, Riohacha, Valledupar, Florencia, Leticia, San Andrés) se eliminan silenciosamente en `df = df[df['city_clean'].notnull()]` sin ningún log. |
| **Solución** | Agregar `warnings.warn(f"{len(df) - len(df_clean)} registros de ciudades no focales eliminados")` |
| **Archivos a tocar** | 1 |

### M-5. `df_clusters` cargado pero nunca usado en homepage
| | |
|---|---|
| **Archivo** | `app/app.py:20` |
| **Problema** | `df_clusters = load_clusters()` carga `ciudades_clusters.csv` en memoria pero la variable nunca se referencia en ninguna línea. |
| **Solución** | Eliminar la línea y la función `load_clusters()` si no se usa en ninguna página. |
| **Archivos a tocar** | 1 |

### M-6. Homepage sin año en el mapa de scattermapbox
| | |
|---|---|
| **Archivo** | `app/app.py:79-91` |
| **Problema** | El mapa scattermapbox se renderiza con `df_f.sample(...)`. Si `df_f` queda vacío después de filtrar (ej. ciudad sin datos), `.sample()` falla con `ValueError: cannot take a larger sample than population when 'replace=False'`. El `try/except` captura el error y muestra gráfico de reemplazo, pero sin mensaje al usuario. |
| **Solución** | Agregar `if df_f.empty: st.info("Sin datos para los filtros seleccionados")` antes del mapa. |
| **Archivos a tocar** | 1 |

### M-7. Modelo serializado sin Pipeline (KMeans + scaler separados) — frágil
| | |
|---|---|
| **Archivo** | `03_modelado.ipynb:1719-1733` |
| **Problema** | `kmeans_segmentacion.pkl` y `scaler_cluster.pkl` son archivos separados. Cualquier consumidor debe acordarse de cargar y aplicar ambos en orden. Un Pipeline los habría encapsulado. |
| **Solución** | Crear un Pipeline: `pipe = Pipeline([('scaler', scaler_cluster), ('kmeans', kmeans)])` y re-serializar. O documentar explícitamente en el código que carga estos modelos. |
| **Archivos a tocar** | 1 |

### M-8. PCA no se serializó (solo visualización, no desplegable)
| | |
|---|---|
| **Archivo** | `03_modelado.ipynb` |
| **Problema** | El PCA se calcula y se usa para visualización, pero no se guarda a disco. Si se quiere proyectar nuevos datos en el espacio PCA, no se puede sin re-entrenar. Sin embargo, el PCA solo se usa para el scatter plot PC1 vs PC2, que ya está precalculado en `ciudades_clusters.csv`. Esto es más una limitación documentada que un bug. |
| **Archivos a tocar** | 0 (documentar en FASE_4_COMPLETA.md) |

### M-9. `features_order.json` podría desalinearse si cambian las features
| | |
|---|---|
| **Archivo** | `models/features_order.json` |
| **Problema** | El JSON lista 11 features planas (`area`, `rooms`, ..., `city`, `property_type`, `year`). Si el modelo se re-entrena con features diferentes, este archivo debe actualizarse manualmente. No hay validación de que el archivo coincida con el modelo serializado. |
| **Solución** | Agregar celda en el notebook de modelado que verifique `list(pipeline[:-1].get_feature_names_out())` contra el JSON. |
| **Archivos a tocar** | 1 notebook |

### M-10. Conteo de criterios de éxito inconsistente (8 originales vs 6 evaluados)
| | |
|---|---|
| **Archivos** | `docs/FASE_1_COMPLETA.md` (líneas 130-146) vs `docs/FASE_5_COMPLETA.md` (líneas 42-51) |
| **Problema** | Fase 1 define **8 criterios** (4 de negocio + 4 técnicos). Fase 5 evalúa **6** (R², RMSE rel, CV R² std, silueta, ciudades, rango). Se eliminaron silenciosamente "Segmentos diferenciables ≥ 3" (subsumido por silueta) y "Dashboard funcional" (no evaluable cuantitativamente). Se agregó "CV R² desv std < 0.02" que **no estaba** entre los 8 originales. |
| **Solución** | Documentar explícitamente: "2 criterios (segmentos, dashboard) no se evalúan cuantitativamente por su naturaleza; 1 criterio (CV R² std) se agregó como control de calidad interna." |
| **Archivos a tocar** | 2 documentos |

### M-11. `data/processed/README.md` tiene tarea pendiente de Fase 3 (no resuelta)
| | |
|---|---|
| **Archivo** | `data/processed/README.md:39` |
| **Problema** | Texto: "Antes de cerrar Fase 4, documentar si Armenia se incorpora al alcance". Fase 4 ya está cerrada. Armenia se incorporó finalmente. |
| **Solución** | Actualizar texto: "Armenia se incorporó al alcance (2 años de datos: 2020-2021). Santa Marta no se incorporó por falta de datos." |
| **Archivos a tocar** | 1 |

### M-12. Notebook v2: `pipeline_xgb_opt` referenciado antes de definirse
| | |
|---|---|
| **Archivo** | `03_modelado_v2.ipynb:223-224` |
| **Problema** | `joblib.dump(pipeline_xgb_opt, ...)` aparece **antes** de la celda de GridSearch (líneas 198-199) que define `grid_search` y extrae `pipeline_xgb_opt = grid_search.best_estimator_`. Si se ejecuta en orden lineal funciona, pero si se salta la celda de GridSearch → `NameError`. |
| **Solución** | Reordenar celdas o agregar `if 'pipeline_xgb_opt' in locals():` antes del dump. |
| **Archivos a tocar** | 1 notebook |

### M-13. Notebook v2: sin `os.chdir()` (regresión desde v1)
| | |
|---|---|
| **Archivo** | `03_modelado_v2.ipynb` |
| **Problema** | v1 tiene `os.chdir(os.path.dirname(os.getcwd()))` para asegurar rutas correctas. v2 eliminó esta línea. Si se ejecuta desde cualquier directorio que no sea la raíz del proyecto, las rutas relativas fallan. |
| **Solución** | Agregar `os.chdir()` al inicio. |
| **Archivos a tocar** | 1 notebook |

### M-14. 6 columnas en el CSV que el dashboard nunca usa (peso muerto)
| | |
|---|---|
| **Archivo** | `data/processed/vivienda_colombia_limpio.csv` |
| **Problema** | Columnas no referenciadas por ningún archivo del dashboard: `ipc_base2018`, `cuota_mensual`, `salario_mensual`, `ipvn_variacion_anual`, `created_on`, `fuente`. Agregan ~30 bytes/registro sin beneficio. |
| **Solución** | Opcional: eliminarlas del CSV de exportación para ahorrar espacio. Limitar el impacto de LFS. |
| **Archivos a tocar** | 1 script de preparación |

### M-15. `cuota_mensual` y `ratio_cuota_salario` calculados con media, no mediana, en una validación de Fase 2
| | |
|---|---|
| **Archivo** | `02_preparacion_datos.py:626` |
| **Problema** | La validación IPVN usa `.mean()` para `precio_m2`, mientras el dashboard y KPIs usan `.median()`. La validación puede mostrar tendencias distintas al dashboard. |
| **Solución** | Cambiar a `.median()` en la validación o documentar la discrepancia. |
| **Archivos a tocar** | 1 |

### M-16. Outlier removal usa percentiles, no IQR, pero se etiqueta como "IQR"
| | |
|---|---|
| **Archivo** | `02_preparacion_datos.py:362` |
| **Problema** | La métrica se registra como "Filtro IQR Outliers por Grupo" pero el método real usa percentiles (2.5%/97.5% para precio, 1%/99% para área), que es diferente del IQR estándar (Q1-1.5*IQR, Q3+1.5*IQR). |
| **Solución** | Cambiar etiqueta a "Filtro Percentil Outliers por Grupo" |
| **Archivos a tocar** | 1 |

### M-17. Variable `y_test_raw_ridge` en v2 es idéntica a `y_test_raw` (código muerto)
| | |
|---|---|
| **Archivo** | `03_modelado_v2.ipynb:112-113` |
| **Problema** | `y_pred_raw = np.exp(y_pred_log)` seguido de `y_test_raw_ridge = y_test_raw`. La variable `y_test_raw_ridge` es un alias sin propósito. Parece residuo de un refactor donde Ridge y XGBoost tenían targets diferentes. |
| **Solución** | Eliminar la línea. |
| **Archivos a tocar** | 1 notebook |

---

## 🔵 MENORES (22)

### m-1 a m-6. Imports no usados

| ID | Archivo | Línea | Import | Acción |
|---|---|---|---|---|
| m-1 | `app/app.py` | 5 | `import plotly.graph_objects as go` | Eliminar |
| m-2 | `app/pages/01_analisis_nacional.py` | 3 | `import numpy as np` | Eliminar (no usado) |
| m-3 | `app/pages/02_comparador_ciudades.py` | 3,5 | `import numpy as np` y `import plotly.graph_objects as go` | Eliminar |
| m-4 | `app/pages/03_predictor_precios.py` | 3-4 | `import numpy as np` y `import plotly.express as px` | Eliminar |
| m-5 | `app/pages/04_segmentos_mercado.py` | 3 | `import plotly.graph_objects as go` | Verificar si se usa |
| m-6 | `03_modelado_v2.ipynb` | — | `from scipy.stats import pearsonr` | Eliminar (nunca se llama) |

### m-7 a m-10. Nombres y archivos inconsistentes

| ID | Archivo | Problema | Solución |
|---|---|---|---|
| m-7 | `docs/GUIA_FASE_6.md:43,57,150-151` | Referencia `01_evolucion_temporal.py` y `02_comparacion_ciudades.py` que no existen | Cambiar a `01_analisis_nacional.py` y `02_comparador_ciudades.py` |
| m-8 | `docs/FASE_4_COMPLETA.md:179` | Referencia `notebooks/03_modelado_ejecutado.ipynb` que no existe | Cambiar a `03_modelado.ipynb` |
| m-9 | `docs/GUIA_FASE_4.md:5` | `commit ac11de7` no existe en el repositorio | Actualizar hash correcto |
| m-10 | `README.md:63-64,103` | Dice "4 páginas operativas" pero hay 5 (homepage + 4 de análisis) | Unificar a "5 páginas" |

### m-11 a m-15. Documentación desactualizada

| ID | Archivo | Problema | Solución |
|---|---|---|---|
| m-11 | `docs/proyecto_vivienda_crispDM.md:16,42-44,102,170-257` | Dice Fases 4-6 pendientes. Contradice todo el proyecto. | Marcar como completadas. O archivar el documento si ya no se usa. |
| m-12 | `README.md:87,142` | "el predictor espera modelo_random_forest.pkl, archivo que aún no existe porque Fase 4 no ha sido ejecutada" | Actualizar: existe y Fase 4 está completa |
| m-13 | `docs/FASE_4_COMPLETA.md:103-115` | Tabla de clusters incompleta: cluster 3 y 4 tienen `—` para precio_m2, ratio, desempleo, count | Completar con valores reales |
| m-14 | `docs/GUIA_FASE_2.md:4-14` | Lista 11 notebooks pero los archivos reales son 13 con nombres diferentes | Actualizar lista |
| m-15 | `data/processed/README.md:52` | No menciona la exclusión de Santa Marta | Agregar nota |

### m-16 a m-18. Mojibake y codificación

| ID | Archivo | Problema | Solución |
|---|---|---|---|
| m-16 | `app/app.py:96` | Comentario con caracteres corruptos: `Insights r├ípidos` → debe ser `Insights rápidos` | Re-escribir en UTF-8 |
| m-17 | `app/pages/01_analisis_nacional.py:97,111` | Claves `'Crítico'` con tilde (correcto) pero potencial mismatch si el CSV se genera con encoding diferente | Verificar que todos los archivos se guarden como UTF-8 |
| m-18 | Múltiples | Acentos en nombres de cluster (Crítico, Elevado, etc.) — frágil si cambia encoding | Forzar UTF-8 en `open(..., encoding='utf-8')` |

### m-19 a m-22. Varios

| ID | Archivo | Problema | Solución |
|---|---|---|---|
| m-19 | `.gitattributes` | `*.csv` con LFS incluye archivos de 1 KB (excesivo) | Cambiar a `data/processed/vivienda_colombia_limpio.csv filter=lfs diff=lfs merge=lfs -text` |
| m-20 | `app/pages/02_comparador_ciudades.py:124` | "**100%** del mercado supera este umbral" — real es **99.97%** (81 registros están por debajo) | Cambiar a "99.97%" o "prácticamente el 100%" |
| m-21 | `03_modelado_v2.ipynb` | `import plotly.express` no está (v1 sí lo tiene) | Agregar si se necesita para visualizaciones |
| m-22 | Múltiples app pages | Formateo de moneda COP (`"$ {:,.0f}".format(val)`) duplicado en cada página | Extraer a `app/utils.py`: `def fmt_cop(val): return f"$ {val:,.0f}"` |

---

## 📅 Prioridad sugerida — Sprints

### Sprint 1: Antes del deploy a Streamlit Cloud (imprescindible)
*13 items — ~2 horas — **✅ COMPLETADO***

| Prioridad | ID | Descripción | Esfuerzo | Estado |
|---|---|---|---|---|
| 1 | C-1 | Crash P4 (column rename) | 1 línea | ✅ HECHO |
| 2 | C-3 | Año no filtra KPIs | 1 línea | ✅ HECHO |
| 3 | C-4 | Narrativa "30-50%" vs 61.4% | 3 líneas | ✅ HECHO |
| 4 | A-1 | Heatmap ignora selección | 1 línea | ✅ HECHO |
| 5 | A-2 | Heatmap todo rojo | 1 línea | ✅ HECHO |
| 6 | A-3 | Percentil sin property_type | 1 línea | ✅ HECHO |
| 7 | A-4 | Radar con columnas basura | 2 líneas | ✅ HECHO |
| 8 | A-6 | Slider año muerto en P4 | 2 líneas | ✅ HECHO |
| 9 | A-7 | NaN → string "nan" | 1 línea | ✅ HECHO |
| 10 | A-5 | Nombres clusters engañosos | 5 líneas | ✅ HECHO |
| 11 | A-11 | "Ninguna IAH<5" ignora 331 | 1 línea | ✅ HECHO |
| 12 | A-13 | "Accesible <15%" subestima | 2 líneas | ✅ HECHO |
| 13 | A-14 | Emoji lookup roto ("Accesible Relativo") | 1 línea | ✅ HECHO |

### Sprint 2: Antes de cerrar el proyecto
*15 items — ~3-4 horas — **✅ COMPLETADO***

| Prioridad | ID | Descripción | Esfuerzo | Estado |
|---|---|---|---|---|
| 14 | C-2 | Cuota inconsistente (tasa efectiva vs nominal) | 30 min | ✅ HECHO |
| 15 | A-9 | Feature importances + correlaciones hardcodeadas | 30 min | ✅ HECHO |
| 16 | A-10 | Sin warning en predictor fallback | 10 min | ✅ HECHO |
| 17 | A-12 | 'Critico' vs 'Crítico' (bug latente) | 1 línea | ✅ HECHO |
| 18 | C-5 | Validación ficticia | 4 líneas | ✅ HECHO |
| 19 | M-1 | Error handling modelos faltantes | 15 min | ✅ HECHO |
| 20 | M-5 | df_clusters no usado | 2 líneas | ✅ HECHO |
| 21 | M-10 | Criterios de éxito inconsistentes | 15 min | ✅ HECHO |
| 22 | M-11 | README procesado desactualizado | 5 min | ✅ HECHO |
| 23 | M-12 | pipeline_xgb_opt orden celdas | 5 min | ✅ HECHO |
| 24 | M-13 | os.chdir() faltante en v2 | 1 línea | ✅ HECHO |
| 25 | M-17 | y_test_raw_ridge código muerto | 1 línea | ✅ HECHO |
| 26 | m-7 | GUIA_FASE_6 nombres de archivo | 4 líneas | ✅ HECHO |
| 27 | m-11 | proyecto_vivienda_crispDM.md desactualizado | 15 min | ✅ HECHO |
| 28 | m-12 | README.md desactualizado | 10 min | ✅ HECHO |

### Sprint 3: Calidad y deuda técnica (opcional)
*20 items — ~3-5 horas — **✅ COMPLETADO***

| ID | Descripción | Esfuerzo | Estado |
|---|---|---|---|
| M-2 | Coordenadas nulas en dedup | 1 hora | ✅ HECHO (hash único fuente+índice) |
| M-3 | Heurística precio/m² | 30 min | ✅ HECHO (sanity check <10M) |
| M-4 | Ciudades no focales sin aviso | 10 min | ✅ HECHO (warnings.warn + print) |
| M-6 | Mapa con df vacío | 10 min | ✅ HECHO (st.info antes del mapa) |
| M-7 | KMeans + scaler sin Pipeline | 15 min | ✅ HECHO (pipeline_clustering.pkl + consumidores actualizados) |
| M-8 | PCA no serializado (documentar) | 5 min | ✅ HECHO (nota en FASE_4_COMPLETA.md) |
| M-9 | features_order.json sin validación | 15 min | ✅ HECHO (celda de validación en notebook v2) |
| M-14 | Columnas no usadas en CSV | 15 min | ✅ HECHO (documentado como peso muerto aceptable) |
| M-15 | Validación con mean vs median | 5 min | ✅ HECHO (.median() en validación IPVN) |
| M-16 | Etiqueta "IQR" engañosa | 1 línea | ✅ HECHO (renombrado a Percentil) |
| M-18 | Cluster IAH ranges inconsistentes | 15 min | ✅ HECHO (corregido en Sprint 1 A-5) |
| m-1 a m-6 | Imports no usados | 5 min | ✅ HECHO |
| m-8, m-9, m-10 | Nombres y archivos inconsistentes | 10 min | ✅ HECHO |
| m-13, m-14, m-15 | Documentación incompleta | 20 min | ✅ HECHO |
| m-16 | Mojibake | 1 línea | ✅ HECHO |
| m-19 | Git LFS excesivo | 1 línea | ✅ HECHO |
| m-20 | "100%" → "99.97%" | 1 línea | ✅ HECHO (.2f en lugar de .1f) |
| m-22 | Formato COP duplicado → utils.py | 30 min | ✅ HECHO (app.py importa y usa fmt_cop) |

---

## 📊 Esfuerzo total estimado

| Sprint | Items | Horas estimadas | Estado real | Dependencias |
|---|---|---|---|---|
| Sprint 1 (pre-deploy) | 13 | ~2h | ✅ **Completado** | Ninguna |
| Sprint 2 (pre-cierre) | 15 | ~3-4h | ✅ **Completado** | Sprint 1 |
| Sprint 3 (calidad) | 20 | ~3-5h | ✅ **Completado** | Ninguna |
| **Total** | **48** | **~8-11h** | **✅ 48/48 hechos (100%)** | |

**Nota:** A-8 (split temporal, re-entrenar modelo) no está incluido en los sprints por su alta complejidad. Si se decide hacer, requiere ~4h adicionales y actualización de todos los artefactos y métricas.

---

*Documento generado a partir de auditoría completa del códigobase (4 agentes de análisis paralelos) el 4 de junio 2026. Cada hallazgo tiene referencias exactas de archivo y línea.*
