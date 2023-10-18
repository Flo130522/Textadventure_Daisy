import pygame
import sys
from datetime import datetime

# Definieren Sie Farben
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Game:
    def __init__(self):
        """
        Initialisiert ein neues Spiel und Pygame.
        """
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Mein Pygame-Spiel")
        self.clock = pygame.time.Clock()
        self.is_running = True

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
                else:
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
        elif all(not monster.is_alive() for monster in monsters):
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