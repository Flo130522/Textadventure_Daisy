"""Aufbau der Spielwelt und des Startzustands."""

from __future__ import annotations

from .models import Character, Enemy, Location


def create_world() -> dict[str, Location]:
    world = {
        "Zuhause": Location(
            "Zuhause",
            "Daisys Elternhaus. Eine Blutspur führt zur offenen Haustür.",
            items=["Heilkraut"],
        ),
        "Grauholz": Location(
            "Grauholz",
            "Ein sonst friedliches Dorf. Heute sind die Straßen verdächtig still.",
        ),
        "Dorfmarkt": Location(
            "Dorfmarkt",
            "Zwischen verlassenen Ständen liegt eine zerrissene Karte.",
            items=["Karte des Finsterwalds"],
        ),
        "Finsterwald": Location(
            "Finsterwald",
            "Dichte Zweige verschlucken das Tageslicht.",
            enemy=Enemy("Spinnen-Monster", health=42, attack_power=9, reward="Silberner Schlüssel"),
        ),
        "Hundewacht": Location(
            "Hundewacht",
            "Die Stadtmauer trägt das Zeichen von Hubertus Snickers.",
        ),
        "Chihuahua-Höllenreich": Location(
            "Chihuahua-Höllenreich",
            "Hinter dem schwarzen Tor wartet Hubertus Snickers.",
            enemy=Enemy("Hubertus Snickers", health=70, attack_power=13),
        ),
    }

    _connect_both(world, "Zuhause", "Grauholz")
    _connect_both(world, "Grauholz", "Dorfmarkt")
    _connect_both(world, "Dorfmarkt", "Finsterwald")
    _connect_both(world, "Finsterwald", "Hundewacht")
    _connect_both(world, "Hundewacht", "Chihuahua-Höllenreich")
    return world


def _connect_both(world: dict[str, Location], first: str, second: str) -> None:
    world[first].connect(second)
    world[second].connect(first)


def create_game() -> "Game":
    # Lokaler Import vermeidet einen zyklischen Modulimport.
    from .game import Game

    daisy = Character(
        name="Daisy",
        breed="Rauhaardackel-Terrier-Mix",
        role="Nahkampf-Spezialistin",
    )
    return Game(player=daisy, locations=create_world(), current_location="Zuhause")

