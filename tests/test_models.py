from daisy.models import Character, Enemy, Location


def test_damage_and_healing_stay_within_limits():
    daisy = Character("Daisy", "Dackel-Mix", "Nahkampf")

    daisy.take_damage(120)
    assert daisy.health == 0

    healed = daisy.heal(200)
    assert healed == 100
    assert daisy.health == 100


def test_healing_item_is_consumed():
    daisy = Character("Daisy", "Dackel-Mix", "Nahkampf", health=50)
    daisy.add_item("Heilkraut")

    assert daisy.use_healing_item() == 30
    assert daisy.health == 80
    assert "Heilkraut" not in daisy.inventory


def test_healing_item_is_not_consumed_at_full_health():
    daisy = Character("Daisy", "Dackel-Mix", "Nahkampf", inventory=["Heilkraut"])

    assert daisy.use_healing_item() == 0
    assert daisy.inventory == ["Heilkraut"]


def test_different_consumables_use_their_own_healing_values():
    daisy = Character(
        "Daisy",
        "Dackel-Mix",
        "Nahkampf",
        health=20,
        inventory=["Heilpilz", "Heilwasser", "Verbandszeug"],
    )

    assert daisy.use_consumable("Heilpilz") == 20
    assert daisy.use_consumable("Verbandszeug") == 25
    assert daisy.use_consumable("Heilwasser") == 35
    assert daisy.health == daisy.max_health
    assert daisy.inventory == []


def test_connections_are_not_duplicated():
    home = Location("Zuhause", "Gemütlich")

    home.connect("Grauholz", "Grauholz")

    assert home.connections == ["Grauholz"]


def test_enemy_cannot_have_negative_health():
    spider = Enemy("Spinne", health=10, attack_power=2)

    spider.take_damage(50)

    assert spider.health == 0
    assert not spider.is_alive


def test_experience_can_award_multiple_levels():
    daisy = Character("Daisy", "Dackel-Mix", "Nahkampf")

    levels = daisy.gain_experience(350)

    assert levels == 2
    assert daisy.level == 3
    assert daisy.experience == 50
    assert daisy.max_health == 120
    assert daisy.health == 120


def test_victories_are_counted_by_enemy_name():
    daisy = Character("Daisy", "Dackel-Mix", "Nahkampf")

    daisy.record_victory("Spinne")
    daisy.record_victory("Spinne")

    assert daisy.defeated_enemies == {"Spinne": 2}


def test_string_inventory_supports_optional_equipment_metadata():
    daisy = Character("Daisy", "Dackel-Mix", "Nahkampf")
    daisy.add_item("Spinnenfänger-Halsband")

    assert daisy.equip("Spinnenfänger-Halsband")
    assert daisy.equipment == {"collar": "Spinnenfänger-Halsband"}
    assert daisy.equipment_defense_bonus == 2
