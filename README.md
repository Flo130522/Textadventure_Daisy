# Das Abenteuer des Rache-Dackels

Ein kleines Terminal-Textadventure über Daisy und ihren Weg durch Grauholz.

## Aktueller Stand

Der spielbare Kern enthält:

- eine verbundene Welt mit mehreren Orten,
- Reisen und Erkundung,
- Gegenstände und Inventar,
- einen rundenbasierten Kampf mit mehreren Attacken,
- Erfahrung, Level und Kampfstatistiken,
- JSON-basierte Weltdaten und Spielstände,
- eine Lebensanzeige für Bosskämpfe,
- ein erreichbares Spielziel.

Die früheren Experimente wurden aus dem aktuellen Projektstand entfernt. Sie
bleiben vollständig über die Git-Historie und die alten Branches erhalten.

## Voraussetzungen

- Python 3.10 oder neuer

Weitere Pakete werden für das Spiel nicht benötigt.

## Spiel starten

Grafische Desktop-Version:

```bash
python run_gui.py
```

Terminal-Version:

```bash
python run_game.py
```

Alternativ:

```bash
python -m daisy
```

Im Spiel werden die verfügbaren Aktionen jeweils als Nummern angezeigt.

## Tests ausführen

```bash
python -m pip install ".[dev]"
python -m pytest
ruff check daisy tests run_game.py
```

## Projektstruktur

```text
daisy/
  game.py       Spielablauf und Benutzereingaben
  models.py     Figuren, Gegner und Orte
  world.py      Laden und Validieren der Welt
  persistence.py  Speichern und Laden als JSON
  data/         Editierbare Welt- und Gegnerdaten
tests/          Automatische Tests
docs/           Präsentation und ursprüngliche Systemskizze
assets/         Illustrationen und visuelle Spielinhalte
run_game.py     Einfacher Einstiegspunkt
run_gui.py      Grafische Desktop-Version
```

## Geplante Erweiterungen

- weitere Orte und Begegnungen
- individuelle Fähigkeiten für Daisys Freunde
- ausführlichere Geschichte und Dialoge
