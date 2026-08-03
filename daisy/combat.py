"""Zentrale, deterministisch testbare Kampfregeln."""

from __future__ import annotations

import random
from dataclasses import dataclass

from .models import Character, Enemy


@dataclass(frozen=True)
class EnemyTurn:
    action: str
    damage: int = 0
    healing: int = 0


def enemy_turn(
    player: Character,
    enemy: Enemy,
    defense_bonus: int,
    rng: random.Random | None = None,
) -> EnemyTurn:
    """Führt genau eine Gegneraktion aus."""

    generator = rng or random
    if not player.is_alive or not enemy.is_alive:
        return EnemyTurn("inactive")
    if enemy.statuses.get("Lähmung", 0) > 0:
        enemy.statuses["Lähmung"] -= 1
        if enemy.statuses["Lähmung"] <= 0:
            del enemy.statuses["Lähmung"]
        return EnemyTurn("paralyzed")

    health_ratio = enemy.health / max(1, enemy.max_health or enemy.health)
    if enemy.heal_power and health_ratio <= 0.35 and generator.random() < 0.6:
        old_health = enemy.health
        enemy.health = min(enemy.max_health or enemy.health, enemy.health + enemy.heal_power)
        return EnemyTurn("heal", healing=enemy.health - old_health)

    if enemy.statuses.pop("Vorbereitung", 0):
        return _deal_damage(player, enemy, defense_bonus, generator, power_bonus=6, action="strong")

    phase_active = enemy.phase_threshold is not None and health_ratio <= enemy.phase_threshold
    roll = generator.random()
    if enemy.behavior in {"tactical", "boss"} and roll < (0.35 if phase_active else 0.2):
        enemy.statuses["Verteidigung"] = 1
        return EnemyTurn("defend")
    if enemy.behavior in {"tactical", "boss"} and roll < (0.7 if phase_active else 0.4):
        enemy.statuses["Vorbereitung"] = 1
        return EnemyTurn("prepare")
    return _deal_damage(player, enemy, defense_bonus, generator)


def _deal_damage(
    player: Character,
    enemy: Enemy,
    defense_bonus: int,
    generator: random.Random,
    *,
    power_bonus: int = 0,
    action: str = "attack",
) -> EnemyTurn:
    weakened = 4 if enemy.statuses.get("Geschwächt", 0) > 0 else 0
    if weakened:
        enemy.statuses["Geschwächt"] -= 1
        if enemy.statuses["Geschwächt"] <= 0:
            del enemy.statuses["Geschwächt"]
    damage = max(
        1,
        enemy.attack_power + generator.randint(-2, 2) + power_bonus - weakened - defense_bonus,
    )
    dealt = player.take_damage(damage)
    if enemy.status_effect and generator.random() < enemy.effect_chance:
        player.statuses[enemy.status_effect] = enemy.effect_duration
    return EnemyTurn(action, damage=dealt)
