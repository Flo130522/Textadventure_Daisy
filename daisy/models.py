"""Datenmodelle für Figuren und Spielwelt."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Character:
    name: str
    breed: str
    role: str
    max_health: int = 100
    attack_power: int = 18
    health: int = 100
    inventory: list[str] = field(default_factory=list)

    @property
    def is_alive(self) -> bool:
        return self.health > 0

    def take_damage(self, amount: int) -> int:
        damage = max(0, amount)
        self.health = max(0, self.health - damage)
        return damage

    def heal(self, amount: int) -> int:
        previous_health = self.health
        self.health = min(self.max_health, self.health + max(0, amount))
        return self.health - previous_health

    def add_item(self, item: str) -> None:
        self.inventory.append(item)

    def use_healing_item(self) -> int:
        if "Heilkraut" not in self.inventory:
            return 0
        self.inventory.remove("Heilkraut")
        return self.heal(30)


@dataclass
class Enemy:
    name: str
    health: int
    attack_power: int
    reward: str | None = None

    @property
    def is_alive(self) -> bool:
        return self.health > 0

    def take_damage(self, amount: int) -> int:
        damage = max(0, amount)
        self.health = max(0, self.health - damage)
        return damage


@dataclass
class Location:
    name: str
    description: str
    connections: list[str] = field(default_factory=list)
    items: list[str] = field(default_factory=list)
    enemy: Enemy | None = None
    visited: bool = False

    def connect(self, *location_names: str) -> None:
        for name in location_names:
            if name not in self.connections:
                self.connections.append(name)

