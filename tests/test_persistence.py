import json

import pytest

from daisy.persistence import (
    SAVE_VERSION,
    _game_to_dict,
    autosave,
    available_saves,
    load_game,
    load_slot,
    save_game,
    save_slot,
)
from daisy.story import StoryEngine
from daisy.world import create_game


def test_save_and_load_round_trip(tmp_path):
    game = create_game()
    game.travel("Grauholz")
    game.player.take_damage(17)
    game.player.add_item("Testgegenstand")
    game.player.gain_experience(25)
    game.locations["Zuhause"].visited = True
    StoryEngine(game).choose("father")
    save_file = tmp_path / "save.json"

    save_game(game, save_file)
    loaded = load_game(save_file)

    assert loaded.current_location == "Grauholz"
    assert loaded.player.health == 83
    assert loaded.player.inventory == ["Testgegenstand"]
    assert loaded.player.experience == 25
    assert loaded.locations["Zuhause"].visited
    assert loaded.story.current_node == "morning_father"
    assert loaded.story.choices == {"prologue_morning": "father"}
    assert "spoke_with_father" in loaded.story.flags
    assert loaded.locations["Finsterwald"].enemy is not None
    assert loaded.locations["Finsterwald"].enemy.name == "Spinnenkönigin"
    assert loaded.locations["Finsterwald"].dungeon_name == "Das Netzgewölbe"
    assert loaded.locations["Finsterwald"].encounters[0].name == "Waldwolf"
    assert loaded.locations["Finsterwald"].dungeon_loot == [
        "Spinnenseide",
        "Heilkraut",
        "Leuchtpilz",
    ]
    assert loaded.locations["Dorfbaumhaus"].safe_haven


def test_old_unversioned_save_without_story_attacks_or_equipment_is_migrated(tmp_path):
    game = create_game()
    save_file = tmp_path / "old-save.json"
    save_game(game, save_file)
    data = json.loads(save_file.read_text(encoding="utf-8"))
    data.pop("save_version")
    data.pop("story")
    data["player"].pop("attacks")
    data["player"].pop("equipment")
    save_file.write_text(json.dumps(data), encoding="utf-8")

    loaded = load_game(save_file)

    assert loaded.story.complete
    assert loaded.player.attacks
    assert loaded.player.equipment == {}


def test_new_save_records_version_and_round_trips_equipment(tmp_path):
    game = create_game()
    game.player.inventory.append("Spinnenfänger-Halsband")
    game.player.equip("Spinnenfänger-Halsband")
    save_file = tmp_path / "save.json"

    save_game(game, save_file)
    data = json.loads(save_file.read_text(encoding="utf-8"))
    loaded = load_game(save_file)

    assert data["save_version"] == SAVE_VERSION
    assert loaded.player.equipment == {"collar": "Spinnenfänger-Halsband"}


def test_named_slots_and_autosave_use_separate_files(tmp_path):
    game = create_game()

    manual = save_slot(game, "slot-1", tmp_path)
    automatic = autosave(game, tmp_path)

    assert manual.name == "slot-1.json"
    assert automatic.name == "autosave.json"
    assert manual.exists() and automatic.exists()


def test_available_saves_exposes_player_facing_metadata(tmp_path):
    game = create_game()
    game.current_location = "Grauholz"
    game.player.level = 3
    save_slot(game, "slot-2", tmp_path)

    saves = available_saves(tmp_path)

    assert len(saves) == 1
    assert saves[0].slot == "slot-2"
    assert saves[0].location == "Grauholz"
    assert saves[0].level == 3


def test_slot_load_recovers_previous_valid_backup(tmp_path):
    game = create_game()
    game.current_location = "Grauholz"
    save_slot(game, "slot-1", tmp_path)
    game.current_location = "Dorfmarkt"
    save_slot(game, "slot-1", tmp_path)
    slot_file = tmp_path / "slot-1.json"
    slot_file.write_text("kaputt", encoding="utf-8")

    loaded = load_slot("slot-1", tmp_path)

    assert loaded.current_location == "Grauholz"
    assert [save.slot for save in available_saves(tmp_path)] == ["slot-1"]


def test_load_removes_equipment_that_is_not_in_inventory(tmp_path):
    game = create_game()
    save_file = tmp_path / "invalid-equipment.json"
    save_game(game, save_file)
    data = json.loads(save_file.read_text(encoding="utf-8"))
    data["player"]["equipment"] = {"collar": "Runenhalsband"}
    save_file.write_text(json.dumps(data), encoding="utf-8")

    loaded = load_game(save_file)

    assert loaded.player.equipment == {}
    assert loaded.player.equipment_attack_bonus == 0


def test_all_current_state_fields_survive_round_trip(tmp_path):
    game = create_game()
    game.player.inventory.append("Runenhalsband")
    game.player.equip("Runenhalsband")
    game.player.statuses["Vergiftung"] = 2
    game.story.party = ["Leika", "Jack"]
    game.story.friendship = {"Leika": 4, "Jack": 5}
    game.story.flags.add("integration-test")
    game.locations["Finsterwald"].enemy.statuses["Verteidigung"] = 1
    save_file = tmp_path / "complete-state.json"

    save_game(game, save_file)
    loaded = load_game(save_file)

    assert _game_to_dict(loaded) == _game_to_dict(game)


def test_load_rejects_inconsistent_completed_quest(tmp_path):
    game = create_game()
    StoryEngine(game).choose("breakfast")
    save_file = tmp_path / "bad-quest.json"
    save_game(game, save_file)
    data = json.loads(save_file.read_text(encoding="utf-8"))
    data["story"]["quests"] = {
        "broken": {
            "title": "Kaputt",
            "description": "Test",
            "status": "completed",
            "progress": 0,
            "target": 1,
        }
    }
    save_file.write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(ValueError, match="Queststatus"):
        load_game(save_file)
