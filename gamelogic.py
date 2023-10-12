import json
import art
import pickle
from datetime import datetime


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

def main():
    print(ascii_art2)
    while True:
        print("\nHauptmenü:")
        print("1. Abenteuer starten")
        print("2. Zuhause erkunden")
        print("3. Spiel beenden")
        choice = input("Bitte wählen Sie eine Option: ")
        if choice == "1":
            start_adventure()
        elif choice == "2":
            explore_home()
        elif choice == "3":
            print("Das Spiel wurde beendet.")
            break
        else:
            print("Ungültige Option. Bitte wählen Sie erneut.")

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
        

if __name__ == "__main__":
    main()