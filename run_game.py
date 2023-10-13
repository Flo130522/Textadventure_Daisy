#region Dateiimport
import json
import pickle
from datetime import datetime
import art
import random
# Locations
with open(r"json\locations.json",encoding="utf-8") as fd:
    locations = json.load(fd)

# Charaktere
with open(r"json\characters.json",encoding="utf-8") as fd:
    charaktere = json.load(fd)
    friends = characters["friends"]
    enemys = characters["enemies"]

# Items
with open(r"json\items.json",encoding="utf-8") as fd:
    items = json.load(fd)

# Skills
with open(r"json\skills.json",encoding="utf-8") as fd:
    skills = json.load(fd)

# Dungeons
with open(r"json\dungeons.json",encoding="utf-8") as fd:
    dungeons = json.load(fd)

# Effects
with open(r"json\effects.json",encoding="utf-8") as fd:
    effects = json.load(fd)
#endregion Dateiimport
#