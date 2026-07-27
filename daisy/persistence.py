"""JSON-basierte Speicherung von Spielständen."""

from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING, Any

from .models import Attack, Character, Enemy, Location

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
        locations[name] = Location(**location_data)
    return Game(
        player=player,
        locations=locations,
        current_location=data["current_location"],
        finished=data["finished"],
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
            }
            for attack in game.player.attacks
        ],
        "level": game.player.level,
        "experience": game.player.experience,
        "defeated_enemies": game.player.defeated_enemies,
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
            }
        locations[name] = {
            "name": location.name,
            "description": location.description,
            "connections": location.connections,
            "items": location.items,
            "enemy": enemy,
            "visited": location.visited,
        }
    return {
        "player": player,
        "locations": locations,
        "current_location": game.current_location,
        "finished": game.finished,
    }
