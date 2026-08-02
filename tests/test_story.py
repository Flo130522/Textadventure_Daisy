import json
import random
from pathlib import Path

import pytest

from daisy.models import Enemy
from daisy.persistence import _game_to_dict, load_game, save_game
from daisy.story import QuestState, StoryEngine, load_story
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


def test_story_loader_rejects_unknown_effects_early(tmp_path):
    story_file = tmp_path / "story.json"
    story_file.write_text(
        json.dumps(
            {
                "nodes": [
                    {
                        "id": "start",
                        "title": "Start",
                        "text": ["Text"],
                        "choices": [
                            {
                                "id": "go",
                                "label": "Los",
                                "next_node": "COMPLETE",
                                "effects": {"typo_flag": "broken"},
                            }
                        ],
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Unbekannte Storyeffekte"):
        load_story(story_file)


def test_story_loader_requires_an_unconditional_fallback_choice(tmp_path):
    story_file = tmp_path / "story.json"
    story_file.write_text(
        json.dumps(
            {
                "nodes": [
                    {
                        "id": "start",
                        "title": "Start",
                        "text": ["Text"],
                        "choices": [
                            {
                                "id": "locked",
                                "label": "Nur später",
                                "next_node": "COMPLETE",
                                "conditions": {"min_level": 99},
                            }
                        ],
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Rückfallentscheidung"):
        load_story(story_file)


def test_story_choices_obey_friendship_party_flags_quest_and_level():
    game = create_game()
    game.story.current_node = "market_aftermath"
    game.story.complete = False
    engine = StoryEngine(game)

    assert "trust_leika" not in {choice.id for choice in engine.available_choices}
    with pytest.raises(ValueError, match="Unbekannte Storyentscheidung"):
        engine.choose("trust_leika")

    game.story.party.append("Leika")
    game.story.add_friendship("Leika", 2)
    assert "trust_leika" in {choice.id for choice in engine.available_choices}
    engine.choose("trust_leika")
    assert "trusted_leika_at_market" in game.story.flags


def test_friendship_unlocks_named_perks_and_strengthens_party_bonus():
    game = create_game()
    game.story.party.append("Leika")
    enemy = game.locations["Finsterwald"].enemy
    assert enemy is not None
    damage_without_level = game.attack(enemy, random.Random(2))

    game.story.add_friendship("Leika", 2)
    enemy.health = enemy.max_health or 70
    damage_with_level = game.attack(enemy, random.Random(2))

    assert game.story.friendship_perks("Leika") == ("Spürsinn",)
    assert damage_with_level == damage_without_level + 1


def test_quest_rewards_experience_and_items_exactly_once():
    game = create_game()
    game.story.quests["delivery"] = QuestState(
        "Lieferung",
        "Bringe das Paket.",
        kind="side",
        reward_experience=35,
        reward_items=["Heilkraut"],
    )

    messages = game.advance_quest("delivery")

    assert game.player.experience == 35
    assert game.player.inventory == ["Heilkraut"]
    assert any("35 EP" in message for message in messages)
    assert game.advance_quest("delivery") == []
    assert game.player.experience == 35


def test_full_inventory_places_quest_item_at_current_location():
    game = create_game()
    game.player.inventory = [
        f"Ballast {number}" for number in range(game.player.inventory_capacity)
    ]
    game.story.quests["reward"] = QuestState(
        "Belohnung",
        "Test",
        reward_items=["Runenhalsband"],
    )

    messages = game.advance_quest("reward")

    assert "Runenhalsband" in game.location.items
    assert any("liegt am Ort bereit" in message for message in messages)


def test_data_driven_item_delivery_can_progress_in_two_visits():
    game = create_game()
    game.current_location = "Rettungs-Hundehütte"
    game.story.quests["medicine"] = QuestState(
        "Medizin",
        "Bringe zwei Kräuter.",
        target=2,
        objective_type="deliver_item",
        objective_target="Heilkraut",
        objective_location="Rettungs-Hundehütte",
    )
    game.player.inventory = ["Heilkraut"]

    first_messages = game.turn_in_quest("medicine")
    assert game.story.quests["medicine"].progress == 1
    assert not game.story.quests["medicine"].completed
    assert "Heilkraut" not in game.player.inventory
    assert any("Abgegeben: 1× Heilkraut" in message for message in first_messages)

    game.player.inventory.append("Heilkraut")
    second_messages = game.turn_in_quest("medicine")
    assert game.story.quests["medicine"].completed
    assert any("Quest abgeschlossen" in message for message in second_messages)


def test_enemy_victory_advances_matching_data_driven_quest():
    game = create_game()
    game.story.quests["hunt"] = QuestState(
        "Jagd",
        "Besiege die Zielspinne.",
        objective_type="defeat_enemy",
        objective_target="Zielspinne",
    )

    messages = game.complete_victory(
        Enemy("Zielspinne", health=0, attack_power=1, experience_reward=0)
    )

    assert game.story.quests["hunt"].completed
    assert any("Quest abgeschlossen: Jagd" in message for message in messages)


def test_quest_summary_explains_the_next_objective_in_german():
    game = create_game()
    game.story.quests["delivery"] = QuestState(
        "Lieferung",
        "Beschreibung",
        target=2,
        progress=1,
        objective_type="deliver_item",
        objective_target="Heilkraut",
        objective_location="Hundewacht",
    )

    summary = game.quest_summary()[0]

    assert "Aktiv" in summary
    assert "1× Heilkraut nach Hundewacht bringen" in summary


def test_completed_quest_no_longer_claims_its_old_objective_is_active():
    game = create_game()
    game.story.quests["done"] = QuestState(
        "Erledigt",
        "Alte Aufgabe",
        status="completed",
        progress=1,
        objective_type="visit_location",
        objective_target="Grauholz",
    )

    summary = game.quest_summary()[0]

    assert "Abgeschlossen." in summary
    assert "Grauholz besuchen" not in summary


def test_primary_objective_prioritizes_active_main_quest():
    game = create_game()
    game.story.quests["side"] = QuestState("Nebenweg", "Optional", kind="side")
    game.story.quests["main"] = QuestState(
        "Die Spur",
        "Folge ihr.",
        kind="main",
        objective_type="visit_location",
        objective_target="Dorfmarkt",
    )

    assert game.primary_objective() == "Die Spur: Dorfmarkt besuchen."


def test_story_guidance_fills_gap_between_jack_and_leo():
    game = create_game()
    game.story.flags.add("jack_joined")
    game.story.party.append("Jack")
    game.current_location = "Heilkräuterhöhle"

    assert "Magierturm" in game.primary_objective()


def test_party_summary_explains_friendship_perks_and_real_bonus():
    game = create_game()
    game.story.party = ["Jack"]
    game.story.friendship["Jack"] = 5

    summary = game.party_summary()[0]

    assert "Stufe 2" in summary
    assert "Starke Medizin" in summary
    assert "Verteidigung +3" in summary
    assert "20 LP" in summary


def test_story_nodes_can_reference_safe_asset_filenames():
    nodes = load_story()

    assert nodes["ashes_of_grauholz"].image == "story-leika-joins.png"
    assert nodes["bruno_recruit"].image == "story-bruno-joins.png"
    assert nodes["jack_backpack_memory"].image == "story-jack-backpack.png"


def test_current_story_references_existing_scene_images():
    nodes = load_story()

    assert all(
        not node.image or (Path(__file__).parents[1] / "daisy" / "assets" / node.image).is_file()
        for node in nodes.values()
    )


def test_jacks_optional_backpack_memory_deepens_trust_once():
    game = create_game()
    game.story.complete = True
    game.story.flags.update({"bruno_joined", "jack_joined"})
    game.story.party.extend(["Bruno", "Jack"])
    game.story.add_friendship("Jack", 2)
    game.current_location = "Waldbaumhaus"

    assert game.activate_story_for_location()
    assert game.story.current_node == "jack_backpack_memory"

    messages = StoryEngine(game).choose("make_room")

    assert game.story.complete
    assert "jack_memory_shared" in game.story.flags
    assert "jack_has_travel_place" in game.story.flags
    assert game.story.friendship_level("Jack") == 2
    assert "Starke Medizin" in game.story.friendship_perks("Jack")
    assert any("Freundschaft mit Jack: Stufe 2" in message for message in messages)
    assert not game.activate_story_for_location()


def test_revenge_choice_after_kaltklinge_has_its_own_consequence():
    game = create_game()
    game.story.current_node = "kaltklinge_defeated"
    game.story.complete = False
    game.story.party = ["Leika"]
    game.story.friendship["Leika"] = 2

    StoryEngine(game).choose("revenge")

    assert "killed_kaltklinge" in game.story.flags
    assert "spared_kaltklinge" not in game.story.flags
    assert game.story.friendship["Leika"] == 1


def test_fighting_willy_requires_battle_before_the_throne_room_opens():
    game = create_game()
    game.current_location = "Schlosstor"
    game.story.current_node = "willy_choice"
    game.story.complete = False

    StoryEngine(game).choose("fight")
    assert "willy_resolved" not in game.story.flags
    assert not game.travel("Thronsaal")

    willy = game.location.enemy
    assert willy is not None
    willy.health = 0
    game.complete_victory(willy)
    assert game.activate_story_for_location()
    StoryEngine(game).choose("continue")

    assert "willy_resolved" in game.story.flags
    assert game.travel("Thronsaal")


@pytest.mark.parametrize("ending", ["revenge", "justice", "mercy"])
def test_every_final_choice_reaches_its_ending(ending):
    game = create_game()
    game.story.current_node = "final_choice"
    game.story.complete = False

    StoryEngine(game).choose(ending)
    StoryEngine(game).choose("end")

    assert game.finished
    assert f"ending_{ending}" in game.story.flags


@pytest.mark.parametrize("battle_seed", [1, 7, 23])
def test_complete_campaign_reaches_justice_ending_across_save_boundaries(
    tmp_path, battle_seed
):
    game = create_game()
    save_file = tmp_path / "campaign.json"

    def reload_at_checkpoint():
        nonlocal game
        expected = _game_to_dict(game)
        save_game(game, save_file)
        game = load_game(save_file)
        assert _game_to_dict(game) == expected

    play_prologue(
        game,
        ["breakfast", "hide", "leave_house", "meet_leika", "accept", "begin"],
    )
    game.collect_items()
    reload_at_checkpoint()

    assert game.travel("Grauholz")
    assert game.travel("Dorfmarkt")
    game.collect_items()
    game.update_location_quests()
    assert game.activate_story_for_location()
    play_prologue(game, ["help", "accept"])

    assert game.travel("Finsterwald")
    spider = game.location.enemy
    win_battle(game, spider, battle_seed)
    assert game.activate_story_for_location()
    play_prologue(game, ["protect"])
    assert "Bruno" in game.story.party
    assert game.player.level >= 2

    assert game.travel("Hundewacht")
    assert game.travel("Rettungs-Hundehütte")
    assert game.activate_story_for_location()
    play_prologue(game, ["promise"])
    game.turn_in_quest("gather_herbs_for_jack")
    assert game.activate_story_for_location()
    play_prologue(game, ["welcome"])
    assert "Jack" in game.story.party
    reload_at_checkpoint()

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
        win_battle(game, enemy, battle_seed)
        assert game.activate_story_for_location()
        play_prologue(game, [choice])
        assert flag in game.story.flags

    reload_at_checkpoint()

    assert game.travel("Feuerreich")
    fire_guard = game.location.enemy
    win_battle(game, fire_guard, battle_seed)

    assert game.travel("Schlosstor")
    assert game.activate_story_for_location()
    play_prologue(game, ["free"])
    assert "willy_resolved" in game.story.flags

    assert game.travel("Thronsaal")
    assert game.activate_story_for_location()
    play_prologue(game, ["fight"])
    hubertus = game.location.enemy
    win_battle(game, hubertus, battle_seed)
    assert game.activate_story_for_location()
    play_prologue(game, ["justice", "end"])

    assert game.finished
    assert "ending_justice" in game.story.flags
    assert game.story.party == ["Leika", "Bruno", "Jack", "Leo"]
