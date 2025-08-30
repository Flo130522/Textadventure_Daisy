import random 
import json      
import art 
def main():
    """
    Die Hauptfunktion, um das Spiel zu starten.
    """
    # print("Willkommen zum Abenteuerspiel!")

    # while True:
    #     print("\nHauptmenü:")
    #     print("1. Abenteuer starten")
    #     print("2. Zuhause erkunden")
    #     print("3. Spiel beenden")
    #     choice = input("Bitte wählen Sie eine Option: ")

    #     if choice == "1":
    #         start_adventure()
    #     elif choice == "2":
    #         explore_home()
    #     elif choice == "3":
    #         print("Das Spiel wurde beendet.")
    #         break
    #     else:
    #         print("Ungültige Option. Bitte wählen Sie erneut.")
    
            
def start_adventure(daisy, monster):
    while True:
        #TODO Main Menu neu gestalten -> Ascii Art
        print("\nWas möchtest du tun?")
        print("1. Ort erkunden")
        print("2. Charakter anzeigen")
        print("3. Spiel beenden")
        choice = input("Bitte wähle eine Option: ")

        if choice == "1":
            daisy.explore_location()
        elif choice == "2":
            daisy.show_character()
        elif choice == "3":
            print("Das Spiel wird beendet. Auf Wiedersehen!")
            break
        else:
            print("Ungültige Eingabe. Bitte wähle eine der verfügbaren Optionen.")
    with open("locations.json", "r") as f:
        locations = json.load(f)
    with open ("characters.json", "r") as f:
        characters = json.load(f)
    with open ("items.json", "r") as f:
        items = json.load(f)

    # Erstelle Orte
    village = Location("Grauholz", "Ein friedliches Dorf, in dem alles begann.")
    village.add_dungeon("Verlassene Höhle", "Eine düstere, verlassene Höhle", [
        ("Spinne", 5, 10),  # Monstername, min_level, max_level
        ("Wildschwein", 8, 15),
        ("Wolf", 12, 20),
    ])


    # Backstory
    print("Huberus Snickers schickt sein Gefolge los, um das Schutzgeld aus Grauholz und anderen Dörfern einzutreiben.")
    print("Daisys Eltern haben nicht genug Geld, um das Schutzgeld zu bezahlen. Sie verstecken Daisy, die Eltern werden jedoch nach einem angespannten Gespräch mit dem Gefolge getötet.")
    print("Daisy bekommt alles mit und schwört sich Rache.")

    print(f"{daisy.name} erwacht aus ihrem Versteck und sieht eine Blutspur vor sich.")
    choice = input("Möchtest du der Blutspur folgen oder das Haus verlassen? (Blutspur folgen / Haus verlassen): ").strip().lower()

    if choice == "blutspur folgen":
        print("Das willst du nicht sehen, gehe lieber nach draußen.")
    elif choice == "haus verlassen":
        print("Du gehst nach draußen.")
        daisy.current_location = in_front_of_home  
    else:
        print("Ungültige Auswahl. Du gehst sicherheitshalber nach draußen.")
        
    while True:
        current_location = daisy.current_location  # Aktualisiere den aktuellen Ort
        explore_location(daisy)  # Hier rufen wir die explore_location-Funktion auf

        print("\nAktueller Ort:", current_location.name)
        print(current_location.description)

        # Zeige freundliche und feindliche Charaktere im aktuellen Ort an
        print("Freundliche Charaktere im aktuellen Ort:")
        for character in current_location.friends:
            if isinstance(character, Character) and character.is_alive():
                print(f"{character.name} ({character.age} Jahre, {character.breed}) - Rolle: {character.role} - Gesundheit: {character.health}")

        print("Feindliche Charaktere im aktuellen Ort:")
        for character in current_location.enemies:
            if isinstance(character, Character) and character.is_alive():
                print(f"{character.name} ({character.age} Jahre, {character.breed}) - Rolle: {character.role} - Gesundheit: {character.health}")

        action = input("Was möchtest du tun? (Angriff / Inventar anzeigen / Team anzeigen / Reisen): ").lower()

        if action == "angriff":
            if current_location.in_battle:
                print("Feindliche Charaktere im aktuellen Ort:")
                for index, enemy in enumerate(current_location.enemies):
                    if isinstance(enemy, Character) and enemy.is_alive():
                        print(f"{index + 1}. {enemy.name} ({enemy.age} Jahre, {enemy.breed}) - Rolle: {enemy.role} - Gesundheit: {enemy.health}")

                enemy_choice = input("Wähle den Feind, den du angreifen möchtest (1, 2, ...): ")

                if enemy_choice.isdigit():
                    enemy_choice = int(enemy_choice) - 1
                    if 0 <= enemy_choice < len(current_location.enemies) and current_location.enemies[enemy_choice].is_alive():
                        target = current_location.enemies[enemy_choice]
                        damage = daisy.attack(target)
                        print(f"{daisy.name} greift {target.name} an und fügt {damage} Schaden zu.")
                        if not target.is_alive():
                            print(f"{target.name} wurde besiegt!")
                    else:
                        print("Ungültige Wahl.")
                else:
                    print("Ungültige Eingabe.")
            else:
                print("Du befindest dich nicht im Kampf. Du kannst nicht angreifen.")

        elif action == "inventar anzeigen":
            daisy.display_inventory()

        elif action == "team anzeigen":
            daisy.display_team()

        elif action == "reisen":
            destination = input("Wohin möchtest du reisen? (Nach Hause / Zum Wald / Zum Magierturm / Zum Nachbarhaus): ").lower()

            # Überprüfen Sie die Benutzereingabe nach dem Ortswechsel innerhalb des entsprechenden Blocks
            if destination == "nach hause":
                daisy.travel_and_encounter("Zuhause", locations)
            elif destination == "zum wald":
                daisy.travel_and_encounter("Höhle im Wald", locations)
            elif destination == "zum magierturm":
                daisy.travel_and_encounter("Magierturm", locations)
            elif destination == "zum nachbarhaus":
                daisy.travel_and_encounter("Nachbarhaus", locations)
            else:
                print("Ungültiges Reiseziel. Wähle Nach Hause, Zum Wald, Zum Magierturm oder Zum Nachbarhaus.")

        # Überprüfen, ob Daisy besiegt wurde
        if not daisy.is_alive():
            print("Daisy wurde besiegt. Hubertus Snickers triumphiert und das Dorf bleibt in Angst.")
            break
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
if __name__ == "__main__":
    main()
