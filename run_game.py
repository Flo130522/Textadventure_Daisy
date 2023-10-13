#region Dateiimport
import json
import pickle
from datetime import datetime
import art
import random
# Locations
with open(r"json\locations.json",encoding="utf-8") as fd:
    locations = json.load(fd)
    infront_of_home = locations["Grauholz"]["Vor deinem Zuhause"]

# Charaktere
with open(r"json\characters.json",encoding="utf-8") as fd:
    character = json.load(fd)
    friends = character["friends"]
    enemys = character["enemies"]
    daisy = character['friends']['Daisy']

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
# Titelgrafik
ascii_art1 = art.text2art("Das Abenteuer des Rachedackels", font="small")
ascii_art2 = ascii_art1 + "\n" + art.text2art("Daisy gegen Hubertus Snickers", font="small")
print(ascii_art2)

class MainMenu:
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

class Character:
    def __init__(self, name, breed, role, is_enemy=False):
        self.name = name
        self.breed = breed
        self.role = role
        self.health = 100 
        self.max_health = 100  
        self.attack = 10 
        self.level = 1
        self.experience_points = 0   
        self.inventory = []  
        self.inventory_limit = 10  
        self.skills = []   
        self.is_enemy = is_enemy
        self.current_location = None  
        self.in_battle = False
        self.is_blocked = False
        self.team = None 
    # EP sammeln    
    def collect_ep(self, ep):
        self.ep = self['ep']
        self.ep += ep
        print(f"{self['Name']} hat {ep} Erfahrungspunkte gesammelt.")
        if self.xp >= 100:
            self.level_up()

    # Levelaufstieg        
    def level_up(self):
        self.level += 1
        self.max_health += 10
        self.health = self.max_health
        self.attack += 5
        print(f"{self['Name']} hat Level {self['level']} erreicht!")
    
    # Skills erlernen    
    def learn_skill(character,skill):
        if skill not in character.skills:
            character.skills.append(skill)
            print(f"{character['name']} hat die Fähigkeit {skill} erlernt!")
        else:
            print(f"{character['name']} hat die Fähigkeit {skill} bereits erlernt!")
    
    # Item in Inventar aufnehmen
    def add_to_inventory(character, item, quantity=1):
        inventory_limit = character['inventory_limit']
        inventory = character['inventory']

        # Inventar voll?
        if len(inventory) >= inventory_limit:
            print("Das Inventar ist voll. Du kannst nichts mehr hinzufügen.")
            return

        # Item bereits im Inventar?
        for item_stack in inventory:
            if item_stack["item"] == item:
                # Berechne verfügbaren Platz im Stack
                available_space = 15 - item_stack["quantity"]
                
                if available_space >= quantity:
                    # Menge hinzufügen ohne Stack zu überschreiten
                    item_stack["quantity"] += quantity
                    print(f"{quantity} x {item} wurde zum Inventar hinzugefügt.")
                    return
                else:
                    # Menge hinzufügen und Stack füllen
                    added_quantity = available_space
                    item_stack["quantity"] = 15
                    print(f"{added_quantity} x {item} wurde zum Inventar hinzugefügt.")
                    quantity -= added_quantity
        # Item nicht im Inventar
        while quantity > 0:
            # Menge auf 15 begrenzen
            stack_quantity = min(quantity, 15) 
            inventory.append({"item": item, "quantity": stack_quantity})
            quantity -= stack_quantity
            print(f"{stack_quantity} x {item} wurde zum Inventar hinzugefügt.")
    
    # Inventar anzeigen
    def display_inventory(character):
        print(f"{character['name']}s Inventar:")
        for item in character['inventory']:
            print(item)
    
    # Location erkunden
    def random_encounter(character):
        print(f"Du befindest dich in {daisy['location']}")
        if random.random() < 0.5:
            encounter = random.choice(character['enemies'])
            print(f"Du triffst auf {encounter['name']} und es kommt zu einem Kampf!")

            while is_alive(character) and is_alive(encounter):
                print("\nWas möchtest du im Kampf tun?")
                print("1. Angreifen")
                print("2. Fliehen")
                battle_choice = input("Bitte wähle eine Option: ")

                if battle_choice == "1":
                    damage_dealt = attack(character, encounter)
                    print(f"Du greifst {encounter['name']} an und verursachst {damage_dealt} Schaden.")
                    print(f"{encounter['name']} hat noch {encounter['health']} Gesundheit.")
                    if not is_alive(encounter):
                        print(f"{encounter['name']} wurde besiegt! Du hast gewonnen.")
                        break
                    else:
                        damage_taken = attack(encounter, character)
                        print(f"{encounter['name']} kontert und verursacht {damage_taken} Schaden.")
                        print(f"Deine Gesundheit: {character['health']}")
                        if not is_alive(character):
                            print(f"{encounter['name']} hat dich besiegt! Du hast verloren.")
                            break
                elif battle_choice == "2":
                    print(f"Du fliehst aus dem Kampf gegen {encounter['name']}.")
                    break
                else:
                    print("Ungültige Option. Bitte wähle erneut.")
        else:
            if random.random() < 0.7:
                print("Du hast ein seltenes Item gefunden!")
                #TODO find_item()
            else:
                print("Du entdeckst eine mysteriöse Höhle.")
                # Hier kannst du die Logik für das Entdecken einer Höhle implementieren
                #TODO enter_cave()    