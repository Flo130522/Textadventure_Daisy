import json
import pickle
from datetime import datetime

with open('characters.json') as f:
    characters = json.load(f)
    daisy = characters["friends"]["Daisy"]

with open('skills.json') as f:
    skills = json.load(f)

with open('items.json') as f:
    items = json.load(f)
    
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
def learn_skill(self,skill):
    if skill not in self.skills:
        self.skills.append(skill)
        print(f"{self.name} hat die Fähigkeit {skill} erlernt!")
    else:
        print(f"{self.name} hat die Fähigkeit {skill} bereits erlernt!")

#EP sammeln (+wenn 100 EP, dann Level-Up)
def collect_xp(characters, ep):
    characters.ep = characters['ep']
    characters.ep += ep
    print(f"{characters['Name']} hat {ep} Erfahrungspunkte gesammelt.")
    if characters.xp >= 100:
        level_up(characters)
        print(f"{characters['Name']} hat Level {characters['level']} erreicht!")
        characters.ep = 0
        
#endregion EP-System

#region Inventar
#Item ins Inventar aufnehmen
#TODO: Inventarslots auf 20 begrenzen // Pro Item 1 Slot // Stacken von Items // 15 Items pro Stack // Items droppen

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
def display_inventory(self):
    print(f"{self.name}s Inventar:")
    for item in self.inventory:
        print(item)
        
#endregion Inventar
#region Team

#Charakter dem Team hinzufügen
def add_friend(self, character):
    self.friends.append(character)
    character.team.append(self)

#Team anzeigen
def display_team(self):
    print("Teamübersicht")
    print(f"{self.name} - Gesundheit: {self.health}")
    for character in self.team:
        print(f"{character.name} - Gesundheit: {character.health}")

def display_stats(self):
        print(f"{self.name} (Level {self.level}) - Gesundheit: {self.health} - Erfahrungspunkte: {self.experience_points}")
        print(f"Rolle: {self.role} - Rasse: {self.breed}")

#endregion Team
#region Charaktereigenschaften

def block(self):
    self.is_blocked = True

def unblock(self):
    self.is_blocked = False
#endregion Charaktereigenschaften

#region Savegame/Loadgame
def save_game(self):
        try:
            with open(filename, "wb") as file:
                pickle.dump(self, file)
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
def auto_save(self, filename):
    current_time = datetime.now()
    if current_time - self.last_save_time > self.save_interval:
        self.save_game(filename)
        self.last_save_time = current_time
#endregion Savegame/Loadgame
