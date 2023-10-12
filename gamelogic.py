import json
import art
import pickle
import random
from datetime import datetime
from Charakterstuff import *


# region load data
#Locations aus JSON Datei laden
with open(r"json\locations.json") as fd:
    locations = json.load(fd)
in_front_of_home = locations['Grauholz']['Vor deinem Zuhause']
    
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

#Dungeons aus JSON Datei laden
with open(r"json\dungeons.json") as fd:
    dungeons = json.load(fd)

#Effects aus JSON Datei laden
with open(r"json\effects.json") as fd:
    effects = json.load(fd)

# endregion load data
#ASCII Art bauen
ascii_art1 = art.text2art("Das Abenteuer des Rachedackels", font="small")
ascii_art2 = ascii_art1 + "\n" + art.text2art("Daisy gegen Hubertus Snickers", font="small")

#Funktion "Explore Home" aus run_game.py
#TODO Storyline erweitern
def explore_home():
    print("Daisy lebt mit ihren Eltern in Grauholz. Es ist ein Tag wie jeder andere, die Sonne scheint und es ist angenehm warm.")

    while True:
        print("\nDu befindest dich im Wohnzimmer von Daisys Zuhause.")
        print("1. Mit deinem Papa reden")
        print("2. Mit deiner Mama reden")
        print("3. Zurück zum Hauptmenü")

        choice = input("Bitte wähle eine Option: ")

        if choice == "1":
            print("Dein Papa ist in seine Zeitung vertieft und sagt, 'Guten Morgen, kleines.'")
        elif choice == "2":
            print("Deine Mama lächelt und sagt, 'Guten Morgen Daisylein, iss dein Frühstück bevor es kalt wird!'")
        elif choice == "3":
            break
        else:
            print("Ungültige Option. Bitte wähle 1, 2 oder 3.")
            

        
#Main Menu
def main_menu():
    while True:
        print("\nHauptmenü:")
        print("1. Neues Spiel starten")
        print("  1.1 Zuhause erkunden")
        print("  1.2 Abenteuer starten")
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

def load_game(self):
    print("Spiel wird geladen...")
    filename = input("Geben Sie den Dateinamen des Spielstands ein (oder 'zurück' zum Hauptmenü): ")
    if filename.lower() == "zurück":
        return 
    loaded_game = self.load_game(filename)
    if loaded_game:
        self.menu_stack.append(self.loaded_game_menu)  

#Einführung
def start_adventure():
    print(f"{daisy['name']} erwacht aus ihrem Versteck und sieht eine Blutspur vor sich.")
    choice = input("Möchtest du der Blutspur folgen oder das Haus verlassen? (Blutspur folgen / Haus verlassen): ").strip().lower()

    if choice == "blutspur folgen":
        print("Das willst du nicht sehen, gehe lieber nach draußen.")
    elif choice == "haus verlassen":
        print("Du gehst nach draußen.")
        daisy['location'] = in_front_of_home  
    else:
        print("Ungültige Auswahl. Du gehst sicherheitshalber nach draußen.")
        daisy['location'] = in_front_of_home

def ingame_menu():
    while True:
        print("\nWas möchtest du tun?")
        print("1. Reisen")
        print("2. Inventar anzeigen")
        print("3. Team anzeigen")
        print("4. Speichern")
        print("5. Spiel beenden")

        choice = input("Bitte wähle eine Option: ")
        choice = int(choice)
        
        if choice == 1:
            travel_menu()
        elif choice == 2:
            daisy.display_inventory()
        elif choice == 3:
            display_team()
        elif choice == 4:
            save_game()
        elif choice == 5:
            print("Spiel wird beendet. Auf Wiedersehen!")
            break
        else:
            print("Ungültige Option. Bitte wähle erneut.")

def travel_menu():
    while True:
        print("\nWohin möchtest du reisen?")
        for key in locations.keys():
            print(f"{key}")

        choice = input("Bitte wähle einen Ort (oder 'zurück', um zum Hauptmenü zurückzukehren): ")

        if choice == 'zurück':
            return
        elif choice in locations:
            location_info = locations[choice]
            print(f"Wohin in {choice} möchtest du reisen?")
            for sub_location in location_info:
                print(f"{sub_location}:\n{locations[choice][sub_location]['description']}")
            sub_choice = input("Bitte wähle einen Ort (oder 'zurück', um zur Hauptauswahl zurückzukehren): ")
            if sub_choice == 'zurück':
                continue
            elif sub_choice in location_info:
                sub_location_info = location_info[sub_choice]
                print(f"\n{sub_choice}: {sub_location_info['description']}")
            else:
                print("Ungültige Auswahl. Bitte wähle eine der verfügbaren Orte.")
        else:
            print("Ungültige Auswahl. Bitte wähle eine der verfügbaren Orte.")
def random_encounter():
    if random < 0.5:
            encounter = random.choice['characters']['enemies'] #TODO: Gegner in Zufallskämpfe anpassen
            print(f"Du triffst auf {encounter['name']}.")
    #TODO: Kämpfe implementieren -> angriffslogik.py
            
def explore_location():
    print("Du befindet dich in daisy['location'] ")        
        
def main():
    while True:
        print(ascii_art2)
        main_menu()
        new_game_menu()
        load_game()
        start_adventure()
        ingame_menu()
        display_team()
        display_inventory()
        display_stats()
        add_friend()
        add_to_inventory()
        learn_skill()
        collect_xp()
        level_up()
        travel_menu()
        random_encounter()
        explore_location()
        # Add an option to exit the game gracefully
        exit_choice = input("Möchtest du das Spiel beenden? (ja/nein): ").strip().lower()
        if exit_choice == "ja":
            print("Spiel wird beendet. Auf Wiedersehen!")
            break

if __name__ == "__main__":
    main()
