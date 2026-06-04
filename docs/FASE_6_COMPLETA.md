# Fase 6 — Despliegue

## Proyecto: Accesibilidad de Vivienda en Colombia · CRISP-DM 2026-I

**Responsable principal:** Kukis · **Apoyo:** Sofía  
**Estado:** ⏳ Pendiente — requiere Fases 4 y 5 completadas  
**Semanas planificadas:** 11-12

---

## Resumen Ejecutivo

Esta fase **no ha sido ejecutada ni validada como despliegue final**. El repositorio contiene una base de aplicación Streamlit en `app/`, pero no existen modelos entrenados en `models/`, no hay URL de producción verificada y no se han documentado pruebas completas de funcionamiento.

Este documento es una plantilla para completar cuando el dashboard esté integrado con artefactos reales de Fase 4 y aprobado por la evaluación de Fase 5.

---

## Contexto dentro de CRISP-DM

| Relación en el ciclo | Descripción |
|---|---|
| Entrada requerida | Modelos, clusters, métricas y conclusiones aprobadas en Fase 5. |
| Rol de Fase 6 | Convertir resultados validados en una aplicación usable y documentada. |
| Salida final | Dashboard desplegado, probado y documentado para usuarios no técnicos. |

---

## Objetivos de la Fase

1. Integrar el dataset procesado, modelos y tablas de evaluación en una app Streamlit.
2. Exponer vistas para análisis nacional, comparación de ciudades, predictor y segmentos.
3. Validar funcionalidad local y en despliegue.
4. Documentar URL pública, limitaciones, instrucciones de uso y mantenimiento.
5. Actualizar README solo cuando el despliegue exista y haya sido probado.

---

## Alcance Planificado

| Componente | Estado actual | Resultado esperado |
|---|---|---|
| Estructura `app/` | ⚠️ Base existente | Validar y ajustar tras Fase 4/Fase 5. |
| Página principal | ⚠️ Base existente | KPIs coherentes con resultados evaluados. |
| Análisis nacional | ⚠️ Base existente | Gráficas validadas con dataset saneado. |
| Comparador de ciudades | ⚠️ Base existente | Comparación robusta por ciudad/año/tipo. |
| Predictor de precios | ⏳ Pendiente | Requiere modelo serializado de Fase 4. |
| Segmentos de mercado | ⏳ Pendiente | Requiere clusters exportados de Fase 4. |
| Pruebas locales | `[PENDIENTE]` | Evidencia de navegación sin errores. |
| Despliegue Streamlit Cloud | `[PENDIENTE]` | URL pública funcional. |

---

## Actividades por Realizar

1. Confirmar que Fase 5 aprobó o condicionó el despliegue.
2. Verificar que todos los artefactos requeridos existen.
3. Cargar el dataset validado de Fase 3 y confirmar que la decisión Armenia/Santa Marta ya esté documentada.
4. Alinear ciudades de la app con las 12 ciudades focales de Fase 1.
5. Integrar modelo de regresión real en el predictor.
6. Integrar tabla de clusters real en la vista de segmentos.
7. Revisar textos de la app para no presentar métricas pendientes como resultados.
8. Ejecutar pruebas locales completas.
9. Desplegar en Streamlit Community Cloud.
10. Registrar URL pública y evidencias de prueba.
11. Actualizar `README.md` y este documento con datos reales.

---

## Correspondencia con GUIA_FASE_6.md

| Actividad planificada | Estado | Evidencia requerida |
|---|---|---|
| Estructura del proyecto y setup | ⚠️ Parcial | `app/` existe, pero falta validación completa. |
| Página principal | ⚠️ Parcial | Debe validarse contra dataset saneado. |
| Página análisis nacional | ⚠️ Parcial | Debe validarse contra métricas finales. |
| Página comparador de ciudades | ⚠️ Parcial | Debe alinearse con 12 ciudades focales. |
| Página predictor de precios | ⏳ Pendiente | Requiere `models/modelo_random_forest.pkl` o modelo elegido. |
| Página segmentos de mercado | ⏳ Pendiente | Requiere `ciudades_clusters.csv` y perfiles. |
| Pruebas locales completas | ⏳ Pendiente | Registro de pruebas manuales. |
| Despliegue Streamlit Cloud | ⏳ Pendiente | URL pública probada. |
| Preparación para presentación | ⏳ Pendiente | Demo y notas finales. |

---

## Metodología a Aplicar

### Validación funcional

| Área | Criterio de aceptación |
|---|---|
| Carga de datos | La app carga dataset saneado sin errores ni marcadores de conflicto. |
| Predictor | El modelo se carga y genera predicciones reproducibles. |
| Segmentos | La vista usa clusters reales y no valores de ejemplo. |
| Filtros | Ciudad, año y tipo funcionan sin romper visualizaciones. |
| Performance | La app carga en tiempo razonable con cache donde aplique. |
| Mensajes | La interfaz distingue resultados reales de estados pendientes. |

### Validación de despliegue

| Área | Criterio de aceptación |
|---|---|
| Build | Streamlit Cloud instala dependencias sin errores. |
| Navegación | Todas las páginas cargan en producción. |
| Datos/modelos | Las rutas relativas funcionan en cloud. |
| Documentación | README contiene URL real solo después de probarla. |

---

## Resultados Obtenidos

| Resultado | Valor |
|---|---|
| URL pública | `[PENDIENTE]` |
| Fecha de despliegue | `[PENDIENTE]` |
| Rama desplegada | `[PENDIENTE]` |
| Commit desplegado | `[PENDIENTE]` |
| Modelo usado por predictor | `[PENDIENTE]` |
| Dataset usado por app | `[PENDIENTE]` |
| Archivo de clusters usado | `[PENDIENTE]` |
| Estado de pruebas locales | `[PENDIENTE]` |
| Estado de pruebas en producción | `[PENDIENTE]` |

---

## Métricas y Estadísticas Relevantes

| Métrica de operación | Valor |
|---|---|
| Tiempo de carga inicial | `[PENDIENTE]` |
| Páginas probadas | `[PENDIENTE]` |
| Errores en consola local | `[PENDIENTE]` |
| Errores en logs de Streamlit Cloud | `[PENDIENTE]` |
| Casos de prueba del predictor | `[PENDIENTE]` |
| Casos de prueba de filtros | `[PENDIENTE]` |

---

## Hallazgos Clave

| Hallazgo | Evidencia |
|---|---|
| `[PENDIENTE]` | `[PENDIENTE — completar solo tras pruebas reales]` |

---

## Problemas Encontrados y Resolución

| Problema | Estado | Resolución esperada |
|---|---|---|
| No existe modelo serializado | ⏳ Pendiente | Ejecutar Fase 4. |
| No existen clusters exportados | ⏳ Pendiente | Ejecutar Fase 4. |
| Fase 5 no ha aprobado despliegue | ⏳ Pendiente | Ejecutar evaluación. |
| Alcance de ciudades difiere de Fase 1 | ⏳ Pendiente | Decidir si la app muestra Armenia o si se regenera el dataset con Santa Marta. |
| Lista de ciudades en app puede no coincidir con Fase 1 | ⏳ Pendiente | Alinear con Bogotá, Medellín, Cali, Barranquilla, Bucaramanga, Cartagena, Pereira, Cúcuta, Manizales, Ibagué, Santa Marta y Villavicencio. |

---

## Validaciones Realizadas

| Validación | Estado |
|---|---|
| `streamlit run app/app.py` ejecutado localmente | `[PENDIENTE]` |
| Página principal probada | `[PENDIENTE]` |
| Análisis nacional probado | `[PENDIENTE]` |
| Comparador probado | `[PENDIENTE]` |
| Predictor probado con modelo real | `[PENDIENTE]` |
| Segmentos probado con clusters reales | `[PENDIENTE]` |
| Despliegue cloud probado | `[PENDIENTE]` |
| URL agregada al README | `[PENDIENTE]` |

---

## Entregables Esperados

| Entregable | Ruta/URL esperada | Estado |
|---|---|---|
| Página principal | `app/app.py` | ⚠️ Base existente |
| Análisis nacional | `app/pages/01_analisis_nacional.py` | ⚠️ Base existente |
| Comparador de ciudades | `app/pages/02_comparador_ciudades.py` | ⚠️ Base existente |
| Predictor de precios | `app/pages/03_predictor_precios.py` | ⚠️ Base existente, requiere modelo |
| Segmentos de mercado | `app/pages/04_segmentos_mercado.py` | ⚠️ Base existente, requiere clusters |
| Configuración Streamlit | `.streamlit/config.toml` | ⚠️ Base existente |
| Dashboard público | `[PENDIENTE — URL Streamlit]` | ⏳ Pendiente |
| Reporte de Fase 6 completado | `docs/FASE_6_COMPLETA.md` | ⏳ Pendiente |

---

## Riesgos o Limitaciones Detectadas

1. No publicar URL ni métricas de dashboard hasta completar pruebas reales.
2. No mostrar predictor como funcional si el modelo no existe.
3. No presentar segmentos si no existen clusters exportados.
4. No presentar la lista de ciudades como equivalente a Fase 1 si se mantiene Armenia y se excluye Santa Marta.
5. Alinear nombres de ciudades en todos los componentes antes del despliegue.

---

## Conclusiones

`[PENDIENTE — redactar únicamente después de validar la app localmente y en producción]`

---

## Preparación para Cierre del Proyecto

Para cerrar Fase 6, el equipo debe entregar:

1. URL pública funcional.
2. Registro de pruebas locales y cloud.
3. README actualizado con estado real.
4. Documento de Fase 6 con evidencia de despliegue.
5. Demo preparada para jurado.
6. Limitaciones operativas del dashboard documentadas.

---

*Plantilla de Fase 6 · CRISP-DM 2026-I · Accesibilidad Habitacional Colombia*
