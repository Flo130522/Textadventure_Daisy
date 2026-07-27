import random

from daisy.models import Attack, Enemy
from daisy.world import create_game


def test_world_has_a_route_to_the_final_location():
    game = create_game()

    route = [
        "Grauholz",
        "Dorfmarkt",
        "Finsterwald",
        "Hundewacht",
        "Chihuahua-Höllenreich",
    ]
    assert all(game.travel(destination) for destination in route)
    assert game.current_location == "Chihuahua-Höllenreich"


def test_collecting_items_only_works_once():
    game = create_game()

    assert game.collect_items() == ["Heilkraut"]
    assert game.collect_items() == []
    assert game.player.inventory == ["Heilkraut"]


def test_player_attack_reduces_enemy_health():
    game = create_game()
    enemy = game.locations["Finsterwald"].enemy
    assert enemy is not None

    damage = game.attack(enemy, random.Random(1))

    assert damage > 0
    assert enemy.health == 42 - damage


def test_invalid_travel_does_not_move_player():
    game = create_game()

    assert not game.travel("Hundewacht")
    assert game.current_location == "Zuhause"


def test_selected_attack_changes_damage():
    weak_game = create_game()
    strong_game = create_game()
    weak_enemy = Enemy("Ziel", health=100, attack_power=0)
    strong_enemy = Enemy("Ziel", health=100, attack_power=0)

    weak_damage = weak_game.attack(
        weak_enemy,
        random.Random(3),
        Attack("Schwach", -5, ""),
    )
    strong_damage = strong_game.attack(
        strong_enemy,
        random.Random(3),
        Attack("Stark", 5, ""),
    )

    assert strong_damage > weak_damage


def test_health_bar_reflects_enemy_health():
    game = create_game()
    enemy = Enemy("Boss", health=50, max_health=100, attack_power=1)

    assert game._health_bar(enemy, width=10) == "[#####-----] 50/100"
