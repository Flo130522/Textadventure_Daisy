# Daisy – Blindtest für die spielbare T0-Fassung

## Ziel

Der Test soll zeigen, ob eine Person Daisy ohne Erklärung spielen, nach einer
Pause fortsetzen und den nächsten sinnvollen Schritt selbst erkennen kann.
Neue Featureideen sind willkommen, werden aber getrennt von Blockern notiert.

## Vorbereitung

1. Die Testperson startet `python run_gui.py` selbst.
2. Erkläre weder Steuerung noch Lösungsweg.
3. Bitte sie, Erwartungen und Irritationen laut auszusprechen.
4. Hilf nur, wenn sie ausdrücklich nicht mehr weiterkommt; notiere dann Ort,
   sichtbare Aktionen und die benötigte Hilfe.

## Testauftrag

> Beginne ein neues Abenteuer. Spiele, bis Jack sich dem Team angeschlossen hat
> und du anschließend an einem sicheren Ort gespeichert hast. Beende das Spiel,
> starte es erneut und setze das Abenteuer über den Autosave oder einen manuellen
> Slot fort.

Wenn genug Zeit vorhanden ist, soll die Testperson danach bis zu einem Ende
weiterspielen.

## Beobachtungsliste

- War innerhalb von 30 Sekunden erkennbar, was als Nächstes zu tun ist?
  - Teilweise, USer können erwarten den aktuellen Ort noch weiter erkunden zu müssen anstelle zu Reisen
- Wurden Hauptziel und Questbuch verstanden?
  - Jap
- Waren gesperrte Reiseziele nachvollziehbar erklärt?
  - Nope, es steht nur dass der Weg versperrt ist aber nicht warum
- Wurden Kampf, Zielauswahl, Heilung und Flucht verstanden?
  - Jap
- War erkennbar, was Friendship und Partyboni bewirken?
  - Boni bei beiden nicht genau erkennbar, wird nicht offensichtlich angezeigt
- Waren Itemtyp, Ausrüstung und angelegte Boni verständlich?
  - Jap
- Funktionierten manueller Slot, Autosave, Beenden und Fortsetzen?
 - Jap
- Trat ein Absturz, Softlock, doppelter Lohn oder verlorener Fortschritt auf?
 - Nope
- Welche Passage fühlte sich zu langsam, zu leicht oder unfair an?
- Welcher Storymoment blieb besonders positiv oder negativ hängen?

## Einstufung

- **T0 Blocker:** Absturz, Saveverlust, Softlock oder Kampagne nicht fortsetzbar.
- **T0 Verständlichkeit:** Testperson benötigt Hilfe, obwohl die nötige Aktion
  verfügbar ist.
- **T1 Politur:** Spielbar, aber Rückmeldung, Text oder Bedienung ist unnötig
  umständlich.
- **Backlog:** Neuer Inhalt oder Komfortwunsch ohne Einfluss auf den Durchlauf.

## Ergebnisnotiz

```text
Testperson / Datum:
Erreichte Spielstelle:
Benötigte Zeit:
Verwendeter Save-Slot:

T0 Blocker:
-

T0 Verständlichkeit:
-

T1 Politur:
- Möglichkeit Artworks anzuklicken um sie zu vergrößern
- Beschreibung der Attacken 
- Healthbar der Gegner
- Jacks Aufgabe wird mit "Erkunden" abgeschlossen
- GUI etwas unscharf, soll sich an Systemauflösung orientieren
- Inventar nach "Gruppe" sortieren (Questitem, Verbrauch, etc.)
- Kapitel deutlich erweitern
- Möglichkeit Teammitgliedern Items zu schenken (erhöht deren Stats, aber je nach Itemstärke das Freundschaftslevel)
- Titelbild anders positionieren

Backlog-Ideen:
-
```
