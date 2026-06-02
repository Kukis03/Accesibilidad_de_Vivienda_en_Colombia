"""
ANALIZADOR DE ESTRUCTURA — corre esto en tu carpeta scripts/
Lee el archivo fincaraiz_raw.html que ya tienes guardado
y muestra exactamente dónde están los datos de propiedades
"""
import json, re
from bs4 import BeautifulSoup

# Leer el HTML guardado
try:
    with open("fincaraiz_raw.html", "r", encoding="utf-8") as f:
        html = f.read()
    print(f"HTML cargado: {len(html):,} bytes")
except FileNotFoundError:
    print("ERROR: No se encontró fincaraiz_raw.html")
    print("Corre primero: py diagnostico_fincaraiz.py")
    exit()

soup = BeautifulSoup(html, "lxml")

# Buscar __NEXT_DATA__ (que el diagnóstico confirmó que existe)
script = soup.find("script", id="__NEXT_DATA__")
if not script:
    print("ERROR: No hay __NEXT_DATA__ en el HTML")
    exit()

print(f"__NEXT_DATA__ encontrado: {len(script.string):,} chars\n")
data = json.loads(script.string)

# Guardar JSON completo para inspección
with open("next_data_completo.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print("JSON guardado en: next_data_completo.json\n")

# ── Explorar estructura buscando listings y paginación ──
encontrados = []

def explorar(obj, path="", depth=0):
    if depth > 8:
        return
    if isinstance(obj, list) and len(obj) >= 3:
        if isinstance(obj[0], dict):
            keys0 = set(obj[0].keys())
            # Detectar si es una lista de propiedades
            prop_keys = {'price','id','listingId','precio','area','rooms',
                        'bedrooms','bathrooms','stratum','slug','title'}
            if keys0 & prop_keys:
                print(f"  🏠 LISTINGS en: {path}")
                print(f"     Cantidad: {len(obj)}")
                print(f"     Keys del primer item: {list(obj[0].keys())}")
                print(f"     Primer item (precio): {obj[0].get('price') or obj[0].get('precio') or obj[0].get('listingId','?')}")
                encontrados.append((path, len(obj), list(obj[0].keys())))
                return

    if isinstance(obj, dict):
        # Buscar claves de paginación
        for k, v in obj.items():
            if any(kw in k.lower() for kw in
                   ['page','total','count','pag','result','listing','found']):
                print(f"  📄 PAGINACIÓN posible — {path}.{k} = {str(v)[:80]}")
            
            if isinstance(v, (dict, list)):
                explorar(v, f"{path}.{k}", depth+1)

explorar(data)

print("\n── RESUMEN ──")
if encontrados:
    for path, cant, keys in encontrados:
        print(f"  Ruta: {path}")
        print(f"  Items: {cant}")
        print(f"  Columnas disponibles: {keys}")
else:
    print("  No se encontraron listings automáticamente")
    print("  Revisa next_data_completo.json manualmente")
    
    # Búsqueda de precio en el JSON como texto
    txt = json.dumps(data)
    # Buscar patrones de precio colombiano
    precios = re.findall(r'"price[^"]*"\s*:\s*(\d{7,12})', txt)
    if precios:
        print(f"\n  Precios encontrados en el JSON: {precios[:5]}")
        # Buscar el contexto del primer precio
        idx = txt.find(f'"price":{precios[0]}') 
        if idx < 0:
            idx = txt.find(precios[0])
        print(f"  Contexto: ...{txt[max(0,idx-100):idx+200]}...")
