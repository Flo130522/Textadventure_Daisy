import random

class Character:
    def __init__(self, name, age, breed, role, is_enemy=False):
        self.name = name
        self.age = age
        self.breed = breed
        self.role = role
        self.health = 100
        self.level = 1
        self.inventory = []
        self.skills = []
        self.is_enemy = is_enemy
        self.current_location = None
        self.in_battle = False
        self.attacks = self.generate_attacks()
        
        if is_enemy:
            self.generate_monster_attributes(name, self.level)

    @staticmethod
    def generate_attacks():
        # Definiere die Standardangriffe für alle Charaktere
        return {
            "Biss": {"damage": random.randint(5, 15), "description": "Ein kräftiger Biss."},
            "Kratzer": {"damage": random.randint(10, 20), "description": "Ein scharfer Kratzer mit den Pfoten."},
            "Bellender Angriff": {"damage": random.randint(1, 10), "description": "Ein lauter bellender Angriff."},
            "Sprung": {"damage": random.randint(15, 25), "description": "Ein mutiger Sprung auf den Feind."},
        }

    def generate_monster_attributes(self, name, level):
        if name == "Spinne":
            if 1 <= level <= 19:
                self.health = level * 10
                self.attacks = {
                    "Seidenfaden": {"damage": level * 2, "description": "Umwickelt den Gegner komplett ein."},
                    "Giftzahn": {"damage": level * 3, "description": "Beißt den Gegner mit vergifteten Zähnen an."},
                    "Turbosprung": {"damage": level * 2, "description": "Springt auf den Gegner und fügt zufälligen Schaden zu."},
                }
            else:
                raise ValueError("Level außerhalb des zulässigen Bereichs für Spinne.")
        elif name == "Wildschwein":
            if 20 <= level <= 49:
                self.health = level * 10
                self.attacks = {
                    "Rammbock": {"damage": level * 2, "description": "Rennt mit schnellen Schritten auf den Gegner zu und fügt ihm zufälligen Schaden zu (Gegner ist verwirrt)."},
                    "Stoßzahn": {"damage": level * 3, "description": "Der Gegner wird im Nahkampf durch Stoßzähne verletzt."},
                    "Teleportation": {"damage": level * 2, "description": "Kann sich weg teleportieren und greift in der nächsten Runde an (Gegner kann ihn nicht angreifen)."},
                }
            else:
                raise ValueError("Level außerhalb des zulässigen Bereichs für Wildschwein.")
        elif name == "Wolf":
            if 50 <= level <= 79:
                self.health = level * 10
                self.attacks = {
                    "Hyperstrahl": {"damage": level * 2, "description": "Schießt einen Strahl aus der Schnauze."},
                    "Mega-Biss": {"damage": level * 3, "description": "Beißt sich am Gegner fest und fügt zufälligen Schaden zu."},
                    "Riesenklaue": {"damage": level * 2, "description": "Greift mit seinen Klauen an und fügt zufällig starken hinzu."}
                }
            else:
                raise ValueError("Level außerhalb des zulässigen Bereichs für Wolf.")
        elif name == "Troll":
            if 80 <= level <= 89:
                self.health = level * 10
                self.attacks = {
                    "Keulenschlag": {"damage": level * 2, "description": "Umwickelt den Gegner komplett ein."},
                    "Giftzahn": {"damage": level * 3, "description": "Beißt den Gegner mit vergifteten Zähnen an."},
                    "Turbosprung": {"damage": level * 2, "description": "Springt auf den Gegner und fügt zufälligen Schaden zu."}
                }
            else:
                raise ValueError("Level außerhalb des zulässigen Bereichs für Troll.")
        else:
            raise ValueError("Ungültiger Monstername.")

    def take_damage(self, damage):
        self.health -= damage

    def attack(self, enemy):
        if self.in_battle and self.can_attack:
            damage = self.calculate_damage()
            self.perform_attack(enemy, damage)

    def calculate_damage(self):
        if self.role == "Fernkampf-Spezialist":
            return random.randint(10, 20)
        elif self.role == "Nahkampf-Spezialistin":
            return random.randint(15, 25)
        elif self.role == "Heiler":
            return 0
        elif self.role == "Magier":
            return random.randint(5, 15)
        else:
            return random.randint(1, 10)

    def perform_attack(self, enemy, damage):
        if self.role == "Spinnen":
            if random.randint(1, 2) == 1:
                print(f"{self.name} führt Seidenfaden aus und kann sich nicht mehr bewegen!")
                self.can_attack = False
            else:
                print(f"{self.name} führt Giftzahn aus und vergiftet {enemy.name}!")
                enemy.poisoned = True
        elif self.role == "Wildschwein":
            if random.randint(1, 2) == 1:
                print(f"{self.name} führt Rammbock aus und verwirrt {enemy.name}!")
                enemy.confused = True
            else:
                print(f"{self.name} führt Teleportation aus und greift in der nächsten Runde an (Gegner kann ihn nicht angreifen).")

class Location:
    def __init__(self, name, description):
        self.name = name
        self.description = description

class Dungeon:
    def __init__(self, name, description, monsters):
        self.name = name
        self.description = description
        self.monsters = monsters

def main():
    print("Das Abenteuer des Rache-Dackels: Daisy gegen Hubertus Snickers")
    while True:
        print("\nOptionen:")
        print("1. Abenteuer beginnen")
        print("2. Zuhause erkunden")
        print("3. Beenden")

        choice = input("Bitte wählen Sie eine Option: ")

        if choice == "1":
            start_adventure()
        elif choice == "2":
            explore_home()
        elif choice == "3":
            print("Vielen Dank fürs Spielen! Auf Wiedersehen.")
            break
        else:
            print("Ungültige Option. Bitte wählen Sie 1, 2 oder 3.")

def initialize_locations():
    locations = {
        "Grauholz": Location("Grauholz", "Ein friedliches Dorf, in dem alles begann."),
        "Finsterwald": Location("Finsterwald", "Ein dunkler Wald, der viele Gefahren birgt."),
        "Hundewacht": Location("Hundewacht", "Eine belebte Stadt mit vielen Menschen."),
        "Chihuahua-Höllenreich": Location("Chihuahua-Höllenreich", "Das dunkle Reich, in dem der Höllenhund Hubertus Snickers sein Unwesen treibt"),
        "Zuhause": Location("Zuhause", "Daisys gemütliches Zuhause."),
        "Bootssteg": Location("Bootssteg", "Der Bootssteg am Flussufer."),
        "Dorfmarkt": Location("Dorfmarkt", "Der belebte Dorfmarkt, auf dem viele Geschäfte sind."),
        "Höhle im Wald": Location("Höhle im Wald", "Eine kleine Höhle im Wald, in der sich Bruno wohl fühlt"),
        "Magierturm": Location("Magierturm", "Hoher Magierturm, tief im Wald versteckt, in dem Leo Zauberexperimente durchführt"),
        "Nachbarhaus": Location("Nachbarhaus", "Das Nachbarhaus, hier duftet es immer wieder nach leckerem Kuchen"),
        "Rettungs-Hundehütte": Location("Rettungs-Hundehütte", "Hier wohnt Jack, der Rettungshund!"),
        "Thron im Höllenschlund": Location("Thron im Höllenschlund", "Hier sitzt Hubertus und versklavt seine Untertanen und sein Gefolge"),
        "Vor dem Haus": Location("Vor dem Haus", "Direkt vor deinem gemütlichen Zuhause."),
        "Dungeon": Dungeon("Waldverlies", "Ein gefährliches Dungeon im Finsterwald.", ["Spinne", "Wildschwein", "Wolf", "Troll"])
    }
    return locations

if __name__ == "__main__":
    main()