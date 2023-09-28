def start_adventure():
    locations = initialize_locations()
    # Erstelle Charaktere
    daisy = Character("Daisy", 4, "Rauhaardackel-Terrier Mix", "Nahkampf-Spezialist", is_enemy=False)
    bruno = Character("Bruno", 3, "Bernhardiner", "Fernkampf-Spezialist", is_enemy=False)
    leika = Character("Leika", 5, "Pudel-Yorkshire Mix", "Nahkampf-Spezialistin", is_enemy=False)
    jack = Character("Jack", 6, "Pudel", "Heiler", is_enemy=False)
    leo = Character("Leo", 12, "Maltester", "Magier", is_enemy=False)
    hubertus = Character("Hubertus Snickers", 30, "Chihuahua", "Höllenhund aus dem Chihuahuareich", is_enemy=True)

    # Erstelle Orte
    village = Location("Grauholz", "Ein friedliches Dorf, in dem alles begann.")
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

    # Einführung
    print(f"{daisy.name} erwacht aus ihrem Versteck und sieht eine Blutspur vor sich.")
    choice = input("Möchtest du der Blutspur folgen oder das Haus verlassen? (Blutspur folgen / Haus verlassen): ").strip().lower()

    if choice == "blutspur folgen":
        print("Das willst du nicht sehen, gehe lieber nach draußen.")
    elif choice == "haus verlassen":
        print("Du gehst nach draußen.")
        daisy.current_location = in_front_of_home  # Hier wird die Location auf "Vor dem Haus" geändert
    else:
        print("Ungültige Auswahl. Du gehst sicherheitshalber nach draußen.")

    while daisy.is_alive():
        current_location = daisy.current_location  # Aktualisiere den aktuellen Ort

        print("\nAktueller Ort:", current_location.name)
        print(current_location.description)

        # Zeige freundliche und feindliche Charaktere im aktuellen Ort an
        print("Freundliche Charaktere im aktuellen Ort:")
        for character in current_location.friends:
            if character.is_alive():
                print(f"{character.name} ({character.age} Jahre, {character.breed}) - Rolle: {character.role} - Gesundheit: {character.health}")

        print("Feindliche Charaktere im aktuellen Ort:")
        for character in current_location.enemies:
            if character.is_alive():
                print(f"{character.name} ({character.age} Jahre, {character.breed}) - Rolle: {character.role} - Gesundheit: {character.health}")

        daisy.encounter(locations)
        action = input("Was möchtest du tun? (Angriff / Inventar anzeigen / Team anzeigen / Reisen): ").lower()

        if action == "angriff":
            if current_location.in_battle:
                print("Feindliche Charaktere im aktuellen Ort:")
                for index, enemy in enumerate(current_location.enemies):
                    if enemy.is_alive():
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

    print("Daisy wurde besiegt. Hubertus Snickers triumphiert und das Dorf bleibt in Angst.")
