import json
with open('characters.json') as f:
    characters = json.load(f)
    daisy = characters["friends"]["Daisy"]

with open('skills.json') as f:
    skills = json.load(f)

with open('items.json') as f:
    items = json.load(f)
    

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
        
#Item ins Inventar aufnehmen
def add_to_inventory(character, item, quantity=1):
    if len(character.inventory) >= character.inventory_limit:
        print("Das Inventar ist voll. Du kannst nichts mehr hinzufügen.")
        return
    for item_stack in character.inventory:
        if item_stack["item"] == item:
            item_stack["quantity"] += quantity
            print(f"{quantity} x {item} wurde zum Inventar hinzugefügt.")
            return
#TODO: Inventarslots auf 20 begrenzen // Pro Item 1 Slot // Stacken von Items // 15 Items pro Stack // Items droppen
    
    # Wenn das Element nicht im Inventar ist, fügen Sie es hinzu
    self.inventory.append({"item": item, "quantity": quantity})
    print(f"{quantity} x {item} wurde zum Inventar hinzugefügt.")
#Inventar anzeigen
def display_inventory(self):
    print(f"{self.name}s Inventar:")
    for item in self.inventory:
        print(item)
        
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

#EP sammeln (+wenn 100 EP, dann Level-Up)
def collect_xp(characters, ep):
    characters.ep = characters['ep']
    characters.ep += ep
    print(f"{characters['Name']} hat {ep} Erfahrungspunkte gesammelt.")
    if characters.xp >= 100:
        level_up(characters)
        print(f"{characters['Name']} hat Level {characters['level']} erreicht!")
        characters.ep = 0

#TODO Vergleich mit "import random 1-5" -> alle Funktionen implementieren
