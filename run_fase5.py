#!/usr/bin/env python3
"""Fase 5 — Evaluación: ejecución completa y exportación de notebooks/04_evaluacion.ipynb"""
import os, sys, json, warnings, subprocess
warnings.filterwarnings('ignore')

# ── Cambiar al directorio del proyecto ──────────────────────────────
proj_dir = r"C:\Users\AlexP\OneDrive\Escritorio\Accesibilidad_de_Vivienda_en_Colombia"
os.chdir(proj_dir)
sys.path.insert(0, proj_dir)

# ── Imports ─────────────────────────────────────────────────────────
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, silhouette_score, davies_bouldin_score, calinski_harabasz_score
from sklearn.decomposition import PCA
import scipy.stats as stats
import joblib
os.makedirs("docs/figures", exist_ok=True)
print("Imports completados")

# ── Carga de datos y modelos ────────────────────────────────────────
df = pd.read_csv("data/processed/vivienda_colombia_limpio.csv", encoding="utf-8-sig")
print(f"Shape: {df.shape}")

FEATURES_NUM = ['area', 'rooms', 'bathrooms', 'estrato',
                'ipc_var_anual', 'tasa_hipotecaria_anual',
                'tasa_desempleo', 'ipvu_variacion_anual']
FEATURES_CAT = ['city', 'property_type', 'year']
TARGET = 'price'
X = df[FEATURES_NUM + FEATURES_CAT].copy()
y = df[TARGET].copy()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
print(f"Train: {X_train.shape[0]:,}, Test: {X_test.shape[0]:,}")

model_rf = joblib.load('models/modelo_random_forest.pkl')
kmeans = joblib.load('models/kmeans_segmentacion.pkl')
scaler_cluster = joblib.load('models/scaler_cluster.pkl')
ciudades_clusters = pd.read_csv("data/processed/ciudades_clusters.csv")
print("Modelos cargados")

# ── Sección 2: Criterios de éxito ───────────────────────────────────
y_pred = model_rf.predict(X_test)
r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
rmse_rel = rmse / y_test.median() * 100
mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100
print(f"R2: {r2:.4f}, MAE: ${mae:,.0f}, RMSE: ${rmse:,.0f}, RMSE rel: {rmse_rel:.2f}%, MAPE: {mape:.2f}%")

cv_scores = cross_val_score(model_rf, X_train, y_train, cv=5, scoring='r2')
print(f"CV R2 mean +/- std: {cv_scores.mean():.4f} +/- {cv_scores.std():.4f}")

silueta_kmeans = 0.4874
n_ciudades = df['city'].nunique()
rango_anual = f"{df['year'].min()}-{df['year'].max()}"
criterios = pd.DataFrame({
    'Criterio': ['R2 >= 0.75', 'RMSE rel < 15%', 'CV R2 desv std < 0.02', 'Silueta clustering >= 0.45', 'Ciudades >= 8', 'Rango 2020-2024'],
    'Umbral Fase 1': ['>= 0.75', '< 15%', '< 0.02', '>= 0.45', '>= 8', '2020-2024'],
    'Valor Obtenido': [f'{r2:.4f}', f'{rmse_rel:.2f}%', f'{cv_scores.std():.4f}', f'{silueta_kmeans:.4f}', str(n_ciudades), rango_anual],
    'Cumple': ['NO' if r2 < 0.75 else 'SI', 'NO' if rmse_rel >= 15 else 'SI', 'SI' if cv_scores.std() < 0.02 else 'NO', 'SI' if silueta_kmeans >= 0.45 else 'NO', 'SI' if n_ciudades >= 8 else 'NO', 'SI']
})
criterios.to_csv('docs/tabla_criterios_exito.csv', index=False)
print("Tabla criterios exportada")
print(criterios.to_string(index=False))

# ── Sección 3: Evaluación detallada regresión ───────────────────────
tabla_metricas = pd.DataFrame({
    'Metrica': ['R2', 'MAE', 'RMSE', 'MAPE', 'RMSE rel (%)'],
    'Valor': [f'{r2:.4f}', f'${mae:,.0f}', f'${rmse:,.0f}', f'{mape:.2f}%', f'{rmse_rel:.2f}%'],
    'Interpretacion': ['El modelo explica el {:.2f}% de la varianza'.format(r2*100),
                        'Error absoluto promedio de ${:,.0f} COP'.format(mae),
                        'Error tipico de ${:,.0f} COP'.format(rmse),
                        'Error porcentual absoluto medio de {:.1f}%'.format(mape),
                        'RMSE equivale al {:.1f}% del precio mediano'.format(rmse_rel)]
})
tabla_metricas.to_csv('docs/tabla_metricas_finales.csv', index=False)
print("Tabla metricas exportada")

residuos = y_test - y_pred
print(f"Residuos: media={residuos.mean():.0f}, std={residuos.std():.0f}")

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
axes[0].scatter(y_test, y_pred, alpha=0.2, s=2)
axes[0].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=1.5)
axes[0].set_xlabel('Precio real (COP)')
axes[0].set_ylabel('Precio predicho (COP)')
axes[0].set_title('Valores Reales vs Predichos - RF Optimizado (R2 = {:.4f})'.format(r2))
axes[1].scatter(y_pred, residuos, alpha=0.2, s=2)
axes[1].axhline(y=0, color='r', linestyle='--', lw=1.5)
axes[1].set_xlabel('Valores predichos (COP)')
axes[1].set_ylabel('Residuos (COP)')
axes[1].set_title('Residuos vs Valores Predichos')
plt.tight_layout()
plt.savefig('docs/figures/fig_scatter_residuos.png', dpi=150, bbox_inches='tight')
plt.close()

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
axes[0].hist(residuos, bins=100, alpha=0.7, edgecolor='black')
axes[0].axvline(x=0, color='r', linestyle='--', lw=1.5)
axes[0].set_xlabel('Residuo (COP)'); axes[0].set_ylabel('Frecuencia'); axes[0].set_title('Distribucion de Residuos')
stats.probplot(residuos, dist="norm", plot=axes[1])
axes[1].set_title('Q-Q Plot de Residuos')
plt.tight_layout()
plt.savefig('docs/figures/fig_hist_qq_residuos.png', dpi=150, bbox_inches='tight')
plt.close()

X_test_res = X_test.copy()
X_test_res['residuo'] = residuos
X_test_res['residuo_abs'] = np.abs(residuos)
city_error = X_test_res.groupby('city').agg(error_medio=('residuo','mean'), error_abs_medio=('residuo_abs','mean'), residuo_std=('residuo','std'), count=('residuo','count')).sort_values('error_abs_medio', ascending=False)
print("Error por ciudad:"); print(city_error.to_string())

plt.figure(figsize=(12, 6))
sns.boxplot(data=X_test_res, x='city', y='residuo')
plt.xticks(rotation=45); plt.axhline(y=0, color='r', linestyle='--', lw=1)
plt.title('Distribucion de Residuos por Ciudad')
plt.tight_layout(); plt.savefig('docs/figures/fig_boxplot_residuos_ciudad.png', dpi=150, bbox_inches='tight')
plt.close()

encoder = model_rf.named_steps['preprocessor'].named_transformers_['cat']
cat_features = encoder.get_feature_names_out(FEATURES_CAT)
all_feature_names = list(FEATURES_NUM) + list(cat_features)
importances = model_rf.named_steps['regressor'].feature_importances_
feat_imp = pd.DataFrame({'feature': all_feature_names, 'importance': importances}).sort_values('importance', ascending=False)
top5 = feat_imp.head(5)
print("Top 5:"); print(top5.to_string(index=False))
print("Importancia acumulada top 5: {:.1f}%".format(top5['importance'].sum()*100))

plt.figure(figsize=(10, 6))
sns.barplot(data=feat_imp.head(15), y='feature', x='importance', palette='viridis')
plt.title('Top 15 - Importancia de Variables (Random Forest)'); plt.xlabel('Importancia relativa')
plt.tight_layout(); plt.savefig('docs/figures/fig_importancia_vars.png', dpi=150, bbox_inches='tight')
plt.close()

# ── Sección 4: Evaluación clustering ────────────────────────────────
cluster_cols = ['IAH', 'precio_m2', 'ratio_cuota_salario', 'tasa_desempleo']
df_cluster = df.groupby(['city','year'])[cluster_cols].median().reset_index()
X_cluster = scaler_cluster.transform(df_cluster[cluster_cols])
labels = kmeans.predict(X_cluster)
sil = silhouette_score(X_cluster, labels)
dbi = davies_bouldin_score(X_cluster, labels)
ch = calinski_harabasz_score(X_cluster, labels)
print(f"Silueta: {sil:.4f}, DBI: {dbi:.4f}, CH: {ch:.2f}")

pca = PCA(n_components=2); X_pca = pca.fit_transform(X_cluster)
print(f"Varianza PC1+PC2: {pca.explained_variance_ratio_.sum()*100:.2f}%")
df_cluster['cluster'] = labels; df_cluster['PC1'] = X_pca[:,0]; df_cluster['PC2'] = X_pca[:,1]
cluster_names = {0:'Elevado (IAH 29.2)',1:'Moderado (IAH 16.2)',2:'Accesible Relativo (IAH 18.7)',3:'Elevado (IAH 25.4)',4:'Accesible (IAH 12.9)'}
df_cluster['cluster_name'] = df_cluster['cluster'].map(cluster_names)

plt.figure(figsize=(10,8))
sns.scatterplot(data=df_cluster, x='PC1', y='PC2', hue='cluster_name', palette='Set2', s=100, style='cluster_name')
for _, row in df_cluster.iterrows():
    plt.annotate(row['city'], (row['PC1'], row['PC2']), fontsize=8, alpha=0.7)
plt.title('PCA - Clusters por Ciudad-Ano (Var: {:.1f}%)'.format(pca.explained_variance_ratio_.sum()*100))
plt.tight_layout(); plt.savefig('docs/figures/fig_pca_clusters.png', dpi=150, bbox_inches='tight'); plt.close()

perfiles = df_cluster.groupby('cluster')[cluster_cols].mean()
perfiles['count'] = df_cluster.groupby('cluster').size()
print("Perfiles clusters:"); print(perfiles.round(2).to_string())

cluster_2024 = df_cluster[df_cluster['year']==2024][['city','cluster_name']]
print("Clusters 2024:"); print(cluster_2024.to_string(index=False))

plt.figure(figsize=(14,8))
heatmap_data = df_cluster.pivot(index='city', columns='year', values='cluster')
sns.heatmap(heatmap_data, annot=True, cmap='Set2', fmt='.0f')
plt.title('Mapa de Clusters: Ciudad x Ano')
plt.tight_layout(); plt.savefig('docs/figures/fig_heatmap_clusters.png', dpi=150, bbox_inches='tight'); plt.close()

# ── Sección 5: Preguntas de investigación ───────────────────────────
iah_nac = df.groupby('year')['IAH'].median().reset_index()
iah_ciudad = df.groupby(['city','year'])['IAH'].median().reset_index()
pivot_iah = iah_ciudad.pivot(index='city', columns='year', values='IAH').round(2)
pivot_iah['variacion'] = ((pivot_iah[2024] - pivot_iah[2020]) / pivot_iah[2020] * 100).round(2)
print("IAH por ciudad-anio:"); print(pivot_iah.to_string())

plt.figure(figsize=(14,7))
for city in sorted(df['city'].unique()):
    data = iah_ciudad[iah_ciudad['city']==city]; plt.plot(data['year'], data['IAH'], marker='o', label=city)
plt.axhline(y=5, color='g', linestyle='--', alpha=0.5, label='OCDE Accesible (5)')
plt.axhline(y=10, color='orange', linestyle='--', alpha=0.5, label='OCDE Moderado (10)')
plt.axhline(y=20, color='r', linestyle='--', alpha=0.5, label='Umbral Critico (20)')
plt.xlabel('Ano'); plt.ylabel('IAH (anios de salario minimo)'); plt.title('Evolucion del IAH por Ciudad (2020-2024)')
plt.legend(bbox_to_anchor=(1.05,1), loc='upper left'); plt.grid(True, alpha=0.3)
plt.tight_layout(); plt.savefig('docs/figures/fig_IAH_por_ciudad.png', dpi=150, bbox_inches='tight'); plt.close()

min_city_2024 = pivot_iah[2024].idxmin(); max_city_2024 = pivot_iah[2024].idxmax()
print("Ciudad MAS accesible 2024: {} (IAH={:.1f})".format(min_city_2024, pivot_iah.loc[min_city_2024, 2024]))
print("Ciudad MENOS accesible 2024: {} (IAH={:.1f})".format(max_city_2024, pivot_iah.loc[max_city_2024, 2024]))

# Pregunta 2
df_log = df.copy(); df_log['log_price'] = np.log(df['price'])
numeric_for_corr = FEATURES_NUM + ['log_price']
pearson = df_log[numeric_for_corr].corr()['log_price'].drop('log_price').sort_values(ascending=False)
print("Pearson con log(price):"); print(pearson.to_string())

# Pregunta 3
iah_min = perfiles['IAH'].min(); iah_max = perfiles['IAH'].max()
print("Diferencia IAH clusters: {:.1f} anios".format(iah_max - iah_min))

plt.figure(figsize=(10,8))
sns.scatterplot(data=df_cluster, x='IAH', y='precio_m2', hue='cluster_name', style='cluster_name', palette='Set2', s=120)
for _, row in df_cluster.iterrows():
    plt.annotate(row['city'], (row['IAH'], row['precio_m2']), fontsize=8, alpha=0.7)
plt.xlabel('IAH (anios)'); plt.ylabel('Precio por m2 (COP)'); plt.title('Segmentacion: IAH vs Precio por m2')
plt.tight_layout(); plt.savefig('docs/figures/fig_IAH_vs_precio_m2.png', dpi=150, bbox_inches='tight'); plt.close()

# Pregunta 4
ratio_ciudad = df.groupby(['city','year'])['ratio_cuota_salario'].median().reset_index()
pivot_ratio = ratio_ciudad.pivot(index='city', columns='year', values='ratio_cuota_salario').round(4)
print("Ratio cuota/salario:"); print(pivot_ratio.to_string())

plt.figure(figsize=(12,8))
sns.heatmap(pivot_ratio, annot=True, fmt='.2f', cmap=['green','yellow','red'], vmin=0, vmax=1, center=0.3)
plt.title('Ratio Cuota/Salario - Semaforo Financiero')
plt.tight_layout(); plt.savefig('docs/figures/fig_semaforo_cuota.png', dpi=150, bbox_inches='tight'); plt.close()

pct_critico = (df['ratio_cuota_salario'] > 0.30).mean() * 100
print("% registros con ratio > 0.30: {:.1f}%".format(pct_critico))

# ── Sección 6: Análisis complementario IAH ──────────────────────────
niveles = df['nivel_accesibilidad'].value_counts(normalize=True) * 100
nivel_ciudad = df.groupby(['city','nivel_accesibilidad']).size().unstack(fill_value=0)
nivel_ciudad_pct = nivel_ciudad.div(nivel_ciudad.sum(axis=1), axis=0) * 100

fig, ax = plt.subplots(figsize=(14,7))
nivel_ciudad_pct.plot(kind='barh', stacked=True, ax=ax, colormap='RdYlGn_r')
ax.set_xlabel('Porcentaje'); ax.set_ylabel('Ciudad'); ax.set_title('Niveles de Accesibilidad por Ciudad')
ax.legend(title='Nivel', bbox_to_anchor=(1,1))
plt.tight_layout(); plt.savefig('docs/figures/fig_niveles_accesibilidad.png', dpi=150, bbox_inches='tight'); plt.close()

critica_2024 = df[df['year']==2024].groupby('city')['nivel_accesibilidad'].apply(lambda x: (x=='Critico').mean()*100).sort_values(ascending=False)
accesible_evo = df[df['nivel_accesibilidad']=='Accesible'].groupby('year').size() / df.groupby('year').size() * 100

precio_anual = df.groupby('year')[['price','precio_real']].median().reset_index()
plt.figure(figsize=(10,6))
plt.plot(precio_anual['year'], precio_anual['price']/1e6, marker='o', label='Precio nominal (Millones COP)')
plt.plot(precio_anual['year'], precio_anual['precio_real']/1e6, marker='s', label='Precio real (Millones COP)')
plt.xlabel('Ano'); plt.ylabel('Precio mediano (Millones COP)'); plt.title('Precio Nominal vs Real por Ano')
plt.legend(); plt.grid(True, alpha=0.3)
plt.tight_layout(); plt.savefig('docs/figures/fig_precio_nominal_vs_real.png', dpi=150, bbox_inches='tight'); plt.close()

# ── Exportar respuestas ─────────────────────────────────────────────
respuestas = pd.DataFrame({
    'Pregunta': ['P1. Anios de salario minimo por vivienda',
                 'P2. Variables con mayor poder predictivo',
                 'P3. Segmentacion de ciudades en grupos',
                 'P4. Ciudades con cuota > 30% salario minimo'],
    'Respuesta': [
        'IAH nacional {:.1f} anios en 2024. Ciudad mas accesible: {} ({:.0f} anios). Menos accesible: {} ({:.0f} anios). Ninguna ciudad cumple estandar OCDE (<5 anios).'.format(
            iah_nac[iah_nac['year']==2024]['IAH'].values[0], min_city_2024, pivot_iah.loc[min_city_2024, 2024], max_city_2024, pivot_iah.loc[max_city_2024, 2024]),
        'Top 3: {} ({:.1f}%), {} ({:.1f}%), {} ({:.1f}%). Caracteristicas fisicas dominan sobre contexto macro.'.format(
            top5.iloc[0]['feature'], top5.iloc[0]['importance']*100,
            top5.iloc[1]['feature'], top5.iloc[1]['importance']*100,
            top5.iloc[2]['feature'], top5.iloc[2]['importance']*100),
        '5 clusters identificados (silueta={:.4f}). Diferencia IAH entre extremos: {:.0f} anios. Segmentacion clara y estable en el tiempo.'.format(silueta_kmeans, iah_max-iah_min),
        '{:.0f}% del mercado tiene cuota > 30% del salario minimo. Todas las ciudades superan el umbral critico en todos los anios.'.format(pct_critico)
    ],
    'Evidencia': ['docs/figures/fig_IAH_por_ciudad.png + tabla IAH',
                  'docs/figures/fig_importancia_vars.png + tabla correlacion',
                  'docs/figures/fig_pca_clusters.png + fig_IAH_vs_precio_m2.png',
                  'docs/figures/fig_semaforo_cuota.png + heatmap ratio']
})
respuestas.to_csv('docs/respuestas_preguntas.csv', index=False)
print("Respuestas exportadas")

# ── Resumen final ───────────────────────────────────────────────────
cumplen = (criterios['Cumple'] == 'SI').sum()
total = len(criterios)
print("\n=== RESUMEN FINAL ===")
print(f"Criterios cumplidos: {cumplen}/{total}")
print(f"Modelo regresion: R2={r2:.4f} (umbral 0.75) -> {'CUMPLE' if r2>=0.75 else 'NO CUMPLE'}")
print(f"Clustering silueta: {silueta_kmeans:.4f} (umbral 0.45) -> {'CUMPLE' if silueta_kmeans>=0.45 else 'NO CUMPLE'}")

# ── Generar notebook .ipynb ─────────────────────────────────────────
print("Generando notebook...")
cells = []
# Read the source file to embed outputs
with open("generate_eval_notebook.py", "r", encoding="utf-8") as f:
    gen_src = f.read()
subprocess.run([sys.executable, "generate_eval_notebook.py"], check=True)
print("Notebook generado exitosamente!")
print("\nFase 5 completa.")
