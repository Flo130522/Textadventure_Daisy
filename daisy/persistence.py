"""JSON-basierte Speicherung von Spielständen."""

from __future__ import annotations

import json
import os
import shutil
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any

from .models import (
    Attack,
    Character,
    EncounterTemplate,
    Enemy,
    Location,
    daisy_attacks,
    item_definition,
)
from .story import QuestState, StoryEngine, StoryState, load_story

if TYPE_CHECKING:
    from .game import Game

DEFAULT_SAVE_FILE = Path("saved_game.json")
SAVE_VERSION = 2
MANUAL_SLOTS = ("slot-1", "slot-2", "slot-3")


@dataclass(frozen=True)
class SaveMetadata:
    """Kleine, ohne vollständiges Laden lesbare Vorschau eines Spielstands."""

    slot: str
    path: Path
    location: str
    level: int
    chapter: str
    modified: datetime


def user_save_directory(app_name: str = "Daisy") -> Path:
    """Liefert einen plattformgerechten Ordner für optionale Save-Slots."""

    if sys.platform == "win32":
        base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
    elif sys.platform == "darwin":
        base = Path.home() / "Library" / "Application Support"
    else:
        base = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
    return base / app_name


def slot_path(slot: str, directory: Path | None = None) -> Path:
    if not slot or not all(character.isalnum() or character in "-_" for character in slot):
        raise ValueError("Ein Save-Slot darf nur Buchstaben, Zahlen, '-' und '_' enthalten.")
    return (directory or user_save_directory()) / f"{slot}.json"


def save_slot(game: Game, slot: str, directory: Path | None = None) -> Path:
    path = slot_path(slot, directory)
    save_game(game, path)
    return path


def load_slot(slot: str, directory: Path | None = None) -> Game:
    path = slot_path(slot, directory)
    try:
        return load_game(path)
    except (OSError, TypeError, ValueError, KeyError, json.JSONDecodeError):
        backup = _backup_path(path)
        if not backup.exists():
            raise
        return load_game(backup)


def autosave(game: Game, directory: Path | None = None) -> Path:
    return save_slot(game, "autosave", directory)


def available_saves(directory: Path | None = None) -> list[SaveMetadata]:
    """Liefert gültige Slot-Vorschauen; kaputte Dateien blockieren das Menü nicht."""

    result = []
    for slot in ("autosave", *MANUAL_SLOTS):
        path = slot_path(slot, directory)
        readable_path = path if path.exists() else _backup_path(path)
        if not readable_path.exists():
            continue
        try:
            data = json.loads(readable_path.read_text(encoding="utf-8"))
            result.append(
                SaveMetadata(
                    slot=slot,
                    path=path,
                    location=str(data["current_location"]),
                    level=int(data["player"]["level"]),
                    chapter=str(data.get("story", {}).get("chapter", "Altes Abenteuer")),
                    modified=datetime.fromtimestamp(readable_path.stat().st_mtime),
                )
            )
        except (OSError, TypeError, ValueError, KeyError, json.JSONDecodeError):
            backup = _backup_path(path)
            if readable_path == backup or not backup.exists():
                continue
            try:
                data = json.loads(backup.read_text(encoding="utf-8"))
                result.append(
                    SaveMetadata(
                        slot=slot,
                        path=path,
                        location=str(data["current_location"]),
                        level=int(data["player"]["level"]),
                        chapter=str(data.get("story", {}).get("chapter", "Altes Abenteuer")),
                        modified=datetime.fromtimestamp(backup.stat().st_mtime),
                    )
                )
            except (OSError, TypeError, ValueError, KeyError, json.JSONDecodeError):
                continue
    return result


def save_game(game: Game, path: Path = DEFAULT_SAVE_FILE) -> None:
    """Speichert den vollständigen veränderlichen Spielzustand."""

    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(_game_to_dict(game), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    # Das vorherige, erfolgreich lesbare Save bleibt als Rettungskopie erhalten.
    if path.exists():
        try:
            existing = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(existing, dict):
                shutil.copy2(path, _backup_path(path))
        except (OSError, json.JSONDecodeError):
            pass
    temporary.replace(path)


def _backup_path(path: Path) -> Path:
    return path.with_suffix(path.suffix + ".bak")


def load_game(path: Path = DEFAULT_SAVE_FILE) -> Game:
    """Lädt einen zuvor gespeicherten Spielzustand."""

    from .game import Game

    raw_data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw_data, dict):
        raise TypeError("Der Spielstand muss ein JSON-Objekt sein.")
    data = _migrate_save(raw_data)
    player_data = dict(data["player"])
    player_data["attacks"] = [
        Attack(**attack) for attack in player_data.get("attacks", [])
    ] or daisy_attacks()
    player_data.setdefault("equipment", {})
    player = Character(**player_data)
    player.equipment = {
        slot: item
        for slot, item in player.equipment.items()
        if item in player.inventory and item_definition(item).slot == slot
    }

    locations: dict[str, Location] = {}
    for name, location_data in data["locations"].items():
        location_data = dict(location_data)
        enemy_data = location_data.pop("enemy", None)
        location_data["enemy"] = Enemy(**enemy_data) if enemy_data else None
        location_data["encounters"] = [
            EncounterTemplate(**encounter) for encounter in location_data.get("encounters", [])
        ]
        locations[name] = Location(**location_data)
    game = Game(
        player=player,
        locations=locations,
        current_location=data["current_location"],
        finished=data.get("finished", False),
        story=_story_from_dict(data.get("story")),
    )
    _validate_loaded_game(game)
    return game


def _game_to_dict(game: Game) -> dict[str, Any]:
    player = {
        "name": game.player.name,
        "breed": game.player.breed,
        "role": game.player.role,
        "max_health": game.player.max_health,
        "attack_power": game.player.attack_power,
        "health": game.player.health,
        "inventory": game.player.inventory,
        "attacks": [
            {
                "name": attack.name,
                "power": attack.power,
                "description": attack.description,
                "effect": attack.effect,
                "effect_chance": attack.effect_chance,
                "effect_duration": attack.effect_duration,
            }
            for attack in game.player.attacks
        ],
        "level": game.player.level,
        "experience": game.player.experience,
        "defeated_enemies": game.player.defeated_enemies,
        "statuses": game.player.statuses,
        "equipment": game.player.equipment,
    }
    locations = {}
    for name, location in game.locations.items():
        enemy = None
        if location.enemy:
            enemy = {
                "name": location.enemy.name,
                "health": location.enemy.health,
                "attack_power": location.enemy.attack_power,
                "reward": location.enemy.reward,
                "experience_reward": location.enemy.experience_reward,
                "max_health": location.enemy.max_health,
                "status_effect": location.enemy.status_effect,
                "effect_chance": location.enemy.effect_chance,
                "effect_duration": location.enemy.effect_duration,
                "statuses": location.enemy.statuses,
                "behavior": location.enemy.behavior,
                "heal_power": location.enemy.heal_power,
                "phase_threshold": location.enemy.phase_threshold,
                "victory_processed": location.enemy.victory_processed,
            }
        locations[name] = {
            "name": location.name,
            "description": location.description,
            "connections": location.connections,
            "items": location.items,
            "enemy": enemy,
            "visited": location.visited,
            "required_level": location.required_level,
            "required_flags": location.required_flags,
            "locked_reason": location.locked_reason,
            "encounters": [
                {
                    "name": encounter.name,
                    "base_health": encounter.base_health,
                    "base_attack": encounter.base_attack,
                    "base_experience": encounter.base_experience,
                    "status_effect": encounter.status_effect,
                    "effect_chance": encounter.effect_chance,
                    "effect_duration": encounter.effect_duration,
                }
                for encounter in location.encounters
            ],
            "dungeon_name": location.dungeon_name,
            "dungeon_loot": location.dungeon_loot,
            "safe_haven": location.safe_haven,
        }
    return {
        "save_version": SAVE_VERSION,
        "player": player,
        "locations": locations,
        "current_location": game.current_location,
        "finished": game.finished,
        "story": _story_to_dict(game.story),
    }


def _story_to_dict(story: StoryState) -> dict[str, Any]:
    return {
        "current_node": story.current_node,
        "chapter": story.chapter,
        "complete": story.complete,
        "flags": sorted(story.flags),
        "choices": story.choices,
        "friendship": story.friendship,
        "party": story.party,
        "quests": {
            quest_id: {
                "title": quest.title,
                "description": quest.description,
                "status": quest.status,
                "progress": quest.progress,
                "target": quest.target,
                "kind": quest.kind,
                "reward_experience": quest.reward_experience,
                "reward_items": quest.reward_items,
                "rewards_claimed": quest.rewards_claimed,
                "objective_type": quest.objective_type,
                "objective_target": quest.objective_target,
                "objective_location": quest.objective_location,
                "completion_text": quest.completion_text,
            }
            for quest_id, quest in story.quests.items()
        },
    }


def _story_from_dict(data: dict[str, Any] | None) -> StoryState:
    if data is None:
        # Alte Spielstände beginnen direkt in der bereits freigeschalteten Welt.
        return StoryState(complete=True, chapter="Kapitel I – Asche über Grauholz")
    return StoryState(
        current_node=data.get("current_node", "prologue_morning"),
        chapter=data.get("chapter", "Prolog – Der letzte friedliche Morgen"),
        complete=data.get("complete", False),
        flags=set(data.get("flags", [])),
        choices=dict(data.get("choices", {})),
        friendship=dict(data.get("friendship", {})),
        party=list(data.get("party", [])),
        quests={
            quest_id: QuestState(**quest) for quest_id, quest in data.get("quests", {}).items()
        },
    )


def _migrate_save(data: dict[str, Any]) -> dict[str, Any]:
    """Ergänzt ausschließlich Felder, die alten Spielständen fehlen."""

    version = data.get("save_version", 1)
    if not isinstance(version, int) or version < 1 or version > SAVE_VERSION:
        raise ValueError(f"Nicht unterstützte Savegame-Version: {version}")
    if "player" not in data or "locations" not in data or "current_location" not in data:
        raise ValueError("Der Spielstand enthält nicht alle erforderlichen Kerndaten.")
    if data["current_location"] not in data["locations"]:
        raise ValueError("Der aktuelle Ort existiert nicht im Spielstand.")
    migrated = dict(data)
    migrated["save_version"] = SAVE_VERSION
    return migrated


def _validate_loaded_game(game: Game) -> None:
    player = game.player
    if player.level < 1 or player.max_health < 1 or not 0 <= player.health <= player.max_health:
        raise ValueError("Der Spielstand enthält ungültige Spielerwerte.")
    if not all(isinstance(item, str) and item for item in player.inventory):
        raise ValueError("Der Spielstand enthält ungültige Inventareinträge.")
    if any(name != location.name for name, location in game.locations.items()):
        raise ValueError("Ortsschlüssel und Ortsnamen im Spielstand stimmen nicht überein.")
    for location in game.locations.values():
        unknown = set(location.connections) - game.locations.keys()
        if unknown:
            raise ValueError(f"Unbekannte Verbindung im Spielstand: {sorted(unknown)}")
        if location.enemy and (
            location.enemy.max_health is None
            or location.enemy.max_health < 1
            or not 0 <= location.enemy.health <= location.enemy.max_health
            or location.enemy.attack_power < 0
        ):
            raise ValueError(f"Ungültige Gegnerwerte im Spielstand: {location.name}")
    known_nodes = load_story()
    if game.story.current_node not in known_nodes:
        raise ValueError(f"Unbekannter Storyknoten im Spielstand: {game.story.current_node}")
    if not game.story.complete and not StoryEngine(game, nodes=known_nodes).available_choices:
        raise ValueError("Der Spielstand befindet sich in einem Storyknoten ohne gültige Auswahl.")
    game.story.party = list(dict.fromkeys(game.story.party))
    for quest in game.story.quests.values():
        if quest.target < 1 or not 0 <= quest.progress <= quest.target:
            raise ValueError("Der Spielstand enthält ungültigen Questfortschritt.")
        if quest.status not in {"active", "completed"}:
            raise ValueError(f"Unbekannter Queststatus: {quest.status}")
        if quest.completed != (quest.progress == quest.target):
            raise ValueError("Queststatus und Questfortschritt stimmen nicht überein.")
