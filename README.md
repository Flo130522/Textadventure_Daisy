# Das Abenteuer des Rache-Dackels

Ein storygetriebenes Text-RPG über Daisy, ihre Gefährten und den Weg zu
Hubertus Snickers. Spielbar im Terminal oder in einer illustrierten
Desktop-Oberfläche.

## Aktueller Stand

Der spielbare Kern enthält:

- eine vollständige Kampagne vom Überfall auf Grauholz bis zum Thronsaal,
- drei unterschiedliche Enden durch Daisys letzte Entscheidung,
- eine verbundene Welt mit dreizehn Orten und mehreren Reichen,
- Reisen und Erkundung,
- stapelbare Gegenstände und ein mit dem Level wachsendes Inventar,
- einen rundenbasierten Kampf mit Lähmung, Schwächung und Vergiftung,
- Erfahrung, Level und Kampfstatistiken,
- skalierende Zufallsbegegnungen und fünf wiederholbare Dungeons,
- JSON-basierte Weltdaten und Spielstände,
- eine vollständig datengetriebene Geschichte mit Entscheidungen,
- Rekrutierungsquests für Leika, Bruno, Jack und Leo,
- individuelle Freundschaftswerte und Team-Boni,
- eine Lebensanzeige für Bosskämpfe,
- automatische Zugangssperren durch Storyfortschritt und Level.

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
  story.py      Storyknoten, Quests und Freundschaften
  data/         Editierbare Welt- und Gegnerdaten
  assets/       Illustrationen und visuelle Spielinhalte
tests/          Automatische Tests
docs/           Präsentation und ursprüngliche Systemskizze
run_game.py     Einfacher Einstiegspunkt
run_gui.py      Grafische Desktop-Version
```

## Denkbare Erweiterungen

- zusätzliche Nebenquests und optionale NPC-Dialoge
- eigene aktive Fähigkeiten für Daisys Freunde
- Musik, Animationen und weitere Illustrationen
