# Das Abenteuer des Rache-Dackels

Ein kleines Terminal-Textadventure über Daisy und ihren Weg durch Grauholz.

## Aktueller Stand

Der spielbare Kern enthält:

- eine verbundene Welt mit mehreren Orten,
- Reisen und Erkundung,
- Gegenstände und Inventar,
- einen einfachen rundenbasierten Kampf,
- ein erreichbares Spielziel.

Die früheren Experimente wurden aus dem aktuellen Projektstand entfernt. Sie
bleiben vollständig über die Git-Historie und die alten Branches erhalten.

## Voraussetzungen

- Python 3.10 oder neuer

Weitere Pakete werden für das Spiel nicht benötigt.

## Spiel starten

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
python -m pytest
```

## Projektstruktur

```text
daisy/
  game.py       Spielablauf und Benutzereingaben
  models.py     Figuren, Gegner und Orte
  world.py      Welt, Geschichte und Startzustand
tests/          Automatische Tests
docs/           Präsentation und ursprüngliche Systemskizze
run_game.py     Einfacher Einstiegspunkt
```

## Geplante Erweiterungen

- Speichern und Laden
- weitere Orte und Begegnungen
- individuelle Fähigkeiten für Daisys Freunde
- ausführlichere Geschichte und Dialoge
