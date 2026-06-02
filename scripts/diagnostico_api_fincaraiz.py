"""
DIAGNÓSTICO API FINCARAÍZ
Averigua qué devuelve la API interna de search-service.fincaraiz.com.co

Uso:
    py scripts/diagnostico_api_fincaraiz.py
"""

import os, sys
sys.stdout.reconfigure(encoding="utf-8")

import requests
import json

SEARCH_API = "https://search-service.fincaraiz.com.co/api/v1/listings/search"
BASE_URL   = "https://www.fincaraiz.com.co"
VILLAVO_ID = "ff817189-005a-4fa7-a8c5-6df23ff69881"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Origin": BASE_URL,
}

PROPERTY_SLUGS = {
    "apartment":     "Apartamento",
    "house":         "Casa",
    "studio":        "Apartaestudio",
    "country-house": "Casa Campestre",
    "lot":           "Lote",
    "project":       "Proyecto",
    "room":          "Habitación",
    "commercial":    "Local",
    "office":        "Oficina",
    "warehouse":     "Bodega",
    "building":      "Edificio",
    "farm":          "Finca",
    "cabin":         "Cabaña",
    "consulting-room": "Consultorio",
    "house-lot":     "Casa Lote",
}

OFFER_SLUGS = {"sell": "Venta", "rent": "Arriendo"}


def _post(body):
    r = requests.post(SEARCH_API, headers=HEADERS, json=body, timeout=15)
    r.raise_for_status()
    return r.json()


def api_info():
    """Muestra metadatos del endpoint OpenAPI."""
    print("\n=== META: ENDPOINTS DISPONIBLES ===")
    r = requests.get("https://search-service.fincaraiz.com.co/openapi.json", timeout=10).json()
    for path, methods in r["paths"].items():
        for method in methods:
            print(f"  {method.upper():>6}  {path}")


def quick_count():
    """Cuenta items por combinación principal."""
    print("\n=== CONTEO x OPERACIÓN x TIPO ===")
    for op_slug, op_label in OFFER_SLUGS.items():
        for prop_slug, prop_label in PROPERTY_SLUGS.items():
            body = {
                "filter": {
                    "locations": {"cities": {"id": [VILLAVO_ID]}},
                    "offer": {"slug": [op_slug]},
                    "property_type": {"slug": [prop_slug]},
                },
                "fields": {"include": [], "exclude": [], "limit": 1, "offset": 0},
            }
            try:
                data = _post(body)
                total = data["hits"]["total"]["value"]
                if total > 0:
                    print(f"  {op_label:>8} + {prop_label:<20} -> {total:>6} items")
            except Exception as e:
                print(f"  {op_label:>8} + {prop_label:<20} -> ERROR: {e}")


def show_sample(op_slug="sell", prop_slug="apartment", limit=3):
    """Muestra campos de N items de muestra."""
    print(f"\n=== MUESTRA: {OFFER_SLUGS[op_slug]} + {PROPERTY_SLUGS[prop_slug]} ({limit} items) ===")
    body = {
        "filter": {
            "locations": {"cities": {"id": [VILLAVO_ID]}},
            "offer": {"slug": [op_slug]},
            "property_type": {"slug": [prop_slug]},
        },
        "fields": {"include": [], "exclude": [], "limit": limit, "offset": 0},
    }
    data = _post(body)
    total = data["hits"]["total"]["value"]
    hits  = data["hits"]["hits"]
    print(f"  Total disponibles: {total}\n")

    for i, hit in enumerate(hits, 1):
        l = hit["_source"]["listing"]
        print(f"  --- Item {i} ---")
        print(f"    _id:             {hit['_id']}")
        print(f"    title:           {l.get('title')}")
        print(f"    price:           {l.get('price')}")
        print(f"    area:            {l.get('area')}")
        print(f"    living_area:     {l.get('living_area')}")
        print(f"    rooms:           {l.get('rooms')}")
        print(f"    baths:           {l.get('baths')}")
        print(f"    garages:         {l.get('garages')}")
        print(f"    stratum:         {l.get('stratum')}")
        print(f"    address:         {l.get('address')}")
        print(f"    administration:  {l.get('administration')}")
        print(f"    offer:           {l.get('offer')}")
        print(f"    property_type:   {l.get('property_type')}")
        print(f"    categories:      {l.get('categories')[:2]}...")
        print(f"    is_new:          {l.get('is_new')}")
        print(f"    condition:       {l.get('condition')}")
        print(f"    age:             {l.get('age')}")
        print(f"    floor:           {l.get('floor')}")
        print(f"    fr_property_id:  {l.get('fr_property_id')}")
        print(f"    property_id:     {l.get('property_id')}")
        print(f"    path:            {l.get('path')}")
        locs = l.get("locations", {})
        for key in ["countries", "states", "cities", "communes", "neighbourhoods"]:
            arr = locs.get(key, [])[:2]
            if arr:
                print(f"    locations.{key}: {[(x.get('name'), x.get('id','')[:20]) for x in arr]}")
        print()


def muestra_respuesta_cruda(op_slug="sell", prop_slug="apartment", max_chars=2000):
    """Imprime el JSON crudo de la respuesta (truncado)."""
    print(f"\n=== RESPUESTA CRUDA (JSON, {max_chars} chars) ===")
    body = {
        "filter": {
            "locations": {"cities": {"id": [VILLAVO_ID]}},
            "offer": {"slug": [op_slug]},
            "property_type": {"slug": [prop_slug]},
        },
        "fields": {"include": [], "exclude": [], "limit": 1, "offset": 0},
    }
    r = requests.post(SEARCH_API, headers=HEADERS, json=body, timeout=15)
    texto = json.dumps(r.json(), indent=2, ensure_ascii=False)
    print(texto[:max_chars])
    if len(texto) > max_chars:
        print(f"\n  ... (truncado, total {len(texto)} chars)")


def paginacion(op_slug="sell", prop_slug="apartment", max_pages=3):
    """Muestra cómo avanza la paginación."""
    print(f"\n=== PAGINACION: {OFFER_SLUGS[op_slug]} + {PROPERTY_SLUGS[prop_slug]} ===")
    offset = 0
    for p in range(1, max_pages + 1):
        body = {
            "filter": {
                "locations": {"cities": {"id": [VILLAVO_ID]}},
                "offer": {"slug": [op_slug]},
                "property_type": {"slug": [prop_slug]},
            },
            "fields": {"include": [], "exclude": [], "limit": 3, "offset": offset},
        }
        data = _post(body)
        total = data["hits"]["total"]["value"]
        hits  = data["hits"]["hits"]
        ids   = [h["_id"][:12] for h in hits]
        print(f"  Pag {p}: offset={offset:>4} -> {len(hits)} items  ids={ids}")
        if len(hits) < 3:
            break
        offset += 3


if __name__ == "__main__":
    print("=" * 60)
    print("  DIAGNÓSTICO API FINCARAÍZ (search-service)")
    print("=" * 60)

    api_info()
    quick_count()
    show_sample("sell", "apartment", 3)
    show_sample("rent", "house", 2)
    paginacion("sell", "apartment", 3)
    muestra_respuesta_cruda("sell", "apartment", 2500)
