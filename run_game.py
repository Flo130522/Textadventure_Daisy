# region load data
#Externe Files importieren
from Charakterstuff import *
from angriffsmechanik import *
from gamelogic import *
from dungeon import *
#Locations aus JSON Datei laden
with open(r"json\locations.json") as fd:
    locations = json.load(fd)
    
#Items aus JSON Datei laden
with open(r"json\items.json") as fd:
    items = json.load(fd)

#Charaktere aus JSON Datei laden
with open(r"json\characters.json") as fd:
    characters = json.load(fd)
    daisy = characters["friends"]["Daisy"]

#Skills aus JSON Datei laden
with open(r"json\skills.json") as fd:
    skills = json.load(fd)

#Effects aus JSON Datei laden
with open(r"json\effects.json") as fd:
    effects = json.load(fd)
# endregion load data

def game():
    while True:
        print(ascii_art2)
        main_menu()
        new_game_menu()
        load_game()
        start_adventure()
        display_team()
        display_inventory()
        display_stats()
        add_friend()
        add_to_inventory()
        learn_skill()
        collect_xp()
        level_up()
        travel_menu()
        ingame_menu()
        random_encounter()
        explore_location()

game()



