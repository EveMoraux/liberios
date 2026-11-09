"""Prepare le numero du jour pour la page LibERIOS (une page, un numero par jour).

Usage : python scripts/preparer_edition.py AAAA-MM-JJ

- copie output/preview/<date>-signal-matin.html vers output/site/editions/<date>.html
- ajoute la date a output/site/editions.json (le fichier deja publie, s'il a ete
  recupere au prealable a cet endroit ; sinon la liste repart de cette date)
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "output" / "site"
WEB_LAYER = ROOT / "web" / "liberios" / "edition-web.html"


def main() -> None:
    if len(sys.argv) != 2 or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", sys.argv[1]):
        sys.exit(__doc__)
    day = sys.argv[1]
    source = ROOT / "output" / "preview" / f"{day}-signal-matin.html"
    if not source.exists():
        sys.exit(f"Numero introuvable : {source}")
    (SITE / "editions").mkdir(parents=True, exist_ok=True)
    html = source.read_text(encoding="utf-8")
    # Couche web : pages qui s'allongent au lieu de couper, carnet et jeux modifiables.
    layer = WEB_LAYER.read_text(encoding="utf-8")
    html = html.replace("</body>", layer + "</body>", 1)
    (SITE / "editions" / f"{day}.html").write_text(html, encoding="utf-8")

    manifest = SITE / "editions.json"
    try:
        days = [d for d in json.loads(manifest.read_text(encoding="utf-8"))
                if isinstance(d, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", d)]
    except (OSError, ValueError):
        days = []
    days = sorted(set(days) | {day}, reverse=True)
    manifest.write_text(json.dumps(days), encoding="utf-8")
    print(f"{len(days)} numeros dans editions.json ; a publier : editions/{day}.html")


if __name__ == "__main__":
    main()
