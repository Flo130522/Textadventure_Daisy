import random
from Character import Character
class Monster(Character):
    def __init__(self, name, level, breed, role, health, attack, attacks=None, current_location=None):
        super().__init__(name, level, breed, role, health, attack)
        self.attacks = attacks if attacks is not None else []
        self.current_location = current_location


    def generate_monster_attacks(self, name, level):
        attacks = {}
        if self.breed == "Spinne":
                attacks["Seidenfaden"] = {"damage": level * 2, "description": "Umwickelt den Gegner komplett ein."}
                attacks["Giftzahn"] = {"damage": level * 3, "description": "Beißt den Gegner mit vergifteten Zähnen an."}
                attacks["Turbosprung"] = {"damage": level * 2, "description": "Springt auf den Gegner und fügt zufälligen Schaden zu."}
                
        elif self.breed == "Wildschwein":
                attacks["Rammbock"] = {"damage": level * 2, "description": "Rennt mit schnellen Schritten auf den Gegner zu und fügt ihm zufälligen Schaden zu (Gegner ist verwirrt)."}
                attacks["Stoßzahn"] = {"damage": level * 3, "description": "Der Gegner wird im Nahkampf durch Stoßzähne verletzt."}
                attacks["Teleportation"] = {"damage": level * 2, "description": "Kann sich weg teleportieren und greift in der nächsten Runde an (Gegner kann ihn nicht angreifen)."}

        elif self.breed == "Wolf":
                attacks["Hyperstrahl"] =  {"damage": level * 2, "description": "Schießt einen Strahl aus der Schnauze."},
                attacks["Mega-Biss"] = {"damage": level * 3, "description": "Beißt sich am Gegner fest und fügt zufälligen Schaden zu."},
                attacks["Riesenklaue"] = {"damage": level * 2, "description": "Greift mit seinen Klauen an und fügt zufällig starken hinzu."}

        elif self.breed == "Troll":
                attacks["Keulenschlag"] = {"damage": level * 2, "description": "Umwickelt den Gegner komplett ein."},
                attacks["Giftzahn"] = {"damage": level * 3, "description": "Beißt den Gegner mit vergifteten Zähnen an."},
                attacks["Turbosprung"] = {"damage": level * 2, "description": "Springt auf den Gegner und fügt zufälligen Schaden zu."}
        else:
            raise ValueError("Ungültiger Monstername.")
        
        # Füge die Standardangriffe hinzu
        attacks["Biss"] = {"damage": level * 2, "description": "Ein kräftiger Biss."}
        attacks["Kratzer"] = {"damage": level * 3, "description": "Ein scharfer Kratzer mit den Pfoten."}
        attacks["Bellender Angriff"] = {"damage": level * 2, "description": "Ein lauter bellender Angriff."}
        attacks["Sprung"] = {"damage": level * 3, "description": "Ein mutiger Sprung auf den Feind."}
        # Attacks zufällig auswählen
        selected_attacks = random.sample(attacks.items(), 3)
        attacks = {}
        for attack in selected_attacks:
            attacks[attack[0]] = attack[1]
            
        return attacks
