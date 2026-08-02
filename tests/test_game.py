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


def test_victory_does_not_claim_reward_when_inventory_is_full():
    game = create_game()
    game.player.inventory = [
        f"Ballast {number}" for number in range(game.player.inventory_capacity)
    ]
    enemy = Enemy("Beutelhüter", health=0, attack_power=1, reward="Seltener Fund")

    messages = game.complete_victory(enemy)

    assert "Seltener Fund" not in game.player.inventory
    assert any("Inventar voll" in message and "Seltener Fund" in message for message in messages)
    assert not any("Daisy erhält: Seltener Fund" in message for message in messages)
    assert "Seltener Fund" in game.location.items


def test_same_enemy_victory_cannot_be_rewarded_twice():
    game = create_game()
    enemy = Enemy("Einmalig", health=0, attack_power=1, experience_reward=25)

    first = game.complete_victory(enemy)
    second = game.complete_victory(enemy)

    assert first
    assert second == []
    assert game.player.experience == 25
    assert game.player.defeated_enemies == {"Einmalig": 1}


def test_poison_death_prevents_player_attack():
    game = create_game()
    game.player.health = 5
    game.player.statuses["Vergiftung"] = 1
    enemy = Enemy("Ziel", health=20, attack_power=1)

    assert game.attack(enemy, random.Random(1)) == 0
    assert not game.player.is_alive
    assert enemy.health == 20


def test_tactical_enemy_can_prepare_and_execute_strong_attack():
    game = create_game()
    enemy = Enemy(
        "Taktiker",
        health=30,
        max_health=100,
        attack_power=10,
        behavior="boss",
        phase_threshold=0.5,
    )

    prepared = game.enemy_turn(enemy, random.Random(9))
    health_before = game.player.health
    strong = game.enemy_turn(enemy, random.Random(1))

    assert prepared.action == "prepare"
    assert strong.action == "strong"
    assert strong.damage == health_before - game.player.health


def test_enemy_can_heal_and_dead_enemy_cannot_act():
    game = create_game()
    enemy = Enemy(
        "Heiler",
        health=30,
        max_health=100,
        attack_power=5,
        heal_power=12,
    )

    healed = game.enemy_turn(enemy, random.Random(1))
    assert healed.action == "heal"
    assert healed.healing == 12
    assert enemy.health == 42

    enemy.health = 0
    assert game.enemy_turn(enemy, random.Random(1)).action == "inactive"


def test_enemy_defense_reduces_exactly_one_player_attack():
    game = create_game()
    enemy = Enemy("Wächter", health=100, attack_power=5)
    enemy.statuses["Verteidigung"] = 1

    defended = game.attack(enemy, random.Random(3), Attack("Test", 0, ""))
    enemy.health = 100
    normal = game.attack(enemy, random.Random(3), Attack("Test", 0, ""))

    assert defended < normal
    assert "Verteidigung" not in enemy.statuses


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


def test_safe_haven_does_not_discard_equipped_or_quest_items():
    game = create_game()
    game.current_location = "Dorfbaumhaus"
    game.player.inventory = ["Spinnenfänger-Halsband", "Schwarzes Abzeichen", "Stein"]
    assert game.player.equip("Spinnenfänger-Halsband")

    assert game.discard_inventory_stack("Spinnenfänger-Halsband") == 0
    assert game.discard_inventory_stack("Schwarzes Abzeichen") == 0
    assert game.discard_inventory_stack("Stein") == 1
    assert game.player.equipment_defense_bonus == 2


def test_cli_equipment_menu_uses_the_same_character_rules():
    game = create_game()
    game.player.inventory.append("Runenhalsband")
    messages: list[str] = []

    game._equipment_menu(lambda _prompt: "1", messages.append)

    assert game.player.equipment == {"collar": "Runenhalsband"}
    assert game.player.equipment_attack_bonus == 3
    assert any("Daisy legt Runenhalsband an" in message for message in messages)


def test_equipment_menu_reports_replacing_the_current_collar():
    game = create_game()
    game.player.inventory = ["Spinnenfänger-Halsband", "Runenhalsband"]
    game.player.equip("Spinnenfänger-Halsband")
    messages: list[str] = []

    game._equipment_menu(lambda _prompt: "2", messages.append)

    assert game.player.equipment == {"collar": "Runenhalsband"}
    assert game.player.equipment_attack_bonus == 3
    assert game.player.equipment_defense_bonus == 0
    assert any("wechselt Spinnenfänger-Halsband" in message for message in messages)


def test_inventory_summary_shows_types_and_equipped_state():
    game = create_game()
    game.player.inventory = ["Heilkraut", "Schwarzes Abzeichen", "Runenhalsband"]
    game.player.equip("Runenhalsband")

    summary = game.inventory_summary()

    assert any("Heilkraut [Verbrauch]" in line and "Heilt 30 LP" in line for line in summary)
    assert any("Schwarzes Abzeichen [Questitem]" in line for line in summary)
    assert any("Runenhalsband [Ausrüstung] – angelegt" in line for line in summary)


def test_inventory_summary_groups_items_for_quick_scanning():
    game = create_game()
    game.player.inventory = ["Stein", "Heilkraut", "Runenhalsband", "Schwarzes Abzeichen"]

    summary = game.inventory_summary(detailed=False)

    assert [line.split(" [")[1].split("]")[0] for line in summary] == [
        "Questitem",
        "Ausrüstung",
        "Verbrauch",
        "Beute",
    ]


def test_locked_destination_explains_story_reason_without_exposing_flags():
    game = create_game()
    game.current_location = "Hundewacht"

    reason = game.travel_block_reason("Water-City")

    assert reason == "Der Weg nach Water-City wird erst mit Leos Magie passierbar."
    assert "leo_joined" not in reason


def test_dungeon_encounter_carries_location_loot():
    game = create_game()
    game.current_location = "Finsterwald"

    enemy = game.create_encounter(random.Random(3), dungeon=True)

    assert enemy is not None
    assert enemy.reward in game.location.dungeon_loot


def test_encounter_group_size_follows_party_size():
    solo_game = create_game()
    solo_game.current_location = "Finsterwald"
    assert len(solo_game.create_encounter_group(random.Random(0))) == 1

    duo_game = create_game()
    duo_game.current_location = "Finsterwald"
    duo_game.story.party = ["Leika"]
    assert len(duo_game.create_encounter_group(random.Random(0))) == 2

    full_game = create_game()
    full_game.current_location = "Finsterwald"
    full_game.story.party = ["Leika", "Bruno", "Jack"]
    assert len(full_game.create_encounter_group(random.Random(0))) == 4


def test_group_battle_rewards_every_defeated_enemy():
    game = create_game()
    game.story.complete = True
    enemies = [
        Enemy("Ratte A", health=1, attack_power=0, experience_reward=10),
        Enemy("Ratte B", health=1, attack_power=0, experience_reward=15),
    ]
    answers = iter(["1", "1", "1", "1", "1"])
    messages: list[str] = []

    game._battle_group(enemies, lambda _prompt: next(answers), messages.append)

    assert game.player.experience == 25
    assert game.player.defeated_enemies == {"Ratte A": 1, "Ratte B": 1}
    assert any("Ratte A wurde besiegt" in message for message in messages)
    assert any("Ratte B wurde besiegt" in message for message in messages)
