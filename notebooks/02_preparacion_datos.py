import pandas as pd
import numpy as np
import os
import re

# Directorios
DIR_RAW = os.path.join("..", "data", "raw")
DIR_PROCESSED = os.path.join("..", "data", "processed")
os.makedirs(DIR_PROCESSED, exist_ok=True)

COLS_CANONICAS = [
    'price', 'area', 'rooms', 'bathrooms', 'property_type', 
    'city', 'lat', 'lon', 'created_on', 'barrio', 'parking', 'estrato', 'fuente'
]

# Diccionario para el reporte de limpieza
reporte_metricas = []

def registrar_metrica(paso, operacion, df_in, df_out):
    regs_in = len(df_in) if df_in is not None else 0
    regs_out = len(df_out)
    eliminados = regs_in - regs_out if df_in is not None else 0
    pct = (eliminados / regs_in * 100) if regs_in > 0 else 0
    
    reporte_metricas.append({
        'Paso': paso,
        'Operacion': operacion,
        'Regs_Entrada': regs_in,
        'Regs_Salida': regs_out,
        'Regs_Eliminados': eliminados,
        'Pct_Eliminado': round(pct, 2)
    })

def cargar_y_canonizar_datasets():
    datasets = []
    
    # A1: Properati Colombia
    df1 = pd.read_csv(os.path.join(DIR_RAW, "A1_colombia_housing_properties.csv"))
    if 'operation_type' in df1.columns:
        df1 = df1[df1['operation_type'] == 'Venta'].copy()
    
    # Avoid duplicate created_on
    if 'created_on' in df1.columns and 'start_date' in df1.columns:
        df1 = df1.drop(columns=['created_on'])
        
    rename_dict1 = {
        'bedrooms': 'rooms',
        'bathrooms': 'bathrooms', 'property_type': 'property_type',
        'l3': 'city', 'start_date': 'created_on'
    }
    if 'surface_total' in df1.columns:
        rename_dict1['surface_total'] = 'area'
    elif 'area' in df1.columns:
        rename_dict1['area'] = 'area'
        
    df1 = df1.rename(columns=rename_dict1)
    df1['fuente'] = 'A1_Properati'
    datasets.append(df1)
    
    # A2: FincaRaiz Colombia 2023-2024
    df2 = pd.read_csv(os.path.join(DIR_RAW, "A2_fincaraiz_colombia.csv"))
    
    # Fix potential BOM in column names
    df2.columns = [c.replace('\ufeff', '') for c in df2.columns]
    
    df2 = df2.rename(columns={
        'Precio': 'price', 'Area Construida': 'area', 'Habitaciones': 'rooms',
        'Banos': 'bathrooms', 'Tipo Propiedad': 'property_type', 'Ciudad': 'city',
        'Estrato': 'estrato'
    })
    
    if 'price' in df2.columns:
        df2['price'] = pd.to_numeric(df2['price'].astype(str).str.replace(r'[^\d.]', '', regex=True), errors='coerce')
        # Check if price needs scaling. The Kaggle dataset says "Precio", let's assume it's raw COP or millions. 
        # The original script multiplied by 1000000. Let's keep that but handle NaNs.
        df2['price'] = df2['price'] * 1000000 
    
    df2['fuente'] = 'A2_FincaRaiz_Kaggle'
    datasets.append(df2)
    
    # A3: Colombia House Prediction
    df3 = pd.read_csv(os.path.join(DIR_RAW, "A3_colombia_house_prediction.csv"))
    df3.columns = [c.replace('\ufeff', '') for c in df3.columns]
    df3 = df3.rename(columns={
        'valor': 'price', 'area': 'area', 'habitaciones': 'rooms',
        'banos': 'bathrooms', 'estrato': 'estrato'
    })
    df3['fuente'] = 'A3_Kaggle'
    datasets.append(df3)
    
    # A4: Real Estate Bogotá
    df4 = pd.read_csv(os.path.join(DIR_RAW, "A4_real_estate_bogota.csv"), encoding='latin1')
    df4.columns = [c.replace('\ufeff', '') for c in df4.columns]
    
    rename_a4 = {}
    for c in df4.columns:
        if 'Valor' in c: rename_a4[c] = 'price'
        elif 'rea' in c: rename_a4[c] = 'area'
        elif 'Habitaciones' in c: rename_a4[c] = 'rooms'
        elif 'Ba' in c and 'os' in c: rename_a4[c] = 'bathrooms'
        elif 'Tipo' in c: rename_a4[c] = 'property_type'
    
    df4 = df4.rename(columns=rename_a4)
    if 'price' in df4.columns:
        df4['price'] = pd.to_numeric(df4['price'].astype(str).str.replace(r'[^\d.]', '', regex=True), errors='coerce')
    df4['city'] = 'Bogotá'
    df4['fuente'] = 'A4_Bogota_Kaggle'
    datasets.append(df4)
    
    # A5: Medellín Properties 2023
    df5 = pd.read_csv(os.path.join(DIR_RAW, "A5_medellin_properties_2023.csv"))
    df5.columns = [c.replace('\ufeff', '') for c in df5.columns]
    df5 = df5.rename(columns={
        'price': 'price', 'area': 'area', 'rooms': 'rooms',
        'baths': 'bathrooms', 'property_type': 'property_type', 
        'neighbourhood': 'barrio', 'stratum': 'estrato'
    })
    df5['city'] = 'Medellín'
    df5['fuente'] = 'A5_Medellin_Kaggle'
    datasets.append(df5)
    
    # A6: Real Estate Bogotá 2023
    df6 = pd.read_csv(os.path.join(DIR_RAW, "A6_real_estate_bogota_2023.csv"), encoding='latin1')
    df6.columns = [c.replace('\ufeff', '') for c in df6.columns]
    
    rename_a6 = {}
    for c in df6.columns:
        if 'precio' in c.lower(): rename_a6[c] = 'price'
        elif 'rea' in c.lower() or 'area' in c.lower(): rename_a6[c] = 'area'
        elif 'habitaciones' in c.lower() or 'cuartos' in c.lower(): rename_a6[c] = 'rooms'
        elif 'ba' in c.lower() and 'os' in c.lower(): rename_a6[c] = 'bathrooms'
        elif 'tipo_de_inmueble' in c.lower(): rename_a6[c] = 'property_type'
    
    df6 = df6.rename(columns=rename_a6)
    df6['city'] = 'Bogotá'
    df6['fuente'] = 'A6_Bogota2023_Kaggle'
    datasets.append(df6)
    
    # A7: Villavicencio Scraping
    if os.path.exists(os.path.join(DIR_RAW, "A7_fincaraiz_villavicencio_scraping.csv")):
        df7 = pd.read_csv(os.path.join(DIR_RAW, "A7_fincaraiz_villavicencio_scraping.csv"))
        df7['fuente'] = 'A7_Scraping_Villavicencio'
        datasets.append(df7)
    
    # A8: Características precios vivienda nueva Bogotá UPZ
    if os.path.exists(os.path.join(DIR_RAW, "A8_carac_pre_viv_nueva.csv")):
        df8 = pd.read_csv(os.path.join(DIR_RAW, "A8_carac_pre_viv_nueva.csv"))
        df8['fuente'] = 'A8_CaracPreVivNueva'
        datasets.append(df8)
    
    df_lista_filtrada = []
    for df in datasets:
        for col in COLS_CANONICAS:
            if col not in df.columns:
                df[col] = np.nan
        df_lista_filtrada.append(df[COLS_CANONICAS])
        
    df_consolidado = pd.concat(df_lista_filtrada, ignore_index=True)
    return df_consolidado

print("1. Cargando y canonizando datasets...")
df_raw_consolidado = cargar_y_canonizar_datasets()
registrar_metrica(0, "Consolidacion Inicial", None, df_raw_consolidado)
print(f"Total registros cargados: {len(df_raw_consolidado)}")

TRM_HISTORICA = {
    2015: 2746.0, 2016: 3051.0, 2017: 2951.0, 2018: 2956.0, 2019: 3281.0,
    2020: 3693.0, 2021: 3743.0, 2022: 4256.0, 2023: 4325.0, 2024: 4000.0
}

def limpiar_precios_y_monedas(df):
    df = df.copy()
    
    df['created_on'] = pd.to_datetime(df['created_on'], errors='coerce')
    df['year_temp'] = df['created_on'].dt.year.fillna(2023).astype(int)
    
    is_properati = df['fuente'] == 'A1_Properati'
    
    if 'currency' in df.columns:
        is_usd = df['currency'] == 'USD'
        for yr, trm in TRM_HISTORICA.items():
            mask = is_properati & is_usd & (df['year_temp'] == yr)
            df.loc[mask, 'price'] = df.loc[mask, 'price'] * trm
        
    is_cop_m2 = is_properati & (df['price'] < 1000000) & (df['price'] > 5000) & (df['area'] > 10)
    df.loc[is_cop_m2, 'price'] = df.loc[is_cop_m2, 'price'] * df.loc[is_cop_m2, 'area']
    
    df = df[df['price'].notnull()]
    df = df[(df['price'] >= 10000000) & (df['price'] <= 10000000000)]
    
    df = df.drop(columns=['year_temp'])
    return df

print("2. Limpiando precios y monedas...")
df_clean_precios = limpiar_precios_y_monedas(df_raw_consolidado)
registrar_metrica(1, "Limpieza Precios e Invalidez", df_raw_consolidado, df_clean_precios)

MAPA_CIUDADES = {
    'bogota': 'Bogotá', 'santa fe de bogota': 'Bogotá', 'bogota d.c.': 'Bogotá', 'bogota d. c.': 'Bogotá',
    'medellin': 'Medellín', 'medelln': 'Medellín',
    'cali': 'Cali', 'santiago de cali': 'Cali',
    'barranquilla': 'Barranquilla', 'barranq': 'Barranquilla',
    'cartagena': 'Cartagena', 'cartagena de indias': 'Cartagena',
    'bucaramanga': 'Bucaramanga', 'bucara': 'Bucaramanga',
    'pereira': 'Pereira',
    'manizales': 'Manizales',
    'armenia': 'Armenia',
    'cucuta': 'Cúcuta', 'sanjose de cucuta': 'Cúcuta', 'cúcuta': 'Cúcuta',
    'ibague': 'Ibagué', 'ibagué': 'Ibagué',
    'villavicencio': 'Villavicencio', 'villavo': 'Villavicencio'
}

def estandarizar_ciudades(df):
    df = df.copy()
    df['city_raw'] = df['city'].astype(str).str.lower().str.normalize('NFKD')\
                              .str.encode('ascii', errors='ignore').str.decode('utf-8').str.strip()
    df['city_clean'] = df['city_raw'].map(MAPA_CIUDADES)
    df = df[df['city_clean'].notnull()].copy()
    df = df.drop(columns=['city', 'city_raw']).rename(columns={'city_clean': 'city'})
    return df

print("3. Estandarizando ciudades...")
df_clean_ciudades = estandarizar_ciudades(df_clean_precios)
registrar_metrica(2, "Estandarizacion / Filtro Ciudades", df_clean_precios, df_clean_ciudades)

def limpiar_fechas(df):
    df = df.copy()
    df['created_on'] = pd.to_datetime(df['created_on'], errors='coerce')
    df['year'] = df['created_on'].dt.year
    
    año_fuente = {
        'A1_Properati': 2020, 'A2_FincaRaiz_Kaggle': 2023, 'A3_Kaggle': 2022,
        'A4_Bogota_Kaggle': 2022, 'A5_Medellin_Kaggle': 2023, 'A6_Bogota2023_Kaggle': 2023,
        'A7_Scraping_Villavicencio': 2024, 'A8_CaracPreVivNueva': 2022
    }
    df['year'] = df['year'].fillna(df['fuente'].map(año_fuente)).fillna(2023).astype(int)
    df = df[(df['year'] >= 2015) & (df['year'] <= 2024)]
    return df

print("4. Aplicando filtro temporal...")
df_clean_temporal = limpiar_fechas(df_clean_ciudades)
registrar_metrica(3, "Restriccion Temporal 2015-2024", df_clean_ciudades, df_clean_temporal)

MAPA_PROPIEDADES = {
    'apartamento': 'Apartamento', 'apto': 'Apartamento', 'apartment': 'Apartamento',
    'casa': 'Casa', 'house': 'Casa', 'casa lote': 'Casa'
}

def estandarizar_propiedad(df):
    df = df.copy()
    df['prop_raw'] = df['property_type'].astype(str).str.lower().str.strip()
    df['property_type_clean'] = df['prop_raw'].map(MAPA_PROPIEDADES)
    df = df[df['property_type_clean'].notnull()].copy()
    df = df.drop(columns=['property_type', 'prop_raw']).rename(columns={'property_type_clean': 'property_type'})
    return df

print("5. Estandarizando tipos de propiedad...")
df_clean_prop = estandarizar_propiedad(df_clean_temporal)
registrar_metrica(4, "Tipo de Inmueble (Casa/Apto)", df_clean_temporal, df_clean_prop)

def eliminar_outliers_grupos(df):
    df = df.copy()
    df_limpio = []
    grupos = df.groupby(['city', 'year', 'property_type'])
    
    for name, group in grupos:
        if len(group) < 10:
            df_limpio.append(group)
            continue
            
        q1_p = group['price'].quantile(0.025)
        q3_p = group['price'].quantile(0.975)
        
        group_f = group[(group['price'] >= q1_p) & (group['price'] <= q3_p)]
        
        if group_f['area'].notnull().any():
            q1_a = group_f['area'].quantile(0.01)
            q3_a = group_f['area'].quantile(0.99)
            area_null_mask = group_f['area'].isnull()
            area_valid_mask = (group_f['area'] >= q1_a) & (group_f['area'] <= q3_a)
            group_f = group_f[area_null_mask | area_valid_mask]
            
        df_limpio.append(group_f)
        
    return pd.concat(df_limpio, ignore_index=True)

print("6. Eliminando outliers por grupo...")
df_clean_outliers = eliminar_outliers_grupos(df_clean_prop)
registrar_metrica(5, "Filtro IQR Outliers por Grupo", df_clean_prop, df_clean_outliers)

def eliminar_duplicados(df):
    df = df.copy()
    df['dup_key'] = (
        df['city'].astype(str) + "_" + 
        np.round(df['price'] / 1000000).astype(str) + "_" + 
        np.round(df['area'].fillna(-1)).astype(str) + "_" + 
        df['property_type'].astype(str) + "_" + 
        df['year'].astype(str)
    )
    
    df['fuente_priority'] = df['fuente'].map({
        'A7_Scraping_Villavicencio': 1, 'A2_FincaRaiz_Kaggle': 2,
        'A1_Properati': 3, 'A6_Bogota2023_Kaggle': 4,
        'A5_Medellin_Kaggle': 5, 'A4_Bogota_Kaggle': 6, 'A3_Kaggle': 7,
        'A8_CaracPreVivNueva': 8
    }).fillna(10)
    
    df = df.sort_values(by='fuente_priority')
    df = df.drop_duplicates(subset=['dup_key'], keep='first')
    df = df.drop(columns=['dup_key', 'fuente_priority'])
    return df

print("7. Deduplicando registros...")
df_clean_final = eliminar_duplicados(df_clean_outliers)
registrar_metrica(6, "Deduplicacion Inter-Dataset", df_clean_outliers, df_clean_final)

def imputar_valores_faltantes(df):
    df = df.copy()
    
    mediana_area_grupo = df.groupby(['city', 'year', 'property_type'])['area'].transform('median')
    df['area'] = df['area'].fillna(mediana_area_grupo)
    mediana_area_global = df.groupby('property_type')['area'].transform('median')
    df['area'] = df['area'].fillna(mediana_area_global)
    
    mediana_hab_grupo = df.groupby(['city', 'property_type'])['rooms'].transform('median')
    df['rooms'] = df['rooms'].fillna(mediana_hab_grupo).fillna(3).astype(int)
    df['rooms'] = df['rooms'].clip(lower=1)
    
    mediana_ban_grupo = df.groupby(['city', 'property_type'])['bathrooms'].transform('median')
    df['bathrooms'] = df['bathrooms'].fillna(mediana_ban_grupo).fillna(2).astype(int)
    df['bathrooms'] = df['bathrooms'].clip(lower=1)
    
    if 'barrio' in df.columns:
        mediana_estrato_barrio = df.groupby(['city', 'barrio'])['estrato'].transform('median')
        df['estrato'] = df['estrato'].fillna(mediana_estrato_barrio)
        
    mediana_estrato_ciudad = df.groupby('city')['estrato'].transform('median')
    df['estrato'] = df['estrato'].fillna(mediana_estrato_ciudad).fillna(3).astype(int)
    df['estrato'] = df['estrato'].clip(1, 6).astype(int)
    
    return df

print("8. Imputando valores faltantes...")
df_imputado = imputar_valores_faltantes(df_clean_final)

def cargar_e_integrar_macro(df_inmuebles):
    # B3: Salario
    b3 = pd.read_csv(os.path.join(DIR_RAW, "B3_salario_minimo_historico.csv"), encoding='utf-8-sig')
    b3 = b3.rename(columns={'Ano': 'year', 'Salario_minimo_mensual': 'salario_mensual'})[['year', 'salario_mensual']]

    # B4: IPC
    b4 = pd.read_csv(os.path.join(DIR_RAW, "B4_ipc_colombia_anual.csv"), encoding='utf-8-sig')
    b4 = b4.rename(columns={'Ano': 'year', 'Variacion_IPC_%': 'ipc_var_anual'})
    b4 = b4.sort_values('year').reset_index(drop=True)
    b4['ipc_base2018'] = 100.0
    idx_2018 = b4.index[b4['year'] == 2018].tolist()
    if idx_2018:
        idx = idx_2018[0]
        for i in range(idx+1, len(b4)):
            b4.loc[i, 'ipc_base2018'] = b4.loc[i-1, 'ipc_base2018'] * (1 + b4.loc[i, 'ipc_var_anual']/100)
        for i in range(idx-1, -1, -1):
            b4.loc[i, 'ipc_base2018'] = b4.loc[i+1, 'ipc_base2018'] / (1 + b4.loc[i+1, 'ipc_var_anual']/100)

    # B2: Tasa Hipotecaria
    b2 = pd.read_csv(os.path.join(DIR_RAW, "B2_tasa_hipotecaria_semanal.csv"), encoding='latin1')
    col_fecha = b2.columns[0]
    b2['year'] = pd.to_datetime(b2[col_fecha], errors='coerce').dt.year
    col_hipotecaria = [c for c in b2.columns if 'colocaci' in c.lower()][0]
    b2_year = b2.groupby('year')[col_hipotecaria].mean().reset_index()
    b2_year = b2_year.rename(columns={col_hipotecaria: 'tasa_hipotecaria_anual'})

    # B5: Desempleo
    b5 = pd.read_csv(os.path.join(DIR_RAW, "B5_geih_empleo_colombia.csv"), encoding='utf-8-sig')
    b5['year'] = pd.to_datetime(b5['fecha'], errors='coerce').dt.year
    b5_nacional = b5[b5['grupo'] == 'nacional'].groupby('year')['td'].mean().reset_index().rename(columns={'td': 'tasa_desempleo'})

    # B1: Indices IPVU e IPVN
    b1 = pd.read_csv(os.path.join(DIR_RAW, "B1_indices_precios_vivienda.csv"), encoding='utf-8-sig')
    b1.columns = [c.encode('ascii', 'ignore').decode('utf-8') for c in b1.columns]
    b1['year'] = pd.to_datetime(b1['fecha'], errors='coerce').dt.year
    b1_year = b1.groupby('year')[['ipvnbr_ndice_nominal_agregado', 'ipvu_indice_nominal']].mean().reset_index()
    b1_year['ipvn_variacion_anual'] = b1_year['ipvnbr_ndice_nominal_agregado'].pct_change() * 100
    b1_year['ipvu_variacion_anual'] = b1_year['ipvu_indice_nominal'].pct_change() * 100

    # Merge todo
    df_macro = pd.DataFrame({'year': range(2015, 2025)})
    df_macro = df_macro.merge(b3, on='year', how='left')
    df_macro = df_macro.merge(b4, on='year', how='left')
    df_macro = df_macro.merge(b2_year, on='year', how='left')
    df_macro = df_macro.merge(b5_nacional, on='year', how='left')
    df_macro = df_macro.merge(b1_year[['year', 'ipvn_variacion_anual', 'ipvu_variacion_anual']], on='year', how='left')
    
    # Rellenar valores nulos (para evitar que se propaguen)
    df_macro = df_macro.ffill().bfill()
    
    # Merge vivienda + tabla macro general
    df_fusionado = df_inmuebles.merge(df_macro, on='year', how='left')
    
    return df_fusionado, df_macro

print("9. Integrando datos macroeconómicos...")
df_integrado_macro, df_tabla_macro = cargar_e_integrar_macro(df_imputado)

def calcular_cuota_mensual(precio, tasa_anual, meses=180, financia=0.70):
    if pd.isna(precio) or pd.isna(tasa_anual) or tasa_anual <= 0:
        return np.nan
    monto_credito = precio * financia
    tasa_mensual = (1 + (tasa_anual / 100)) ** (1/12) - 1
    cuota = monto_credito * (tasa_mensual * (1 + tasa_mensual)**meses) / ((1 + tasa_mensual)**meses - 1)
    return cuota

def construir_variables_derivadas(df):
    df = df.copy()
    df['salario_anual'] = df['salario_mensual'] * 12
    df['IAH'] = df['price'] / df['salario_anual']
    df['precio_real'] = df['price'] / (df['ipc_base2018'] / 100)
    df['precio_m2'] = df['price'] / df['area']
    
    df['cuota_mensual'] = df.apply(
        lambda row: calcular_cuota_mensual(row['price'], row['tasa_hipotecaria_anual']), axis=1
    )
    
    df['ratio_cuota_salario'] = df['cuota_mensual'] / df['salario_mensual']
    
    condiciones = [
        (df['IAH'] <= 5),
        (df['IAH'] > 5) & (df['IAH'] <= 10),
        (df['IAH'] > 10) & (df['IAH'] <= 20),
        (df['IAH'] > 20)
    ]
    categorias = ['Accesible', 'Moderado', 'Elevado', 'Crítico']
    df['nivel_accesibilidad'] = np.select(condiciones, categorias, default='Crítico')
    
    return df

print("10. Construyendo variables derivadas...")
df_variables = construir_variables_derivadas(df_integrado_macro)

def validar_dataset_final(df):
    null_counts = df.isnull().sum()
    print("Conteo de nulos por columna:")
    print(null_counts[null_counts > 0])
    
    columnas_criticas = ['price', 'area', 'rooms', 'bathrooms', 'property_type', 'city', 'estrato', 'year', 'IAH']
    for col in columnas_criticas:
        assert df[col].isnull().sum() == 0, f"Error: Existen valores nulos en la columna crítica {col}"
        
    assert (df['price'] > 0).all(), "Error: Existen precios menores o iguales a cero"
    assert (df['area'] > 0).all(), "Error: Existen areas menores o iguales a cero"
    assert (df['rooms'] >= 1).all(), "Error: Cantidad de habitaciones invalida"
    assert (df['bathrooms'] >= 1).all(), "Error: Cantidad de banos invalida"
    assert df['city'].isin(MAPA_CIUDADES.values()).all(), "Error: Ciudades fuera del catalogo"
    assert df['year'].between(2015, 2024).all(), "Error: Anos fuera del periodo temporal"
    assert df['estrato'].between(1, 6).all(), "Error: Estratos fuera del rango 1-6"
    print("Validacion de integridad aprobada exitosamente.")

print("11. Validando dataset final...")
# Drop columns that shouldn't be in the final export, like barrio, parking
columns_to_export = [
    'price', 'area', 'rooms', 'bathrooms', 'property_type', 'city', 'lat', 'lon', 
    'created_on', 'estrato', 'fuente', 'year', 'salario_mensual', 'ipc_var_anual', 
    'ipc_base2018', 'tasa_hipotecaria_anual', 'tasa_desempleo', 'ipvu_variacion_anual', 
    'ipvn_variacion_anual', 'salario_anual', 'IAH', 'precio_real', 'precio_m2', 
    'cuota_mensual', 'ratio_cuota_salario', 'nivel_accesibilidad'
]
df_final = df_variables[columns_to_export].copy()
validar_dataset_final(df_final)

print("12. Exportando...")
df_final.to_csv(os.path.join(DIR_PROCESSED, "vivienda_colombia_limpio.csv"), index=False)
pd.DataFrame(reporte_metricas).to_csv(os.path.join(DIR_PROCESSED, "reporte_limpieza.csv"), index=False)
print("Archivos exportados exitosamente.")
