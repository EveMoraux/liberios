"""Construit config.yaml = config.base.yaml + taches de « Mon suivi » (page Bonjour).

Usage : python scripts/bonjour_taches.py <dossier_json_bonjour>

Le dossier contient un fichier JSON par tache, tel que l'exporte la base de la
page Bonjour (collection data/users/me). Rubrique Priorites : taches « a faire »
et « en cours », en retard d'abord, puis par echeance et priorite. Rubrique
Rappels : taches « en attente », avec depuis quand.
"""
from __future__ import annotations

import datetime as dt
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
PRIO = {1: "high", 2: "normal", 3: "low"}
MAX_PRIORITIES = 7
MAX_REMINDERS = 4


def _date(value: object) -> dt.date | None:
    try:
        return dt.date.fromisoformat(str(value)[:10]) if value else None
    except ValueError:
        return None


def load_tasks(folder: Path) -> list[dict]:
    tasks = []
    for path in folder.glob("*.json"):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(data, dict) and data.get("title") and data.get("status"):
            tasks.append(data)
    return tasks


def build(tasks: list[dict], today: dt.date) -> tuple[list[dict], list[dict]]:
    active = [t for t in tasks if t["status"] in ("todo", "doing")]

    def key(t: dict):
        due = _date(t.get("due"))
        late = due is not None and due < today
        return (not late, due or dt.date.max, t.get("priority") or 2, t.get("order") or 0)

    priorities = []
    for t in sorted(active, key=key)[:MAX_PRIORITIES]:
        due = _date(t.get("due"))
        prio = PRIO.get(t.get("priority"), "normal")
        context = [t.get("tag") or ""]
        if t["status"] == "doing":
            context.append("en cours")
        if due and due < today:
            context.append(f"en retard depuis le {due:%d/%m}")
            if prio != "high":
                prio = "high"
        item = {"title": t["title"], "importance": prio,
                "context": " · ".join(c for c in context if c)}
        if due:
            item["due"] = f"{due.isoformat()}T18:00:00"
        priorities.append(item)

    waiting = [t for t in tasks if t["status"] == "waiting"]
    waiting.sort(key=lambda t: _date(t.get("waitingSince")) or dt.date.max)
    reminders = []
    for t in waiting[:MAX_REMINDERS]:
        since = _date(t.get("waitingSince"))
        context = "en attente" + (f" depuis {(today - since).days} j" if since else "")
        if t.get("tag"):
            context = f"{t['tag']} · {context}"
        reminders.append({"title": t["title"], "importance": "normal", "context": context})
    return priorities, reminders


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    folder = Path(sys.argv[1])
    config = yaml.safe_load((ROOT / "config.base.yaml").read_text(encoding="utf-8"))
    priorities, reminders = build(load_tasks(folder), dt.date.today())
    config["tasks"] = {"priorities": priorities, "reminders": reminders}
    (ROOT / "config.yaml").write_text(
        "# Genere automatiquement par scripts/bonjour_taches.py — modifier config.base.yaml\n"
        + yaml.safe_dump(config, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    print(f"config.yaml : {len(priorities)} priorites, {len(reminders)} rappels")


if __name__ == "__main__":
    main()
