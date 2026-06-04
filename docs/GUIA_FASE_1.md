# Fase 1 — Comprensión del Negocio
## Estado: ✅ COMPLETADA
**Responsable:** Steve · **Apoyo:** Sofía, Kukis
**Documento generado:**
- `docs/FASE_1_COMPLETA.md` — Documentación completa de Fase 1

---

## Sección 1: Contexto y Justificación del Negocio
**Documentar el problema de negocio**
- [x] Investigar el déficit habitacional cuantitativo en Colombia (cifras DANE)
- [x] Documentar la evolución del precio de vivienda vs salario mínimo real
- [x] Identificar el Price-to-Income Ratio (PIR) como estándar internacional de referencia
- [x] Recopilar datos de incrementos de precios por ciudad (Bogotá, Medellín, Barranquilla, Cúcuta)
- [x] Redactar la justificación del proyecto con citas de fuentes oficiales

---

## Sección 2: Pregunta Central y Preguntas Derivadas
**Definir las preguntas de investigación**
- [x] Formular la pregunta central sobre evolución de accesibilidad habitacional (2019–2024)
- [x] Derivar 4 preguntas secundarias específicas y medibles:
  - [x] Años de salario mínimo por ciudad y evolución temporal
  - [x] Variables con mayor poder predictivo sobre el precio
  - [x] Clasificación de mercados mediante clustering no supervisado
  - [x] Ciudades donde la cuota hipotecaria supera el 30% del ingreso mínimo
- [x] Validar que cada pregunta sea respondible con los datos disponibles

---

## Sección 3: Objetivos del Proyecto
**Establecer objetivos general y específicos**
- [x] Redactar objetivo general alineado con la pregunta central
- [x] Definir 4 objetivos específicos:
  - [x] Construir y validar el Índice de Accesibilidad Habitacional (IAH)
  - [x] Entrenar modelos de regresión para predicción de precios
  - [x] Segmentar mercados mediante clustering no supervisado
  - [x] Desplegar resultados en dashboard interactivo (Streamlit)
- [x] Verificar que los objetivos sean evaluables (SMART)

---

## Sección 4: Alcance Geográfico
**Definir la cobertura espacial del proyecto**
- [x] Nivel 1: Análisis nacional (macroeconómico, IAH nacional)
- [x] Nivel 2: Identificar 12 ciudades focales con justificación
- [x] Clasificar ciudades por tamaño y región
- [x] Establecer umbral mínimo de registros por ciudad (≥500)
- [x] Documentar la estrategia de cobertura y su justificación demográfica

---

## Sección 5: Criterios de Éxito
**Definir métricas de evaluación del proyecto**
- [x] Especificar 8 criterios de éxito con métricas cuantitativas:
  - [x] RMSE relativo < 15%
  - [x] R² ≥ 0,75
  - [x] Coeficiente de silueta ≥ 0,45
  - [x] Mínimo 3 clusters diferenciables
  - [x] Cobertura ≥ 8 ciudades con análisis completo
  - [x] Cobertura temporal 2019–2024
  - [x] Dashboard funcional con filtros
  - [x] 4 de 4 preguntas respondidas con evidencia
- [x] Definir umbrales mínimos aceptables para cada métrica

---

## Sección 6: Identificación de Stakeholders
**Mapear los actores involucrados**
- [x] Identificar jurado/profesor como stakeholder principal
- [x] Identificar potencial comprador de vivienda como usuario final
- [x] Identificar investigadores/tomadores de decisión pública
- [x] Identificar entidades financieras/sector inmobiliario
- [x] Documentar qué busca cada stakeholder y cómo impacta el proyecto

---

## Sección 7: Supuestos y Restricciones
**Documentar limitaciones del proyecto**
- [x] Supuesto: datos de Kaggle representan mercado formal urbano digital
- [x] Supuesto: salario mínimo como proxy del ingreso de referencia
- [x] Supuesto: exclusión de ciudades con <500 registros
- [x] Restricción: dataset A1 cubre solo hasta 2021
- [x] Restricción: sin datos catastrales georreferenciados
- [x] Restricción: solo vivienda urbana, no rural
- [x] Restricción: solo transacciones listadas en plataformas digitales

---

## Sección 8: Inventario de Herramientas
**Confirmar el stack tecnológico**
- [x] Python + Jupyter/Google Colab confirmados
- [x] pandas, numpy, matplotlib, seaborn, plotly disponibles
- [x] scikit-learn confirmado (Random Forest, Ridge, KMeans, DBSCAN)
- [x] Streamlit disponible para dashboard
- [x] GitHub configurado con ramas por fase
- [x] Kaggle API configurada (token `kaggle.json`)

---

## Sección 9: Inventario de Datasets
**Identificar todas las fuentes de datos**
- [x] Grupo A: identificar 8 datasets de precios de vivienda (A1–A8)
- [x] Verificar URLs y disponibilidad de cada dataset en Kaggle
- [x] Grupo B: identificar 8 variables macroeconómicas (B1–B8)
- [x] Verificar URLs de fuentes oficiales (DANE, BanRep, Fedesarrollo, IGAC)
- [x] Crear tabla resumen de inventario con 16 archivos CSV documentados
- [x] Documentar tamaño, registros y período de cada dataset

---

## Sección 10: Glosario de Términos Técnicos
**Definir vocabulario especializado del proyecto**
- [x] Definir indicadores económicos: PIR, IAH, SMLMV, Ratio Cuota/Salario
- [x] Definir variables macro: IPVN, IPVU, IPC, TRM, VIS, GEIH, TD
- [x] Definir métricas de evaluación: R², MAE, RMSE, MAPE, Silueta, DBI, VIF, CV
- [x] Definir términos de procesamiento: IQR, CAGR, OHE, UPZ

---

## Sección 11: Análisis Costo-Beneficio
**Evaluar recursos vs valor del proyecto**
- [x] Documentar costos: descarga de datos ($0), scraping ($0), cómputo local ($0), software open source ($0)
- [x] Cuantificar horas-persona (~412 h totales)
- [x] Documentar beneficios por stakeholder (formativos, académicos, sociales, sectoriales)
- [x] Listar entregables concretos del proyecto
- [x] Concluir que el retorno supera la inversión

---

## Sección 12: Identificación de Riesgos
**Documentar y mitigar riesgos del proyecto**
- [x] Identificar mínimo 9 riesgos (R1–R9)
- [x] Asignar probabilidad e impacto a cada riesgo
- [x] Definir estrategia de mitigación concreta por riesgo
- [x] Cubrir: datos incompletos, esquemas dispares, duplicados, desalineación temporal, multicolinealidad, cobertura insuficiente, clusters no diferenciables, memoria, rendimiento

---

## Sección 13: Cronograma del Proyecto
**Planificar las 6 fases CRISP-DM**
- [x] Semanas 1–2: Fase 1 (Comprensión del negocio)
- [x] Semanas 3–4: Fase 2 (Comprensión de los datos)
- [x] Semanas 5–6: Fase 3 (Preparación de los datos)
- [x] Semanas 7–8: Fase 4 (Modelado)
- [x] Semana 9: Fase 5 (Evaluación)
- [x] Semanas 10–11: Fase 6 (Despliegue)
- [x] Semana 12: Preparación presentación final
- [x] Semana 13: Presentación ante jurado
- [x] Asignar responsable por fase

---

## Sección 14: Checklist de Cierre
**Verificar integridad del documento de fase**
- [x] Contexto y justificación con cifras reales documentado
- [x] 1 pregunta central + 4 derivadas redactadas
- [x] 1 objetivo general + 4 específicos definidos
- [x] 8 criterios de éxito con métricas y umbrales
- [x] Alcance geográfico con 12 ciudades focales justificado
- [x] 4 stakeholders identificados con intereses
- [x] Supuestos y restricciones documentados
- [x] Stack tecnológico confirmado
- [x] 16 fuentes de datos verificadas con URLs
- [x] Glosario técnico completo
- [x] Análisis costo-beneficio detallado
- [x] 9 riesgos con mitigaciones
- [x] Cronograma completo (Fases 1–6 + presentación)
- [x] Checklist de cierre con todos los entregables listados
- [ ] Revisión y visto bueno del profesor/jurado (pendiente entrega Semana 2)

---

## Entregables Generados

| Archivo | Ruta |
|---------|------|
| Documento de fase | `docs/FASE_1_COMPLETA.md` |

*Nota: La Fase 1 es una fase de planificación y documentación. No genera notebooks, scripts ni datasets.*
