"""Interaktiver Spielablauf."""

from __future__ import annotations

import random
from collections.abc import Callable
from dataclasses import dataclass

from .models import Attack, Character, Enemy, Location

Input = Callable[[str], str]
Output = Callable[[str], None]


@dataclass
class Game:
    """Aktueller Zustand einer Spielrunde."""

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

    def attack(
        self,
        enemy: Enemy,
        rng: random.Random | None = None,
        attack: Attack | None = None,
    ) -> int:
        generator = rng or random
        selected_attack = attack or self.player.attacks[0]
        spread = 5 if selected_attack.name == "Sprung" else 3
        variation = generator.randint(-spread, spread)
        damage = max(1, self.player.attack_power + selected_attack.power + variation)
        return enemy.take_damage(damage)

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
            output("\n1. Erkunden  2. Reisen  3. Inventar  4. Status  5. Speichern  6. Beenden")
            choice = input_fn("> ").strip()

            if choice == "1":
                self._explore(input_fn, output)
            elif choice == "2":
                self._travel_menu(input_fn, output)
            elif choice == "3":
                self._inventory_menu(input_fn, output)
            elif choice == "4":
                self._show_stats(output)
            elif choice == "5":
                from .persistence import save_game

                save_game(self)
                output("Spielstand gespeichert.")
            elif choice == "6":
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

    def _show_stats(self, output: Output) -> None:
        victories = sum(self.player.defeated_enemies.values())
        visited = sum(location.visited for location in self.locations.values())
        output(f"\nLevel: {self.player.level}")
        output(f"EP: {self.player.experience}/{self.player.experience_for_next_level}")
        output(f"Besiegte Gegner: {victories}")
        output(f"Erkundete Orte: {visited}/{len(self.locations)}")
        if self.player.defeated_enemies:
            details = ", ".join(
                f"{name}: {count}" for name, count in self.player.defeated_enemies.items()
            )
            output(details)

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
        if (
            "Heilkraut" in self.player.inventory
            and self.player.health < self.player.max_health
            and input_fn("Heilkraut benutzen? (j/n) ").strip().lower() == "j"
        ):
            healed = self.player.use_healing_item()
            output(f"Daisy erhält {healed} Gesundheit zurück.")

    def _choose_attack(self, input_fn: Input, output: Output) -> Attack | None:
        for number, attack in enumerate(self.player.attacks, start=1):
            output(f"{number}. {attack.name} – {attack.description}")
        choice = input_fn("Attacke: ").strip()
        if not choice.isdigit() or not 1 <= int(choice) <= len(self.player.attacks):
            output("Unbekannte Attacke.")
            return None
        return self.player.attacks[int(choice) - 1]

    @staticmethod
    def _health_bar(enemy: Enemy, width: int = 20) -> str:
        ratio = enemy.health / max(1, enemy.max_health or enemy.health)
        filled = round(width * ratio)
        return f"[{'#' * filled}{'-' * (width - filled)}] {enemy.health}/{enemy.max_health}"

    def _battle(self, enemy: Enemy, input_fn: Input, output: Output) -> None:
        output(f"\n{enemy.name} greift an!")
        while self.player.is_alive and enemy.is_alive:
            output(f"Daisy: {self.player.health}/{self.player.max_health} LP")
            output(f"{enemy.name}: {self._health_bar(enemy)}")
            choice = input_fn("1. Angreifen  2. Heilkraut  3. Fliehen\n> ").strip()
            if choice == "1":
                selected_attack = self._choose_attack(input_fn, output)
                if selected_attack is None:
                    continue
                damage = self.attack(enemy, attack=selected_attack)
                output(f"{selected_attack.name} verursacht {damage} Schaden.")
            elif choice == "2":
                healed = self.player.use_healing_item()
                output(f"Daisy heilt {healed} LP." if healed else "Daisy hat kein Heilkraut.")
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
        self.player.record_victory(enemy.name)
        levels = self.player.gain_experience(enemy.experience_reward)
        output(f"Daisy erhält {enemy.experience_reward} EP.")
        if levels:
            output(f"Levelaufstieg! Daisy ist jetzt Level {self.player.level}.")
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
    """Startet ein neues Spiel oder lädt den lokalen Spielstand."""

    from .persistence import DEFAULT_SAVE_FILE, load_game
    from .world import create_game

    if DEFAULT_SAVE_FILE.exists():
        choice = input("1. Neues Spiel  2. Spiel laden\n> ").strip()
        game = load_game() if choice == "2" else create_game()
    else:
        game = create_game()
    game.run()


if __name__ == "__main__":
    main()
