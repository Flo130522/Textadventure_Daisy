import random

class Character:
    def __init__(self, name, age, breed, role, is_enemy=False):
        self.name = name
        self.age = age
        self.breed = breed
        self.role = role
        self.health = 100
        self.level = 1
        self.experience_points = 0
        self.inventory = []
        self.inventory_limit = 20
        self.skills = []
        self.is_enemy = is_enemy
        self.current_location = None
        self.in_battle = False
        self.attacks = self.generate_attacks()
        self.is_blocked = False
        self.team = []

        if is_enemy:
            self.attacks = self.generate_attacks()

    def block(self):
        self.is_blocked = True
    
    def unblock(self):
        self.is_blocked = False
    
    def earn_experience_points(self, amount):
        self.experience_points += amount
        print(f"{self.name} hat {amount} EP erhalten!")
    
    def check_level_up(self):
        if self.experience_points >= self.level * 100:
            self.level += 1
            print(f"{self.name} ist auf Level {self.level} aufgestiegen!")
    
    def earn_random_experience_points(self, enemy_level):
        min_ep = enemy_level * 5
        max_ep = enemy_level * 10
        earned_ep = random.randint(min_ep, max_ep)
        self.experience_points += earned_ep
        print(f"{self.name} hat {earned_ep} EP erhalten!")
        self.check_level_up()
    
    def add_to_inventory(self, item, quantity=1):
        if len(self.inventory) >= self.inventory_limit:
            print("Das Inventar ist voll. Du kannst nichts mehr hinzufügen.")
            return
        for item_stack in self.inventory:
            if item_stack["item"] == item:
                item_stack["quantity"] += quantity
                print(f"{quantity} x {item} wurde zum Inventar hinzugefügt.")
                return
        self.inventory.append({"item": item, "quantity": quantity})
        print(f"{quantity} x {item} wurde zum Inventar hinzugefügt.")

    def generate_attacks(self):
        return {
            "Biss": {"damage": random.randint(5, 15), "description": "Ein kräftiger Biss."},
            "Kratzer": {"damage": random.randint(10, 20), "description": "Ein scharfer Kratzer mit den Pfoten."},
            "Bellender Angriff": {"damage": random.randint(1, 10), "description": "Ein lauter bellender Angriff."},
            "Sprung": {"damage": random.randint(15, 25), "description": "Ein mutiger Sprung auf den Feind."},
        }
    
    def display_inventory(self):
        print("Inventar:")
        for item_stack in self.inventory:
            item = item_stack["item"]
            quantity = item_stack["quantity"]
            print(f"{item}: {quantity}")

    def take_damage(self, damage):
        self.health -= damage

    def attack(self, enemy):
        if self.in_battle and self.can_attack():
            damage = self.calculate_damage()
            self.perform_attack(enemy, damage)
            return damage, f"{self.name} greift {enemy.name} an und fügt {damage} Schaden zu."
        return 0, f"{self.name} kann nicht angreifen."  # Tupel: (Schaden, Statusmeldung)

    def can_attack(self):
        if self.role == "Spinnen":
            return random.randint(1, 2) == 1
        elif self.role == "Wildschwein":
            return random.randint(1, 2) == 1
        elif self.role == "Heiler":
            # Heiler greift nur an, wenn ein Teammitglied unter einem bestimmten Gesundheitswert ist
            for friend in self.current_location.friends:
                if isinstance(friend, Character) and friend.is_alive() and friend.health < 50:  # Anpassen des Schwellenwerts nach Bedarf
                    return True
            return False
        else:
            return True

    def calculate_damage(self):
        if self.role == "Fernkampf-Spezialist":
            return random.randint(10, 20)
        elif self.role == "Nahkampf-Spezialistin":
            return random.randint(15, 25)
        elif self.role == "Heiler":
            # Der Heiler fügt keinen Schaden zu, sondern heilt ein zufälliges verletztes Teammitglied
            injured_friends = [friend for friend in self.current_location.friends if isinstance(friend, Character) and friend.is_alive() and friend.health < 100]
            if injured_friends:
                target = random.choice(injured_friends)
                # Hier können Sie die Heilung entsprechend anpassen
                healing_amount = random.randint(20, 40)
                target.health += healing_amount
                print(f"{self.name} heilt {target.name} um {healing_amount} Gesundheitspunkte.")
            else:
                print(f"{self.name} kann niemanden heilen, da niemand verletzt ist.")
            return 0  # Dieses return 0 gehört zur Heilungslogik des Heilers
        elif self.role == "Magier":
            return random.randint(5, 15)
        else:
            return random.randint(1, 10)

    def is_alive(self):
        return self.health > 0

    def display_team(self):
        print("Teamübersicht:")
        print(f"{self.name} - Level {self.level} (EP: {self.experience_points}) - Gesundheit: {self.health}")

    def travel_and_encounter(self, destination, locations):
        if destination in locations:
            new_location = locations[destination]
            new_location.add_friend(self)  # Füge das aktuelle Teammitglied zum Zielort hinzu
            self.current_location = new_location
            self.encounter(locations)
        else:
            print(f"{self.name} kann nicht dorthin reisen. Der Ort existiert nicht.")
    
    def encounter(self, locations):
        current_location = self.current_location
        if current_location.enemies:
            print("Feindliche Charaktere nähern sich!")
            self.in_battle = True
            while self.in_battle:
                # Überprüfen Sie, ob es noch lebende Feinde in der aktuellen Location gibt
                living_enemies = [enemy for enemy in current_location.enemies if isinstance(enemy, Character) and enemy.is_alive()]
                if not living_enemies:
                    self.in_battle = False
                    break  # Beenden Sie den Kampf, wenn keine lebenden Feinde mehr vorhanden sind
                pass  # Hier geht der Kampf weiter
        if current_location.friends:
            print("Freundliche Charaktere sind hier und könnten dir helfen!")
    def is_alive(self):
        return self.health > 0
       
class Monster:
    def __init__(self, name, level):
        self.name = name
        self.level = level
        self.health = level * 10
        self.attacks = self.generate_monster_attacks(name, level)
    
    def generate_monster_attacks(self, name, level):
        if name == "Spinne":
            if 1 <= level <= 19:
                return {
                    "Seidenfaden": {"damage": level * 2, "description": "Umwickelt den Gegner komplett ein."},
                    "Giftzahn": {"damage": level * 3, "description": "Beißt den Gegner mit vergifteten Zähnen an."},
                    "Turbosprung": {"damage": level * 2, "description": "Springt auf den Gegner und fügt zufälligen Schaden zu."},
                }
            else:
                raise ValueError("Level außerhalb des zulässigen Bereichs für Spinne.")
        elif name == "Wildschwein":
            if 20 <= level <= 49:
                return {
                    "Rammbock": {"damage": level * 2, "description": "Rennt mit schnellen Schritten auf den Gegner zu und fügt ihm zufälligen Schaden zu (Gegner ist verwirrt)."},
                    "Stoßzahn": {"damage": level * 3, "description": "Der Gegner wird im Nahkampf durch Stoßzähne verletzt."},
                    "Teleportation": {"damage": level * 2, "description": "Kann sich weg teleportieren und greift in der nächsten Runde an (Gegner kann ihn nicht angreifen)."},
                }
            else:
                raise ValueError("Level außerhalb des zulässigen Bereichs für Wildschwein.")
        elif name == "Wolf":
            if 50 <= level <= 79:
                return {
                    "Hyperstrahl": {"damage": level * 2, "description": "Schießt einen Strahl aus der Schnauze."},
                    "Mega-Biss": {"damage": level * 3, "description": "Beißt sich am Gegner fest und fügt zufälligen Schaden zu."},
                    "Riesenklaue": {"damage": level * 2, "description": "Greift mit seinen Klauen an und fügt zufällig starken hinzu."}
                }
            else:
                raise ValueError("Level außerhalb des zulässigen Bereichs für Wolf.")
        elif name == "Troll":
            if 80 <= level <= 89:
                return {
                    "Keulenschlag": {"damage": level * 2, "description": "Umwickelt den Gegner komplett ein."},
                    "Giftzahn": {"damage": level * 3, "description": "Beißt den Gegner mit vergifteten Zähnen an."},
                    "Turbosprung": {"damage": level * 2, "description": "Springt auf den Gegner und fügt zufälligen Schaden zu."}
                }
            else:
                raise ValueError("Level außerhalb des zulässigen Bereichs für Troll.")
        else:
            raise ValueError("Ungültiger Monstername.")

class Dungeon:
    def __init__(self, name, description, monsters):
        self.name = name
        self.description = description
        self.monsters = monsters

    def add_random_monster(self, monster_name, min_level, max_level):
        random_level = random.randint(min_level, max_level)
        monster = Monster(monster_name, random_level)
        self.monsters.append(monster)

class Location:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.friends = []  # Hier speichern wir Charaktere, die sich im selben Ort befinden
        self.enemies = []  # Hier speichern wir Feinde, die sich im selben Ort befinden

    def add_friend(self, character):
        self.friends.append(character)
    
    def add_enemy(self, character):
        self.enemies.append(character)

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
        "Magierturm": Location("Magierturm", "Ein mysteriöser Turm, in dem der Magier Merlin lebt."),
        "Kristallsee": Location("Kristallsee", "Ein zauberhafter See, der von glitzernden Kristallen umgeben ist."),
        "Gefängniszelle": Location("Gefängniszelle", "Eine düstere Zelle im Kerker von Hundewacht."),
    }

    # Verbindungen zwischen den Orten festlegen
    locations["Grauholz"].add_friend(locations["Finsterwald"])
    locations["Grauholz"].add_friend(locations["Hundewacht"])
    locations["Finsterwald"].add_friend(locations["Grauholz"])
    locations["Finsterwald"].add_friend(locations["Hundewacht"])
    locations["Hundewacht"].add_friend(locations["Grauholz"])
    locations["Hundewacht"].add_friend(locations["Finsterwald"])
    locations["Hundewacht"].add_friend(locations["Chihuahua-Höllenreich"])
    locations["Chihuahua-Höllenreich"].add_friend(locations["Hundewacht"])
    locations["Zuhause"].add_friend(locations["Bootssteg"])
    locations["Bootssteg"].add_friend(locations["Zuhause"])
    locations["Bootssteg"].add_friend(locations["Dorfmarkt"])
    locations["Dorfmarkt"].add_friend(locations["Bootssteg"])
    locations["Dorfmarkt"].add_friend(locations["Höhle im Wald"])
    locations["Dorfmarkt"].add_friend(locations["Magierturm"])
    locations["Dorfmarkt"].add_friend(locations["Kristallsee"])
    locations["Höhle im Wald"].add_friend(locations["Dorfmarkt"])
    locations["Magierturm"].add_friend(locations["Dorfmarkt"])
    locations["Kristallsee"].add_friend(locations["Dorfmarkt"])
    locations["Hundewacht"].add_enemy(locations["Gefängniszelle"])
    locations["Gefängniszelle"].add_friend(locations["Hundewacht"])

    return locations
def main():
    print("Willkommen zum Abenteuer!")

    while True:
        print("\nHauptmenü:")
        print("1. Abenteuer starten")
        print("2. Zuhause erkunden")
        print("3. Beenden")

        choice = input("Bitte wählen Sie eine Option: ")

        if choice == "1":
            start_adventure()  # Abenteuer starten
            break
        elif choice == "2":
            explore_home()  # Zuhause erkunden
        elif choice == "3":
            print("Vielen Dank fürs Spielen. Auf Wiedersehen!")
            break
        else:
            print("Ungültige Option. Bitte wählen Sie 1, 2 oder 3.")
            
def start_adventure():
    locations = initialize_locations()
    # Erstelle Charaktere
    daisy = Character("Daisy", 4, "Rauhaardackel-Terrier Mix", "Nahkampf-Spezialist", is_enemy=False)
    bruno = Character("Bruno", 3, "Bernhardiner", "Fernkampf-Spezialist", is_enemy=False)
    leika = Character("Leika", 5, "Pudel-Yorkshire Mix", "Nahkampf-Spezialistin", is_enemy=False)
    jack = Character("Jack", 6, "Pudel", "Heiler", is_enemy=False)
    leo = Character("Leo", 12, "Maltester", "Magier", is_enemy=False)
    hubertus = Character("Hubertus Snickers", 30, "Chihuahua", "Höllenhund aus dem Chihuahuareich", is_enemy=True)
    team = [daisy, bruno, leika, jack, leo]

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
        daisy.current_location = in_front_of_home  
    else:
        print("Ungültige Auswahl. Du gehst sicherheitshalber nach draußen.")

    while True:
        current_location = daisy.current_location  # Aktualisiere den aktuellen Ort

        print("\nAktueller Ort:", current_location.name)
        print(current_location.description)

        # Zeige freundliche und feindliche Charaktere im aktuellen Ort an
        print("Freundliche Charaktere im aktuellen Ort:")
        for character in current_location.friends:
            if isinstance(character, Character) and character.is_alive():
                print(f"{character.name} ({character.age} Jahre, {character.breed}) - Rolle: {character.role} - Gesundheit: {character.health}")

        print("Feindliche Charaktere im aktuellen Ort:")
        for character in current_location.enemies:
            if isinstance(character, Character) and character.is_alive():
                print(f"{character.name} ({character.age} Jahre, {character.breed}) - Rolle: {character.role} - Gesundheit: {character.health}")

        action = input("Was möchtest du tun? (Angriff / Inventar anzeigen / Team anzeigen / Reisen): ").lower()

        if action == "angriff":
            if current_location.in_battle:
                print("Feindliche Charaktere im aktuellen Ort:")
                for index, enemy in enumerate(current_location.enemies):
                    if isinstance(enemy, Character) and enemy.is_alive():
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

            # Überprüfen Sie die Benutzereingabe nach dem Ortswechsel innerhalb des entsprechenden Blocks
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

        # Überprüfen, ob Daisy besiegt wurde
        if not daisy.is_alive():
            print("Daisy wurde besiegt. Hubertus Snickers triumphiert und das Dorf bleibt in Angst.")
            break
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
