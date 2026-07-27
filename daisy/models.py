"""Datenmodelle für Figuren, Gegner, Attacken und Spielwelt."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Attack:
    """Eine auswählbare Kampffähigkeit."""

    name: str
    power: int
    description: str


def daisy_attacks() -> list[Attack]:
    """Daisys anfängliche Attacken."""

    return [
        Attack("Biss", 0, "Ein zuverlässiger Angriff."),
        Attack("Sprung", 5, "Mehr Schaden, aber mit größerer Streuung."),
        Attack("Kampfbellen", -3, "Ein vorsichtiger Angriff mit wenig Schaden."),
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

    @property
    def is_alive(self) -> bool:
        return self.health > 0

    @property
    def experience_for_next_level(self) -> int:
        return self.level * 100

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


@dataclass
class Location:
    """Ein Ort der Welt mit Verbindungen und optionaler Begegnung."""

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
