"""Datenmodelle für Figuren, Gegner, Attacken und Spielwelt."""

from __future__ import annotations

import random
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Attack:
    """Eine auswählbare Kampffähigkeit."""

    name: str
    power: int
    description: str
    effect: str | None = None
    effect_chance: float = 0.0
    effect_duration: int = 0


def daisy_attacks() -> list[Attack]:
    """Daisys anfängliche Attacken."""

    return [
        Attack("Biss", 0, "Ein zuverlässiger Angriff."),
        Attack(
            "Sprung",
            5,
            "Hoher Schaden; kann Gegner kurz lähmen.",
            effect="Lähmung",
            effect_chance=0.25,
            effect_duration=1,
        ),
        Attack(
            "Kampfbellen",
            -3,
            "Wenig Schaden; kann den Angriff des Gegners schwächen.",
            effect="Geschwächt",
            effect_chance=0.4,
            effect_duration=2,
        ),
    ]


@dataclass
class Character:
    """Spielbare Figur mit Fortschritt und Inventar."""

    name: str
    breed: str
    role: str
    max_health: int = 100
    attack_power: int = 18
    health: int = 100
    inventory: list[str] = field(default_factory=list)
    attacks: list[Attack] = field(default_factory=daisy_attacks)
    level: int = 1
    experience: int = 0
    defeated_enemies: dict[str, int] = field(default_factory=dict)
    statuses: dict[str, int] = field(default_factory=dict)

    @property
    def is_alive(self) -> bool:
        return self.health > 0

    @property
    def experience_for_next_level(self) -> int:
        return self.level * 100

    @property
    def inventory_capacity(self) -> int:
        return 8 + self.level * 2

    def take_damage(self, amount: int) -> int:
        damage = max(0, amount)
        self.health = max(0, self.health - damage)
        return damage

    def heal(self, amount: int) -> int:
        previous_health = self.health
        self.health = min(self.max_health, self.health + max(0, amount))
        return self.health - previous_health

    def add_item(self, item: str) -> bool:
        if len(self.inventory) >= self.inventory_capacity:
            return False
        self.inventory.append(item)
        return True

    def use_healing_item(self) -> int:
        if "Heilkraut" not in self.inventory:
            return 0
        self.inventory.remove("Heilkraut")
        return self.heal(30)

    def gain_experience(self, amount: int) -> int:
        """Vergibt EP und gibt die Anzahl der neuen Level zurück."""

        self.experience += max(0, amount)
        levels_gained = 0
        while self.experience >= self.experience_for_next_level:
            self.experience -= self.experience_for_next_level
            self.level += 1
            self.max_health += 10
            self.health = self.max_health
            self.attack_power += 2
            levels_gained += 1
        return levels_gained

    def record_victory(self, enemy_name: str) -> None:
        self.defeated_enemies[enemy_name] = self.defeated_enemies.get(enemy_name, 0) + 1


@dataclass
class Enemy:
    """Gegner mit Belohnung und Erfahrungspunkten."""

    name: str
    health: int
    attack_power: int
    reward: str | None = None
    experience_reward: int = 30
    max_health: int | None = None
    status_effect: str | None = None
    effect_chance: float = 0.0
    effect_duration: int = 0
    statuses: dict[str, int] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.max_health is None:
            self.max_health = self.health

    @property
    def is_alive(self) -> bool:
        return self.health > 0

    def take_damage(self, amount: int) -> int:
        damage = max(0, amount)
        self.health = max(0, self.health - damage)
        return damage


@dataclass(frozen=True)
class EncounterTemplate:
    """Vorlage für skalierende Zufalls- und Dungeonbegegnungen."""

    name: str
    base_health: int
    base_attack: int
    base_experience: int
    status_effect: str | None = None
    effect_chance: float = 0.0
    effect_duration: int = 0

    def create_enemy(
        self,
        player_level: int,
        rng: random.Random | None = None,
    ) -> Enemy:
        generator = rng or random
        level = max(1, player_level + generator.randint(-1, 1))
        return Enemy(
            name=f"{self.name} (Level {level})",
            health=self.base_health + level * 12,
            attack_power=self.base_attack + level * 2,
            experience_reward=self.base_experience + level * 8,
            status_effect=self.status_effect,
            effect_chance=self.effect_chance,
            effect_duration=self.effect_duration,
        )


@dataclass
class Location:
    """Ein Ort der Welt mit Verbindungen und optionaler Begegnung."""

    name: str
    description: str
    connections: list[str] = field(default_factory=list)
    items: list[str] = field(default_factory=list)
    enemy: Enemy | None = None
    visited: bool = False
    required_level: int = 1
    required_flags: list[str] = field(default_factory=list)
    encounters: list[EncounterTemplate] = field(default_factory=list)
    dungeon_name: str | None = None

    def connect(self, *location_names: str) -> None:
        for name in location_names:
            if name not in self.connections:
                self.connections.append(name)
