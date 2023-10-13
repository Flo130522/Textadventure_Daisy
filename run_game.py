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
#region Main Menu
# Titelgrafik
ascii_art1 = art.text2art("Das Abenteuer des Rachedackels", font="small")
ascii_art2 = ascii_art1 + "\n" + art.text2art("Daisy gegen Hubertus Snickers", font="small")
print(ascii_art2)

# Hauptmenü
def main_menu():
    while True:
        print("\nHauptmenü:")
        print("1. Neues Spiel starten")
        print("2. Spiel laden")
        print("3. Spiel beenden")

        choice = input("Bitte wähle eine Option: ")

        if choice == "1":
            new_game_menu()
        elif choice == "2":
            load_game()
        elif choice == "3":
            print("Spiel wird beendet. Auf Wiedersehen!")
            break
        else:
            print("Ungültige Option. Bitte wähle erneut.")
            
# Untermenü "Neues Spiel erstellen"
def new_game_menu():
    print("\nNeues Spiel starten:")
    print("1. Zuhause erkunden")
    print("2. Abenteuer starten")

    choice = input("Bitte wähle eine Option: ")

    if choice == "1":
        explore_home()
    elif choice == "2":
        start_adventure()
    else:
        print("Ungültige Option. Bitte wähle erneut.")
        
#Untermenü "Spiel laden"
def load_game(self):
    print("Spiel wird geladen...")
    filename = input("Geben Sie den Dateinamen des Spielstands ein (oder 'zurück' zum Hauptmenü): ")
    if filename.lower() == "zurück":
        return 
    loaded_game = self.load_game(filename)
    if loaded_game:
        self.menu_stack.append(self.loaded_game_menu)
#endregion Main Menu
 