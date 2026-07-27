from daisy.persistence import load_game, save_game
from daisy.world import create_game


def test_save_and_load_round_trip(tmp_path):
    game = create_game()
    game.travel("Grauholz")
    game.player.take_damage(17)
    game.player.add_item("Testgegenstand")
    game.player.gain_experience(25)
    game.locations["Zuhause"].visited = True
    save_file = tmp_path / "save.json"

    save_game(game, save_file)
    loaded = load_game(save_file)

    assert loaded.current_location == "Grauholz"
    assert loaded.player.health == 83
    assert loaded.player.inventory == ["Testgegenstand"]
    assert loaded.player.experience == 25
    assert loaded.locations["Zuhause"].visited
    assert loaded.locations["Finsterwald"].enemy is not None
    assert loaded.locations["Finsterwald"].enemy.name == "Spinnen-Monster"
