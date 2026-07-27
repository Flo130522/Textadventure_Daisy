"""Interaktiver Spielablauf."""

from __future__ import annotations

import random
from collections import Counter
from collections.abc import Callable
from dataclasses import dataclass, field

from .models import Attack, Character, Enemy, Location
from .story import StoryEngine, StoryState

Input = Callable[[str], str]
Output = Callable[[str], None]


@dataclass
class Game:
    """Aktueller Zustand einer Spielrunde."""

    player: Character
    locations: dict[str, Location]
    current_location: str
    finished: bool = False
    story: StoryState = field(default_factory=StoryState)

    @property
    def location(self) -> Location:
        return self.locations[self.current_location]

    def travel(self, destination: str) -> bool:
        if destination not in self.location.connections:
            return False
        target = self.locations[destination]
        if self.player.level < target.required_level:
            return False
        if not set(target.required_flags).issubset(self.story.flags):
            return False
        self.current_location = destination
        return True

    def travel_block_reason(self, destination: str) -> str | None:
        if destination not in self.location.connections:
            return "Dieses Ziel ist von hier aus nicht erreichbar."
        target = self.locations[destination]
        if self.player.level < target.required_level:
            return f"Benötigtes Level: {target.required_level}"
        missing = set(target.required_flags) - self.story.flags
        if missing:
            return "Der Weg ist noch verborgen."
        return None

    def collect_items(self) -> list[str]:
        found: list[str] = []
        remaining: list[str] = []
        for item in self.location.items:
            if self.player.add_item(item):
                found.append(item)
            else:
                remaining.append(item)
        self.location.items = remaining
        return found

    def attack(
        self,
        enemy: Enemy,
        rng: random.Random | None = None,
        attack: Attack | None = None,
    ) -> int:
        generator = rng or random
        selected_attack = attack or self.player.attacks[0]
        self._apply_player_status_tick()
        spread = 5 if selected_attack.name == "Sprung" else 3
        variation = generator.randint(-spread, spread)
        damage = max(
            1,
            self.player.attack_power
            + selected_attack.power
            + variation
            + self._team_attack_bonus(),
        )
        dealt = enemy.take_damage(damage)
        if selected_attack.effect and generator.random() < selected_attack.effect_chance:
            enemy.statuses[selected_attack.effect] = selected_attack.effect_duration
        return dealt

    def enemy_attack(self, enemy: Enemy, rng: random.Random | None = None) -> int:
        generator = rng or random
        if enemy.statuses.get("Lähmung", 0) > 0:
            enemy.statuses["Lähmung"] -= 1
            return 0
        variation = generator.randint(-2, 2)
        weakened = 4 if enemy.statuses.get("Geschwächt", 0) > 0 else 0
        if weakened:
            enemy.statuses["Geschwächt"] -= 1
        damage = max(
            1,
            enemy.attack_power + variation - weakened - self._team_defense_bonus(),
        )
        dealt = self.player.take_damage(damage)
        if enemy.status_effect and generator.random() < enemy.effect_chance:
            self.player.statuses[enemy.status_effect] = enemy.effect_duration
        return dealt

    def _apply_player_status_tick(self) -> None:
        if self.player.statuses.get("Vergiftung", 0) > 0:
            self.player.take_damage(5)
            self.player.statuses["Vergiftung"] -= 1

    def _team_attack_bonus(self) -> int:
        bonus = 0
        if "Leika" in self.story.party:
            bonus += 2 + self.story.friendship_level("Leika")
        if "Leo" in self.story.party:
            bonus += 2 + self.story.friendship_level("Leo")
        return bonus

    def _team_defense_bonus(self) -> int:
        bonus = 0
        if "Bruno" in self.story.party:
            bonus += 2 + self.story.friendship_level("Bruno")
        if "Jack" in self.story.party:
            bonus += 1 + self.story.friendship_level("Jack")
        return bonus

    def complete_victory(self, enemy: Enemy) -> list[str]:
        """Verarbeitet Belohnungen und gibt passende Meldungen zurück."""

        messages = [f"{enemy.name} wurde besiegt!"]
        self.story.flags.add(f"defeated:{enemy.name}")
        self.player.record_victory(enemy.name)
        levels = self.player.gain_experience(enemy.experience_reward)
        messages.append(f"Daisy erhält {enemy.experience_reward} EP.")
        if levels:
            messages.append(f"Levelaufstieg! Daisy ist jetzt Level {self.player.level}.")
        if enemy.reward:
            self.player.add_item(enemy.reward)
            messages.append(f"Daisy erhält: {enemy.reward}")
        if "Jack" in self.story.party and self.player.is_alive:
            healing = 10 + self.story.friendship_level("Jack") * 5
            healed = self.player.heal(healing)
            if healed:
                messages.append(f"Jack versorgt das Team und heilt Daisy um {healed} LP.")
        return messages

    def update_location_quests(self) -> list[str]:
        """Aktualisiert Storyquests für den gegenwärtigen Ort."""

        messages: list[str] = []
        if self.current_location == "Dorfmarkt":
            quest = self.story.quests.get("trace_collectors")
            if quest and quest.advance():
                messages.extend(
                    [
                        f"Quest abgeschlossen: {quest.title}",
                        "Zwischen den Marktständen entdeckt Daisy Schleifspuren "
                        "und schwarzen Stoff. Die Eintreiber flohen in den Finsterwald.",
                    ]
                )
        if self.current_location == "Rettungs-Hundehütte":
            quest = self.story.quests.get("gather_herbs_for_jack")
            herb_count = self.player.inventory.count("Heilkraut")
            if quest and not quest.completed and herb_count >= quest.target:
                for _ in range(quest.target):
                    self.player.inventory.remove("Heilkraut")
                quest.advance(quest.target)
                messages.extend(
                    [
                        f"Quest abgeschlossen: {quest.title}",
                        "Jack kann genügend Medizin für die Verletzten herstellen.",
                    ]
                )
        return messages

    def activate_story_for_location(self) -> bool:
        return StoryEngine(self).activate_location_trigger()

    def create_encounter(self, rng: random.Random | None = None) -> Enemy | None:
        """Erzeugt eine zum Spielerlevel passende Begegnung am aktuellen Ort."""

        if not self.location.encounters:
            return None
        generator = rng or random
        template = generator.choice(self.location.encounters)
        return template.create_enemy(self.player.level, generator)

    def run(self, input_fn: Input = input, output: Output = print) -> None:
        output("Das Abenteuer des Rache-Dackels")
        output("Daisy gegen Hubertus Snickers\n")

        if not self.story.complete:
            self._run_story(input_fn, output)
            output("\nDie offene Welt ist nun verfügbar.")

        while self.player.is_alive and not self.finished:
            self._show_location(output)
            output(
                "\n1. Erkunden  2. Reisen  3. Inventar  4. Status  "
                "5. Speichern  6. Beenden  7. Dungeon"
            )
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
            elif choice == "7":
                self._dungeon(input_fn, output)
            else:
                output("Bitte wähle eine der angezeigten Nummern.")

        if not self.player.is_alive:
            output("\nDaisy wurde besiegt. Doch ein Rache-Dackel gibt niemals endgültig auf!")

    def _run_story(self, input_fn: Input, output: Output) -> None:
        engine = StoryEngine(self)
        while not self.story.complete:
            node = engine.current
            output(f"\n=== {node.title} ===")
            for paragraph in node.text:
                output(paragraph)
            for number, choice in enumerate(node.choices, start=1):
                output(f"{number}. {choice.label}")

            answer = input_fn("> ").strip()
            if not answer.isdigit() or not 1 <= int(answer) <= len(node.choices):
                output("Bitte wähle eine der angezeigten Nummern.")
                continue
            selected = node.choices[int(answer) - 1]
            for message in engine.choose(selected.id):
                output(message)

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
        for message in self.update_location_quests():
            output(message)
        if self.activate_story_for_location():
            self._run_story(input_fn, output)

    def _travel_menu(self, input_fn: Input, output: Output) -> None:
        connections = self.location.connections
        for number, name in enumerate(connections, start=1):
            output(f"{number}. {name}")
        choice = input_fn("Wohin? ").strip()
        if not choice.isdigit() or not 1 <= int(choice) <= len(connections):
            output("Dieses Reiseziel gibt es nicht.")
            return
        destination = connections[int(choice) - 1]
        reason = self.travel_block_reason(destination)
        if reason:
            output(reason)
            return
        self.travel(destination)
        if self.activate_story_for_location():
            self._run_story(input_fn, output)
        elif self.location.encounters and random.random() < 0.25:
            enemy = self.create_encounter()
            if enemy:
                output("Auf dem Weg lauert Daisy eine Gegnergruppe auf.")
                self._battle(enemy, input_fn, output)

    def _dungeon(self, input_fn: Input, output: Output) -> None:
        enemy = self.create_encounter()
        if enemy is None or not self.location.dungeon_name:
            output("An diesem Ort gibt es keinen zugänglichen Dungeon.")
            return
        output(f"Daisy betritt: {self.location.dungeon_name}")
        self._battle(enemy, input_fn, output)

    def _inventory_menu(self, input_fn: Input, output: Output) -> None:
        if not self.player.inventory:
            output("Daisys Inventar ist leer.")
            return
        stacks = ", ".join(
            f"{amount}× {item}" for item, amount in Counter(self.player.inventory).items()
        )
        output(
            f"Inventar ({len(self.player.inventory)}/{self.player.inventory_capacity}): {stacks}"
        )
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
        for message in self.complete_victory(enemy):
            output(message)
        if self.activate_story_for_location():
            self._run_story(input_fn, output)


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
