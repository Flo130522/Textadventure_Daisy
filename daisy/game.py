"""Interaktiver Spielablauf."""

from __future__ import annotations

import random
from collections import Counter
from collections.abc import Callable
from dataclasses import dataclass, field

from .combat import EnemyTurn
from .combat import enemy_turn as resolve_enemy_turn
from .models import Attack, Character, Enemy, Location, item_definition
from .story import QuestState, StoryEngine, StoryState, load_story_guidance

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
            return target.locked_reason or "Der Weg ist noch verborgen. Folge zuerst dem Hauptziel."
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
        if not self.player.is_alive:
            return 0
        spread = 5 if selected_attack.name == "Sprung" else 3
        variation = generator.randint(-spread, spread)
        damage = max(
            1,
            self.player.attack_power
            + selected_attack.power
            + variation
            + self._team_attack_bonus()
            + self.player.equipment_attack_bonus,
        )
        if enemy.statuses.pop("Verteidigung", 0):
            damage = max(1, damage // 2)
        dealt = enemy.take_damage(damage)
        if selected_attack.effect and generator.random() < selected_attack.effect_chance:
            enemy.statuses[selected_attack.effect] = selected_attack.effect_duration
        return dealt

    def enemy_attack(self, enemy: Enemy, rng: random.Random | None = None) -> int:
        return self.enemy_turn(enemy, rng).damage

    def enemy_turn(self, enemy: Enemy, rng: random.Random | None = None) -> EnemyTurn:
        return resolve_enemy_turn(
            self.player,
            enemy,
            self._team_defense_bonus() + self.player.equipment_defense_bonus,
            rng,
        )

    def resolve_enemy_action(
        self, enemy: Enemy, rng: random.Random | None = None
    ) -> tuple[EnemyTurn, str]:
        """Gemeinsame Gegneraktion samt Text für CLI und GUI."""

        result = self.enemy_turn(enemy, rng)
        messages = {
            "inactive": f"{enemy.name} kann nicht handeln.",
            "paralyzed": f"{enemy.name} ist gelähmt und setzt aus.",
            "defend": f"{enemy.name} geht in Verteidigung.",
            "prepare": f"{enemy.name} bereitet einen starken Angriff vor!",
            "heal": f"{enemy.name} regeneriert {result.healing} LP.",
            "strong": f"{enemy.name} entfesselt den starken Angriff: {result.damage} Schaden.",
            "attack": f"{enemy.name} verursacht {result.damage} Schaden.",
        }
        return result, messages[result.action]

    def _apply_player_status_tick(self) -> None:
        if self.player.statuses.get("Vergiftung", 0) > 0:
            self.player.take_damage(5)
            self.player.statuses["Vergiftung"] -= 1
            if self.player.statuses["Vergiftung"] <= 0:
                del self.player.statuses["Vergiftung"]

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

        if enemy.is_alive or enemy.victory_processed:
            return []
        enemy.victory_processed = True
        messages = [f"{enemy.name} wurde besiegt!"]
        self.story.flags.add(f"defeated:{enemy.name}")
        self.player.record_victory(enemy.name)
        levels = self.player.gain_experience(enemy.experience_reward)
        messages.append(f"Daisy erhält {enemy.experience_reward} EP.")
        if levels:
            messages.append(f"Levelaufstieg! Daisy ist jetzt Level {self.player.level}.")
        if enemy.reward:
            if self.player.add_item(enemy.reward):
                messages.append(f"Daisy erhält: {enemy.reward}")
            else:
                self.location.items.append(enemy.reward)
                messages.append(f"Inventar voll – {enemy.reward} liegt am Ort bereit.")
        messages.extend(self.process_quest_event("defeat_enemy", enemy.name))
        if "Jack" in self.story.party and self.player.is_alive:
            healing = 10 + self.story.friendship_level("Jack") * 5
            healed = self.player.heal(healing)
            if healed:
                messages.append(f"Jack versorgt das Team und heilt Daisy um {healed} LP.")
        return messages

    def advance_quest(self, quest_id: str, amount: int = 1, *, complete: bool = False) -> list[str]:
        """Aktualisiert eine Quest und vergibt ihre Belohnung genau einmal."""

        quest = self.story.quests.get(quest_id)
        if quest is None or quest.completed:
            return []
        completed = quest.advance(quest.target if complete else amount)
        if not completed:
            return []

        messages = [f"Quest abgeschlossen: {quest.title}"]
        if quest.completion_text:
            messages.append(quest.completion_text)
        if not quest.rewards_claimed:
            levels = self.player.gain_experience(quest.reward_experience)
            if quest.reward_experience:
                messages.append(f"Questbelohnung: {quest.reward_experience} EP.")
            if levels:
                messages.append(f"Levelaufstieg! Daisy ist jetzt Level {self.player.level}.")
            for item in quest.reward_items:
                if self.player.add_item(item):
                    messages.append(f"Questbelohnung: {item}")
                else:
                    self.location.items.append(item)
                    messages.append(f"Inventar voll – Questbelohnung {item} liegt am Ort bereit.")
            quest.rewards_claimed = True
        return messages

    def process_quest_event(self, objective_type: str, target: str) -> list[str]:
        """Wendet ein Gameplay-Ereignis auf passende aktive Quests an."""

        messages: list[str] = []
        for quest_id, quest in self.story.quests.items():
            if quest.completed or quest.objective_type != objective_type:
                continue
            target_matches = quest.objective_target == target
            if objective_type == "defeat_enemy" and quest.objective_target:
                target_matches = target_matches or target.startswith(
                    f"{quest.objective_target} (Level "
                )
            if not target_matches:
                continue
            if quest.objective_location and quest.objective_location != self.current_location:
                continue

            amount = 1
            if objective_type == "deliver_item":
                amount = min(
                    self.player.inventory.count(target),
                    quest.target - quest.progress,
                )
                if amount <= 0:
                    continue
                for _ in range(amount):
                    self.player.inventory.remove(target)
                messages.append(f"Abgegeben: {amount}× {target}")
            messages.extend(self.advance_quest(quest_id, amount))
        return messages

    def quest_summary(self) -> list[str]:
        labels = {"main": "Hauptquest", "side": "Nebenquest", "personal": "Persönlich"}
        status_labels = {"active": "Aktiv", "completed": "Abgeschlossen"}
        summaries = []
        quests = sorted(
            self.story.quests.values(),
            key=lambda quest: (
                quest.completed,
                {"main": 0, "personal": 1, "side": 2}.get(quest.kind, 3),
                quest.title,
            ),
        )
        for quest in quests:
            heading = (
                f"[{labels.get(quest.kind, quest.kind)}] {quest.title}: "
                f"{quest.progress}/{quest.target} – {status_labels.get(quest.status, quest.status)}"
            )
            objective = None if quest.completed else self._quest_objective_text(quest)
            detail = "Abgeschlossen." if quest.completed else objective or quest.description
            summaries.append(f"{heading}\n{detail}")
        return summaries

    def primary_objective(self) -> str:
        """Kurzes nächstes Ziel für die ständig sichtbare Statusanzeige."""

        turn_ins = self.available_quest_turn_ins()
        if turn_ins:
            _quest_id, quest = turn_ins[0]
            return f"Übergib {quest.objective_target} für „{quest.title}“."
        guidance = next(
            (item for item in load_story_guidance() if item.matches(self)),
            None,
        )
        if guidance:
            return guidance.text
        active = [quest for quest in self.story.quests.values() if not quest.completed]
        if not active:
            return "Erkunde die Welt und folge Daisys Geschichte."
        quest = min(
            active,
            key=lambda item: ({"main": 0, "personal": 1, "side": 2}.get(item.kind, 3), item.title),
        )
        objective = self._quest_objective_text(quest) or quest.description
        if objective.startswith("Ziel: "):
            objective = objective.removeprefix("Ziel: ")
        return f"{quest.title}: {objective}"

    def inventory_summary(self, *, detailed: bool = True) -> list[str]:
        kind_labels = {
            "consumable": "Verbrauch",
            "equipment": "Ausrüstung",
            "quest": "Questitem",
            "misc": "Beute",
        }
        summaries = []
        items = Counter(self.player.inventory).items()
        ordered_items = sorted(
            items,
            key=lambda entry: (
                {"quest": 0, "equipment": 1, "consumable": 2, "misc": 3}.get(
                    item_definition(entry[0]).kind, 4
                ),
                entry[0] not in self.player.equipment.values(),
                entry[0],
            ),
        )
        for item, amount in ordered_items:
            definition = item_definition(item)
            equipped = " – angelegt" if item in self.player.equipment.values() else ""
            summary = (
                f"{amount}× {item} [{kind_labels.get(definition.kind, definition.kind)}]{equipped}"
            )
            if detailed:
                summary += f": {definition.description}"
            summaries.append(summary)
        return summaries

    def party_summary(self) -> list[str]:
        """Erklärt Freundschaft, Perks und die tatsächlich aktiven Team-Boni."""

        summaries = []
        for character in self.story.party:
            level = self.story.friendship_level(character)
            points = self.story.friendship.get(character, 0)
            perks = ", ".join(self.story.friendship_perks(character)) or "Noch kein Perk"
            bonus = {
                "Leika": f"Angriff +{2 + level}",
                "Leo": f"Angriff +{2 + level}",
                "Bruno": f"Verteidigung +{2 + level}",
                "Jack": (f"Verteidigung +{1 + level}; heilt nach Siegen {10 + level * 5} LP"),
            }.get(character, "Kein aktiver Kampfbonus")
            summaries.append(
                f"{character} – Freundschaft {points} Punkte / Stufe {level}\n"
                f"Perks: {perks}\nBonus: {bonus}"
            )
        return summaries

    def available_consumables(self) -> list[str]:
        return [
            item
            for item in dict.fromkeys(self.player.inventory)
            if item_definition(item).kind == "consumable" and item_definition(item).healing > 0
        ]

    @staticmethod
    def _quest_objective_text(quest: QuestState) -> str | None:
        if quest.objective_type == "visit_location":
            return f"Ziel: {quest.objective_target} besuchen."
        if quest.objective_type == "defeat_enemy":
            return f"Ziel: {quest.objective_target} besiegen."
        if quest.objective_type == "deliver_item":
            destination = f" nach {quest.objective_location}" if quest.objective_location else ""
            remaining = max(0, quest.target - quest.progress)
            return f"Ziel: {remaining}× {quest.objective_target}{destination} bringen."
        return None

    def update_location_quests(self) -> list[str]:
        """Aktualisiert Storyquests für den gegenwärtigen Ort."""

        return self.process_quest_event("visit_location", self.current_location)

    def available_quest_turn_ins(self) -> list[tuple[str, QuestState]]:
        return [
            (quest_id, quest)
            for quest_id, quest in self.story.quests.items()
            if not quest.completed
            and quest.objective_type == "deliver_item"
            and quest.objective_target in self.player.inventory
            and (not quest.objective_location or quest.objective_location == self.current_location)
        ]

    def turn_in_quest(self, quest_id: str) -> list[str]:
        quest = self.story.quests.get(quest_id)
        if not quest or (quest_id, quest) not in self.available_quest_turn_ins():
            return ["Diese Quest kann hier gerade nicht abgegeben werden."]
        return self.process_quest_event("deliver_item", quest.objective_target or "")

    def activate_story_for_location(self) -> bool:
        return StoryEngine(self).activate_location_trigger()

    def create_encounter(
        self,
        rng: random.Random | None = None,
        *,
        dungeon: bool = False,
    ) -> Enemy | None:
        """Erzeugt eine zum Spielerlevel passende Begegnung am aktuellen Ort."""

        if not self.location.encounters:
            return None
        generator = rng or random
        template = generator.choice(self.location.encounters)
        enemy = template.create_enemy(self.player.level, generator)
        if dungeon and self.location.dungeon_loot:
            enemy.reward = generator.choice(self.location.dungeon_loot)
        return enemy

    def create_encounter_group(
        self,
        rng: random.Random | None = None,
        *,
        dungeon: bool = False,
    ) -> list[Enemy]:
        """Erzeugt eine Gegnergruppe passend zur Größe von Daisys Team."""

        if not self.location.encounters:
            return []
        generator = rng or random
        team_size = 1 + len(self.story.party)
        enemy_count = generator.randint(1, team_size)
        enemies = [self.create_encounter(generator) for _ in range(enemy_count)]
        group = [enemy for enemy in enemies if enemy is not None]
        if dungeon and group and self.location.dungeon_loot:
            generator.choice(group).reward = generator.choice(self.location.dungeon_loot)
        return group

    def rest(self) -> int | None:
        """Heilt Daisy an einem sicheren Rastplatz vollständig."""

        if not self.location.safe_haven:
            return None
        healed = self.player.heal(self.player.max_health)
        self.player.statuses.clear()
        return healed

    def discard_inventory_stack(self, item: str) -> int:
        """Entfernt einen vollständigen Gegenstandsstapel."""

        if self.discard_block_reason(item):
            return 0
        amount = self.player.inventory.count(item)
        self.player.inventory = [
            inventory_item for inventory_item in self.player.inventory if inventory_item != item
        ]
        return amount

    def discard_block_reason(self, item: str) -> str | None:
        if not self.location.safe_haven:
            return "Das Inventar lässt sich nur an einem sicheren Ort ausmisten."
        if item in self.player.equipment.values():
            return "Ausgerüstete Gegenstände können nicht abgelegt werden."
        if item_definition(item).kind == "quest":
            return "Questgegenstände können nicht abgelegt werden."
        return None

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
                "5. Speichern  6. Beenden  7. Dungeon  8. Rasten  9. Ausmisten"
                "  10. Ausrüstung  11. Team  12. Quest abgeben"
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
            elif choice == "8":
                self._rest(output)
            elif choice == "9":
                self._discard_menu(input_fn, output)
            elif choice == "10":
                self._equipment_menu(input_fn, output)
            elif choice == "11":
                for member in self.party_summary():
                    output(member)
            elif choice == "12":
                self._quest_turn_in_menu(input_fn, output)
            else:
                output("Bitte wähle eine der angezeigten Nummern.")

        if not self.player.is_alive:
            output("\nDaisy wurde besiegt. Doch ein Rache-Dackel gibt niemals endgültig auf!")

    def _run_story(self, input_fn: Input, output: Output) -> None:
        engine = StoryEngine(self)
        while not self.story.complete:
            node = engine.current
            choices = engine.available_choices
            if not choices:
                raise RuntimeError(f"Storyknoten ohne verfügbare Entscheidung: {node.id}")
            output(f"\n=== {node.title} ===")
            for paragraph in node.text:
                output(paragraph)
            for number, choice in enumerate(choices, start=1):
                output(f"{number}. {choice.label}")

            answer = input_fn("> ").strip()
            if not answer.isdigit() or not 1 <= int(answer) <= len(choices):
                output("Bitte wähle eine der angezeigten Nummern.")
                continue
            selected = choices[int(answer) - 1]
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
        if self.story.quests:
            output("Quests:")
            for quest in self.quest_summary():
                output(quest)

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

        for message in self.update_location_quests():
            output(message)
        if location.enemy and location.enemy.is_alive:
            self._battle(location.enemy, input_fn, output)
            if not self.player.is_alive:
                return
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
            enemies = self.create_encounter_group()
            if enemies:
                output("Auf dem Weg lauert Daisy eine Gegnergruppe auf.")
                self._battle_group(enemies, input_fn, output)

    def _dungeon(self, input_fn: Input, output: Output) -> None:
        enemies = self.create_encounter_group(dungeon=True)
        if not enemies or not self.location.dungeon_name:
            output("An diesem Ort gibt es keinen zugänglichen Dungeon.")
            return
        output(f"Daisy betritt: {self.location.dungeon_name}")
        self._battle_group(enemies, input_fn, output)

    def _rest(self, output: Output) -> None:
        healed = self.rest()
        if healed is None:
            output("Daisy kann nur in einem sicheren Baumhaus rasten.")
            return
        from .persistence import save_game

        save_game(self)
        output(f"Daisy ruht sich aus, heilt {healed} LP und speichert das Abenteuer.")

    def _discard_menu(self, input_fn: Input, output: Output) -> None:
        if not self.location.safe_haven:
            output("Das Inventar lässt sich nur an einem sicheren Baumhaus ausmisten.")
            return
        stacks = [
            item for item in Counter(self.player.inventory) if not self.discard_block_reason(item)
        ]
        if not stacks:
            output("Daisy hat keine ablegbaren Gegenstände.")
            return
        for number, item in enumerate(stacks, start=1):
            output(f"{number}. {item} ({self.player.inventory.count(item)}×)")
        choice = input_fn("Welchen Stapel zurücklassen? ").strip()
        if not choice.isdigit() or not 1 <= int(choice) <= len(stacks):
            output("Dieser Stapel existiert nicht.")
            return
        item = stacks[int(choice) - 1]
        amount = self.discard_inventory_stack(item)
        output(f"{amount}× {item} zurückgelassen.")

    def _inventory_menu(self, input_fn: Input, output: Output) -> None:
        if not self.player.inventory:
            output("Daisys Inventar ist leer.")
            return
        output(f"Inventar ({len(self.player.inventory)}/{self.player.inventory_capacity}):")
        for summary in self.inventory_summary():
            output(summary)
        if self.player.health < self.player.max_health and self.available_consumables():
            item = self._choose_consumable(input_fn, output, allow_cancel=True)
            if item:
                healed = self.player.use_consumable(item)
                output(f"{item}: Daisy erhält {healed} Gesundheit zurück.")

    def _choose_consumable(
        self,
        input_fn: Input,
        output: Output,
        *,
        allow_cancel: bool = False,
    ) -> str | None:
        consumables = self.available_consumables()
        if not consumables:
            output("Daisy besitzt kein verwendbares Heilitem.")
            return None
        for number, item in enumerate(consumables, start=1):
            output(f"{number}. {item} – heilt {item_definition(item).healing} LP")
        prompt = "Heilitem (Enter zum Abbrechen): " if allow_cancel else "Heilitem: "
        choice = input_fn(prompt).strip()
        if allow_cancel and not choice:
            return None
        if not choice.isdigit() or not 1 <= int(choice) <= len(consumables):
            output("Dieses Heilitem existiert nicht.")
            return None
        return consumables[int(choice) - 1]

    def _equipment_menu(self, input_fn: Input, output: Output) -> None:
        equipment = [
            item
            for item in dict.fromkeys(self.player.inventory)
            if item_definition(item).kind == "equipment"
        ]
        if not equipment:
            output("Daisy besitzt noch keine Ausrüstung.")
            return
        for number, item in enumerate(equipment, start=1):
            definition = item_definition(item)
            marker = " (angelegt)" if item in self.player.equipment.values() else ""
            output(
                f"{number}. {item}{marker} – Angriff +{definition.attack_bonus}, "
                f"Verteidigung +{definition.defense_bonus}"
            )
        choice = input_fn("Welche Ausrüstung anlegen? ").strip()
        if not choice.isdigit() or not 1 <= int(choice) <= len(equipment):
            output("Diese Ausrüstung existiert nicht.")
            return
        item = equipment[int(choice) - 1]
        definition = item_definition(item)
        previous = self.player.equipment.get(definition.slot or "")
        self.player.equip(item)
        if previous and previous != item:
            output(f"Daisy wechselt {previous} gegen {item}.")
        else:
            output(f"Daisy legt {item} an.")

    def _quest_turn_in_menu(self, input_fn: Input, output: Output) -> None:
        turn_ins = self.available_quest_turn_ins()
        if not turn_ins:
            output("Hier kann gerade keine Quest abgegeben werden.")
            return
        for number, (_quest_id, quest) in enumerate(turn_ins, start=1):
            output(f"{number}. {quest.title} – {quest.objective_target} übergeben")
        choice = input_fn("Welche Quest abgeben? ").strip()
        if not choice.isdigit() or not 1 <= int(choice) <= len(turn_ins):
            output("Diese Quest kann nicht abgegeben werden.")
            return
        quest_id, _quest = turn_ins[int(choice) - 1]
        for message in self.turn_in_quest(quest_id):
            output(message)

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
        self._battle_group([enemy], input_fn, output)

    def _battle_group(
        self,
        enemies: list[Enemy],
        input_fn: Input,
        output: Output,
    ) -> None:
        active = [enemy for enemy in enemies if enemy.is_alive]
        output(f"\n{len(active)} Gegner greifen an!")
        while self.player.is_alive and active:
            output(f"Daisy: {self.player.health}/{self.player.max_health} LP")
            for number, enemy in enumerate(active, start=1):
                output(f"{number}. {enemy.name}: {self._health_bar(enemy)}")
            choice = input_fn("1. Angreifen  2. Heilitem  3. Fliehen\n> ").strip()
            if choice == "1":
                selected_attack = self._choose_attack(input_fn, output)
                if selected_attack is None:
                    continue
                target = active[0]
                if len(active) > 1:
                    target_choice = input_fn("Ziel: ").strip()
                    if not target_choice.isdigit() or not 1 <= int(target_choice) <= len(active):
                        output("Dieses Ziel existiert nicht.")
                        continue
                    target = active[int(target_choice) - 1]
                damage = self.attack(target, attack=selected_attack)
                output(f"{selected_attack.name} verursacht {damage} Schaden.")
                if not self.player.is_alive:
                    break
                if not target.is_alive:
                    for message in self.complete_victory(target):
                        output(message)
                    active.remove(target)
            elif choice == "2":
                item = self._choose_consumable(input_fn, output)
                if item is None:
                    continue
                healed = self.player.use_consumable(item)
                output(f"{item}: Daisy heilt {healed} LP." if healed else "Heilung nicht nötig.")
                if not healed:
                    continue
            elif choice == "3":
                output("Daisy zieht sich zurück.")
                return
            else:
                output("Ungültige Auswahl.")
                continue

            for enemy in active:
                _result, message = self.resolve_enemy_action(enemy)
                output(message)
                if not self.player.is_alive:
                    break

        if active:
            return
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
