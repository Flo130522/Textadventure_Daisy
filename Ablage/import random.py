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

    def generate_attacks(self):
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
def start_adventure():
    locations = initialize_locations()
    # Erstelle Charaktere
    daisy = Character("Daisy", 4, "Rauhaardackel-Terrier Mix", "Nahkampf-Spezialist", is_enemy=False)
    bruno = Character("Bruno", 3, "Bernhardiner", "Fernkampf-Spezialist", is_enemy=False)
    leika = Character("Leika", 5, "Pudel-Yorkshire Mix", "Nahkampf-Spezialistin", is_enemy=False)
    jack = Character("Jack", 6, "Pudel", "Heiler", is_enemy=False)
    leo = Character("Leo", 12, "Maltester", "Magier", is_enemy=False)
    hubertus = Character("Hubertus Snickers", 30, "Chihuahua", "Höllenhund aus dem Chihuahuareich", is_enemy=True)

    # Erstelle Orte
    village = Location("Grauholz", "Ein friedliches Dorf, in dem alles begann.")
    forest = Location("Finsterwald", "Ein dunkler Wald, der viele Gefahren birgt.")
    city = Location("Hundewacht", "Eine belebte Stadt mit vielen Menschen.")
    endgame = Location("Chihuahua-Höllenreich", "Das dunkle Reich, in dem der Höllenhund Hubertus Snickers sein Unwesen treibt")
    home = Location("Zuhause", "Daisys gemütliches Zuhause.")
    dock = Location("Bootssteg", "Der Bootssteg am Flussufer.")
    market = Location("Dorfmarkt", "Der belebte Dorfmarkt, auf dem viele Geschäfte sind.")
    woodhome = Location("Höhle im Wald", "Eine kleine Höhle im Wald, in der sich Bruno wohl fühlt")
    homemagic = Location("Magierturm", "Hoher Magierturm, tief im Wald versteckt, in dem Leo Zauberexperimente durchführt")
    homenah = Location("Nachbarhaus", "Das Nachbarhaus, hier duftet es immer wieder nach leckerem Kuchen")
    homemed = Location("Rettungs-Hundehütte", "Hier wohnt Jack, der Rettungshund!")
    homeend = Location("Thron im Höllenschlund", "Hier sitzt Hubertus und versklavt seine Untertanen und sein Gefolge")
    in_front_of_home = Location("Vor dem Haus", "Direkt vor deinem gemütlichen Zuhause.")
    dungon = Location("Waldverlies", "Ein gefährliches Dungeon im Finsterwald")

    # Setze die Startorte für die Charaktere
    daisy.current_location = home
    bruno.current_location = woodhome
    leika.current_location = homenah
    jack.current_location = homemed
    leo.current_location = homemagic
    hubertus.current_location = homeend

    # Füge Charaktere zu Orten hinzu
    forest.add_friend(bruno)
    village.add_friend(leika)
    village.add_friend(daisy)
    village.add_friend(leo)
    city.add_friend(jack)
    city.add_friend(daisy)
    endgame.add_enemy(hubertus)

    # Backstory
    print("Huberus Snickers schickt sein Gefolge los, um das Schutzgeld aus Grauholz und anderen Dörfern einzutreiben.")
    print("Daisys Eltern haben nicht genug Geld, um das Schutzgeld zu bezahlen. Sie verstecken Daisy, die Eltern werden jedoch nach einem angespannten Gespräch mit dem Gefolge getötet.")
    print("Daisy bekommt alles mit und schwört sich Rache.")

    # Einführung
    print(f"{daisy.name} erwacht aus ihrem Versteck und sieht eine Blutspur vor sich.")
    choice = input("Möchtest du der Blutspur folgen oder das Haus verlassen? (Blutspur folgen / Haus verlassen): ").strip().lower()

    if choice == "blutspur folgen":
        print("Das willst du nicht sehen, gehe lieber nach draußen.")
    elif choice == "haus verlassen":
        print("Du gehst nach draußen.")
        daisy.current_location = in_front_of_home  # Hier wird die Location auf "Vor dem Haus" geändert
    else:
        print("Ungültige Auswahl. Du gehst sicherheitshalber nach draußen.")

    while daisy.is_alive():
        current_location = daisy.current_location  # Aktualisiere den aktuellen Ort

        print("\nAktueller Ort:", current_location.name)
        print(current_location.description)

        # Zeige freundliche und feindliche Charaktere im aktuellen Ort an
        print("Freundliche Charaktere im aktuellen Ort:")
        for character in current_location.friends:
            if character.is_alive():
                print(f"{character.name} ({character.age} Jahre, {character.breed}) - Rolle: {character.role} - Gesundheit: {character.health}")

        print("Feindliche Charaktere im aktuellen Ort:")
        for character in current_location.enemies:
            if character.is_alive():
                print(f"{character.name} ({character.age} Jahre, {character.breed}) - Rolle: {character.role} - Gesundheit: {character.health}")

        daisy.encounter(locations)
        action = input("Was möchtest du tun? (Angriff / Inventar anzeigen / Team anzeigen / Reisen): ").lower()

        if action == "angriff":
            if current_location.in_battle:
                print("Feindliche Charaktere im aktuellen Ort:")
                for index, enemy in enumerate(current_location.enemies):
                    if enemy.is_alive():
                        print(f"{index + 1}. {enemy.name} ({enemy.age} Jahre, {enemy.breed}) - Rolle: {enemy.role} - Gesundheit: {enemy.health}")

                enemy_choice = input("Wähle den Feind, den du angreifen möchtest (1, 2, ...): ")

                if enemy_choice.isdigit():
                    enemy_choice = int(enemy_choice) - 1
                    if 0 <= enemy_choice < len(current_location.enemies) and current_location.enemies[enemy_choice].is_alive():
                        target = current_location.enemies[enemy_choice]
                        damage = daisy.attack(target)
                        print(f"{daisy.name} greift {target.name} an und fügt {damage} Schaden zu.")
                        if not target.is_alive():
                            print(f"{target.name} wurde besiegt!")
                    else:
                        print("Ungültige Wahl.")
                else:
                    print("Ungültige Eingabe.")
            else:
                print("Du befindest dich nicht im Kampf. Du kannst nicht angreifen.")

        elif action == "inventar anzeigen":
            daisy.display_inventory()

        elif action == "team anzeigen":
            daisy.display_team()

        elif action == "reisen":
            destination = input("Wohin möchtest du reisen? (Nach Hause / Zum Wald / Zum Magierturm / Zum Nachbarhaus): ").lower()
            if destination == "nach hause":
                daisy.travel_and_encounter("Zuhause", locations)
            elif destination == "zum wald":
                daisy.travel_and_encounter("Höhle im Wald", locations)
            elif destination == "zum magierturm":
                daisy.travel_and_encounter("Magierturm", locations)
            elif destination == "zum nachbarhaus":
                daisy.travel_and_encounter("Nachbarhaus", locations)
            else:
                print("Ungültiges Reiseziel. Wähle Nach Hause, Zum Wald, Zum Magierturm oder Zum Nachbarhaus.")

    print("Daisy wurde besiegt. Hubertus Snickers triumphiert und das Dorf bleibt in Angst.")
def explore_home():
    print("Daisy lebt mit ihren Eltern in Grauholz. Es ist ein Tag wie jeder andere, die Sonne scheint und es ist angenehm warm.")

    while True:
        print("\nDu befindest dich im Wohnzimmer von Daisys Zuhause.")
        print("1. Mit deinem Papa reden")
        print("2. Mit deiner Mama reden")
        print("3. Zurück zum Hauptmenü")

        choice = input("Bitte wähle eine Option: ")

        if choice == "1":
            print("Dein Papa ist in seine Zeitung vertieft und sagt, 'Guten Morgen, kleines.'")
        elif choice == "2":
            print("Deine Mama lächelt und sagt, 'Guten Morgen Daisylein, iss dein Frühstück bevor es kalt wird!'")
        elif choice == "3":
            break
        else:
            print("Ungültige Option. Bitte wähle 1, 2 oder 3.")
if __name__ == "__main__":
    main()