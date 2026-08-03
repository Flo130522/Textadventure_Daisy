"""Grafische Desktop-Oberfläche für das Daisy-Textadventure."""

from __future__ import annotations

import ctypes
import random
import sys
import tkinter as tk
from collections import Counter
from contextlib import suppress
from pathlib import Path
from tkinter import messagebox, ttk
from typing import TYPE_CHECKING

from .models import item_definition
from .persistence import (
    DEFAULT_SAVE_FILE,
    MANUAL_SLOTS,
    autosave,
    available_saves,
    load_game,
    load_slot,
    save_slot,
)
from .story import StoryEngine
from .world import create_game

if TYPE_CHECKING:
    from .game import Game
    from .models import Attack, Enemy

ASSET_DIR = Path(__file__).parent / "assets"
TITLE_IMAGE = ASSET_DIR / "daisy-title.png"

COLORS = {
    "background": "#0d1821",
    "panel": "#152632",
    "panel_light": "#1d3442",
    "text": "#f2ead7",
    "muted": "#a9b8b8",
    "gold": "#d7a84a",
    "gold_active": "#efc76d",
    "danger": "#a7463e",
    "health": "#6eaa78",
}


class DaisyApp(tk.Tk):
    """Hauptfenster mit Titel- und Spielansicht."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Das Abenteuer des Rache-Dackels")
        self.geometry("1180x760")
        self.minsize(980, 680)
        self.configure(bg=COLORS["background"])
        self.game: Game | None = None
        self.active_slot: str | None = None
        self.enemies: list[Enemy] = []
        self.title_image: tk.PhotoImage | None = None
        self.scene_image: tk.PhotoImage | None = None
        self.protocol("WM_DELETE_WINDOW", self.close_game)
        self._configure_styles()
        self.show_title()

    def _configure_styles(self) -> None:
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure(
            "Daisy.TButton",
            background=COLORS["gold"],
            foreground="#17130c",
            borderwidth=0,
            font=("Segoe UI Semibold", 11),
            padding=(18, 10),
        )
        style.map(
            "Daisy.TButton",
            background=[("active", COLORS["gold_active"]), ("disabled", "#53616a")],
        )
        style.configure(
            "Quiet.TButton",
            background=COLORS["panel_light"],
            foreground=COLORS["text"],
            borderwidth=0,
            font=("Segoe UI", 10),
            padding=(14, 9),
        )
        style.map("Quiet.TButton", background=[("active", "#29495b")])
        style.configure(
            "Danger.TButton",
            background=COLORS["danger"],
            foreground=COLORS["text"],
            borderwidth=0,
            font=("Segoe UI Semibold", 10),
            padding=(14, 9),
        )

    def clear(self) -> None:
        for child in self.winfo_children():
            child.destroy()

    def show_title(self) -> None:
        self.clear()
        canvas = tk.Canvas(
            self,
            bg=COLORS["background"],
            highlightthickness=0,
            width=1180,
            height=760,
        )
        canvas.pack(fill="both", expand=True)

        image_item = None
        if TITLE_IMAGE.exists():
            original = tk.PhotoImage(file=TITLE_IMAGE)
            self.title_image = original.subsample(2, 2)
            image_item = canvas.create_image(590, 0, image=self.title_image, anchor="n")

        cover = canvas.create_rectangle(0, 470, 1180, 760, fill=COLORS["background"], outline="")
        title = canvas.create_text(
            590,
            515,
            text="DAS ABENTEUER DES RACHE-DACKELS",
            fill=COLORS["gold"],
            font=("Georgia", 26, "bold"),
        )
        subtitle = canvas.create_text(
            590,
            557,
            text="Daisy gegen Hubertus Snickers",
            fill=COLORS["text"],
            font=("Georgia", 17, "italic"),
        )

        new_button = ttk.Button(
            canvas,
            text="Neues Abenteuer",
            style="Daisy.TButton",
            command=self.start_new_game,
        )
        new_window = canvas.create_window(480, 625, window=new_button, width=220)
        load_button = ttk.Button(
            canvas,
            text="Spielstand laden",
            style="Quiet.TButton",
            command=self.show_load_slots,
            state="normal" if available_saves() or DEFAULT_SAVE_FILE.exists() else "disabled",
        )
        load_window = canvas.create_window(710, 625, window=load_button, width=200)
        footer = canvas.create_text(
            590,
            705,
            text="Ein kleines datengetriebenes Text-RPG",
            fill=COLORS["muted"],
            font=("Segoe UI", 10),
        )

        def center_title(event: tk.Event) -> None:
            center = event.width / 2
            canvas.coords(cover, 0, 470, event.width, max(760, event.height))
            canvas.coords(title, center, 515)
            canvas.coords(subtitle, center, 557)
            canvas.coords(new_window, center - 115, 625)
            canvas.coords(load_window, center + 115, 625)
            canvas.coords(footer, center, 705)
            if image_item is not None:
                canvas.coords(image_item, center, 0)

        canvas.bind("<Configure>", center_title)

    def start_new_game(self) -> None:
        self.game = create_game()
        self.active_slot = None
        self.show_game()

    def show_load_slots(self) -> None:
        """Zeigt valide Saves mit genug Kontext für eine sichere Auswahl."""

        self.clear()
        frame = tk.Frame(self, bg=COLORS["background"], padx=80, pady=55)
        frame.pack(fill="both", expand=True)
        tk.Label(
            frame,
            text="ABENTEUER FORTSETZEN",
            bg=COLORS["background"],
            fg=COLORS["gold"],
            font=("Georgia", 24, "bold"),
        ).pack(pady=(0, 24))
        saves = available_saves()
        for metadata in saves:
            slot_name = (
                "Autosave"
                if metadata.slot == "autosave"
                else metadata.slot.replace("slot-", "Slot ")
            )
            label = (
                f"{slot_name}: {metadata.location}, Level {metadata.level}\n"
                f"{metadata.chapter} · {metadata.modified:%d.%m.%Y %H:%M}"
            )
            ttk.Button(
                frame,
                text=label,
                style="Quiet.TButton",
                command=lambda slot=metadata.slot: self.load_saved_game(slot=slot),
            ).pack(fill="x", pady=5)
        if DEFAULT_SAVE_FILE.exists():
            ttk.Button(
                frame,
                text="Alten saved_game.json laden",
                style="Quiet.TButton",
                command=lambda: self.load_saved_game(legacy=True),
            ).pack(fill="x", pady=5)
        ttk.Button(frame, text="Zurück", style="Danger.TButton", command=self.show_title).pack(
            pady=(24, 0)
        )

    def load_saved_game(self, *, slot: str | None = None, legacy: bool = False) -> None:
        try:
            self.game = load_game() if legacy else load_slot(slot or "autosave")
        except (OSError, TypeError, ValueError, KeyError) as error:
            messagebox.showerror(
                "Spielstand", f"Der Spielstand konnte nicht geladen werden:\n{error}"
            )
            return
        self.active_slot = None if legacy or slot == "autosave" else slot
        self.show_game()
        self.log("Willkommen zurück, Daisy. Dein Abenteuer geht weiter.")

    def show_game(self) -> None:
        if self.game is None:
            return
        self.clear()
        self.enemies = []

        header = tk.Frame(self, bg=COLORS["background"], padx=24, pady=18)
        header.pack(fill="x")
        tk.Label(
            header,
            text="DAISY",
            bg=COLORS["background"],
            fg=COLORS["gold"],
            font=("Georgia", 21, "bold"),
        ).pack(side="left")
        self.location_label = tk.Label(
            header,
            bg=COLORS["background"],
            fg=COLORS["text"],
            font=("Segoe UI Semibold", 14),
        )
        self.location_label.pack(side="right")

        body = tk.Frame(self, bg=COLORS["background"], padx=24)
        body.pack(fill="both", expand=True)
        left = tk.Frame(body, bg=COLORS["panel"], padx=22, pady=18)
        left.pack(side="left", fill="both", expand=True)
        right = tk.Frame(body, bg=COLORS["panel_light"], width=290, padx=20, pady=18)
        right.pack(side="right", fill="y", padx=(18, 0))
        right.pack_propagate(False)

        self.scene_label = tk.Label(
            left,
            bg=COLORS["panel"],
            bd=0,
        )
        self.story = tk.Text(
            left,
            height=8,
            width=50,
            wrap="word",
            bg=COLORS["panel"],
            fg=COLORS["text"],
            insertbackground=COLORS["text"],
            relief="flat",
            font=("Georgia", 12),
            spacing1=4,
            spacing3=9,
            padx=6,
            pady=6,
            state="disabled",
        )
        self.story.pack(fill="both", expand=True)
        self.battle_label = tk.Label(
            left,
            justify="left",
            bg=COLORS["background"],
            fg=COLORS["text"],
            font=("Consolas", 11, "bold"),
            padx=12,
            pady=8,
        )
        self.actions = tk.Frame(left, bg=COLORS["panel"], pady=14)
        self.actions.pack(fill="x")

        tk.Label(
            right,
            text="STATUS",
            bg=COLORS["panel_light"],
            fg=COLORS["gold"],
            font=("Segoe UI Semibold", 12),
        ).pack(anchor="w")
        self.status_label = tk.Label(
            right,
            justify="left",
            wraplength=245,
            bg=COLORS["panel_light"],
            fg=COLORS["text"],
            font=("Segoe UI", 11),
            pady=12,
        )
        self.status_label.pack(anchor="w")
        self.health_canvas = tk.Canvas(
            right,
            height=18,
            bg=COLORS["background"],
            highlightthickness=0,
        )
        self.health_canvas.pack(fill="x", pady=(0, 18))

        tk.Label(
            right,
            text="INVENTAR",
            bg=COLORS["panel_light"],
            fg=COLORS["gold"],
            font=("Segoe UI Semibold", 12),
        ).pack(anchor="w")
        self.inventory_label = tk.Label(
            right,
            justify="left",
            wraplength=240,
            bg=COLORS["panel_light"],
            fg=COLORS["muted"],
            font=("Segoe UI", 10),
            pady=10,
        )
        self.inventory_label.pack(anchor="w")

        bottom = tk.Frame(right, bg=COLORS["panel_light"])
        bottom.pack(side="bottom", fill="x")
        ttk.Button(
            bottom,
            text="Speichern",
            style="Quiet.TButton",
            command=self.show_save_actions,
        ).pack(fill="x", pady=4)
        ttk.Button(
            bottom,
            text="Zum Titel",
            style="Quiet.TButton",
            command=self.return_to_title,
        ).pack(fill="x", pady=4)

        self.refresh()
        if self.game.story.complete:
            self.show_main_actions()
        else:
            self.show_story_node()

    def refresh(self) -> None:
        if self.game is None:
            return
        player = self.game.player
        self.location_label.configure(text=self.game.current_location)
        self.status_label.configure(
            text=(
                f"Level {player.level}\n"
                f"{player.health}/{player.max_health} LP\n"
                f"{player.experience}/{player.experience_for_next_level} EP\n"
                f"{sum(player.defeated_enemies.values())} Siege\n\n"
                f"{self.game.story.chapter}\n\n"
                f"Nächstes Ziel:\n{self.game.primary_objective()}\n\n"
                f"Team: {', '.join(self.game.story.party) or 'Daisy allein'}\n"
                f"Ausrüstung: {', '.join(player.equipment.values()) or 'Keine'}\n"
                f"Ausrüstungsboni: ANG +{player.equipment_attack_bonus}, "
                f"VER +{player.equipment_defense_bonus}"
            )
        )
        inventory_text = "\n".join(
            f"• {line}" for line in self.game.inventory_summary(detailed=False)
        )
        self.inventory_label.configure(
            text=(
                f"{len(player.inventory)}/{player.inventory_capacity} Plätze\n"
                f"{inventory_text or 'Noch leer'}"
            )
        )
        self.health_canvas.delete("all")
        self.health_canvas.update_idletasks()
        width = max(1, self.health_canvas.winfo_width())
        ratio = player.health / player.max_health
        self.health_canvas.create_rectangle(0, 0, width, 18, fill=COLORS["background"], outline="")
        self.health_canvas.create_rectangle(
            0,
            0,
            width * ratio,
            18,
            fill=COLORS["health"] if ratio > 0.3 else COLORS["danger"],
            outline="",
        )

    def log(self, message: str) -> None:
        self.story.configure(state="normal")
        self.story.insert("end", message.strip() + "\n\n")
        self.story.see("end")
        self.story.configure(state="disabled")

    def set_actions(
        self,
        actions: list[tuple[str, object, str]],
        *,
        vertical: bool = False,
    ) -> None:
        for child in self.actions.winfo_children():
            child.destroy()
        for text, command, style in actions:
            button = ttk.Button(
                self.actions,
                text=text,
                command=command,
                style=style,
            )
            if vertical:
                button.pack(fill="x", pady=(0, 6))
            else:
                index = len(self.actions.grid_slaves())
                button.grid(
                    row=index // 3,
                    column=index % 3,
                    sticky="ew",
                    padx=(0, 8),
                    pady=(0, 6),
                )
        if not vertical:
            for column in range(3):
                self.actions.grid_columnconfigure(column, weight=1)

    def show_main_actions(self) -> None:
        self.show_story_image(None)
        actions = [
            ("Erkunden", self.explore, "Daisy.TButton"),
            ("Reisen", self.show_travel_actions, "Quiet.TButton"),
            ("Heilen", self.show_healing_actions, "Quiet.TButton"),
            ("Quests", self.show_quests, "Quiet.TButton"),
            ("Team", self.show_team, "Quiet.TButton"),
            ("Ausrüstung", self.show_equipment_actions, "Quiet.TButton"),
        ]
        if self.game is not None and self.game.available_quest_turn_ins():
            actions.append(("Quest abgeben", self.show_quest_turn_ins, "Daisy.TButton"))
        if (
            self.game is not None
            and self.game.location.dungeon_name
            and self.game.location.encounters
        ):
            actions.append(("Dungeon", self.enter_dungeon, "Danger.TButton"))
        if self.game is not None and self.game.location.safe_haven:
            actions.extend(
                [
                    ("Rasten & speichern", self.rest, "Quiet.TButton"),
                    ("Inventar ausmisten", self.show_discard_actions, "Quiet.TButton"),
                ]
            )
        self.set_actions(actions)

    def show_quests(self) -> None:
        if self.game is None:
            return
        quests = self.game.quest_summary()
        self.log("QUESTBUCH\n" + ("\n".join(quests) if quests else "Noch keine Quests."))
        self.show_main_actions()

    def show_team(self) -> None:
        if self.game is None:
            return
        members = self.game.party_summary()
        details = "\n\n".join(members) if members else "Daisy reist allein."
        self.log("TEAM & FREUNDSCHAFT\n" + details)
        self.show_main_actions()

    def show_quest_turn_ins(self) -> None:
        if self.game is None:
            return
        actions = []
        for quest_id, quest in self.game.available_quest_turn_ins():
            owned = self.game.player.inventory.count(quest.objective_target or "")
            remaining = quest.target - quest.progress
            actions.append(
                (
                    f"{quest.objective_target} übergeben ({owned}/{remaining})",
                    lambda selected=quest_id: self.turn_in_quest(selected),
                    "Daisy.TButton",
                )
            )
        actions.append(("Zurück", self.show_main_actions, "Danger.TButton"))
        self.set_actions(actions, vertical=True)

    def turn_in_quest(self, quest_id: str) -> None:
        if self.game is None:
            return
        for message in self.game.turn_in_quest(quest_id):
            self.log(message)
        self.autosave_safely()
        self.refresh()
        if self.game.activate_story_for_location():
            self.show_story_node()
        else:
            self.show_main_actions()

    def show_equipment_actions(self) -> None:
        if self.game is None:
            return
        equipment = [
            item
            for item in dict.fromkeys(self.game.player.inventory)
            if item_definition(item).kind == "equipment"
        ]
        if not equipment:
            self.log("Daisy besitzt noch keine Ausrüstung.")
            self.show_main_actions()
            return
        actions = []
        for item in equipment:
            definition = item_definition(item)
            marker = " ✓" if item in self.game.player.equipment.values() else ""
            label = (
                f"{item}{marker} (ANG +{definition.attack_bonus}, VER +{definition.defense_bonus})"
            )
            actions.append(
                (label, lambda selected=item: self.equip_item(selected), "Quiet.TButton")
            )
        actions.append(("Zurück", self.show_main_actions, "Danger.TButton"))
        self.set_actions(actions)

    def equip_item(self, item: str) -> None:
        if self.game is None:
            return
        definition = item_definition(item)
        previous = self.game.player.equipment.get(definition.slot or "")
        if self.game.player.equip(item):
            if previous and previous != item:
                self.log(f"Daisy wechselt {previous} gegen {item}.")
            else:
                self.log(f"Daisy legt {item} an.")
        else:
            self.log(f"{item} kann nicht angelegt werden.")
        self.refresh()
        self.show_equipment_actions()

    def show_healing_actions(self, *, battle: bool = False) -> None:
        if self.game is None:
            return
        consumables = self.game.available_consumables()
        if not consumables:
            self.log("Daisy besitzt kein verwendbares Heilitem.")
            self.show_attack_actions() if battle else self.show_main_actions()
            return
        actions = [
            (
                f"{item} (+{item_definition(item).healing} LP)",
                lambda selected=item: self.use_consumable(selected, battle=battle),
                "Quiet.TButton",
            )
            for item in consumables
        ]
        back = self.show_attack_actions if battle else self.show_main_actions
        actions.append(("Zurück", back, "Danger.TButton"))
        self.set_actions(actions)

    def use_consumable(self, item: str, *, battle: bool = False) -> None:
        if self.game is None:
            return
        healed = self.game.player.use_consumable(item)
        self.log(f"{item}: Daisy heilt {healed} LP." if healed else "Heilung nicht nötig.")
        self.refresh()
        if battle and healed:
            self.enemy_turn()
        elif battle:
            self.show_attack_actions()
        else:
            self.show_main_actions()

    def show_story_node(self) -> None:
        if self.game is None or self.game.story.complete:
            self.show_main_actions()
            return
        engine = StoryEngine(self.game)
        node = engine.current
        self.show_story_image(node.image)
        self.log(node.title.upper())
        for paragraph in node.text:
            self.log(paragraph)
        self.set_actions(
            [
                (
                    choice.label,
                    lambda choice_id=choice.id: self.choose_story(choice_id),
                    "Daisy.TButton",
                )
                for choice in engine.available_choices
            ],
            vertical=True,
        )

    def show_story_image(self, filename: str | None) -> None:
        """Blendet ein optionales, vom Storyknoten referenziertes Szenenbild ein."""

        self.scene_label.pack_forget()
        self.scene_image = None
        if not filename:
            return
        path = ASSET_DIR / filename
        if not path.exists():
            self.log(f"Szenenbild fehlt: {filename}")
            return
        original = tk.PhotoImage(file=path)
        self.update_idletasks()
        available_width = max(1, self.story.winfo_width())
        factor = max(1, (original.width() + available_width - 1) // available_width)
        self.scene_image = original.subsample(factor, factor)
        self.scene_label.configure(image=self.scene_image, cursor="hand2")
        self.scene_label.bind("<Button-1>", lambda _event: self.enlarge_story_image(path))
        self.scene_label.pack(fill="x", before=self.story, pady=(0, 12))

    def enlarge_story_image(self, path: Path) -> None:
        """Öffnet ein Szenenbild möglichst groß, ohne es abzuschneiden."""

        popup = tk.Toplevel(self)
        popup.title("Szenenbild – zum Schließen anklicken")
        popup.configure(bg=COLORS["background"])
        original = tk.PhotoImage(file=path)
        max_width = max(1, int(self.winfo_screenwidth() * 0.9))
        max_height = max(1, int(self.winfo_screenheight() * 0.85))
        factor = max(
            1,
            (original.width() + max_width - 1) // max_width,
            (original.height() + max_height - 1) // max_height,
        )
        popup.scene_image = original.subsample(factor, factor)
        label = tk.Label(
            popup,
            image=popup.scene_image,
            bg=COLORS["background"],
            cursor="hand2",
        )
        label.pack()
        label.bind("<Button-1>", lambda _event: popup.destroy())

    def choose_story(self, choice_id: str) -> None:
        if self.game is None:
            return
        for message in StoryEngine(self.game).choose(choice_id):
            self.log(message)
        self.autosave_safely()
        self.refresh()
        if self.game.story.complete:
            if self.game.finished:
                self.set_actions([("Zum Titel", self.show_title, "Daisy.TButton")])
            else:
                self.show_main_actions()
        else:
            self.show_story_node()

    def explore(self) -> None:
        if self.game is None:
            return
        location = self.game.location
        location.visited = True
        self.log(f"{location.name}\n{location.description}")
        found = self.game.collect_items()
        self.log("Gefunden: " + ", ".join(found) if found else "Daisy findet nichts Neues.")
        quest_messages = self.game.update_location_quests()
        for message in quest_messages:
            self.log(message)
        self.autosave_safely()
        self.refresh()
        if location.enemy and location.enemy.is_alive:
            self.start_battle(location.enemy)
            return
        if self.game.activate_story_for_location():
            self.show_story_node()
            return
        self.refresh()

    def show_travel_actions(self) -> None:
        if self.game is None:
            return
        actions = [
            (name, lambda destination=name: self.travel(destination), "Quiet.TButton")
            for name in self.game.location.connections
        ]
        actions.append(("Zurück", self.show_main_actions, "Danger.TButton"))
        self.set_actions(actions)

    def travel(self, destination: str) -> None:
        if self.game is None:
            return
        reason = self.game.travel_block_reason(destination)
        if reason:
            self.log(reason)
            self.show_main_actions()
            return
        self.game.travel(destination)
        self.log(f"Daisy reist nach {destination}.")
        self.refresh()
        if self.game.activate_story_for_location():
            self.show_story_node()
        elif self.game.location.encounters and random.random() < 0.25:
            enemies = self.game.create_encounter_group()
            if enemies:
                self.log("Auf dem Weg lauert Daisy eine Gegnergruppe auf.")
                self.start_battle(enemies)
        else:
            self.show_main_actions()

    def enter_dungeon(self) -> None:
        if self.game is None:
            return
        enemies = self.game.create_encounter_group(dungeon=True)
        if not enemies or not self.game.location.dungeon_name:
            self.log("An diesem Ort gibt es keinen zugänglichen Dungeon.")
            self.show_main_actions()
            return
        self.log(f"Daisy betritt: {self.game.location.dungeon_name}")
        self.start_battle(enemies)

    def rest(self) -> None:
        if self.game is None:
            return
        healed = self.game.rest()
        if healed is None:
            self.log("Daisy kann hier nicht sicher rasten.")
            return
        self.autosave_safely()
        self.log(f"Daisy ruht sich aus, heilt {healed} LP; der Autosave wurde aktualisiert.")
        self.refresh()

    def show_discard_actions(self) -> None:
        if self.game is None or not self.game.location.safe_haven:
            self.show_main_actions()
            return
        stacks = [
            item
            for item in Counter(self.game.player.inventory)
            if not self.game.discard_block_reason(item)
        ]
        if not stacks:
            self.log("Daisy hat keine ablegbaren Gegenstände.")
            self.show_main_actions()
            return
        actions = [
            (
                f"{item} ({self.game.player.inventory.count(item)}×)",
                lambda selected=item: self.discard_stack(selected),
                "Danger.TButton",
            )
            for item in stacks
        ]
        actions.append(("Zurück", self.show_main_actions, "Quiet.TButton"))
        self.set_actions(actions)

    def discard_stack(self, item: str) -> None:
        if self.game is None:
            return
        amount = self.game.discard_inventory_stack(item)
        self.log(f"{amount}× {item} zurückgelassen.")
        self.refresh()
        self.show_discard_actions()

    def show_save_actions(self) -> None:
        if self.game is None:
            return
        metadata = {save.slot: save for save in available_saves()}
        actions = []
        for slot in MANUAL_SLOTS:
            saved = metadata.get(slot)
            label = slot.replace("slot-", "Slot ")
            if saved:
                label += f" überschreiben ({saved.location}, Level {saved.level})"
            actions.append(
                (label, lambda selected=slot: self.save_to_slot(selected), "Quiet.TButton")
            )
        actions.append(("Zurück", self.show_main_actions, "Danger.TButton"))
        self.set_actions(actions, vertical=True)

    def save_to_slot(self, slot: str) -> None:
        if self.game is None:
            return
        existing = {save.slot for save in available_saves()}
        if slot in existing and not messagebox.askyesno(
            "Spielstand überschreiben", "Diesen Spielstand wirklich überschreiben?"
        ):
            self.show_save_actions()
            return
        try:
            save_slot(self.game, slot)
        except OSError as error:
            messagebox.showerror("Spielstand", f"Speichern fehlgeschlagen:\n{error}")
            return
        self.active_slot = slot
        self.log(f"{slot.replace('slot-', 'Slot ')} gespeichert.")
        self.show_main_actions()

    def autosave_safely(self) -> None:
        # Eine Niederlage darf den letzten fortsetzbaren Autosave nicht ersetzen.
        if self.game is None or not self.game.player.is_alive:
            return
        try:
            autosave(self.game)
        except OSError as error:
            self.log(f"Autosave fehlgeschlagen: {error}")

    def return_to_title(self) -> None:
        if self.game is not None:
            self.autosave_safely()
        self.show_title()

    def close_game(self) -> None:
        if self.game is not None:
            self.autosave_safely()
        self.destroy()

    def start_battle(self, enemies: Enemy | list[Enemy]) -> None:
        self.enemies = enemies if isinstance(enemies, list) else [enemies]
        names = ", ".join(enemy.name for enemy in self.enemies)
        self.log(f"{len(self.enemies)} Gegner greifen an: {names}")
        self.battle_label.pack(fill="x", before=self.actions, pady=(8, 0))
        self.refresh_battle_status()
        self.show_attack_actions()

    def refresh_battle_status(self) -> None:
        if not self.enemies:
            self.battle_label.pack_forget()
            return
        lines = []
        for enemy in self.enemies:
            maximum = max(1, enemy.max_health or enemy.health)
            filled = round(18 * enemy.health / maximum)
            bar = "█" * filled + "░" * (18 - filled)
            lines.append(f"{enemy.name:<24} [{bar}] {enemy.health}/{maximum} LP")
        self.battle_label.configure(text="\n".join(lines))

    def show_attack_actions(self) -> None:
        if self.game is None:
            return
        actions = [
            (
                f"{attack.name}\n{attack.description}",
                lambda selected=attack: self.show_target_actions(selected),
                "Daisy.TButton",
            )
            for attack in self.game.player.attacks
        ]
        actions.extend(
            [
                ("Heilitem", lambda: self.show_healing_actions(battle=True), "Quiet.TButton"),
                ("Fliehen", self.flee, "Danger.TButton"),
            ]
        )
        self.set_actions(actions)

    def show_target_actions(self, attack: Attack) -> None:
        if len(self.enemies) == 1:
            self.perform_attack(attack, self.enemies[0])
            return
        actions = [
            (
                f"{enemy.name} ({enemy.health}/{enemy.max_health} LP)",
                lambda target=enemy: self.perform_attack(attack, target),
                "Danger.TButton",
            )
            for enemy in self.enemies
        ]
        actions.append(("Zurück", self.show_attack_actions, "Quiet.TButton"))
        self.set_actions(actions)

    def perform_attack(self, attack: Attack, enemy: Enemy) -> None:
        if self.game is None or enemy not in self.enemies:
            return
        damage = self.game.attack(enemy, attack=attack)
        self.log(f"{attack.name} gegen {enemy.name}: {damage} Schaden.")
        self.refresh_battle_status()
        if not self.game.player.is_alive:
            self.refresh()
            self.show_defeat_actions()
            self.log("Die Vergiftung war zu stark. Daisy wurde besiegt.")
            return
        if not enemy.is_alive:
            for message in self.game.complete_victory(enemy):
                self.log(message)
            self.enemies.remove(enemy)
        if not self.enemies:
            self.finish_battle()
            return
        self.enemy_turn()

    def enemy_turn(self) -> None:
        if self.game is None or not self.enemies:
            return
        for enemy in self.enemies:
            _result, message = self.game.resolve_enemy_action(enemy)
            self.log(message)
            if not self.game.player.is_alive:
                break
        self.refresh()
        self.refresh_battle_status()
        if not self.game.player.is_alive:
            self.show_defeat_actions()
            self.log("Daisy wurde besiegt. Das Abenteuer ist noch nicht vorbei.")
        else:
            self.show_attack_actions()

    def finish_battle(self) -> None:
        if self.game is None:
            return
        self.enemies = []
        self.refresh_battle_status()
        self.autosave_safely()
        self.refresh()
        if self.game.activate_story_for_location():
            self.show_story_node()
        elif self.game.finished:
            self.set_actions([("Zum Titel", self.show_title, "Daisy.TButton")])
        else:
            self.show_main_actions()

    def flee(self) -> None:
        self.log("Daisy zieht sich zurück.")
        self.enemies = []
        self.refresh_battle_status()
        self.show_main_actions()

    def show_defeat_actions(self) -> None:
        self.set_actions(
            [
                ("Autosave laden", self.show_load_slots, "Daisy.TButton"),
                ("Neues Spiel", self.start_new_game, "Danger.TButton"),
                ("Zum Titel", self.return_to_title, "Quiet.TButton"),
            ],
            vertical=True,
        )


def main() -> None:
    """Startet die grafische Oberfläche."""

    _enable_dpi_awareness()
    DaisyApp().mainloop()


def _enable_dpi_awareness() -> None:
    """Verhindert unscharfe Windows-Skalierung auf hochauflösenden Displays."""

    if sys.platform != "win32":
        return
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except (AttributeError, OSError):
        with suppress(AttributeError, OSError):
            ctypes.windll.user32.SetProcessDPIAware()


if __name__ == "__main__":
    main()
