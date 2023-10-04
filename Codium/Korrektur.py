import logging
import getpass
import random             
            
def start_adventure(daisy, monster):
    while True:
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

    locations = initialize_locations()
    # Erstelle Charaktere
    daisy = Character("Daisy", 4, "Rauhaardackel-Terrier Mix", "Nahkampf-Spezialist", is_enemy=False)
    bruno = Character("Bruno", 3, "Bernhardiner", "Fernkampf-Spezialist", is_enemy=False)
    leika = Character("Leika", 5, "Pudel-Yorkshire Mix", "Nahkampf-Spezialistin", is_enemy=False)
    jack = Character("Jack", 6, "Pudel", "Heiler", is_enemy=False)
    leo = Character("Leo", 12, "Maltester", "Magier", is_enemy=False)
    hubertus = Character("Hubertus Snickers", 30, "Chihuahua", "Höllenhund aus dem Chihuahuareich", is_enemy=True)
    team = [daisy, bruno, leika, jack, leo]

    # Erstelle Orte
    village = Location("Grauholz", "Ein friedliches Dorf, in dem alles begann.")
    village.add_dungeon("Verlassene Höhle", "Eine düstere, verlassene Höhle", [
        ("Spinne", 5, 10),  # Monstername, min_level, max_level
        ("Wildschwein", 8, 15),
        ("Wolf", 12, 20),
    ])    
    forest = Location("Finsterwald", "Ein dunkler Wald, der viele Gefahren birgt.")
    city = Location("Hundewacht", "Eine belebte Stadt mit vielen Menschen.")
    endgame = Location("Chihuahua-Höllenreich", "Das dunkle Reich, in dem der Höllenhund Hubertus Snickers sein Unwesen treibt")
    home = Location("Zuhause", "Daisys gemütliches Zuhause.")
    dock = Location("Bootssteg", "Der Bootssteg am Flussufer.")
    market = Location("Dorfmarkt", "Der belebte Dorfmarkt, auf dem viele Geschäfte sind.")
    woodhome = Location("Höhle im Wald", "Eine kleine Höhle im Wald, in der sich Bruno wohl fühlt")
    homemagic = Location("Magierturm", "Hoher Magierturm, tief im Wald versteckt, in dem Leo Zauberexperimente durchführt")
    homenah = Location("Nachbarhaus", "Das Nachbarhaus, hier duftet es immer wieder nach leckerem Kuchen")
    homemed = Location("Rettungs-Hundehütte", "Hier wohnt Jack, der Rettungshund!")
    homeend = Location("Thron im Höllenschlund", "Hier sitzt Hubertus und versklavt seine Untertanen und sein Gefolge")
    in_front_of_home = Location("Vor dem Haus", "Direkt vor deinem gemütlichen Zuhause.")
    dungon = Location("Waldverlies", "Ein gefährliches Dungeon im Finsterwald")

    # Setze die Startorte für die Charaktere
    daisy.current_location = home
    bruno.current_location = woodhome
    leika.current_location = homenah
    jack.current_location = homemed
    leo.current_location = homemagic
    hubertus.current_location = homeend

    # Füge Charaktere zu Orten hinzu
    forest.add_friend(bruno)
    village.add_friend(leika)
    village.add_friend(daisy)
    village.add_friend(leo)
    city.add_friend(jack)
    city.add_friend(daisy)
    endgame.add_enemy(hubertus)

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
    
    
def get_user_choice(prompt, max_attempts=3, validation_func=None):
    """
    Prompt the user to enter a choice and validate the input using the provided validation function.
    If the input is not valid after `max_attempts`, raise a ValueError.

    Args:
        prompt (str): The prompt message to display to the user.
        max_attempts (int): The maximum number of attempts to get a valid input. Defaults to 3.
        validation_func (function): The validation function to use for validating the input. Defaults to None.

    Returns:
        str: The user's choice.

    Raises:
        ValueError: If the user fails to provide valid input after several attempts.
    """
    attempts = 0
    while attempts < max_attempts:
        try:
            choice = input(prompt)
            if validation_func is None or validation_func(choice):
                return choice
            else:
                logging.error("Invalid input. Please try again.")
        except (EOFError, KeyboardInterrupt):
            raise
        attempts += 1
    raise ValueError("Maximum number of attempts reached. Please try again.")

def main():
    options = [
        ("1", start_adventure),
        ("2", explore_home),
        ("3", end_game),
    ]

    logging.basicConfig(level=logging.INFO)

    is_running = True
    while is_running:
        logging.info("Willkommen zum Abenteuerspiel!")
        logging.info("\nHauptmenü:")
        for option in options:
            logging.info(f"{option[0]}. {option[1].__name__.replace('_', ' ')}")
        choice = get_user_choice()

        if choice in [option[0] for option in options]:
            for option in options:
                if option[0] == choice:
                    option[1]()
                    is_running = False
                    break
        else:
            logging.error("Ungültige Option. Bitte wählen Sie erneut.")

    while is_running:
        try:
            choice = get_user_choice()
            if choice in [option[0] for option in options]:
                for option in options:
                    if option[0] == choice:
                        option[1]()
                        is_running = False
                        break
            else:
                logging.error("Ungültige Option. Bitte wählen Sie erneut.")
        except Exception as e:
            logging.error("Ein Fehler ist aufgetreten: %s", str(e))

    while is_running:
        choice = get_user_choice()
        if choice in [option[0] for option in options]:
            for option in options:
                if option[0] == choice:
                    option[1]()
                    is_running = False
                    break
        else:
            logging.error("Ungültige Option. Bitte wählen Sie erneut.")

    while is_running:
        choice = get_user_choice()
        switcher = {
            "1": start_adventure,
            "2": explore_home,
            "3": end_game,
        }
        func = switcher.get(choice, lambda: logging.error("Ungültige Option. Bitte wählen Sie erneut."))
        func()
        is_running = False

    while is_running:
        choice = get_user_choice()
        if choice == "1":
            start_adventure()
            is_running = False
        elif choice == "2":
            explore_home()
            is_running = False
        elif choice == "3":
            logging.info("Das Spiel wurde beendet.")
            is_running = False
        else:
            logging.error("Ungültige Option. Bitte wählen Sie erneut.")
if __name__ == "__main__":
    main()