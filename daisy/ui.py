"""Grafische Desktop-Oberfläche für das Daisy-Textadventure."""

from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk
from typing import TYPE_CHECKING

from .persistence import DEFAULT_SAVE_FILE, load_game, save_game
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
        self.enemy: Enemy | None = None
        self.title_image: tk.PhotoImage | None = None
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

        if TITLE_IMAGE.exists():
            original = tk.PhotoImage(file=TITLE_IMAGE)
            self.title_image = original.subsample(2, 2)
            canvas.create_image(0, 0, image=self.title_image, anchor="nw")

        canvas.create_rectangle(0, 470, 1180, 760, fill=COLORS["background"], outline="")
        canvas.create_text(
            590,
            515,
            text="DAS ABENTEUER DES RACHE-DACKELS",
            fill=COLORS["gold"],
            font=("Georgia", 26, "bold"),
        )
        canvas.create_text(
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
        canvas.create_window(480, 625, window=new_button, width=220)
        load_button = ttk.Button(
            canvas,
            text="Spielstand laden",
            style="Quiet.TButton",
            command=self.load_saved_game,
            state="normal" if DEFAULT_SAVE_FILE.exists() else "disabled",
        )
        canvas.create_window(710, 625, window=load_button, width=200)
        canvas.create_text(
            590,
            705,
            text="Ein kleines datengetriebenes Text-RPG",
            fill=COLORS["muted"],
            font=("Segoe UI", 10),
        )

    def start_new_game(self) -> None:
        self.game = create_game()
        self.show_game()
        self.log(
            "Hubertus' Gefolge hat Grauholz überfallen. Daisy folgt der Spur "
            "und schwört, das Dorf zu befreien."
        )

    def load_saved_game(self) -> None:
        try:
            self.game = load_game()
        except (OSError, ValueError, KeyError) as error:
            messagebox.showerror(
                "Spielstand", f"Der Spielstand konnte nicht geladen werden:\n{error}"
            )
            return
        self.show_game()
        self.log("Willkommen zurück, Daisy. Dein Abenteuer geht weiter.")

    def show_game(self) -> None:
        if self.game is None:
            return
        self.clear()
        self.enemy = None

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

        self.story = tk.Text(
            left,
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
            command=self.save,
        ).pack(fill="x", pady=4)
        ttk.Button(
            bottom,
            text="Zum Titel",
            style="Quiet.TButton",
            command=self.show_title,
        ).pack(fill="x", pady=4)

        self.refresh()
        self.show_main_actions()

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
                f"{sum(player.defeated_enemies.values())} Siege"
            )
        )
        self.inventory_label.configure(
            text="\n".join(f"• {item}" for item in player.inventory) or "Noch leer"
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

    def set_actions(self, actions: list[tuple[str, object, str]]) -> None:
        for child in self.actions.winfo_children():
            child.destroy()
        for text, command, style in actions:
            ttk.Button(
                self.actions,
                text=text,
                command=command,
                style=style,
            ).pack(side="left", padx=(0, 8))

    def show_main_actions(self) -> None:
        self.set_actions(
            [
                ("Erkunden", self.explore, "Daisy.TButton"),
                ("Reisen", self.show_travel_actions, "Quiet.TButton"),
                ("Heilkraut", self.heal, "Quiet.TButton"),
            ]
        )

    def explore(self) -> None:
        if self.game is None:
            return
        location = self.game.location
        location.visited = True
        self.log(f"{location.name}\n{location.description}")
        found = self.game.collect_items()
        self.log("Gefunden: " + ", ".join(found) if found else "Daisy findet nichts Neues.")
        self.refresh()
        if location.enemy and location.enemy.is_alive:
            self.start_battle(location.enemy)

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
        self.game.travel(destination)
        self.log(f"Daisy reist nach {destination}.")
        self.refresh()
        self.show_main_actions()

    def heal(self) -> None:
        if self.game is None:
            return
        healed = self.game.player.use_healing_item()
        self.log(f"Daisy heilt {healed} LP." if healed else "Daisy hat kein Heilkraut.")
        self.refresh()

    def save(self) -> None:
        if self.game is None:
            return
        save_game(self.game)
        self.log("Spielstand gespeichert.")

    def start_battle(self, enemy: Enemy) -> None:
        self.enemy = enemy
        self.log(f"{enemy.name} greift an!")
        self.show_attack_actions()

    def show_attack_actions(self) -> None:
        if self.game is None:
            return
        actions = [
            (attack.name, lambda selected=attack: self.perform_attack(selected), "Daisy.TButton")
            for attack in self.game.player.attacks
        ]
        actions.extend(
            [
                ("Heilkraut", self.battle_heal, "Quiet.TButton"),
                ("Fliehen", self.flee, "Danger.TButton"),
            ]
        )
        self.set_actions(actions)

    def perform_attack(self, attack: Attack) -> None:
        if self.game is None or self.enemy is None:
            return
        damage = self.game.attack(self.enemy, attack=attack)
        self.log(f"{attack.name}: {damage} Schaden.")
        if not self.enemy.is_alive:
            self.finish_battle()
            return
        self.enemy_turn()

    def battle_heal(self) -> None:
        if self.game is None:
            return
        healed = self.game.player.use_healing_item()
        self.log(f"Daisy heilt {healed} LP." if healed else "Kein Heilkraut vorhanden.")
        if healed:
            self.enemy_turn()
        self.refresh()

    def enemy_turn(self) -> None:
        if self.game is None or self.enemy is None:
            return
        damage = self.game.enemy_attack(self.enemy)
        self.log(f"{self.enemy.name} verursacht {damage} Schaden.")
        self.refresh()
        if not self.game.player.is_alive:
            self.set_actions([("Neues Spiel", self.start_new_game, "Danger.TButton")])
            self.log("Daisy wurde besiegt. Das Abenteuer ist noch nicht vorbei.")

    def finish_battle(self) -> None:
        if self.game is None or self.enemy is None:
            return
        for message in self.game.complete_victory(self.enemy):
            self.log(message)
        self.enemy = None
        self.refresh()
        if self.game.finished:
            self.set_actions([("Zum Titel", self.show_title, "Daisy.TButton")])
        else:
            self.show_main_actions()

    def flee(self) -> None:
        self.log("Daisy zieht sich zurück.")
        self.enemy = None
        self.show_main_actions()


def main() -> None:
    """Startet die grafische Oberfläche."""

    DaisyApp().mainloop()


if __name__ == "__main__":
    main()
