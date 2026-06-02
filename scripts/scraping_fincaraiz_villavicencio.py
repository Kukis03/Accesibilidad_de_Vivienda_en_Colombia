"""
scraping_fincaraiz_villavicencio.py
Extrae listados de venta de FincaRaiz para Villavicencio (Meta) y los guarda
en data/raw/fincaraiz_villavicencio_scraping.csv con el esquema canónico del proyecto.

Dependencias: requests, beautifulsoup4, pandas (todas en el requirements.txt del proyecto)
Costo: $0 — acceso público sin autenticación
Tiempo estimado: 30–60 minutos para 3.000–5.000 listados

Uso:
    python scripts/scraping_fincaraiz_villavicencio.py
    python scripts/scraping_fincaraiz_villavicencio.py --max-paginas 50
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import logging
import argparse
from datetime import date
from pathlib import Path

# ── Configuración ────────────────────────────────────────────────────────────

BASE_URL = "https://www.fincaraiz.com.co/venta/apartamentos/villavicencio/"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "es-CO,es;q=0.9,en;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

DELAY_MIN = 2.0
DELAY_MAX = 4.5
MAX_PAGINAS_DEFAULT = 100

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)


def obtener_pagina(url: str, session: requests.Session) -> BeautifulSoup | None:
    try:
        resp = session.get(url, headers=HEADERS, timeout=20)
        resp.raise_for_status()
        return BeautifulSoup(resp.text, "html.parser")
    except requests.RequestException as e:
        log.warning(f"Error al obtener {url}: {e}")
        return None


def extraer_listados(soup: BeautifulSoup) -> list[dict]:
    propiedades = []

    tarjetas = soup.select("div.listing-card, article.card-property, div[data-testid='listing-card']")

    if not tarjetas:
        tarjetas = soup.select("[data-id]")

    for tarjeta in tarjetas:
        prop = {}
        try:
            precio_tag = tarjeta.select_one(
                ".price, .listing-price, [data-testid='price'], span.valor"
            )
            if precio_tag:
                precio_texto = precio_tag.get_text(strip=True)
                precio_num = precio_texto.replace("$", "").replace(".", "").replace(",", "").strip()
                if "M" in precio_num.upper():
                    precio_num = precio_num.upper().replace("M", "").strip()
                    prop["price"] = float(precio_num) * 1_000_000
                else:
                    prop["price"] = float(precio_num) if precio_num.isdigit() else None

            area_tag = tarjeta.select_one(
                ".area, .surface, [data-testid='area'], span.m2, li.area"
            )
            if area_tag:
                area_texto = area_tag.get_text(strip=True)
                area_num = "".join(c for c in area_texto if c.isdigit() or c == ".")
                prop["area"] = float(area_num) if area_num else None

            hab_tag = tarjeta.select_one(
                ".rooms, .bedrooms, [data-testid='rooms'], li.hab, span.habitaciones"
            )
            if hab_tag:
                hab_texto = "".join(c for c in hab_tag.get_text() if c.isdigit())
                prop["rooms"] = int(hab_texto) if hab_texto else None

            banos_tag = tarjeta.select_one(
                ".bathrooms, .baths, [data-testid='bathrooms'], li.bano, span.banos"
            )
            if banos_tag:
                banos_texto = "".join(c for c in banos_tag.get_text() if c.isdigit())
                prop["bathrooms"] = int(banos_texto) if banos_texto else None

            barrio_tag = tarjeta.select_one(
                ".location, .neighborhood, [data-testid='location'], span.barrio, p.ubicacion"
            )
            prop["barrio"] = barrio_tag.get_text(strip=True) if barrio_tag else None

            prop["property_type"] = None

            link_tag = tarjeta.select_one("a[href]")
            prop["url_listado"] = "https://www.fincaraiz.com.co" + link_tag["href"] if link_tag else None

            prop["city"] = "Villavicencio"
            prop["operation_type"] = "Venta"
            prop["currency"] = "COP"
            prop["created_on"] = str(date.today())
            prop["fuente"] = "scraping_fincaraiz"

            if prop.get("price") and prop["price"] > 0:
                propiedades.append(prop)

        except (ValueError, TypeError, AttributeError) as e:
            log.debug(f"Error extrayendo tarjeta: {e}")
            continue

    return propiedades


def hay_pagina_siguiente(soup: BeautifulSoup) -> bool:
    siguiente = soup.select_one(
        "a[rel='next'], .pagination-next, button.next-page, a.siguiente"
    )
    return siguiente is not None


def construir_url_pagina(pagina: int, tipo_inmueble: str = "apartamentos") -> str:
    base = f"https://www.fincaraiz.com.co/venta/{tipo_inmueble}/villavicencio/"
    if pagina == 1:
        return base
    return f"{base}?pagina={pagina}"


def scraping_villavicencio(
    tipos: list[str] = None,
    max_paginas: int = MAX_PAGINAS_DEFAULT,
    output_path: str = "data/raw/fincaraiz_villavicencio_scraping.csv"
) -> pd.DataFrame:
    if tipos is None:
        tipos = ["apartamentos", "casas"]

    todos_los_registros = []
    session = requests.Session()
    session.headers.update(HEADERS)

    for tipo in tipos:
        log.info(f"=== Iniciando scraping: {tipo} en Villavicencio ===")
        pagina = 1
        registros_tipo = 0

        while pagina <= max_paginas:
            url = construir_url_pagina(pagina, tipo)
            log.info(f"  Página {pagina}: {url}")

            soup = obtener_pagina(url, session)
            if soup is None:
                log.warning(f"  No se pudo obtener la página {pagina}. Deteniendo para {tipo}.")
                break

            listados = extraer_listados(soup)

            if not listados:
                log.info(f"  Sin listados en página {pagina}. Fin del tipo '{tipo}'.")
                break

            tipo_canónico = {
                "apartamentos": "Apartamento",
                "casas": "Casa",
                "lotes": "Lote/Terreno",
            }.get(tipo, tipo.capitalize())

            for r in listados:
                r["property_type"] = tipo_canónico

            todos_los_registros.extend(listados)
            registros_tipo += len(listados)
            log.info(f"  +{len(listados)} registros (total {tipo}: {registros_tipo})")

            if not hay_pagina_siguiente(soup):
                log.info(f"  Última página alcanzada para '{tipo}'.")
                break

            pagina += 1
            tiempo_espera = random.uniform(DELAY_MIN, DELAY_MAX)
            time.sleep(tiempo_espera)

        log.info(f"  Total extraído para {tipo}: {registros_tipo} registros")

    df = pd.DataFrame(todos_los_registros)

    if df.empty:
        log.warning("No se extrajo ningún registro. Verificar selectores CSS.")
        return df

    n_antes = len(df)
    df = df.drop_duplicates(subset=["url_listado"]).reset_index(drop=True)
    log.info(f"Deduplicados por URL: {n_antes - len(df)} eliminados. Total final: {len(df)}")

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    log.info(f"CSV exportado: {output_path} ({len(df)} filas)")

    log.info("\n--- Resumen de calidad del scraping ---")
    log.info(f"  Precio válido:  {df['price'].notna().sum()} / {len(df)} ({df['price'].notna().mean()*100:.1f}%)")
    log.info(f"  Área válida:    {df['area'].notna().sum()} / {len(df)} ({df['area'].notna().mean()*100:.1f}%)")
    log.info(f"  Habitaciones:   {df['rooms'].notna().sum()} / {len(df)} ({df['rooms'].notna().mean()*100:.1f}%)")
    log.info(f"  Precio mediano: ${df['price'].median():,.0f} COP")
    log.info(f"  Área mediana:   {df['area'].median():.0f} m²")

    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scraping FincaRaiz — Villavicencio")
    parser.add_argument("--max-paginas", type=int, default=MAX_PAGINAS_DEFAULT,
                        help=f"Máximo de páginas por tipo (default: {MAX_PAGINAS_DEFAULT})")
    parser.add_argument("--tipos", nargs="+", default=["apartamentos", "casas"],
                        choices=["apartamentos", "casas", "lotes"],
                        help="Tipos de inmueble a scrapear")
    parser.add_argument("--output", default="data/raw/fincaraiz_villavicencio_scraping.csv",
                        help="Ruta del CSV de salida")
    args = parser.parse_args()

    df_resultado = scraping_villavicencio(
        tipos=args.tipos,
        max_paginas=args.max_paginas,
        output_path=args.output
    )
    print(f"\n✅ Scraping completado: {len(df_resultado)} registros en {args.output}")
