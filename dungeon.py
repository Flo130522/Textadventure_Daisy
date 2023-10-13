def explore(character):
    print(f"Du betrittst den Dungeon {dungeon['Name']}. {dungeon['description']}")
    for monster in character['monsters']:
        print(f"Ein {monster} lauert hier!")
    while True:
        print("\nWas möchtest du tun?")
        print("1. Mit Monstern kämpfen")
        print("2. Weiter zum nächsten Dungeon")
        print("3. Zurück zum vorherigen Ort")
        choice = input("Bitte wähle eine Option: ")
        if choice == "1":
            character.battle_monsters()
        elif choice == "2":
            if character.dungeons:
                character.explore_next_dungeon()
            else:
                print("Es gibt keine weiteren Dungeons.")
        elif choice == "3":
            print(f"Du verlässt den Dungeon {character.name}.")
            break
        else:
            print("Ungültige Option. Bitte wähle erneut.")
def encounter(character, locations):
    current_location = locations.get(character['location']) 

    if current_location.get('enemies'):
        print("Feindliche Charaktere nähern sich!")
        character['in_battle'] = True
        while character['in_battle']:
            living_enemies = [enemy for enemy in current_location['enemies'] if isinstance(enemy, dict) and enemy['is_alive']]
            if not living_enemies:
                character['in_battle'] = False
                break  
            pass  

    if current_location.get('dungeons'):
        for dungeon in current_location['dungeons']:
            print(f"Du befindest dich in einem Dungeon namens {dungeon['name']}.")
            # Fügen Sie hier Logik für die Erkundung des Dungeons hinzu, falls erforderlich.