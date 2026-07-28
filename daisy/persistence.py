"""JSON-basierte Speicherung von Spielständen."""

from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING, Any

from .models import Attack, Character, EncounterTemplate, Enemy, Location
from .story import QuestState, StoryState

if TYPE_CHECKING:
    from .game import Game

DEFAULT_SAVE_FILE = Path("saved_game.json")


def save_game(game: Game, path: Path = DEFAULT_SAVE_FILE) -> None:
    """Speichert den vollständigen veränderlichen Spielzustand."""

    path.write_text(
        json.dumps(_game_to_dict(game), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def load_game(path: Path = DEFAULT_SAVE_FILE) -> Game:
    """Lädt einen zuvor gespeicherten Spielzustand."""

    from .game import Game

    data = json.loads(path.read_text(encoding="utf-8"))
    player_data = data["player"]
    player_data["attacks"] = [Attack(**attack) for attack in player_data["attacks"]]
    player = Character(**player_data)

    locations: dict[str, Location] = {}
    for name, location_data in data["locations"].items():
        enemy_data = location_data.pop("enemy")
        location_data["enemy"] = Enemy(**enemy_data) if enemy_data else None
        location_data["encounters"] = [
            EncounterTemplate(**encounter) for encounter in location_data.get("encounters", [])
        ]
        locations[name] = Location(**location_data)
    return Game(
        player=player,
        locations=locations,
        current_location=data["current_location"],
        finished=data["finished"],
        story=_story_from_dict(data.get("story")),
    )


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
            }
            for quest_id, quest in story.quests.items()
        },
    }


def _story_from_dict(data: dict[str, Any] | None) -> StoryState:
    if data is None:
        # Alte Spielstände beginnen direkt in der bereits freigeschalteten Welt.
        return StoryState(complete=True, chapter="Kapitel I – Asche über Grauholz")
    return StoryState(
        current_node=data["current_node"],
        chapter=data["chapter"],
        complete=data["complete"],
        flags=set(data.get("flags", [])),
        choices=dict(data.get("choices", {})),
        friendship=dict(data.get("friendship", {})),
        party=list(data.get("party", [])),
        quests={
            quest_id: QuestState(**quest) for quest_id, quest in data.get("quests", {}).items()
        },
    )
