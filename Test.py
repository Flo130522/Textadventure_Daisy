import json

with open(r"json\locations.json") as fd:
    locations = json.load(fd)
def travel_menu():
    while True:
        print("\nWohin möchtest du reisen?")
        for key in locations:
            print(f"{key}")

        choice = input("Bitte wähle einen Ort (oder 'zurück', um zum Hauptmenü zurückzukehren): ")

        if choice == 'zurück':
            return
        elif choice in locations:
            location_info = locations[choice]
            print(f"Wohin in {choice} möchtest du reisen?")
            for sub_location in location_info:
                print(f"{sub_location}{['description']}")
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
            
travel_menu()
