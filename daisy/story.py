"""Datengetriebener Storyablauf, Quests und Freundschaften."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .game import Game

STORY_FILE = Path(__file__).parent / "data" / "story.json"
FRIENDSHIP_THRESHOLDS = (2, 5, 9, 14, 20)


@dataclass
class QuestState:
    """Speicherbarer Fortschritt einer Quest."""

    title: str
    description: str
    status: str = "active"
    progress: int = 0
    target: int = 1

    @property
    def completed(self) -> bool:
        return self.status == "completed"

    def advance(self, amount: int = 1) -> bool:
        if self.completed:
            return False
        self.progress = min(self.target, self.progress + max(0, amount))
        if self.progress >= self.target:
            self.status = "completed"
            return True
        return False


@dataclass
class StoryState:
    """Alle veränderlichen Storydaten eines Spielstands."""

    current_node: str = "prologue_morning"
    chapter: str = "Prolog – Der letzte friedliche Morgen"
    complete: bool = False
    flags: set[str] = field(default_factory=set)
    choices: dict[str, str] = field(default_factory=dict)
    friendship: dict[str, int] = field(default_factory=dict)
    party: list[str] = field(default_factory=list)
    quests: dict[str, QuestState] = field(default_factory=dict)

    def friendship_level(self, character: str) -> int:
        points = self.friendship.get(character, 0)
        return sum(points >= threshold for threshold in FRIENDSHIP_THRESHOLDS)

    def add_friendship(self, character: str, points: int) -> int:
        self.friendship[character] = max(0, self.friendship.get(character, 0) + points)
        return self.friendship_level(character)


@dataclass(frozen=True)
class StoryChoice:
    """Eine auswählbare Reaktion innerhalb eines Storyknotens."""

    id: str
    label: str
    next_node: str
    effects: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class StoryNode:
    """Ein Abschnitt aus Text und möglichen Entscheidungen."""

    id: str
    title: str
    text: tuple[str, ...]
    choices: tuple[StoryChoice, ...]


@dataclass(frozen=True)
class StoryTrigger:
    """Startet einen Storyabschnitt, sobald Bedingungen erfüllt sind."""

    id: str
    location: str
    node: str
    requires_flags: tuple[str, ...] = ()
    excludes_flags: tuple[str, ...] = ()
    quest_active: str | None = None
    quest_completed: str | None = None
    party_contains: str | None = None
    min_level: int = 1

    def matches(self, game: Game) -> bool:
        state = game.story
        if f"triggered:{self.id}" in state.flags:
            return False
        if self.location != game.current_location or game.player.level < self.min_level:
            return False
        if not set(self.requires_flags).issubset(state.flags):
            return False
        if set(self.excludes_flags) & state.flags:
            return False
        if self.party_contains and self.party_contains not in state.party:
            return False
        if self.quest_active:
            quest = state.quests.get(self.quest_active)
            if not quest or quest.status != "active":
                return False
        if self.quest_completed:
            quest = state.quests.get(self.quest_completed)
            if not quest or not quest.completed:
                return False
        return True


def load_story(path: Path = STORY_FILE) -> dict[str, StoryNode]:
    """Lädt und validiert Storyknoten aus JSON."""

    data = json.loads(path.read_text(encoding="utf-8"))
    raw_nodes = data.get("nodes")
    if not isinstance(raw_nodes, list):
        raise TypeError("Die Storydatei benötigt eine Liste 'nodes'.")

    nodes: dict[str, StoryNode] = {}
    for raw_node in raw_nodes:
        choices = tuple(StoryChoice(**choice) for choice in raw_node.get("choices", []))
        node = StoryNode(
            id=raw_node["id"],
            title=raw_node["title"],
            text=tuple(raw_node["text"]),
            choices=choices,
        )
        if node.id in nodes:
            raise ValueError(f"Doppelter Storyknoten: {node.id}")
        nodes[node.id] = node

    referenced_nodes = {
        choice.next_node
        for node in nodes.values()
        for choice in node.choices
        if choice.next_node != "COMPLETE"
    }
    unknown = referenced_nodes - nodes.keys()
    if unknown:
        raise ValueError(f"Unbekannte Storyknoten: {sorted(unknown)}")
    return nodes


def load_story_triggers(path: Path = STORY_FILE) -> tuple[StoryTrigger, ...]:
    """Lädt ortsbasierte Auslöser aus der Storydatei."""

    data = json.loads(path.read_text(encoding="utf-8"))
    triggers = []
    for raw_trigger in data.get("triggers", []):
        raw_trigger["requires_flags"] = tuple(raw_trigger.get("requires_flags", []))
        raw_trigger["excludes_flags"] = tuple(raw_trigger.get("excludes_flags", []))
        triggers.append(StoryTrigger(**raw_trigger))
    return tuple(triggers)


class StoryEngine:
    """Wendet Storyentscheidungen auf einen Spielstand an."""

    def __init__(
        self,
        game: Game,
        nodes: dict[str, StoryNode] | None = None,
        triggers: tuple[StoryTrigger, ...] | None = None,
    ) -> None:
        self.game = game
        self.nodes = nodes or load_story()
        self.triggers = triggers if triggers is not None else load_story_triggers()

    @property
    def current(self) -> StoryNode:
        return self.nodes[self.game.story.current_node]

    def choose(self, choice_id: str) -> list[str]:
        choice = next(
            (candidate for candidate in self.current.choices if candidate.id == choice_id),
            None,
        )
        if choice is None:
            raise ValueError(f"Unbekannte Storyentscheidung: {choice_id}")

        self.game.story.choices[self.current.id] = choice.id
        messages = self._apply_effects(choice.effects)
        if choice.next_node == "COMPLETE":
            self.game.story.complete = True
        else:
            self.game.story.current_node = choice.next_node
        return messages

    def activate_location_trigger(self) -> bool:
        """Aktiviert den ersten passenden, bisher ungenutzten Ortsauslöser."""

        if not self.game.story.complete:
            return False
        trigger = next((item for item in self.triggers if item.matches(self.game)), None)
        if trigger is None:
            return False
        self.game.story.flags.add(f"triggered:{trigger.id}")
        self.game.story.current_node = trigger.node
        self.game.story.complete = False
        return True

    def _apply_effects(self, effects: dict[str, Any]) -> list[str]:
        messages: list[str] = []
        state = self.game.story

        if flag := effects.get("flag"):
            state.flags.add(flag)
        state.flags.update(effects.get("flags", []))
        if chapter := effects.get("chapter"):
            state.chapter = chapter
        if item := effects.get("add_item"):
            if self.game.player.add_item(item):
                messages.append(f"Erhalten: {item}")
            else:
                messages.append(f"Inventar voll – {item} bleibt zurück.")
        for item in effects.get("add_items", []):
            if self.game.player.add_item(item):
                messages.append(f"Erhalten: {item}")
            else:
                messages.append(f"Inventar voll – {item} bleibt zurück.")
        for item in effects.get("remove_items", []):
            if item in self.game.player.inventory:
                self.game.player.inventory.remove(item)
        if effects.get("heal_full"):
            healed = self.game.player.heal(self.game.player.max_health)
            if healed:
                messages.append(f"Das Team rastet. Daisy regeneriert {healed} LP.")
        if (character := effects.get("join_party")) and character not in state.party:
            state.party.append(character)
            messages.append(f"{character} schließt sich Daisy an.")
        if friendship := effects.get("friendship"):
            character = friendship["character"]
            old_level = state.friendship_level(character)
            new_level = state.add_friendship(character, friendship["points"])
            if new_level > old_level:
                messages.append(f"Freundschaft mit {character}: Stufe {new_level}")
        if quest := effects.get("start_quest"):
            quest_id = quest["id"]
            if quest_id not in state.quests:
                state.quests[quest_id] = QuestState(
                    title=quest["title"],
                    description=quest["description"],
                    target=quest.get("target", 1),
                )
                messages.append(f"Neue Quest: {quest['title']}")
        if quest_id := effects.get("complete_quest"):
            quest = state.quests.get(quest_id)
            if quest and not quest.completed:
                quest.progress = quest.target
                quest.status = "completed"
                messages.append(f"Quest abgeschlossen: {quest.title}")
        if effects.get("pacify_enemy") and self.game.location.enemy:
            self.game.location.enemy.health = 0
        if effects.get("finish_game"):
            self.game.finished = True
        return messages
