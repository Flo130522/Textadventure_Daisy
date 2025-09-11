from Character import *
from item import *

class Player_Character(Character):
    def __init__(self, name, age, breed, role, is_enemy=False):
        super().__init__(name, age, breed, role, is_enemy=False)
        
    def display_inventory(self):
        """
        Zeigt den Inventarinhalt des Charakters an.
        """
        print("Inventar:")
        for item in self.inventory:
            print(f"- {item.name}: {item.description}")
    
    def display_team(self):
        """
        Zeigt die Teammitglieder des Charakters an.
        """
        print("Team:")
        for character in self.team:
            print(f"- {character.name}: Gesundheit {character.health}/{character.max_health}, Angriff {character.attack}")