"""
DIAGNÓSTICO FINCARAÍZ — corre esto y pégame el output completo
"""
import requests
from bs4 import BeautifulSoup
import json, re, os

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "es-CO,es;q=0.9,en;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Referer": "https://www.fincaraiz.com.co/",
}

URL = "https://www.fincaraiz.com.co/venta/apartamentos/villavicencio/meta/"

print("=" * 60)
print("DIAGNÓSTICO FINCARAÍZ")
print("=" * 60)

session = requests.Session()
session.get("https://www.fincaraiz.com.co/", headers=HEADERS, timeout=15)

import time; time.sleep(3)

r = session.get(URL, headers=HEADERS, timeout=20)
print(f"\nStatus HTTP:    {r.status_code}")
print(f"Bytes recibidos: {len(r.text)}")
print(f"Content-Type:   {r.headers.get('Content-Type','?')}")

soup = BeautifulSoup(r.text, "lxml")

# 1. Scripts
scripts = soup.find_all("script")
print(f"\nTotal <script> tags: {len(scripts)}")
for i, s in enumerate(scripts):
    txt = (s.string or "").strip()
    tipo = s.get("type","")
    sid  = s.get("id","")
    src  = s.get("src","")
    print(f"  [{i:02d}] id='{sid}' type='{tipo}' src='{src[:50]}' len={len(txt)}")
    if txt and len(txt) > 20:
        # Guardar el contenido de cada script para análisis
        fname = f"script_{i:02d}.txt"
        with open(fname, "w", encoding="utf-8") as f:
            f.write(txt)
        print(f"        → Primeros 150 chars: {txt[:150].replace(chr(10),' ')}")

# 2. Divs con clase
print(f"\nPrimeras 20 clases de <div>:")
for d in soup.find_all("div", class_=True)[:20]:
    print(f"  {d.get('class')}")

# 3. Buscar palabras clave de propiedades en el HTML
html_lower = r.text.lower()
for kw in ["precio", "price", "apartamento", "habitacion", "m²", "estrato",
           "listing", "property", "inmueble", "villavicencio"]:
    idx = html_lower.find(kw)
    if idx >= 0:
        print(f"\n  Keyword '{kw}' encontrado en pos {idx}:")
        print(f"    ...{r.text[max(0,idx-30):idx+80]}...")

# 4. Guardar HTML completo para inspección
with open("fincaraiz_raw.html", "w", encoding="utf-8") as f:
    f.write(r.text)
print(f"\nHTML completo guardado en: fincaraiz_raw.html")
print(f"(ábrelo en el navegador o en VS Code para ver la estructura)")

# 5. Primeros 500 chars del HTML
print(f"\nPrimeros 500 chars del HTML recibido:")
print(r.text[:500])
print("\n" + "=" * 60)
