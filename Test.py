import json
import art
import random
from Charakterstuff import *
from angriffsmechanik import *
from gamelogic import *
from dungeon import *

# Laden der Daten
with open(r"json\locations.json") as fd:
    locations = json.load(fd)

with open(r"json\items.json") as fd:
    items = json.load(fd)

with open(r"json\characters.json") as fd:
    characters = json.load(fd)
daisy = characters["friends"]["Daisy"]

# Weitere Daten laden (Skills, Dungeons, Effects, etc.)

# ASCII Art erstellen
ascii_art1 = art.text2art("Das Abenteuer des Rachedackels", font="small")
ascii_art2 = ascii_art1 + "\n" + art.text2art("Daisy gegen Hubertus Snickers", font="small")

def main_menu():
    while True:
        print("\nHauptmenü:")
        print("1. Neues Spiel starten")
        print("2. Spiel laden")
        print("3. Spiel beenden")

        choice = input("Bitte wähle eine Option: ")

        if choice == "1":
            new_game()
        elif choice == "2":
            load_game()
        elif choice == "3":
            print("Spiel wird beendet. Auf Wiedersehen!")
            break
        else:
            print("Ungültige Option. Bitte wähle erneut.")

def new_game():
    start_adventure()

def start_adventure():
    print(f"{daisy['name']} erwacht aus ihrem Versteck und sieht eine Blutspur vor sich.")
    choice = input("Möchtest du der Blutspur folgen oder das Haus verlassen? (Blutspur folgen / Haus verlassen): ").strip().lower()

    if choice == "blutspur folgen":
        print("Das willst du nicht sehen, gehe lieber nach draußen.")
    elif choice == "haus verlassen":
        print("Du gehst nach draußen.")
        daisy['location'] = in_front_of_home
        ingame_menu()  
    else:
        print("Ungültige Auswahl. Du gehst sicherheitshalber nach draußen.")
        daisy['location'] = in_front_of_home
        ingame_menu()

def ingame_menu():
    while True:
        print("\nWas möchtest du tun?")
        print("1. Reisen")
        print("2. Inventar anzeigen")
        print("3. Team anzeigen")
        print("4. Speichern")
        print("5. Spiel beenden")

        choice = input("Bitte wähle eine Option: ")

        if choice == "1":
            travel_menu()
        elif choice == "2":
            daisy.display_inventory()
        elif choice == "3":
            display_team()
        elif choice == "4":
            save_game()
        elif choice == "5":
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

def explore_location():
    print(f"Du befindest dich in {daisy['location']}")

def random_encounter():
    if random.random() < 0.5:
        encounter = random.choice(characters['enemies'])
        print(f"Du triffst auf {encounter['name']}.")
        # Implementiere den Kampf hier

# Weitere Funktionen wie display_team, display_inventory, etc. müssen noch implementiert werden

def main():
    while True:
        print(ascii_art2)
        main_menu()
        ingame_menu()
        # Weitere Funktionen aufrufen, wenn sie implementiert sind
        random_encounter()
        explore_location()

        # Spiel beenden
        exit_choice = input("Möchtest du das Spiel beenden? (ja/nein): ").strip().lower()
        if exit_choice == "ja":
            print("Spiel wird beendet. Auf Wiedersehen!")
            break

if __name__ == "__main__":
    main()
    
