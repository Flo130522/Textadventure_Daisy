import json
import random

import pytest

from daisy.story import StoryEngine, load_story
from daisy.world import create_game


def play_prologue(game, choices):
    engine = StoryEngine(game)
    messages = []
    for choice in choices:
        messages.extend(engine.choose(choice))
    return messages


def win_battle(game, enemy, seed=7):
    rng = random.Random(seed)
    while enemy.is_alive and game.player.is_alive:
        game.attack(enemy, rng=rng, attack=game.player.attacks[1])
        if enemy.is_alive:
            game.enemy_attack(enemy, rng=rng)
    assert game.player.is_alive
    return game.complete_victory(enemy)


def test_accepting_leika_starts_first_quest_and_friendship():
    game = create_game()

    messages = play_prologue(
        game,
        ["father", "continue", "hide", "follow_blood", "take_sigil", "accept", "begin"],
    )

    assert game.story.complete
    assert game.story.chapter == "Kapitel I – Asche über Grauholz"
    assert game.story.party == ["Leika"]
    assert game.story.friendship_level("Leika") == 1
    assert "Schwarzes Abzeichen" in game.player.inventory
    assert "trace_collectors" in game.story.quests
    assert any("Neue Quest" in message for message in messages)


def test_leika_joins_even_if_daisy_initially_refuses():
    game = create_game()

    play_prologue(
        game,
        [
            "breakfast",
            "resist",
            "leave_house",
            "meet_leika",
            "push_away",
            "relent",
            "begin",
        ],
    )

    assert game.story.party == ["Leika"]
    assert game.story.friendship_level("Leika") == 0
    assert "pushed_leika_away" in game.story.flags


def test_dorfmarkt_completes_the_first_story_quest():
    game = create_game()
    play_prologue(
        game,
        ["breakfast", "hide", "leave_house", "meet_leika", "accept", "begin"],
    )
    game.travel("Grauholz")
    game.travel("Dorfmarkt")

    messages = game.update_location_quests()

    assert game.story.quests["trace_collectors"].completed
    assert any("Quest abgeschlossen" in message for message in messages)
    assert game.update_location_quests() == []


def test_story_loader_rejects_unknown_nodes(tmp_path):
    story_file = tmp_path / "story.json"
    story_file.write_text(
        json.dumps(
            {
                "nodes": [
                    {
                        "id": "start",
                        "title": "Start",
                        "text": ["Text"],
                        "choices": [{"id": "go", "label": "Los", "next_node": "missing"}],
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Unbekannte Storyknoten"):
        load_story(story_file)


def test_complete_campaign_reaches_justice_ending():
    game = create_game()
    play_prologue(
        game,
        ["breakfast", "hide", "leave_house", "meet_leika", "accept", "begin"],
    )
    game.collect_items()

    assert game.travel("Grauholz")
    assert game.travel("Dorfmarkt")
    game.collect_items()
    game.update_location_quests()
    assert game.activate_story_for_location()
    play_prologue(game, ["help", "accept"])

    assert game.travel("Finsterwald")
    spider = game.location.enemy
    win_battle(game, spider)
    assert game.activate_story_for_location()
    play_prologue(game, ["protect"])
    assert "Bruno" in game.story.party
    assert game.player.level >= 2

    assert game.travel("Hundewacht")
    assert game.travel("Rettungs-Hundehütte")
    assert game.activate_story_for_location()
    play_prologue(game, ["promise"])
    game.update_location_quests()
    assert game.activate_story_for_location()
    play_prologue(game, ["welcome"])
    assert "Jack" in game.story.party

    assert game.travel("Hundewacht")
    assert game.travel("Finsterwald")
    assert game.travel("Magierturm")
    assert game.activate_story_for_location()
    play_prologue(game, ["learn"])
    assert "Leo" in game.story.party

    assert game.travel("Finsterwald")
    assert game.travel("Hundewacht")
    for location, choice, flag in [
        ("Water-City", "accept", "water_sign"),
        ("Bootswacht", "accept", "earth_sign"),
        ("Wolkenstadt", "accept", "sky_sign"),
        ("Säuresumpf", "spare", "spared_kaltklinge"),
    ]:
        assert game.travel(location)
        enemy = game.location.enemy
        win_battle(game, enemy)
        assert game.activate_story_for_location()
        play_prologue(game, [choice])
        assert flag in game.story.flags

    assert game.travel("Schlosstor")
    assert game.activate_story_for_location()
    play_prologue(game, ["free"])
    assert "willy_resolved" in game.story.flags

    assert game.travel("Thronsaal")
    assert game.activate_story_for_location()
    play_prologue(game, ["fight"])
    hubertus = game.location.enemy
    win_battle(game, hubertus)
    assert game.activate_story_for_location()
    play_prologue(game, ["justice", "end"])

    assert game.finished
    assert "ending_justice" in game.story.flags
    assert game.story.party == ["Leika", "Bruno", "Jack", "Leo"]
