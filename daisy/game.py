"""Interaktiver Spielablauf."""

from __future__ import annotations

import random
from collections.abc import Callable
from dataclasses import dataclass

from .models import Character, Enemy, Location

Input = Callable[[str], str]
Output = Callable[[str], None]


@dataclass
class Game:
    player: Character
    locations: dict[str, Location]
    current_location: str
    finished: bool = False

    @property
    def location(self) -> Location:
        return self.locations[self.current_location]

    def travel(self, destination: str) -> bool:
        if destination not in self.location.connections:
            return False
        self.current_location = destination
        return True

    def collect_items(self) -> list[str]:
        found = list(self.location.items)
        self.player.inventory.extend(found)
        self.location.items.clear()
        return found

    def attack(self, enemy: Enemy, rng: random.Random | None = None) -> int:
        generator = rng or random
        variation = generator.randint(-3, 3)
        return enemy.take_damage(self.player.attack_power + variation)

    def enemy_attack(self, enemy: Enemy, rng: random.Random | None = None) -> int:
        generator = rng or random
        variation = generator.randint(-2, 2)
        return self.player.take_damage(enemy.attack_power + variation)

    def run(self, input_fn: Input = input, output: Output = print) -> None:
        output("Das Abenteuer des Rache-Dackels")
        output("Daisy gegen Hubertus Snickers\n")
        output(
            "Hubertus' Gefolge hat Grauholz überfallen. "
            "Daisy folgt der Spur und schwört, ihn aufzuhalten."
        )

        while self.player.is_alive and not self.finished:
            self._show_location(output)
            output("\n1. Erkunden  2. Reisen  3. Inventar  4. Beenden")
            choice = input_fn("> ").strip()

            if choice == "1":
                self._explore(input_fn, output)
            elif choice == "2":
                self._travel_menu(input_fn, output)
            elif choice == "3":
                self._inventory_menu(input_fn, output)
            elif choice == "4":
                output("Daisy setzt ihr Abenteuer später fort.")
                return
            else:
                output("Bitte wähle eine der angezeigten Nummern.")

        if not self.player.is_alive:
            output("\nDaisy wurde besiegt. Doch ein Rache-Dackel gibt niemals endgültig auf!")

    def _show_location(self, output: Output) -> None:
        output(f"\n=== {self.location.name} ===")
        output(self.location.description)
        output(f"Gesundheit: {self.player.health}/{self.player.max_health}")

    def _explore(self, input_fn: Input, output: Output) -> None:
        location = self.location
        first_visit = not location.visited
        location.visited = True
        found = self.collect_items()

        if found:
            output("Gefunden: " + ", ".join(found))
        elif first_visit:
            output("Daisy untersucht jeden Winkel, findet aber nichts.")
        else:
            output("Hier gibt es im Moment nichts Neues zu entdecken.")

        if location.enemy and location.enemy.is_alive:
            self._battle(location.enemy, input_fn, output)

    def _travel_menu(self, input_fn: Input, output: Output) -> None:
        connections = self.location.connections
        for number, name in enumerate(connections, start=1):
            output(f"{number}. {name}")
        choice = input_fn("Wohin? ").strip()
        if not choice.isdigit() or not 1 <= int(choice) <= len(connections):
            output("Dieses Reiseziel gibt es nicht.")
            return
        self.travel(connections[int(choice) - 1])

    def _inventory_menu(self, input_fn: Input, output: Output) -> None:
        if not self.player.inventory:
            output("Daisys Inventar ist leer.")
            return
        output("Inventar: " + ", ".join(self.player.inventory))
        if "Heilkraut" in self.player.inventory and self.player.health < self.player.max_health:
            if input_fn("Heilkraut benutzen? (j/n) ").strip().lower() == "j":
                healed = self.player.use_healing_item()
                output(f"Daisy erhält {healed} Gesundheit zurück.")

    def _battle(self, enemy: Enemy, input_fn: Input, output: Output) -> None:
        output(f"\n{enemy.name} greift an!")
        while self.player.is_alive and enemy.is_alive:
            output(
                f"Daisy: {self.player.health} LP | "
                f"{enemy.name}: {enemy.health} LP"
            )
            choice = input_fn("1. Angreifen  2. Heilkraut  3. Fliehen\n> ").strip()
            if choice == "1":
                damage = self.attack(enemy)
                output(f"Daisy verursacht {damage} Schaden.")
            elif choice == "2":
                healed = self.player.use_healing_item()
                output(
                    f"Daisy heilt {healed} LP."
                    if healed
                    else "Daisy hat kein Heilkraut."
                )
                if not healed:
                    continue
            elif choice == "3":
                output("Daisy zieht sich zurück.")
                return
            else:
                output("Ungültige Auswahl.")
                continue

            if enemy.is_alive:
                damage = self.enemy_attack(enemy)
                output(f"{enemy.name} verursacht {damage} Schaden.")

        if enemy.is_alive:
            return
        output(f"{enemy.name} wurde besiegt!")
        if enemy.reward:
            self.player.add_item(enemy.reward)
            output(f"Daisy erhält: {enemy.reward}")
        if enemy.name == "Hubertus Snickers":
            self.finished = True
            output(
                "\nHubertus ist geschlagen. Grauholz ist frei – "
                "und Daisy wird zur Heldin des Dorfes!"
            )


def main() -> None:
    from .world import create_game

    create_game().run()


if __name__ == "__main__":
    main()

