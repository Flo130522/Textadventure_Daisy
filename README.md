# Das Abenteuer des Rache-Dackels

Ein storygetriebenes Text-RPG über Daisy, ihre Gefährten und den Weg zu
Hubertus Snickers. Spielbar im Terminal oder in einer illustrierten
Desktop-Oberfläche.

## Aktueller Stand

Der spielbare Kern enthält:

- eine vollständige Kampagne vom Überfall auf Grauholz bis zum Thronsaal,
- drei unterschiedliche Enden durch Daisys letzte Entscheidung,
- eine verbundene Welt mit neunzehn Orten und mehreren Reichen,
- Reisen und Erkundung,
- sichtbare Itemtypen, mehrere Heilitems und ein mit dem Level wachsendes Inventar,
- wechselbare Halsbänder mit angezeigten Angriffs- und Verteidigungsboni,
- geschützte Questgegenstände und geschützte ausgerüstete Items,
- einen rundenbasierten Kampf mit Lähmung, Schwächung und Vergiftung,
- Erfahrung, Level und Kampfstatistiken,
- skalierende Zufallsbegegnungen und neun wiederholbare Dungeons mit Beute,
- Gegnergruppen, deren Größe mit Daisys eigenem Team von eins bis vier wächst,
- sichere Baumhäuser zum Rasten, Speichern und Ausmisten des Inventars,
- drei manuelle Save-Slots, Autosave, Vorschau und Rettungskopie,
- JSON-basierte Weltdaten und Spielstände,
- eine vollständig datengetriebene Geschichte mit Entscheidungen,
- bedingte Entscheidungen anhand von Flags, Quests, Party, Level und Freundschaft,
- ein Questbuch mit Haupt-, Neben- und persönlichen Quests samt EP- und Itembelohnungen,
- illustrierte Schlüsselmomente in der GUI, die direkt von Storyknoten referenziert werden,
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
  game.py       Gemeinsamer Spielzustand und Terminal-Präsentation
  combat.py     Deterministische Kampf- und Gegnerregeln
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

## Architekturentscheidungen

JSON-Dateien beschreiben Welt, Story, Bedingungen und Effekte. `story.py`,
`combat.py` und die Methoden von `Game` wenden diese Regeln an; CLI und GUI
zeigen deren Ergebnisse nur an. Inventare bleiben zur Savegame-Kompatibilität
Listen aus Namen. Optionale Item-Metadaten und Ausrüstung erweitern dieses Format,
ohne alte Gegenstände umzuschreiben.

Neue Spielstände tragen eine Versionsnummer und werden atomar geschrieben.
`saved_game.json` bleibt der Standardpfad. `slot_path()` bietet zusätzlich eine
plattformgerechte Ablage für drei manuelle Slots und den Autosave. Die GUI nutzt
diese Slots direkt; vorhandene `saved_game.json`-Dateien können weiterhin über
das Lademenü geöffnet werden. Unversionierte Saves gelten beim Laden als Version
1. Beim Überschreiben bleibt der vorherige gültige Slot als `.bak` erhalten.

## Blindtest

Die vorbereitete Anleitung für einen Durchlauf ohne Entwicklerwissen liegt in
[`docs/PLAYTEST.md`](docs/PLAYTEST.md).

## Denkbare Erweiterungen

- zusätzliche Nebenquests und optionale NPC-Dialoge
- eigene aktive Fähigkeiten für Daisys Freunde
- Musik, Animationen und weitere Illustrationen

## Lizenz und Nutzung

Dieses Repository ist öffentlich einsehbar, steht derzeit jedoch nicht unter
einer Open-Source-Lizenz. Der Quellcode sowie Spielwelt, Story, Figuren,
Dialoge, Illustrationen und weitere Inhalte dürfen ohne vorherige schriftliche
Genehmigung nicht kopiert, verändert, weitergegeben oder für abgeleitete Spiele
verwendet werden. Weitere Informationen stehen in [LICENSE.md](LICENSE.md).

Hinweise zu Beiträgen, Verhalten und Sicherheitsmeldungen stehen in
[CONTRIBUTING.md](CONTRIBUTING.md), [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
und [SECURITY.md](SECURITY.md).
