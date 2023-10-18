import random
import pickle
from datetime import datetime
from typing import Dict, Optional, List, Union

class Character:
    """
    Erstellt einen neuen Charakter mit den angegebenen Eigenschaften.

    Args:
        name (str): Der Name des Charakters.
        age (int): Das Alter des Charakters.
        breed (str): Die Rasse des Charakters.
        role (str): Die Rolle des Charakters.
        health (int, optional): Die Gesundheit des Charakters (Standardwert: 100).
        attack (int, optional): Die Angriffskraft des Charakters (Standardwert: 0).
        is_enemy (bool, optional): Gibt an, ob der Charakter ein Feind ist (Standardwert: False).
    """
    MAX_HEALTH = 100
    MAX_INVENTORY_LIMIT = 20

    def __init__(self, name: str, age: int, breed: str, role: str, health: int = MAX_HEALTH, attack: int = 0, is_enemy: bool = False):
        self.name = name
        self.age = age
        self.breed = breed
        self.role = role
        self.health = health
        self.attack = attack
        self.level = 1
        self.experience_points = 0
        self.inventory: List[Dict[str, Union[str, int]]] = []  # Typannotation für die "inventory"-Liste
        self.inventory_limit = 20
        self.skills: List[str] = []  # Typannotation für die "skills"-Liste
        self.is_enemy = is_enemy
        self.current_location: Optional[Location] = None  # Typannotation für "current_location" mit Optional
        self.in_battle = False
        self.is_blocked = False
        self.team: List[Character] = []  # Typannotation für die "team"-Liste


    def earn_experience_points(self, amount):
        self.experience_points += amount
        print(f"{self.name} hat {amount} EP erhalten!")

    def check_level_up(self):
        level_up_threshold = self.level * 100
        if self.experience_points >= level_up_threshold:
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

    @staticmethod
    def generate_attacks():
        return {
            "Biss": {"damage": random.randint(5, 15), "description": "Ein kräftiger Biss."},
            "Kratzer": {"damage": random.randint(10, 20), "description": "Ein scharfer Kratzer mit den Pfoten."},
            "Bellender Angriff": {"damage": random.randint(1, 10), "description": "Ein lauter bellender Angriff."},
            "Sprung": {"damage": random.randint(15, 25), "description": "Ein mutiger Sprung auf den Feind."},
        }

    def block(self):
        self.is_blocked = True

    def unblock(self):
        self.is_blocked = False

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def perform_attack(self, enemy, damage):
        if enemy.is_alive():
            enemy.take_damage(damage)
            print(f"{self.name} hat {enemy.name} angegriffen und {damage} Schaden zugefügt.")
            if not enemy.is_alive():
                print(f"{enemy.name} wurde besiegt!")

    def heal(self, amount):
        self.health += amount
        if self.health > self.MAX_HEALTH:
            self.health = self.MAX_HEALTH
        print(f"{self.name} hat {amount} Gesundheit erhalten.")

    def is_alive(self):
        return self.health > 0

class Monster(Character):
    """
    Erstellt ein Monster mit den angegebenen Eigenschaften.

    Args:
        name (str): Der Name des Monsters.
        level (int): Das Level des Monsters.
        breed (str): Die Rasse des Monsters.
        role (str): Die Rolle des Monsters.
        health (int): Die Gesundheit des Monsters.
        attack (int): Die Angriffskraft des Monsters.
        attacks (dict, optional): Eine Liste von Angriffen für das Monster (Standardwert: None).
    """
    def __init__(self, name: str, level: int, breed: str, role: str, health: int, attack: int, attacks: dict = None):
        super().__init__(name, level, breed, role, health, is_enemy=True)
        self.attack = attack
        self.attacks = attacks if attacks else []
        self.current_location = None
        self.health = health 


    def generate_monster_attacks(self, name: str, level: int) -> Dict[str, Dict[str, int]]:
        attacks = {}
        if name == "Spinne":
            attacks["Seidenfaden"] = {"damage": level * 2, "description": "Umwickelt den Gegner komplett ein."}
            attacks["Giftzahn"] = {"damage": level * 3, "description": "Beißt den Gegner mit vergifteten Zähnen an."}
            attacks["Turbosprung"] = {"damage": level * 2, "description": "Springt auf den Gegner und fügt zufälligen Schaden zu."}
                
        elif name == "Wildschwein":
            attacks["Rammbock"] = {"damage": level * 2, "description": "Rennt mit schnellen Schritten auf den Gegner zu und fügt ihm zufälligen Schaden zu (Gegner ist verwirrt)."}
            attacks["Stoßzahn"] = {"damage": level * 3, "description": "Der Gegner wird im Nahkampf durch Stoßzähne verletzt."}
            attacks["Teleportation"] = {"damage": level * 2, "description": "Kann sich weg teleportieren und greift in der nächsten Runde an (Gegner kann ihn nicht angreifen)."}

        elif name == "Wolf":
            attacks["Hyperstrahl"] = {"damage": level * 2, "description": "Schießt einen Strahl aus der Schnauze."}
            attacks["Mega-Biss"] = {"damage": level * 3, "description": "Beißt sich am Gegner fest und fügt zufälligen Schaden zu."}
            attacks["Riesenklaue"] = {"damage": level * 2, "description": "Greift mit seinen Klauen an und fügt zufällig starken hinzu."}

        elif name == "Troll":
            attacks["Keulenschlag"] = {"damage": level * 2, "description": "Umwickelt den Gegner komplett ein."}
            attacks["Giftzahn"] = {"damage": level * 3, "description": "Beißt den Gegner mit vergifteten Zähnen an."}
            attacks["Turbosprung"] = {"damage": level * 2, "description": "Springt auf den Gegner und fügt zufälligen Schaden zu."}
        else:
            raise ValueError("Ungültiger Monstername.")
        return attacks
    
class Location:
    def __init__(self, name: str, description: str):
        """
        Erstellt eine neue Location mit einem Namen und einer Beschreibung.

        Args:
            name (str): Der Name der Location.
            description (str): Die Beschreibung der Location.
        """
        self.name = name
        self.description = description
        self.friends: List[Character] = []  
        self.enemies: List[Character] = []
        self.connections = []  # Hier speichern wir die verbundenen Orte

    def add_connection(self, location):
        self.connections.append(location)

    def add_friend(self, character: Character):
        """
        Fügt einen befreundeten Charakter zur Location hinzu.

        Args:
            character (Character): Der Charakter, der hinzugefügt werden soll.
        """
        if isinstance(character, Character):
            self.friends.append(character)
        else:
            raise ValueError("Nur Instanzen der Klasse 'Character' können als Freunde hinzugefügt werden.")

    def add_enemy(self, character: Character):
        """
        Fügt einen feindlichen Charakter zur Location hinzu.

        Args:
            character (Character): Der Charakter, der hinzugefügt werden soll.
        """
        if isinstance(character, Character):
            self.enemies.append(character)
        else:
            raise ValueError("Nur Instanzen der Klasse 'Character' können als Feinde hinzugefügt werden.")

class Game:
    def __init__(self):
        """
        Initialisiert ein neues Spiel.
        """
        self.characters = []
        self.locations = self.initialize_locations()
        self.current_character = None
        self.save_interval = 3600  # Intervall zum automatischen Speichern in Sekunden (hier 1 Stunde)
        self.last_save_time = datetime.now()
        self.saved_game_filename = "saved_game.pickle"
        self.current_state = None

    @staticmethod
    def initialize_locations():
        """
        Initialisiert die Spielorte und ihre Verbindungen.
        
        Returns:
            dict: Ein Dictionary von Ort-Namen auf Location-Objekte.
        """
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
        locations["Grauholz"].add_connection(locations["Finsterwald"])
        locations["Grauholz"].add_connection(locations["Hundewacht"])
        locations["Finsterwald"].add_connection(locations["Grauholz"])
        locations["Finsterwald"].add_connection(locations["Hundewacht"])
        locations["Hundewacht"].add_connection(locations["Grauholz"])
        locations["Hundewacht"].add_connection(locations["Finsterwald"])
        locations["Hundewacht"].add_connection(locations["Chihuahua-Höllenreich"])
        locations["Chihuahua-Höllenreich"].add_connection(locations["Hundewacht"])
        locations["Zuhause"].add_connection(locations["Bootssteg"])
        locations["Bootssteg"].add_connection(locations["Zuhause"])
        locations["Bootssteg"].add_connection(locations["Dorfmarkt"])
        locations["Dorfmarkt"].add_connection(locations["Bootssteg"])
        locations["Dorfmarkt"].add_connection(locations["Höhle im Wald"])
        locations["Dorfmarkt"].add_connection(locations["Magierturm"])
        locations["Dorfmarkt"].add_connection(locations["Kristallsee"])
        locations["Höhle im Wald"].add_connection(locations["Dorfmarkt"])
        locations["Magierturm"].add_connection(locations["Dorfmarkt"])
        locations["Kristallsee"].add_connection(locations["Dorfmarkt"])
        locations["Hundewacht"].add_connection(locations["Gefängniszelle"])
        locations["Gefängniszelle"].add_connection(locations["Hundewacht"])
        return locations
    
    @staticmethod
    def initialize_characters():
        """
        Initialisiert die Spielcharaktere.
        
        Returns:
            list: Eine Liste von Character-Objekten.
        """
        characters = [
            Character("Daisy", 4, "Rauhaardackel-Terrier Mix", "Nahkampf-Spezialist", 100, 20, is_enemy=False),
            Character("Bruno", 3, "Bernhardiner", "Fernkampf-Spezialist", 100, 20, is_enemy=False),
            Character("Leika", 5, "Pudel-Yorkshire Mix", "Nahkampf-Spezialistin", 100, 20, is_enemy=False),
            Character("Jack", 6, "Pudel", "Heiler", 100, 20, is_enemy=False),
            Character("Leo", 12, "Maltester", "Magier", 100, 20, is_enemy=False),
            Character("Hubertus Snickers", 30, "Chihuahua", "Höllenhund aus dem Chihuahuareich", 100, 20, is_enemy=True),
        ]
        
        # Spinnen-Monster hinzufügen
        spider_level = random.randint(1, 19)
        spider_health = spider_level * 10  # Pass Gesundheit entsprechend an
        spider_attack = spider_level * 2  # Pass Angriff entsprechend an
        spider_attacks = Monster.generate_monster_attacks("Spinne", "Spinne", spider_level)  # Monsterangriffe generieren
        spider_monster = Monster("Spinnen-Monster", spider_level, "Spinne", "Monster", spider_health, spider_attack, attacks=spider_attacks)
        characters.append(spider_monster)


        # Weitere Monster hinzufügen
        # Beispiel für Wildschwein
        boar_level = random.randint(20, 49)
        boar_health = boar_level * 10  # Pass Gesundheit entsprechend an
        boar_attack = boar_level * 2  # Pass Angriff entsprechend an
        boar_attacks = Monster.generate_monster_attacks("Wildschwein", "Wildschwein", boar_level)
        boar_monster = Monster("Wildschwein-Monster", boar_level, "Wildschwein", "Monster", boar_health, boar_attack, attacks=boar_attacks)
        characters.append(boar_monster)

        # Beispiel für Wolf
        wolf_level = random.randint(50, 79)
        wolf_health = wolf_level * 10  # Pass Gesundheit entsprechend an
        wolf_attack = wolf_level * 2  # Pass Angriff entsprechend an
        wolf_attacks = Monster.generate_monster_attacks("Wolf", "Wolf", wolf_level)
        wolf_monster = Monster("Wolf-Monster", wolf_level, "Wolf", "Monster", wolf_health, wolf_attack, attacks=wolf_attacks)
        characters.append(wolf_monster)

        # Beispiel für Troll
        troll_level = random.randint(80, 89)
        troll_health = troll_level * 10  # Pass Gesundheit entsprechend an
        troll_attack = troll_level * 2  # Pass Angriff entsprechend an
        troll_attacks = Monster.generate_monster_attacks("Troll", "Troll", troll_level)
        troll_monster = Monster("Troll-Monster", troll_level, "Troll", "Monster", troll_health, troll_attack, attacks=troll_attacks)
        characters.append(troll_monster)
        
        return characters
    
    def auto_save(self):
        """
        Automatisches Speichern des Spiels, basierend auf dem angegebenen Intervall.
        """
        current_time = datetime.now()
        time_difference = current_time - self.last_save_time
        if time_difference.total_seconds() >= self.save_interval:
            self.save_game(self.saved_game_filename)
            self.last_save_time = current_time
            print("Das Spiel wurde automatisch gespeichert.")

    def save_game(self, filename):
        """
        Speichert den aktuellen Spielzustand in einer Datei.
        
        Args:
            filename (str): Der Dateiname, unter dem das Spiel gespeichert wird.
        """
        game_state = {
            "characters": self.characters,
            "locations": self.locations,
            "current_character": self.current_character,
        }
        with open(filename, 'wb') as file:
            pickle.dump(game_state, file)
        print("Das Spiel wurde gespeichert.")

    @staticmethod
    def load_game(filename):
        """
        Lädt einen gespeicherten Spielzustand aus einer Datei.
        
        Args:
            filename (str): Der Dateiname der gespeicherten Spiels.
            
        Returns:
            dict: Ein Dictionary mit den gespeicherten Spielinformationen.
        """
        try:
            with open(filename, 'rb') as file:
                game_state = pickle.load(file)
            return game_state
        except FileNotFoundError:
            print("Kein gespeichertes Spiel gefunden.")
            return None
    
    @staticmethod
    def select_character(characters):
        """
        Lässt den Spieler einen Charakter auswählen.

        Args:
            characters (list): Eine Liste von Charakteren, aus denen der Spieler auswählen kann.

        Returns:
            Character: Der ausgewählte Charakter.
        """
        print("Wähle einen Charakter:")
        for i, character in enumerate(characters):
            print(f"{i + 1}. {character.name}")

        while True:
            try:
                choice = int(input("Gib die Nummer des Charakters ein: ")) - 1
                if 0 <= choice < len(characters):
                    return characters[choice]  # Gib den ausgewählten Charakter zurück
                print("Ungültige Auswahl. Bitte wähle erneut.")
            except ValueError:
                print("Ungültige Eingabe. Bitte gib eine Nummer ein.")
    
    def start_new_game(self):
        """
        Startet ein neues Spiel und initialisiert die Charaktere und den aktuellen Ort.
        """
        self.characters = self.initialize_characters()
        self.current_character = self.select_character(self.characters)
        self.current_character.current_location = self.locations["Grauholz"]
        self.current_character.team = []  # Der Charakter startet nicht im Team
        self.current_character.in_battle = False
        self.current_state = "New Game State"


    def start(self):
        """
        Startet das Spiel und zeigt das Hauptmenü an.
        """
        print("Willkommen bei 'Das Abenteuer der mutigen Hunde'!")
        print("1. Neues Spiel starten")
        print("2. Spiel laden")
        print("3. Beenden")
        choice = input("Wähle eine Option: ")
        if choice == "1":
            self.start_new_game()
            self.start_adventure()
        elif choice == "2":
            loaded_game = self.load_game(self.saved_game_filename)
            if loaded_game:
                self.characters = loaded_game["characters"]
                self.locations = loaded_game["locations"]
                self.current_character = loaded_game["current_character"]
                print("Spiel wurde geladen.")
                self.start_adventure()
            else:
                self.start()
        elif choice == "3":
            print("Auf Wiedersehen!")
        else:
            print("Ungültige Eingabe. Bitte wähle eine der verfügbaren Optionen.")

    def load_game_menu(self):
        """
        Zeigt das Menü zum Laden eines gespeicherten Spiels an.
        """
        filename = input("Gib den Dateinamen des gespeicherten Spiels ein: ")
        loaded_state = self.load_game(filename)
        self.current_state = loaded_state

    def start_adventure(self):
        """
        Startet das Abenteuer und zeigt das Hauptspielmenü an.
        """
        print(f"Willkommen, {self.current_character.name}! Du befindest dich in {self.current_character.location.name}.")
        while self.current_character.is_alive():
            print("\nWas möchtest du tun?")
            print("1. Ort erkunden")
            print("2. Inventar anzeigen")
            print("3. Team anzeigen")
            print("4. Spiel speichern")
            print("5. Beenden")
            choice = input("Wähle eine Option: ")
            if choice == "1":
                self.explore_location()
            elif choice == "2":
                self.display_inventory()
            elif choice == "3":
                self.display_team()
            elif choice == "4":
                self.save_game(self.saved_game_filename)
            elif choice == "5":
                print("Auf Wiedersehen!")
                break
            else:
                print("Ungültige Eingabe. Bitte wähle eine der verfügbaren Optionen.")
        else:
            print(f"{self.current_character.name} ist besiegt. Das Abenteuer endet hier.")
    
    def start_battle(self, characters, monsters):
        """
        Startet einen Kampf zwischen Charakteren und Monstern.
    
        Args:
            characters (list): Eine Liste von Charakteren, die am Kampf teilnehmen.
            monsters (list): Eine Liste von Monstern, die am Kampf teilnehmen.
        """
        print("Ein Kampf beginnt!")
        while True:
            for character in characters + monsters:
                if character.is_alive():
                    if isinstance(character, Character):
                        # Spielercharakter ist dran
                        self.player_turn(character, monsters)
                    else:
                        # Monster ist dran
                        self.monster_turn(character, characters)
                    # Überprüfe, ob der Kampf vorbei ist
                    if not self.check_battle_over(characters, monsters):
                        return

    @staticmethod
    def player_turn(character, monsters):
        """
        Führt den Zug eines Spielercharakters im Kampf durch.

        Args:
            character (Character): Der ausgewählte Spielercharakter.
            monsters (list): Eine Liste von Monstern, die am Kampf teilnehmen.
        """
        print(f"Dein Zug mit {character.name}:")
    
        # Implementiere hier die Aktionen für den ausgewählten Charakter
        # Zum Beispiel den Angriff auf ein zufälliges Monster
        target_monster = random.choice(monsters)
        damage_dealt = character.attack(target_monster)
    
        print(f"{character.name} greift {target_monster.name} an und fügt {damage_dealt} Schaden zu.")
        print(f"{target_monster.name} hat noch {target_monster.health} Gesundheit.")

        # Überprüfe, ob das Monster besiegt wurde
        if not target_monster.is_alive():
            print(f"{target_monster.name} wurde besiegt!")
    
    @staticmethod
    def monster_turn(monster, characters):
        """
        Führt den Zug eines Monstercharakters im Kampf durch.

        Args:
            monster (Character): Das Monster, das am Zug ist.
            characters (list): Eine Liste von Charakteren, die am Kampf teilnehmen.
        """
        monster_attack, attack_description = monster.attack()
        selected_character = random.choice(characters)
    
        damage, status_message = selected_character.take_damage(monster_attack)
        print(f"{monster.name} kontert mit einem Angriff von {attack_description}.")
        print(f"{selected_character.name} erleidet {damage} Schaden.")
        print(f"Die Gesundheit von {selected_character.name}: {selected_character.health}")
    
        # Überprüfe, ob der ausgewählte Charakter besiegt wurde
        if not selected_character.is_alive():
            print(f"{selected_character.name} wurde besiegt!")

    @staticmethod
    def check_battle_over(characters, monsters):
        """
        Überprüft, ob der Kampf vorbei ist, indem geprüft wird, ob alle Charaktere oder Monster besiegt wurden.

        Args:
            characters (list): Eine Liste von Charakteren, die am Kampf teilnehmen.
            monsters (list): Eine Liste von Monstern, die am Kampf teilnehmen.

        Returns:
            bool: True, wenn der Kampf vorbei ist, False sonst.
        """
        if all(not character.is_alive() for character in characters):
            print("Alle Charaktere wurden besiegt! Die Monster gewinnen den Kampf.")
            return False
        if all(not monster.is_alive() for monster in monsters):
            print("Alle Monster wurden besiegt! Die Charaktere gewinnen den Kampf.")
            return False
        return True


    def explore_location(self):
        """
        Erkundet den aktuellen Ort und führt Ereignisse aus.
        """
        current_location = self.current_character.location
        print(f"Du erkundest {current_location.name}: {current_location.description}")
        
        # Überprüfe, ob es Feinde gibt
        if current_location.enemies:
            print("Feinde nähern sich!")
            self.start_battle(self.current_character.team, current_location.enemies)
        else:
            print("Es gibt keine Feinde hier.")

        # Überprüfe, ob es Gegenstände gibt
        if current_location.items:
            print("Du findest Gegenstände:")
            for item in current_location.items:
                print(f"- {item.name}: {item.description}")
            self.current_character.add_items(current_location.items)
            current_location.items = []  # Entferne die aufgesammelten Gegenstände

        # Überprüfe, ob es versteckte Orte gibt
        if current_location.hidden_locations:
            print("Du entdeckst versteckte Orte:")
            for location_name in current_location.hidden_locations:
                print(f"- {location_name}")
            hidden_location_choice = input("Möchtest du einen versteckten Ort erkunden? (Ja/Nein): ")
            if hidden_location_choice.lower() == "ja":
                self.explore_hidden_location(current_location)

        # Aktualisiere den aktuellen Ort des Charakters
        self.current_character.location = current_location.random_friend()

    def explore_hidden_location(self, current_location):
        """
        Erkundet einen versteckten Ort und führt Ereignisse aus.

        Args:
            current_location (Location): Der aktuelle Ort, der den versteckten Ort enthält.
        """
        hidden_location_name = input("Gib den Namen des versteckten Ortes ein, den du erkunden möchtest: ")
        if hidden_location_name in current_location.hidden_locations:
            hidden_location = self.locations[hidden_location_name]
            print(f"Du erkundest den versteckten Ort {hidden_location.name}: {hidden_location.description}")
            
            # Überprüfe, ob es Feinde gibt
            if hidden_location.enemies:
                print("Feinde nähern sich!")
                self.start_battle(self.current_character.team, hidden_location.enemies)
            else:
                print("Es gibt keine Feinde hier.")
            
            # Überprüfe, ob es Gegenstände gibt
            if hidden_location.items:
                print("Du findest Gegenstände:")
                for item in hidden_location.items:
                    print(f"- {item.name}: {item.description}")
                self.current_character.add_items(hidden_location.items)
                hidden_location.items = []  # Entferne die aufgesammelten Gegenstände
        else:
            print("Ungültiger Ort. Bitte gib den Namen eines versteckten Ortes ein, den du erkunden möchtest.")

    def display_inventory(self):
        """
        Zeigt den Inventarinhalt des Charakters an.
        """
        print("Inventar:")
        for item in self.current_character.inventory:
            print(f"- {item.name}: {item.description}")

    def display_team(self):
        """
        Zeigt die Teammitglieder des Charakters an.
        """
        print("Team:")
        for character in self.current_character.team:
            print(f"- {character.name}: Gesundheit {character.health}/{character.max_health}, Angriff {character.attack}")
if __name__ == "__main__":
    game = Game()
    game.start()
