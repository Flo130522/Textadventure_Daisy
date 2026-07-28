"""Lädt die Spielwelt aus einer JSON-Datei."""

from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING, Any

from .models import Character, EncounterTemplate, Enemy, Location

if TYPE_CHECKING:
    from .game import Game

WORLD_FILE = Path(__file__).parent / "data" / "world.json"


def load_world_data(path: Path = WORLD_FILE) -> dict[str, Any]:
    """Liest und validiert die grundlegende Struktur der Weltdaten."""

    with path.open(encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data.get("locations"), list):
        raise TypeError("Die Weltdatei benötigt eine Liste 'locations'.")
    return data


def create_world(path: Path = WORLD_FILE) -> dict[str, Location]:
    """Erzeugt Spielobjekte aus den deklarativen Weltdaten."""

    world: dict[str, Location] = {}
    for location_data in load_world_data(path)["locations"]:
        enemy_data = location_data.get("enemy")
        enemy = Enemy(**enemy_data) if enemy_data else None
        encounters = [
            EncounterTemplate(**encounter) for encounter in location_data.get("encounters", [])
        ]
        location = Location(
            name=location_data["name"],
            description=location_data["description"],
            connections=list(location_data.get("connections", [])),
            items=list(location_data.get("items", [])),
            enemy=enemy,
            required_level=location_data.get("required_level", 1),
            required_flags=list(location_data.get("required_flags", [])),
            encounters=encounters,
            dungeon_name=location_data.get("dungeon_name"),
        )
        world[location.name] = location

    for location in world.values():
        unknown = set(location.connections) - world.keys()
        if unknown:
            raise ValueError(f"Unbekannte Verbindung bei {location.name}: {sorted(unknown)}")
    return world


def create_game() -> Game:
    """Erzeugt einen neuen Spielstand."""

    from .game import Game

    daisy = Character(
        name="Daisy",
        breed="Rauhaardackel-Terrier-Mix",
        role="Nahkampf-Spezialistin",
    )
    return Game(player=daisy, locations=create_world(), current_location="Zuhause")
