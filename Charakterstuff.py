import json
import pickle
from datetime import datetime

#Locations aus JSON Datei laden
with open(r"json\locations.json") as fd:
    locations = json.load(fd)
    
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

#Effects aus JSON Datei laden
with open(r"json\effects.json") as fd:
    effects = json.load(fd)
    
#region EP-System
#Level-Up Funktion
def level_up(characters):
        level = characters["level"]
        max_health = characters["max_health"]
        health = characters["health"]
        attack_damage = characters["attack"]
        defense = characters["defense"]
        
        level += 1
        max_health += 10
        health = max_health
        attack_damage += 5
        defense += 2

# Neuen Skill erlernen
def learn_skill(character,skill):
    if skill not in character.skills:
        character.skills.append(skill)
        print(f"{character['name']} hat die Fähigkeit {skill} erlernt!")
    else:
        print(f"{character['name']} hat die Fähigkeit {skill} bereits erlernt!")

#EP sammeln (+wenn 100 EP, dann Level-Up)
def collect_xp(character, ep):
    character.ep = character['ep']
    character.ep += ep
    print(f"{character['Name']} hat {ep} Erfahrungspunkte gesammelt.")
    if character.xp >= 100:
        level_up(character)
        print(f"{character['Name']} hat Level {character['level']} erreicht!")
        characters.ep = 0
        
#endregion EP-System

#region Inventar
#Item ins Inventar aufnehmen
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

#Inventar anzeigen
def display_inventory(character):
    print(f"{character['name']}s Inventar:")
    for item in character['inventory']:
        print(item)
        
#endregion Inventar
#region Team

#Charakter dem Team hinzufügen
def add_friend(character):
    character.friends.append(character)
    character.team.append(character)

#Team anzeigen
def display_team(character):
    print("Teamübersicht")
    print(f"{character['name']} - Gesundheit: {character.health}")
    for character in character.team:
        print(f"{character['name']} - Gesundheit: {character.health}")

def display_stats(character):
        print(f"{character['name']} (Level {character['level']}) - Gesundheit: {character['level']} - Erfahrungspunkte: {character['ep']}")
        print(f"Rolle: {character['role']} - Rasse: {character['breed']}")

#endregion Team
#region Charaktereigenschaften

def block(character):
    character.is_blocked = True

def unblock(character):
    character.is_blocked = False
#endregion Charaktereigenschaften

#region Savegame/Loadgame
def save_game(character, filename):
    try:
        with open(filename, "wb") as file:
            pickle.dump(character, file)
        print("Spielstand wurde gespeichert.")
    except Exception as e:
        print(f"Fehler beim Speichern des Spielstands: {e}")
def loadgame(filename):
    try:
        with open(filename, "rb") as file:
            game = pickle.load(file)
        print("Spielstand wurde geladen.")
        return game
    except FileNotFoundError:
        print("Die angegebene Datei wurde nicht gefunden.")
        return None
    except Exception as e:
        print(f"Fehler beim Laden des Spielstands: {e}")
        return None
def auto_save(character, filename):
    current_time = datetime.now()
    if current_time - character.last_save_time > character.save_interval:
        character.save_game(filename)
        character.last_save_time = current_time
#endregion Savegame/Loadgame
