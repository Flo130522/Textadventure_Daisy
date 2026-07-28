import random

from daisy.models import Attack, Enemy
from daisy.world import create_game


def test_world_has_a_route_to_the_final_location():
    game = create_game()
    game.story.flags.update(
        {
            "leo_joined",
            "water_sign",
            "earth_sign",
            "sky_sign",
            "defeated:Kaltklinge",
            "defeated:Höllenwache",
            "willy_resolved",
        }
    )

    route = [
        "Grauholz",
        "Dorfmarkt",
        "Finsterwald",
        "Hundewacht",
        "Water-City",
        "Bootswacht",
        "Wolkenstadt",
        "Säuresumpf",
        "Feuerreich",
        "Schlosstor",
        "Thronsaal",
    ]

    assert all(game.travel(destination) for destination in route)
    assert game.current_location == "Thronsaal"


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
    assert enemy.health == 70 - damage


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


def test_victory_rewards_are_shared_by_all_interfaces():
    game = create_game()
    enemy = Enemy(
        "Testgegner",
        health=0,
        attack_power=1,
        reward="Testschlüssel",
        experience_reward=40,
    )

    messages = game.complete_victory(enemy)

    assert game.player.experience == 40
    assert game.player.inventory == ["Testschlüssel"]
    assert game.player.defeated_enemies == {"Testgegner": 1}
    assert any("40 EP" in message for message in messages)


def test_encounters_scale_with_player_level():
    game = create_game()
    game.current_location = "Finsterwald"
    game.player.level = 5

    enemy = game.create_encounter(random.Random(4))

    assert enemy is not None
    assert "(Level 5)" in enemy.name
    assert enemy.health > 50
    assert enemy.experience_reward > 40


def test_attack_effects_and_poison_are_applied():
    game = create_game()
    enemy = Enemy(
        "Giftzahn",
        health=100,
        attack_power=1,
        status_effect="Vergiftung",
        effect_chance=1,
        effect_duration=2,
    )
    stunning_attack = Attack(
        "Sicherer Sprung",
        0,
        "",
        effect="Lähmung",
        effect_chance=1,
        effect_duration=1,
    )

    game.attack(enemy, random.Random(1), stunning_attack)
    assert enemy.statuses == {"Lähmung": 1}
    assert game.enemy_attack(enemy, random.Random(1)) == 0

    game.enemy_attack(enemy, random.Random(1))
    assert game.player.statuses == {"Vergiftung": 2}
    health_before_poison = game.player.health
    game.attack(enemy, random.Random(1))
    assert game.player.health == health_before_poison - 5


def test_inventory_capacity_grows_with_level():
    game = create_game()

    for number in range(game.player.inventory_capacity):
        assert game.player.add_item(f"Gegenstand {number}")
    assert not game.player.add_item("Zu viel")

    game.player.level += 1
    assert game.player.add_item("Passt nach Levelaufstieg")


def test_treehouse_restores_health_clears_status_and_discards_stacks():
    game = create_game()
    game.current_location = "Dorfbaumhaus"
    game.player.take_damage(45)
    game.player.statuses["Vergiftung"] = 2
    game.player.inventory = ["Heilkraut", "Stein", "Heilkraut"]

    assert game.rest() == 45
    assert game.player.health == game.player.max_health
    assert game.player.statuses == {}
    assert game.discard_inventory_stack("Heilkraut") == 2
    assert game.player.inventory == ["Stein"]


def test_rest_and_discard_require_a_safe_haven():
    game = create_game()
    game.player.take_damage(10)
    game.player.inventory = ["Stein"]

    assert game.rest() is None
    assert game.discard_inventory_stack("Stein") == 0
    assert game.player.health == 90
    assert game.player.inventory == ["Stein"]


def test_dungeon_encounter_carries_location_loot():
    game = create_game()
    game.current_location = "Finsterwald"

    enemy = game.create_encounter(random.Random(3), dungeon=True)

    assert enemy is not None
    assert enemy.reward in game.location.dungeon_loot
