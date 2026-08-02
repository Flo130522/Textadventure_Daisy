"""Datengetriebener Storyablauf, Quests und Freundschaften."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .game import Game

STORY_FILE = Path(__file__).parent / "data" / "story.json"
ASSET_DIR = Path(__file__).parent / "assets"
FRIENDSHIP_THRESHOLDS = (2, 5, 9, 14, 20)
KNOWN_EFFECTS = {
    "add_item",
    "add_items",
    "advance_quest",
    "chapter",
    "complete_quest",
    "finish_game",
    "flag",
    "flags",
    "friendship",
    "heal_full",
    "join_party",
    "pacify_enemy",
    "remove_items",
    "start_quest",
}


@dataclass
class QuestState:
    """Speicherbarer Fortschritt einer Quest."""

    title: str
    description: str
    status: str = "active"
    progress: int = 0
    target: int = 1
    kind: str = "side"
    reward_experience: int = 0
    reward_items: list[str] = field(default_factory=list)
    rewards_claimed: bool = False
    objective_type: str | None = None
    objective_target: str | None = None
    objective_location: str | None = None
    completion_text: str | None = None

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

    def friendship_perks(self, character: str) -> tuple[str, ...]:
        """Kleine, stabile Grundlage für charakterbezogene Freischaltungen."""

        level = self.friendship_level(character)
        perks = {
            "Leika": ("Spürsinn", "Gemeinsamer Angriff"),
            "Bruno": ("Wachsamkeit", "Standhalten"),
            "Jack": ("Feldversorgung", "Starke Medizin"),
            "Leo": ("Magischer Beistand", "Arkane Verstärkung"),
        }.get(character, ())
        return perks[: min(level, len(perks))]


@dataclass(frozen=True)
class ChoiceConditions:
    requires_flags: tuple[str, ...] = ()
    excludes_flags: tuple[str, ...] = ()
    min_friendship: dict[str, int] = field(default_factory=dict)
    quest_active: str | None = None
    quest_completed: str | None = None
    party_contains: str | None = None
    min_level: int = 1

    def matches(self, game: Game) -> bool:
        state = game.story
        if game.player.level < self.min_level:
            return False
        if not set(self.requires_flags).issubset(state.flags):
            return False
        if set(self.excludes_flags) & state.flags:
            return False
        if self.party_contains and self.party_contains not in state.party:
            return False
        if any(state.friendship_level(name) < level for name, level in self.min_friendship.items()):
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


@dataclass(frozen=True)
class StoryChoice:
    """Eine auswählbare Reaktion innerhalb eines Storyknotens."""

    id: str
    label: str
    next_node: str
    effects: dict[str, Any] = field(default_factory=dict)
    conditions: ChoiceConditions = field(default_factory=ChoiceConditions)


@dataclass(frozen=True)
class StoryNode:
    """Ein Abschnitt aus Text und möglichen Entscheidungen."""

    id: str
    title: str
    text: tuple[str, ...]
    choices: tuple[StoryChoice, ...]
    image: str | None = None


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


@dataclass(frozen=True)
class StoryGuidance:
    """Datengetriebener Hinweis auf den nächsten sinnvollen Handlungsschritt."""

    id: str
    text: str
    destination: str | None = None
    conditions: ChoiceConditions = field(default_factory=ChoiceConditions)

    def matches(self, game: Game) -> bool:
        return self.conditions.matches(game)


def load_story(path: Path = STORY_FILE) -> dict[str, StoryNode]:
    """Lädt und validiert Storyknoten aus JSON."""

    data = json.loads(path.read_text(encoding="utf-8"))
    raw_nodes = data.get("nodes")
    if not isinstance(raw_nodes, list):
        raise TypeError("Die Storydatei benötigt eine Liste 'nodes'.")

    nodes: dict[str, StoryNode] = {}
    for raw_node in raw_nodes:
        choices = []
        for raw_choice in raw_node.get("choices", []):
            choice_data = dict(raw_choice)
            conditions = dict(choice_data.pop("conditions", {}))
            conditions["requires_flags"] = tuple(conditions.get("requires_flags", []))
            conditions["excludes_flags"] = tuple(conditions.get("excludes_flags", []))
            choice_data["conditions"] = ChoiceConditions(**conditions)
            choice = StoryChoice(**choice_data)
            if not isinstance(choice.effects, dict):
                raise TypeError(f"Effekte müssen ein Objekt sein: {choice.id}")
            unknown_effects = set(choice.effects) - KNOWN_EFFECTS
            if unknown_effects:
                raise ValueError(
                    f"Unbekannte Storyeffekte bei {choice.id}: {sorted(unknown_effects)}"
                )
            if choice.conditions.min_level < 1:
                raise ValueError(f"Ungültiges Mindestlevel bei Entscheidung: {choice.id}")
            if any(level < 0 for level in choice.conditions.min_friendship.values()):
                raise ValueError(f"Ungültige Freundschaftsbedingung: {choice.id}")
            quest = choice.effects.get("start_quest")
            if quest and quest.get("kind", "side") not in {"main", "side", "personal"}:
                raise ValueError(f"Ungültiger Questtyp bei Entscheidung: {choice.id}")
            if quest and quest.get("objective_type") not in {
                None,
                "visit_location",
                "deliver_item",
                "defeat_enemy",
            }:
                raise ValueError(f"Ungültiges Questziel bei Entscheidung: {choice.id}")
            if quest and bool(quest.get("objective_type")) != bool(quest.get("objective_target")):
                raise ValueError(f"Unvollständiges Questziel bei Entscheidung: {choice.id}")
            if quest and (
                not isinstance(quest.get("target", 1), int)
                or quest.get("target", 1) < 1
            ):
                raise ValueError(f"Ungültiges Questziel bei Entscheidung: {choice.id}")
            if quest and (
                not isinstance(quest.get("reward_experience", 0), int)
                or quest.get("reward_experience", 0) < 0
            ):
                raise ValueError(f"Ungültige Quest-EP bei Entscheidung: {choice.id}")
            choices.append(choice)
        node = StoryNode(
            id=raw_node["id"],
            title=raw_node["title"],
            text=tuple(raw_node["text"]),
            choices=tuple(choices),
            image=raw_node.get("image"),
        )
        if node.id in nodes:
            raise ValueError(f"Doppelter Storyknoten: {node.id}")
        if node.image and Path(node.image).name != node.image:
            raise ValueError(f"Ungültiger Bildpfad bei Storyknoten: {node.id}")
        if node.image and path == STORY_FILE and not (ASSET_DIR / node.image).is_file():
            raise ValueError(f"Fehlendes Szenenbild bei Storyknoten {node.id}: {node.image}")
        choice_ids = [choice.id for choice in node.choices]
        if not choice_ids:
            raise ValueError(f"Storyknoten ohne Entscheidungen: {node.id}")
        if len(choice_ids) != len(set(choice_ids)):
            raise ValueError(f"Doppelte Entscheidung in Storyknoten: {node.id}")
        if not any(_is_unconditional(choice.conditions) for choice in node.choices):
            raise ValueError(
                f"Storyknoten ohne bedingungslose Rückfallentscheidung: {node.id}"
            )
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
    quest_ids: list[str] = []
    quest_references: list[tuple[str, str]] = []
    for node in nodes.values():
        for choice in node.choices:
            if quest := choice.effects.get("start_quest"):
                quest_ids.append(quest["id"])
            for key in ("advance_quest", "complete_quest"):
                if quest_id := choice.effects.get(key):
                    quest_references.append((choice.id, quest_id))
            for quest_id in (
                choice.conditions.quest_active,
                choice.conditions.quest_completed,
            ):
                if quest_id:
                    quest_references.append((choice.id, quest_id))
    if len(quest_ids) != len(set(quest_ids)):
        raise ValueError("Doppelte Quest-IDs sind nicht erlaubt.")
    unknown_quests = {
        (source, quest) for source, quest in quest_references if quest not in quest_ids
    }
    if unknown_quests:
        raise ValueError(f"Unbekannte Questreferenzen: {sorted(unknown_quests)}")
    return nodes


def load_story_guidance(path: Path = STORY_FILE) -> tuple[StoryGuidance, ...]:
    data = json.loads(path.read_text(encoding="utf-8"))
    guidance = []
    seen_ids = set()
    for raw_item in data.get("guidance", []):
        item = dict(raw_item)
        conditions = dict(item.pop("conditions", {}))
        conditions["requires_flags"] = tuple(conditions.get("requires_flags", []))
        conditions["excludes_flags"] = tuple(conditions.get("excludes_flags", []))
        entry = StoryGuidance(**item, conditions=ChoiceConditions(**conditions))
        if entry.id in seen_ids:
            raise ValueError(f"Doppelter Storyhinweis: {entry.id}")
        if not entry.text.strip():
            raise ValueError(f"Leerer Storyhinweis: {entry.id}")
        seen_ids.add(entry.id)
        guidance.append(entry)
    return tuple(guidance)


def _is_unconditional(conditions: ChoiceConditions) -> bool:
    return (
        conditions.min_level == 1
        and not conditions.requires_flags
        and not conditions.excludes_flags
        and not conditions.min_friendship
        and conditions.quest_active is None
        and conditions.quest_completed is None
        and conditions.party_contains is None
    )


def load_story_triggers(path: Path = STORY_FILE) -> tuple[StoryTrigger, ...]:
    """Lädt ortsbasierte Auslöser aus der Storydatei."""

    data = json.loads(path.read_text(encoding="utf-8"))
    triggers = []
    for source in data.get("triggers", []):
        raw_trigger = dict(source)
        raw_trigger["requires_flags"] = tuple(raw_trigger.get("requires_flags", []))
        raw_trigger["excludes_flags"] = tuple(raw_trigger.get("excludes_flags", []))
        triggers.append(StoryTrigger(**raw_trigger))
    ids = [trigger.id for trigger in triggers]
    if len(ids) != len(set(ids)):
        raise ValueError("Doppelte Storytrigger sind nicht erlaubt.")
    nodes = load_story(path)
    unknown_nodes = {trigger.node for trigger in triggers} - nodes.keys()
    if unknown_nodes:
        raise ValueError(f"Storytrigger verweist auf unbekannte Knoten: {sorted(unknown_nodes)}")
    quest_ids = {
        quest["id"]
        for node in nodes.values()
        for choice in node.choices
        if (quest := choice.effects.get("start_quest"))
    }
    for trigger in triggers:
        if trigger.min_level < 1:
            raise ValueError(f"Ungültiges Mindestlevel bei Trigger: {trigger.id}")
        for quest_id in (trigger.quest_active, trigger.quest_completed):
            if quest_id and quest_id not in quest_ids:
                raise ValueError(f"Unbekannte Quest bei Trigger {trigger.id}: {quest_id}")
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
        self.nodes = nodes if nodes is not None else load_story()
        self.triggers = triggers if triggers is not None else load_story_triggers()

    @property
    def current(self) -> StoryNode:
        return self.nodes[self.game.story.current_node]

    @property
    def available_choices(self) -> tuple[StoryChoice, ...]:
        return tuple(
            choice for choice in self.current.choices if choice.conditions.matches(self.game)
        )

    def choose(self, choice_id: str) -> list[str]:
        choice = next(
            (candidate for candidate in self.available_choices if candidate.id == choice_id),
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
                self.game.location.items.append(item)
                messages.append(f"Inventar voll – {item} liegt am Ort bereit.")
        for item in effects.get("add_items", []):
            if self.game.player.add_item(item):
                messages.append(f"Erhalten: {item}")
            else:
                self.game.location.items.append(item)
                messages.append(f"Inventar voll – {item} liegt am Ort bereit.")
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
                    kind=quest.get("kind", "side"),
                    reward_experience=quest.get("reward_experience", 0),
                    reward_items=list(quest.get("reward_items", [])),
                    objective_type=quest.get("objective_type"),
                    objective_target=quest.get("objective_target"),
                    objective_location=quest.get("objective_location"),
                    completion_text=quest.get("completion_text"),
                )
                messages.append(f"Neue Quest: {quest['title']}")
        if quest_id := effects.get("complete_quest"):
            messages.extend(self.game.advance_quest(quest_id, complete=True))
        if quest_id := effects.get("advance_quest"):
            messages.extend(self.game.advance_quest(quest_id))
        if effects.get("pacify_enemy") and self.game.location.enemy:
            self.game.location.enemy.health = 0
        if effects.get("finish_game"):
            self.game.finished = True
        return messages
