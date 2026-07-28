from daisy.persistence import load_game, save_game
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
