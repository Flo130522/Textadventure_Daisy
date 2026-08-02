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
            locked_reason=location_data.get("locked_reason"),
            encounters=encounters,
            dungeon_name=location_data.get("dungeon_name"),
            dungeon_loot=list(location_data.get("dungeon_loot", [])),
            safe_haven=location_data.get("safe_haven", False),
        )
        if location.name in world:
            raise ValueError(f"Doppelter Ort: {location.name}")
        if location.required_level < 1:
            raise ValueError(f"Ungültiges Mindestlevel bei {location.name}")
        if len(location.connections) != len(set(location.connections)):
            raise ValueError(f"Doppelte Verbindung bei {location.name}")
        if enemy:
            if (
                enemy.health < 1
                or enemy.max_health is None
                or enemy.max_health < enemy.health
                or enemy.attack_power < 0
                or enemy.experience_reward < 0
            ):
                raise ValueError(f"Ungültige Gegnerwerte bei {location.name}")
            if enemy.behavior not in {"aggressive", "tactical", "boss"}:
                raise ValueError(f"Unbekanntes Gegnerverhalten bei {location.name}")
            if enemy.heal_power < 0 or (
                enemy.phase_threshold is not None
                and not 0 < enemy.phase_threshold <= 1
            ):
                raise ValueError(f"Ungültige Gegnerphase bei {location.name}")
            if not 0 <= enemy.effect_chance <= 1 or enemy.effect_duration < 0:
                raise ValueError(f"Ungültiger Statuseffekt bei {location.name}")
        if any(
            encounter.base_health < 1
            or encounter.base_attack < 0
            or encounter.base_experience < 0
            or not 0 <= encounter.effect_chance <= 1
            or encounter.effect_duration < 0
            for encounter in encounters
        ):
            raise ValueError(f"Ungültige Begegnungswerte bei {location.name}")
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
    locations = create_world()
    from .story import load_story, load_story_guidance, load_story_triggers

    trigger_locations = {trigger.location for trigger in load_story_triggers()}
    unknown_trigger_locations = trigger_locations - locations.keys()
    if unknown_trigger_locations:
        raise ValueError(f"Storytrigger an unbekannten Orten: {sorted(unknown_trigger_locations)}")
    guidance_locations = {
        item.destination for item in load_story_guidance() if item.destination is not None
    }
    unknown_guidance_locations = guidance_locations - locations.keys()
    if unknown_guidance_locations:
        raise ValueError(
            f"Storyhinweise an unbekannten Orten: {sorted(unknown_guidance_locations)}"
        )
    fixed_enemies = {
        location.enemy.name for location in locations.values() if location.enemy is not None
    }
    known_enemies = fixed_enemies | {
        encounter.name for location in locations.values() for encounter in location.encounters
    }
    nodes = load_story()
    for node in nodes.values():
        for choice in node.choices:
            quest = choice.effects.get("start_quest")
            if not quest:
                continue
            objective_type = quest.get("objective_type")
            objective_target = quest.get("objective_target")
            objective_location = quest.get("objective_location")
            if objective_type == "visit_location" and objective_target not in locations:
                raise ValueError(f"Questziel an unbekanntem Ort: {objective_target}")
            if objective_location and objective_location not in locations:
                raise ValueError(f"Questabgabe an unbekanntem Ort: {objective_location}")
            if objective_type == "defeat_enemy" and objective_target not in known_enemies:
                raise ValueError(f"Questziel mit unbekanntem Gegner: {objective_target}")
    return Game(player=daisy, locations=locations, current_location="Zuhause")
