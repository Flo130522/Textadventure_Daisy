import json
with open('characters.json') as f:
    characters = json.load(f)
    daisy = characters["friends"]["Daisy"]

with open('skills.json') as f:
    skills = json.load(f)

#Level-Up Funktion
def level_up(self):
    self.level += 1
    self.max_health += 10
    self.health = self.max_health
    self.attack_damage += 2
    self.defense += 1
    print(f"{self.name} hat Level {self.level} erreicht!")

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