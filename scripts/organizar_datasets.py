"""
ORGANIZAR DATASETS
Consolida, renombra, limpia y unifica todos los datasets del proyecto.
Ejecutar desde la raiz del repo:
    py scripts/organizar_datasets.py
"""

import os, shutil, re
import pandas as pd

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW  = os.path.join(RAIZ, "data", "raw")
ARRE = os.path.join(RAW, "arreglar_datos")

os.chdir(RAIZ)
print(f"Raiz del proyecto: {RAIZ}")


# ── 1. ELIMINAR DUPLICADOS ────────────────────────────────
def eliminar_duplicados():
    print("\n=== 1. ELIMINAR DUPLICADOS ===")
    dups = [
        ("data/raw/colombia_housing_properties_price.csv",
         "copia exacta de colombian_properties_2023.csv"),
        ("data/raw/arreglar_datos/Tasas de inter\u00e9s.xlsx",
         "copia exacta de data/raw/tasa_de_interes.xlsx"),
    ]
    for path, razon in dups:
        full = os.path.join(RAIZ, path)
        if os.path.exists(full):
            sz = os.path.getsize(full)
            os.remove(full)
            print(f"  BORRADO  {path}  ({sz/1e6:.1f} MB) — {razon}")
        else:
            print(f"  NO EXISTE {path}")


# ── 2. RENOMBRAR DATASETS ─────────────────────────────────
def renombrar():
    print("\n=== 2. RENOMBRAR DATASETS ===")
    cambios = [
        ("data/raw/tasa_de_interes.xlsx",
         "data/raw/tasa_hipotecaria_mensual.xlsx"),
        ("data/raw/arreglar_datos/IPVNBR_Indice de precios de la vivienda nueva.csv",
         "data/raw/ipvn_trimestral.csv"),
        ("data/raw/arreglar_datos/IPVU_Indice de precios de la vivienda usada.csv",
         "data/raw/ipvu_trimestral.csv"),
        ("data/raw/arreglar_datos/QCON368BIS.csv",
         "data/raw/qcon_confianza_constructora.csv"),
        ("data/raw/arreglar_datos/QCON628BIS.csv",
         "data/raw/qcon_licencias_construccion.csv"),
    ]
    for src, dst in cambios:
        src_f = os.path.join(RAIZ, src)
        dst_f = os.path.join(RAIZ, dst)
        if os.path.exists(src_f):
            os.makedirs(os.path.dirname(dst_f), exist_ok=True)
            shutil.move(src_f, dst_f)
            print(f"  RENOMBRADO  {src}  ->  {dst}")
        else:
            print(f"  NO EXISTE  {src}")


# ── 3. MOVER DE arreglar_datos A RAW ─────────────────────
def mover_desde_arreglar():
    print("\n=== 3. MOVER DESDE arreglar_datos/ A data/raw/ ===")
    movidas = [
        ("data/raw/arreglar_datos/anex-GEIH-abr2026.xlsx",
         "data/raw/geih_empleo_mensual.xlsx"),
        ("data/raw/arreglar_datos/anex-GEIH-Desestacionalizado-abr2026.xlsx",
         "data/raw/geih_desestacionalizado.xlsx"),
        ("data/raw/arreglar_datos/anex-IPVN-Itrim2026.xlsx",
         "data/raw/ipvn_detalle_trimestral.xlsx"),
        ("data/raw/arreglar_datos/Anexo IVPUB 2025.xlsx",
         "data/raw/ivpub_bogota_2025.xlsx"),
        ("data/raw/Estados_Localidades_Colombia.csv",
         "data/raw/geo_estados_localidades.csv"),
    ]
    for src, dst in movidas:
        src_f = os.path.join(RAIZ, src)
        dst_f = os.path.join(RAIZ, dst)
        if os.path.exists(src_f):
            os.makedirs(os.path.dirname(dst_f), exist_ok=True)
            shutil.move(src_f, dst_f)
            print(f"  MOVIDO  {src}  ->  {dst}")
        else:
            print(f"  NO EXISTE  {src}")


# ── 4. CORREGIR ENCODING DE CSVs ─────────────────────────
def corregir_encoding():
    print("\n=== 4. CORREGIR ENCODING DE CSVs A UTF-8-SIG ===")
    # Archivos en RAW que son CSV y pueden tener encoding roto
    csvs = [f for f in os.listdir(RAW) if f.endswith(".csv") and f != ".gitkeep"]
    cont = 0
    for fname in sorted(csvs):
        fpath = os.path.join(RAW, fname)
        try:
            with open(fpath, "rb") as f:
                raw = f.read()
            # Detectar si ya es UTF-8 limpio
            try:
                raw.decode("utf-8")
                ya_utf8 = True
            except UnicodeDecodeError:
                ya_utf8 = False

            if ya_utf8 and not raw.startswith(b'\xef\xbb\xbf'):
                # Ya es UTF-8 sin BOM, re-escribir con BOM
                df = pd.read_csv(fpath, encoding="utf-8")
                df.to_csv(fpath, index=False, encoding="utf-8-sig")
                print(f"  RE-ESCRITO  {fname}  (BOM anyadido)")
                cont += 1
            elif not ya_utf8:
                # Intentar detectar encoding real
                for enc in ["latin-1", "cp1252", "ISO-8859-1"]:
                    try:
                        df = pd.read_csv(fpath, encoding=enc)
                        df.to_csv(fpath, index=False, encoding="utf-8-sig")
                        print(f"  CORREGIDO  {fname}  ({enc} -> utf-8-sig)")
                        cont += 1
                        break
                    except Exception:
                        continue
            else:
                print(f"  OK         {fname}  (ya utf-8-sig)")
        except Exception as e:
            print(f"  ERROR      {fname}: {e}")
    print(f"  Total: {cont} archivos actualizados")


# ── 5. CONVERTIR XLSX A CSV ──────────────────────────────
# Hojas relevantes (nombres exactos verificados contra disco)
HOJAS_RELEVANTES = {
    "ipc_colombia_mensual.xlsx": {
        "rename": "ipc_colombia_anual.csv",
        "sheets": ["1"],
    },
    "salario_minimo_historico.xlsx": {
        "rename": "salario_minimo_historico.csv",
        "sheets": ["Hist\u00f3rico del salario m\u00ednimo"],  # acentos reales
    },
    "tasa_hipotecaria_mensual.xlsx": {
        "rename": "tasa_hipotecaria_mensual.csv",
        "sheets": ["Datos"],
    },
    "geih_empleo_mensual.xlsx": {
        "multi": {
            "Total nacional":              "geih_empleo_nacional.csv",
            "Ocupados TN_T13_rama":        "geih_empleo_rama.csv",
            "Total 13 ciudades A.M.":      "geih_empleo_13ciudades.csv",
        },
    },
    "geih_desestacionalizado.xlsx": {
        "multi": {
            "Total nacional":              "geih_desestacionalizado_nacional.csv",
        },
    },
    "ipvn_detalle_trimestral.xlsx": {
        "multi": {
            "TOTAL Y DESTINOS ":            "ipvn_detalle_trimestral.csv",
            "\u00c1REAS - DESTINO":         "ipvn_detalle_areas.csv",
        },
    },
    "ivpub_bogota_2025.xlsx": {
        "rename": "ivpub_bogota_avaluos_2025.csv",
        "sheets": ["Cuadro 5"],
    },
}


def convertir_xlsx_a_csv():
    print("\n=== 5. CONVERTIR XLSX A CSV ===")
    xlsx_files = [f for f in os.listdir(RAW) if f.endswith(".xlsx")]
    for fname in sorted(xlsx_files):
        fpath = os.path.join(RAW, fname)
        if fname not in HOJAS_RELEVANTES:
            print(f"  SALTADO   {fname}  (sin regla de conversion)")
            continue

        regla = HOJAS_RELEVANTES[fname]
        try:
            if "multi" in regla:
                for hoja, csv_name in regla["multi"].items():
                    df = pd.read_excel(fpath, sheet_name=hoja)
                    # Limpiar columnas unnamed
                    df = df.loc[:, ~df.columns.str.contains("^Unnamed", na=False)]
                    # Eliminar filas completamente vacias
                    df = df.dropna(how="all")
                    csv_path = os.path.join(RAW, csv_name)
                    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
                    print(f"  CREADO   {csv_name}  ({len(df)} filas, {len(df.columns)} cols)")
            else:
                for hoja in regla["sheets"]:
                    df = pd.read_excel(fpath, sheet_name=hoja)
                    df = df.loc[:, ~df.columns.str.contains("^Unnamed", na=False)]
                    df = df.dropna(how="all")
                    csv_path = os.path.join(RAW, regla["rename"])
                    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
                    print(f"  CREADO   {regla['rename']}  ({len(df)} filas, {len(df.columns)} cols)")

            # Confirmacion: borrar xlsx solo si se generaron CSVs exitosamente
            os.remove(fpath)
            print(f"  BORRADO  {fname}  (reemplazado por CSV)")

        except Exception as e:
            print(f"  ERROR     {fname}: {e}")


# ── 6. LIMPIAR COLUMNAS IRRELEVANTES ─────────────────────
def limpiar_columnas():
    print("\n=== 6. LIMPIAR COLUMNAS IRRELEVANTES ===")
    # colombia_house_prediction.csv: columnas con >90% NaN
    fpath = os.path.join(RAW, "colombia_house_prediction.csv")
    if os.path.exists(fpath):
        df = pd.read_csv(fpath, encoding="utf-8-sig", low_memory=False)
        antes = df.shape[1]
        # Primera columna es un indice sin nombre
        if df.columns[0].startswith("Unnamed"):
            df = df.drop(columns=[df.columns[0]])
        # Columnas con >90% NaN
        umbral = 0.9 * len(df)
        cols_basura = [c for c in df.columns if df[c].isna().sum() > umbral]
        if cols_basura:
            df = df.drop(columns=cols_basura)
            print(f"  LIMPIADO  colombia_house_prediction.csv: "
                  f"{antes} cols -> {df.shape[1]} cols  (quitadas {len(cols_basura)}: {cols_basura})")
        # Columnas booleanas con valores mixtos: normalizar Si/No a 1/0
        for c in df.columns:
            if df[c].dtype == object:
                vals = df[c].dropna().unique()
                if set(vals).issubset({"Si", "No", "si", "no", "SI", "NO", 1.0, 0.0}):
                    df[c] = df[c].map({"Si": 1, "si": 1, "SI": 1,
                                        "No": 0, "no": 0, "NO": 0, 1.0: 1, 0.0: 0})
        df.to_csv(fpath, index=False, encoding="utf-8-sig")

    # real_estate_bogota.csv: columna Valor (string -> int)
    fpath = os.path.join(RAW, "real_estate_bogota.csv")
    if os.path.exists(fpath):
        df = pd.read_csv(fpath, encoding="utf-8-sig")
        if "Valor" in df.columns:
            antes = df["Valor"].dtype
            df["Valor"] = df["Valor"].astype(str).str.replace(r"[$\s\.]", "", regex=True)
            df["Valor"] = pd.to_numeric(df["Valor"], errors="coerce")
            print(f"  LIMPIADO  real_estate_bogota.csv: Valor {antes} -> int")
        df.to_csv(fpath, index=False, encoding="utf-8-sig")


# ── 7. ELIMINAR CARPETA arreglar_datos SI QUEDO VACIA ────
def limpiar_arreglar():
    print("\n=== 7. LIMPIAR CARPETA arreglar_datos ===")
    if os.path.exists(ARRE):
        resto = [f for f in os.listdir(ARRE) if not f.startswith(".")]
        if not resto:
            os.rmdir(ARRE)
            print(f"  ELIMINADA carpeta {ARRE}")
        else:
            print(f"  QUEDAN {len(resto)} archivos en arreglar_datos (no se elimina): {resto}")


# ── MAIN ──────────────────────────────────────────────────
def main():
    print("=" * 60)
    print("  ORGANIZAR DATASETS")
    print("  Accesibilidad de Vivienda en Colombia")
    print("=" * 60)

    eliminar_duplicados()
    renombrar()
    mover_desde_arreglar()
    corregir_encoding()
    convertir_xlsx_a_csv()
    limpiar_columnas()
    limpiar_arreglar()

    # Reporte final
    print("\n" + "=" * 60)
    print("  REPORTE FINAL: data/raw/")
    print("=" * 60)
    archivos = sorted([f for f in os.listdir(RAW) if not f.startswith(".")])
    total_mb = 0
    for f in archivos:
        fp = os.path.join(RAW, f)
        sz = os.path.getsize(fp)
        total_mb += sz
        print(f"  {f:<45s} {sz/1e6:>8.1f} MB")
    print(f"  {'':-<45s} {'--------'}")
    print(f"  {'TOTAL':<45s} {total_mb/1e6:>8.1f} MB  ({len(archivos)} archivos)")


if __name__ == "__main__":
    main()
