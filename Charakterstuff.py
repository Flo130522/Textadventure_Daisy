import json
with open('characters.json') as f:
    characters = json.load(f)
    daisy = characters["friends"]["Daisy"]

with open('skills.json') as f:
    skills = json.load(f)

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

def learn_skill(self,skill):
    if skill not in self.skills:
        self.skills.append(skill)
        print(f"{self.name} hat die Fähigkeit {skill} erlernt!")
    else:
        print(f"{self.name} hat die Fähigkeit {skill} bereits erlernt!")
        
def add_item_to_inventory(self, item):
        self.inventory.append(item)

def display_inventory(self):
    print(f"{self.name}s Inventar:")
    for item in self.inventory:
        print(item)