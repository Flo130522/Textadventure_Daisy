import random
import pickle
import os
from datetime import datetime


    
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
    
    def __init__(self, name, level, breed, role, health, attack):
        self.name = name
        self.level = level
        self.breed = breed
        self.role = role
        self.health = health
        self.attack = attack

    def battle_monster(self, monster):
        """
        Simuliert einen Kampf mit einem Monster.
        """
        print(f"Du trittst in den Kampf gegen {monster.name} ein!")

        while True:
            print("\nWas möchtest du im Kampf tun?")
            print("1. Angreifen")
            print("2. Verteidigen")
            print("3. Fliehen")

            battle_choice = input("Bitte wähle eine Option: ")

            if battle_choice == "1":
            # Hier implementieren Sie den Angriff auf das Monster
                self_attack = self.attack()  # Angriff des Spielers
            monster_health = monster.take_damage(self_attack)  # Das Monster erleidet Schaden
            print(f"Du greifst {monster.name} mit {self_attack} an.")
            print(f"{monster.name} hat noch {monster_health} Gesundheit.")

            if monster_health <= 0:
                print(f"{monster.name} wurde besiegt! Du hast gewonnen.")
                break

            # Das Monster kontert
            monster_attack = monster.attack()
            self_health = self.take_damage(monster_attack)
            print(f"{monster.name} kontert mit einem Angriff von {monster_attack}.")
            print(f"Deine Gesundheit: {self_health}")
            
            if self_health <= 0:
                print(f"{monster.name} hat dich besiegt! Du hast verloren.")
                break

            elif battle_choice == "2":
            # Hier implementieren Sie die Verteidigung
                pass
            elif battle_choice == "3":
                print(f"Du fliehst aus dem Kampf gegen {monster.name}.")
            break
        else:
            print("Ungültige Option. Bitte wähle erneut.")
                
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
            injured_friends = [friend for friend in self.current_location.friends if isinstance(friend, Character) and friend.is_alive() and friend.health < 100]
            if injured_friends:
                target = random.choice(injured_friends)
                healing_amount = random.randint(10, 20)
                target.heal(healing_amount)
                return 0  # Heiler heilt und fügt keinen Schaden zu
        else:
            # Standardangriff
            return random.randint(5, 15)

    
    def perform_attack(self, enemy, damage):
        if enemy.is_alive():
            enemy.take_damage(damage)
            print(f"{self.name} hat {enemy.name} angegriffen und {damage} Schaden zugefügt.")
            if not enemy.is_alive():
                print(f"{enemy.name} wurde besiegt!")

    def heal(self, amount):
        self.health += amount
        if self.health > 100:
            self.health = 100
        print(f"{self.name} hat {amount} Gesundheit erhalten.")

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
    
    def flee(self):
        self.in_battle = False
        self.current_location = None
        print(f"{self.name} ist geflohen!")

    def join_team(self, other_character):
        self.team.append(other_character)
        print(f"{self.name} hat {other_character.name} dem Team beigetreten.")
    
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
    
    def display_stats(self):
        print(f"{self.name} (Level {self.level}) - Gesundheit: {self.health} - Erfahrungspunkte: {self.experience_points}")
        print(f"Rolle: {self.role} - Rasse: {self.breed}")
        
class Game:
    def __init__(self):
        self.characters = []
        self.locations = self.initialize_locations()
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
    def start(self):
        print("Willkommen zum Abenteuerspiel!")
        while True:
            print("\nHauptmenü:")
            print("1. Neues Spiel starten")
            print("2. Spielstand laden")
            print("3. Spiel beenden")
            choice = input("Bitte wählen Sie eine Option: ")
            if choice == "1":
                self.new_game()
            elif choice == "2":
                self.load_game()
            elif choice == "3":
                print("Das Spiel wurde beendet.")
                break
            else:
                print("Ungültige Option. Bitte wählen Sie erneut.")
    def new_game(self):
        print("Neues Spiel wird gestartet...")
        self.characters = self.initialize_characters()
        self.locations = self.initialize_locations()
        self.start_adventure()
    def initialize_characters(self):
        characters = {
            "Daisy": Character("Daisy", 4, "Rauhaardackel-Terrier Mix", "Nahkampf-Spezialist", is_enemy=False),
            "Bruno": Character("Bruno", 3, "Bernhardiner", "Fernkampf-Spezialist", is_enemy=False),
            "Leika": Character("Leika", 5, "Pudel-Yorkshire Mix", "Nahkampf-Spezialistin", is_enemy=False),
            "Jack": Character("Jack", 6, "Pudel", "Heiler", is_enemy=False),
            "Leo": Character("Leo", 12, "Maltester", "Magier", is_enemy=False),
            "Hubertus Snickers": Character("Hubertus Snickers", 30, "Chihuahua", "Höllenhund aus dem Chihuahuareich", is_enemy=True),
        }
        return characters
    class Locations(Game):
        def initialize_locations(self):
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
        
class Monster(Character):
    def __init__(self, name, level, breed, role, health, attack, attacks=None, current_location=None):
        super().__init__(name, level, breed, role, health, attack)
        self.attacks = attacks if attacks is not None else []
        self.current_location = current_location


    def generate_monster_attacks(self, name, level):
        attacks = {}
        if name == "Spinne":
            if 1 <= level <= 19:
                attacks["Seidenfaden"] = {"damage": level * 2, "description": "Umwickelt den Gegner komplett ein."}
                attacks["Giftzahn"] = {"damage": level * 3, "description": "Beißt den Gegner mit vergifteten Zähnen an."}
                attacks["Turbosprung"] = {"damage": level * 2, "description": "Springt auf den Gegner und fügt zufälligen Schaden zu."}
            else:
                raise ValueError("Level außerhalb des zulässigen Bereichs für Spinne.")
        elif name == "Wildschwein":
            if 20 <= level <= 49:
                attacks["Rammbock"] = {"damage": level * 2, "description": "Rennt mit schnellen Schritten auf den Gegner zu und fügt ihm zufälligen Schaden zu (Gegner ist verwirrt)."}
                attacks["Stoßzahn"] = {"damage": level * 3, "description": "Der Gegner wird im Nahkampf durch Stoßzähne verletzt."}
                attacks["Teleportation"] = {"damage": level * 2, "description": "Kann sich weg teleportieren und greift in der nächsten Runde an (Gegner kann ihn nicht angreifen)."}
            else:
                raise ValueError("Level außerhalb des zulässigen Bereichs für Wildschwein.")
        elif name == "Wolf":
            if 50 <= level <= 79:
                attacks["Hyperstrahl"] =  {"damage": level * 2, "description": "Schießt einen Strahl aus der Schnauze."},
                attacks["Mega-Biss"] = {"damage": level * 3, "description": "Beißt sich am Gegner fest und fügt zufälligen Schaden zu."},
                attacks["Riesenklaue"] = {"damage": level * 2, "description": "Greift mit seinen Klauen an und fügt zufällig starken hinzu."}
            else:
                raise ValueError("Level außerhalb des zulässigen Bereichs für Wolf.")
        elif name == "Troll":
            if 80 <= level <= 89:
                attacks["Keulenschlag"] = {"damage": level * 2, "description": "Umwickelt den Gegner komplett ein."},
                attacks["Giftzahn"] = {"damage": level * 3, "description": "Beißt den Gegner mit vergifteten Zähnen an."},
                attacks["Turbosprung"] = {"damage": level * 2, "description": "Springt auf den Gegner und fügt zufälligen Schaden zu."}
            else:
                raise ValueError("Level außerhalb des zulässigen Bereichs für Troll.")
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

class Dungeon:
    def __init__(self, name, description, monsters=None, dungeons=None):
        self.name = name
        self.description = description
        self.monsters = monsters or []  # Hier werden die Monster im Dungeon gespeichert
        self.dungeons = dungeons or []  # Hier können untergeordnete Dungeons definiert werden

    def add_monster(self, monster):
        """
        Füge ein Monster zum Dungeon hinzu.
        """
        self.monsters.append(monster)

    def add_dungeon(self, dungeon):
        """
        Füge einen untergeordneten Dungeon hinzu.
        """
        self.dungeon.append(dungeon)

    def add_random_monster(self):
        """
        Füge ein zufälliges Monster zum Dungeon hinzu.
        """
        if self.monsters:
            random_monster = random.choice(self.monsters)
            self.add_monster(random_monster)

    def explore(self):
        """
        Erkunde den Dungeon.
        """
        print(f"Du betrittst den Dungeon {self.name}. {self.description}")
        for monster in self.monsters:
            print(f"Ein {monster} lauert hier!")

        while True:
            print("\nWas möchtest du tun?")
            print("1. Mit Monstern kämpfen")
            print("2. Weiter zum nächsten Dungeon")
            print("3. Zurück zum vorherigen Ort")
            choice = input("Bitte wähle eine Option: ")

            if choice == "1":
                self.battle_monsters()
            elif choice == "2":
                if self.dungeons:
                    self.explore_next_dungeon()
                else:
                    print("Es gibt keine weiteren Dungeons.")
            elif choice == "3":
                print(f"Du verlässt den Dungeon {self.name}.")
                break
            else:
                print("Ungültige Option. Bitte wähle erneut.")

    def battle_monster(self, monster):
        """
        Simuliert einen Kampf mit einem Monster.
        """
        print(f"Du trittst in den Kampf gegen {monster.name} ein!")

        while True:
            print("\nWas möchtest du im Kampf tun?")
            print("1. Angreifen")
            print("2. Verteidigen")
            print("3. Fliehen")

            battle_choice = input("Bitte wähle eine Option: ")

            if battle_choice == "1":
            # Hier implementieren Sie den Angriff auf das Monster
                player_attack = self.attack()  # Angriff des Spielers
                monster_health = monster.take_damage(player_attack)  # Das Monster erleidet Schaden
                print(f"Du greifst {monster.name} mit {player_attack} an.")
                print(f"{monster.name} hat noch {monster_health} Gesundheit.")

                if monster_health <= 0:
                    print(f"{monster.name} wurde besiegt! Du hast gewonnen.")
                    break

                # Das Monster kontert
                monster_attack = monster.attack()
                player_health = self.take_damage(monster_attack)
                print(f"{monster.name} kontert mit einem Angriff von {monster_attack}.")
                print(f"Deine Gesundheit: {player_health}")
            
                if player_health <= 0:
                    print(f"{monster.name} hat dich besiegt! Du hast verloren.")
                    break
            elif battle_choice == "2":
                # Hier implementieren Sie die Verteidigung
                # Zum Beispiel: self.health -= monster.attack
                print(f"{monster.name} greift dich an und verursacht Schaden.")
                if self.health <= 0:
                    print("Du wurdest besiegt!")
                    break
            elif battle_choice == "3":
                print(f"Du fliehst aus dem Kampf gegen {monster.name}.")
                break
            else:
                print("Ungültige Option. Bitte wähle erneut.")

    def explore_next_dungeon(self):
        """
        Erkunde den nächsten untergeordneten Dungeon.
        """
        if not self.current_location.has_dungeons():
            print("Hier gibt es keine Dungeons zu erkunden.")
            return

        # Annahme: Dungeons sind in einer Liste gespeichert
        dungeons = self.current_location.dungeons
        current_dungeon_index = self.current_location.current_dungeon_index

        # Überprüfen, ob es noch unerkundete Dungeons gibt
        if current_dungeon_index >= len(dungeons):
            print("Du hast bereits alle Dungeons erkundet.")
            return

        # Den nächsten Dungeon auswählen
        next_dungeon = dungeons[current_dungeon_index]

        # Hier kannst du weitere Logik für die Erkundung des Dungeons hinzufügen
        # Zum Beispiel, du könntest eine separate Funktion verwenden, um den Dungeon zu betreten und zu erkunden.

        # Aktualisiere den Index des aktuellen Dungeons, um zum nächsten zu gelangen
        self.current_location.current_dungeon_index += 1

        # Drucke eine Nachricht, um den Übergang zum nächsten Dungeon anzuzeigen
        print(f"Du betrittst den Dungeon: {next_dungeon.name}")

        # Weitere Logik zur Erkundung des Dungeons hier

class Location:
    def __init__(self, name, description):
        """
        Initialisiert einen neuen Ort.

        Args:
            name (str): Der Name des Ortes.
            description (str): Eine Beschreibung des Ortes.

        """
        self.name = name
        self.description = description
        self.characters = []
        self.enemies = []
        self.dungeons = []
    
    def add_friend(self, character):
        self.friends.append(character)
        character.current_location = self

    def add_enemy(self, enemy):
        """
        Fügt einen Feind zum Ort hinzu.

        Args:
            enemy (Enemy): Der hinzuzufügende Feind.

        """
        self.enemies.append(enemy)

    def add_dungeon(self, dungeon):
        """
        Fügt einen Dungeon zum Ort hinzu.

        Args:
            dungeon (Dungeon): Der hinzuzufügende Dungeon.

        """
        self.dungeons.append(dungeon)
        if __name__ == "__main__":
            dungeon1 = Dungeon("Höhle des Unheils", 10, "Eine dunkle Höhle, in der gefährliche Monster lauern.")
            dungeon2 = Dungeon("Verzauberter Wald", 25, "Ein Wald voller magischer Geheimnisse.")

            location = Location("Geheimer Wald", "Ein abgelegener Wald, den nur die Mutigsten betreten.")
            location.add_dungeon(dungeon1)
            location.add_dungeon(dungeon2)

            print(f"Ort: {location.name}")
            print(f"Beschreibung: {location.description}")
            print("Dungeons:")
            for dungeon in location.dungeons:
                print(f"- {dungeon.name} (Empfohlenes Level: {dungeon.level})")

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
def explore_location(location):
    """
    Erkunde einen Ort und interagiere mit seinen Elementen.
    """
    print(f"Du befindest dich in {location.name}.")

    while True:
        print("\nWas möchtest du tun?")
        print("1. Mit Freunden sprechen")
        print("2. Mit Feinden kämpfen")
        print("3. Einen Dungeon betreten")
        print("4. Zurück zum Hauptmenü")
        choice = input("Bitte wähle eine Option: ")

        if choice == "1":
            location.list_friends()
            friend_choice = input("Mit welchem Freund möchtest du sprechen? (Gib den Namen ein): ")
            location.interact_with_friend(friend_choice)
        elif choice == "2":
            if location.has_monster():  # Hier wurde "self.current_location" zu "location" geändert
                monster = location.monster  # Hier wurde "self.current_location" zu "location" geändert
                (monster)  # Sie müssen die Methode battle_monster() entsprechend implementieren
        elif choice == "3":
            location.list_dungeons()
            dungeon_choice = input("Welchen Dungeon möchtest du betreten? (Gib den Namen ein): ")
            location.enter_dungeon(dungeon_choice)
        elif choice == "4":
            print("Du kehrst zurück zum Hauptmenü.")
            break
        else:
            print("Ungültige Option. Bitte wähle erneut.")
            
def main():
    """
    Die Hauptfunktion, um das Spiel zu starten.
    """
    print("Willkommen zum Abenteuerspiel!")

    while True:
        print("\nHauptmenü:")
        print("1. Abenteuer starten")
        print("2. Zuhause erkunden")
        print("3. Spiel beenden")
        choice = input("Bitte wählen Sie eine Option: ")

        if choice == "1":
            start_adventure()
        elif choice == "2":
            explore_home()
        elif choice == "3":
            print("Das Spiel wurde beendet.")
            break
        else:
            print("Ungültige Option. Bitte wählen Sie erneut.")
            
def start_adventure(daisy, monster):
    while True:
        print("\nWas möchtest du tun?")
        print("1. Ort erkunden")
        print("2. Charakter anzeigen")
        print("3. Spiel beenden")
        choice = input("Bitte wähle eine Option: ")

        if choice == "1":
            daisy.explore_location()
        elif choice == "2":
            daisy.show_character()
        elif choice == "3":
            print("Das Spiel wird beendet. Auf Wiedersehen!")
            break
        else:
            print("Ungültige Eingabe. Bitte wähle eine der verfügbaren Optionen.")

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
    village.add_dungeon("Verlassene Höhle", "Eine düstere, verlassene Höhle", [
        ("Spinne", 5, 10),  # Monstername, min_level, max_level
        ("Wildschwein", 8, 15),
        ("Wolf", 12, 20),
    ])    
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
        explore_location(daisy)  # Hier rufen wir die explore_location-Funktion auf

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