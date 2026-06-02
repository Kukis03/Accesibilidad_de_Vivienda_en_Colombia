"""
=============================================================
SCRAPING FINCARAIZ — VILLAVICENCIO  (v4 — API directa)
=============================================================
Proyecto: Accesibilidad de Vivienda en Colombia
Dataset:  A9 — Scraping propio
Objetivo: 3.000–6.000 registros de Villavicencio

Por qué v4 (historial):
  v1  — BeautifulSoup sobre HTML; la paginación se detenía en pág 1.
  v2  — Buscaba __NEXT_DATA__ solamente; FincaRaíz reparte los datos
        en varios <script>, no solo en __NEXT_DATA__.
  v3  — Buscaba en TODOS los <script>, PERO usaba el parámetro de URL
        ?pagina=N para iterar. **El servidor ignora ese parámetro**
        (Next.js + Apollo Client hace la paginación client-side).
        Por eso solo se obtenía la primera página de cada combinación.
  v4  — Llama directo a la API interna del frontend:
            POST https://search-service.fincaraiz.com.co/api/v1/listings/search
        Body JSON con:
            filter.locations.cities.id      = UUID de la ciudad
            filter.property_type.slug       = apartment | house | studio | ...
            filter.offer.slug                = sell | rent
            fields.limit / fields.offset     = paginación real
        Devuelve los items en hits.hits[]._source.listing
        (formato Elasticsearch: {took, hits: {total, hits}}).

        Hallazgos clave descubiertos en el diagnóstico:
          - property_type.slug usa inglés: "apartment", "house", "studio",
            "country-house", "lot", "project", ...
          - offer.slug es "sell" o "rent"
          - city.id es UUID ("ff817189-005a-4fa7-a8c5-6df23ff69881")
          - Paginación: offset += limit, hasta que hits.hits esté vacío
          - Límite recomendado: limit=50 (la API acepta más pero 50 evita timeouts)

Uso:
    py scraping_fincaraiz_villavicencio.py

Salida:
    ../data/raw/fincaraiz_villavicencio_scraping.csv
=============================================================
"""

import requests
import pandas as pd
import time, random, os
from datetime import datetime

# ── CONFIGURACIÓN ──────────────────────────────────────────
OUTPUT_DIR  = "../../data/raw"
OUTPUT_FILE = "fincaraiz_villavicencio_scraping.csv"

# (slug_url, slug_api, etiqueta_legible)
OPERACIONES = [
    ("venta",    "sell", "Venta"),
    ("arriendo", "rent", "Arriendo"),
]
TIPOS_INMUEBLE = [
    ("apartamentos",      "apartment",     "Apartamento"),
    ("casas",             "house",         "Casa"),
    ("apartaestudios",    "studio",        "Apartaestudio"),
    ("casas-campestres",  "country-house", "Casa Campestre"),
    ("lotes",             "lot",           "Lote"),
]

# UUID de la ciudad Villavicencio (no cambia)
CIUDAD_ID  = "ff817189-005a-4fa7-a8c5-6df23ff69881"
CIUDAD     = "Villavicencio"
DEPTO      = "Meta"
BASE_URL   = "https://www.fincaraiz.com.co"
SEARCH_API = "https://search-service.fincaraiz.com.co/api/v1/listings/search"

PAGE_SIZE  = 50        # items por request (la API soporta 50 sin problema)
MAX_PAGINAS = 40       # tope de seguridad: 40 * 50 = 2000 items por combo
PAUSA_MIN  = 1.0       # segundos entre requests (la API es más permisiva que el HTML)
PAUSA_MAX  = 2.5

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "es-CO,es;q=0.9,en;q=0.8",
    "Content-Type": "application/json",
    "Origin": BASE_URL,
    "Referer": BASE_URL + "/",
    "Connection": "keep-alive",
}


# ── UTILIDADES ─────────────────────────────────────────────

def _nid(v):
    """Extrae un id numérico de un campo tipo {id: N, name: '...', slug: '...'}."""
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return int(v)
    if isinstance(v, dict):
        x = v.get("id")
        if x is not None:
            return int(x) if str(x).isdigit() else None
        # Fallback: primer entero en 'name'
        if v.get("name"):
            import re
            m = re.search(r"\d+", str(v["name"]))
            return int(m.group()) if m else None
    return None


def _num(v):
    """Convierte a float/int si es numérico (string o número). None si no."""
    if v is None or v == "":
        return None
    if isinstance(v, (int, float)):
        return v
    if isinstance(v, str):
        try:
            return float(v)
        except ValueError:
            return None
    if isinstance(v, dict):
        return _num(v.get("amount") or v.get("price") or v.get("value"))
    return None


def _first_loc(locs, *keys):
    """Toma el primer elemento de cada key en locations."""
    for k in keys:
        arr = locs.get(k) or []
        if arr:
            return arr[0].get("name")
    return ""


def parsear_prop(item, op_label, tipo_label):
    """Convierte un listing (dict) en una fila CSV."""
    listing = item["_source"]["listing"]

    locs = listing.get("locations") or {}
    barrio = (_first_loc(locs, "neighbourhoods", "zones", "communes", "localities")
              or "").strip()
    ciudad_api  = _first_loc(locs, "cities")  or ""
    depto_api   = _first_loc(locs, "states")  or ""
    pais        = _first_loc(locs, "countries") or "Colombia"

    admin = listing.get("administration") or {}
    admin_precio = _num(admin.get("price"))

    precio = _num(listing.get("price"))
    if admin_precio and admin.get("is_included") is False and admin_precio > 0:
        pass  # admin separado, lo guardamos en su columna

    return {
        "id_anuncio":      listing.get("fr_property_id") or item.get("_id"),
        "uuid":            item.get("_id"),
        "precio_cop":      int(precio) if precio is not None else None,
        "admin_cop":       int(admin_precio) if admin_precio else None,
        "admin_incluida":  admin.get("is_included"),
        "tipo_inmueble":   tipo_label,
        "tipo_operacion":  op_label,
        "area_m2":         _num(listing.get("area")),
        "area_construida_m2": _num(listing.get("living_area")),
        "habitaciones":    _nid(listing.get("rooms")),
        "banos":           _nid(listing.get("baths")),
        "parqueaderos":    _nid(listing.get("garages")),
        "estrato":         _nid(listing.get("stratum")),
        "piso":            _nid(listing.get("floor")),
        "antiguedad":      (listing.get("age") or {}).get("name"),
        "estado":          (listing.get("condition") or {}).get("name"),
        "es_nuevo":        listing.get("is_new"),
        "barrio":          barrio,
        "ciudad":          ciudad_api or CIUDAD,
        "departamento":    depto_api or DEPTO,
        "pais":            pais,
        "titulo":          (listing.get("title") or "")[:150].strip(),
        "url_anuncio":     f"{BASE_URL}/inmueble/{item.get('_id')}",
        "fecha_scraping":  datetime.now().strftime("%Y-%m-%d"),
    }


# ── REQUEST ────────────────────────────────────────────────

def build_body(op_slug, tipo_slug, offset, limit=PAGE_SIZE):
    """Cuerpo del POST al search-service."""
    return {
        "filter": {
            "locations":    {"cities": {"id": [CIUDAD_ID]}},
            "property_type": {"slug": [tipo_slug]},
            "offer":        {"slug": [op_slug]},
        },
        "fields": {
            "include": [],
            "exclude": [],
            "limit":  limit,
            "offset": offset,
        },
    }


def get_pagina(body, sesion, intento=1):
    """POST al search-service con reintentos."""
    time.sleep(random.uniform(PAUSA_MIN, PAUSA_MAX))
    try:
        r = sesion.post(SEARCH_API, headers=HEADERS, json=body, timeout=25)
        if r.status_code == 200:
            return r.json()
        if r.status_code == 429 or r.status_code == 403:
            espera = 30 if r.status_code == 429 else 60
            print(f"    ⚠️  HTTP {r.status_code} — esperando {espera}s...", end=" ", flush=True)
            time.sleep(espera)
            if intento < 3:
                return get_pagina(body, sesion, intento + 1)
        print(f"    HTTP {r.status_code}: {r.text[:200]}")
        return None
    except requests.exceptions.Timeout:
        if intento < 3:
            time.sleep(10)
            return get_pagina(body, sesion, intento + 1)
        print("    Timeout.")
        return None
    except Exception as e:
        print(f"    Error: {e}")
        return None


# ── MAIN ───────────────────────────────────────────────────

def scrape_combo(sesion, op_slug, op_label, tipo_slug, tipo_label):
    """Scrapea una combinación operación×tipo. Devuelve lista de filas."""
    filas = []
    offset = 0
    pagina = 0
    total = None

    while pagina < MAX_PAGINAS:
        pagina += 1
        body = build_body(op_slug, tipo_slug, offset)
        print(f"  → Pág {pagina:02d} (offset {offset:>4}): ", end="", flush=True)

        data = get_pagina(body, sesion)
        if data is None:
            print("sin respuesta.")
            break

        hits_block = data.get("hits") or {}
        hits = hits_block.get("hits") or []
        if total is None:
            total = (hits_block.get("total") or {}).get("value", "?")

        if not hits:
            print("sin datos — fin.")
            break

        for item in hits:
            filas.append(parsear_prop(item, op_label, tipo_label))

        print(f"{len(hits)} items  (acum: {len(filas)}/{total})")

        # Si recibimos menos del tamaño de página, no hay más
        if len(hits) < PAGE_SIZE:
            print(f"  ℹ️  Página incompleta — última página.")
            break

        offset += PAGE_SIZE

    return filas, total


def main():
    print("=" * 60)
    print("  SCRAPING FINCARAÍZ — VILLAVICENCIO  (v4 — API directa)")
    print(f"  Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    todos  = []
    sesion = requests.Session()

    # Calentar la sesión (opcional, la API no lo exige, pero ayuda)
    print("\nCalentando sesión...")
    try:
        sesion.get(BASE_URL, headers=HEADERS, timeout=15)
    except Exception as e:
        print(f"  Aviso: warm-up falló ({e}), continuando...")
    time.sleep(2)

    total_combos = len(OPERACIONES) * len(TIPOS_INMUEBLE)
    n = 0

    for op_slug, op_api, op_label in OPERACIONES:
        for tipo_slug, tipo_api, tipo_label in TIPOS_INMUEBLE:
            n += 1
            print(f"\n[{n}/{total_combos}] {op_label.upper()} — {tipo_label}")
            filas, total = scrape_combo(sesion, op_api, op_label, tipo_api, tipo_label)
            print(f"  Subtotal: {len(filas)} de {total} disponibles")
            todos.extend(filas)

    # ── Guardar ────────────────────────────────────────────
    if not todos:
        print("\n⚠️  Sin registros. Revisa la conexión o espera 10 min.")
        return

    df = pd.DataFrame(todos)
    for col in ("precio_cop", "admin_cop", "area_m2", "area_construida_m2"):
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Deduplicar por fr_property_id (que es estable)
    antes = len(df)
    df = df.drop_duplicates(subset=["id_anuncio"])
    print(f"\n  Duplicados eliminados: {antes - len(df)}")

    ruta = os.path.join(OUTPUT_DIR, OUTPUT_FILE)
    df.to_csv(ruta, index=False, encoding="utf-8-sig")

    # ── Reporte ────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("  ✅  SCRAPING COMPLETADO")
    print(f"  Registros únicos:     {len(df)}")
    print(f"  Archivo:              {ruta}")
    print("=" * 60)

    print("\n── Distribución ──")
    print(df.groupby(["tipo_operacion", "tipo_inmueble"]).size().to_string())

    print("\n── Precios (COP) ──")
    for op_label, _ in [(o[2], o) for o in OPERACIONES]:
        sub = df[(df["tipo_operacion"] == op_label) & df["precio_cop"].notna()]
        if not sub.empty:
            print(f"  {op_label}: "
                  f"min=${sub['precio_cop'].min():>14,.0f} "
                  f"| med=${sub['precio_cop'].median():>14,.0f} "
                  f"| max=${sub['precio_cop'].max():>14,.0f}")

    print(f"\n  Con precio válido: {df['precio_cop'].notna().sum()}/{len(df)}")
    print(f"  Con área válida:   {df['area_m2'].notna().sum()}/{len(df)}")
    print(f"  Con barrio:        {df['barrio'].astype(bool).sum()}/{len(df)}")
    print(f"  Con estrato:       {df['estrato'].notna().sum()}/{len(df)}")


if __name__ == "__main__":
    main()
