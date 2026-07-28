import json

import pytest

from daisy.world import create_world


def test_world_is_loaded_from_json():
    world = create_world()

    assert set(world) == {
        "Zuhause",
        "Grauholz",
        "Dorfmarkt",
        "Finsterwald",
        "Hundewacht",
        "Magierturm",
        "Rettungs-Hundehütte",
        "Water-City",
        "Bootswacht",
        "Wolkenstadt",
        "Säuresumpf",
        "Dorfbaumhaus",
        "Waldbaumhaus",
        "Wolkenbaumhaus",
        "Kristallhöhle",
        "Heilkräuterhöhle",
        "Feuerreich",
        "Schlosstor",
        "Thronsaal",
    }
    assert world["Finsterwald"].enemy is not None
    assert world["Dorfbaumhaus"].safe_haven
    assert world["Feuerreich"].enemy is not None


def test_unknown_connection_is_rejected(tmp_path):
    world_file = tmp_path / "world.json"
    world_file.write_text(
        json.dumps(
            {
                "locations": [
                    {
                        "name": "Zuhause",
                        "description": "Test",
                        "connections": ["Nirgendwo"],
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Unbekannte Verbindung"):
        create_world(world_file)
