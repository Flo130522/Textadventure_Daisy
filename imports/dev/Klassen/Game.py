class Game:
    def __init__(self):
            self.characters = []
            self.locations = self.initialize_locations()
            self.current_character = None
            self.save_interval = 3600  # Intervall zum automatischen Speichern in Sekunden (hier 1 Stunde)
            self.last_save_time = datetime.now()
            self.saved_game_filename = "saved_game.pickle"  # Dateiname für den gespeicherten Spielstand


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
    
    def initialize_characters(self):
        characters = {
            "Daisy": Character("Daisy", 4, "Rauhaardackel-Terrier Mix", "Nahkampf-Spezialist", 100, 20, is_enemy=False),
            "Bruno": Character("Bruno", 3, "Bernhardiner", "Fernkampf-Spezialist", 100, 20, is_enemy=False),
            "Leika": Character("Leika", 5, "Pudel-Yorkshire Mix", "Nahkampf-Spezialistin", 100, 20, is_enemy=False),
            "Jack": Character("Jack", 6, "Pudel", "Heiler", 100, 20, is_enemy=False),
            "Leo": Character("Leo", 12, "Maltester", "Magier", 100, 20, is_enemy=False),
            "Hubertus Snickers": Character("Hubertus Snickers", 30, "Chihuahua", "Höllenhund aus dem Chihuahuareich", 100, 20, is_enemy=True),
        }
        
        # Spinnen-Monster hinzufügen
        spider_level = random.randint(1, 19)
        spider_health = spider_level * 10  # Pass Gesundheit entsprechend an
        spider_attack = spider_level * 2  # Pass Angriff entsprechend an
        monster_attacks = Monster.generate_monster_attacks("Spinne", spider_level)
        spider_monster = Monster("Spinnen-Monster", spider_level, "Spinne", "Monster", spider_health, spider_attack, attacks=monster_attacks)
        characters["Spinnen-Monster"] = spider_monster

        # Weitere Monster hinzufügen
        # Beispiel für Wildschwein
        boar_level = random.randint(20, 49)
        boar_health = boar_level * 10  # Pass Gesundheit entsprechend an
        boar_attack = boar_level * 2  # Pass Angriff entsprechend an
        monster_attacks = Monster.generate_monster_attacks("Wildschwein", boar_level)
        boar_monster = Monster("Wildschwein-Monster", boar_level, "Wildschwein", "Monster", boar_health, boar_attack, attacks=monster_attacks)
        characters["Wildschwein-Monster"] = boar_monster

        # Beispiel für Wolf
        wolf_level = random.randint(50, 79)
        wolf_health = wolf_level * 10  # Pass Gesundheit entsprechend an
        wolf_attack = wolf_level * 2  # Pass Angriff entsprechend an
        monster_attacks = Monster.generate_monster_attacks("Wolf", wolf_level)
        wolf_monster = Monster("Wolf-Monster", wolf_level, "Wolf", "Monster", wolf_health, wolf_attack, attacks=monster_attacks)
        characters["Wolf-Monster"] = wolf_monster

        # Beispiel für Troll
        troll_level = random.randint(80, 89)
        troll_health = troll_level * 10  # Pass Gesundheit entsprechend an
        troll_attack = troll_level * 2  # Pass Angriff entsprechend an
        monster_attacks = Monster.generate_monster_attacks("Troll", troll_level)
        troll_monster = Monster("Troll-Monster", troll_level, "Troll", "Monster", troll_health, troll_attack, attacks=monster_attacks)
        characters["Troll-Monster"] = troll_monster
        
        return characters
    
    def auto_save(self):
        current_time = datetime.now()
        if (current_time - self.last_save_time).seconds > self.save_interval:
            self.save_game(self.saved_game_filename)
            self.last_save_time = current_time
            print("Spielstand wurde automatisch gespeichert.")

    def save_game(self, filename):
        try:
            with open(filename, "wb") as file:
                pickle.dump(self, file)
            print("Spielstand wurde gespeichert.")
        except Exception as e:
            print(f"Fehler beim Speichern des Spielstands: {e}")

    @staticmethod
    def load_game(filename):
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

    def start(self):
        print("Willkommen zum Abenteuerspiel!")
        while True:
            if not self.menu_stack:
                # Wenn der Menü-Stack leer ist, befinden wir uns im Hauptmenü
                print("\nHauptmenü:")
                print("1. Neues Spiel starten")
                print("2. Spielstand laden")
                print("3. Spiel beenden")
                choice = input("Bitte wählen Sie eine Option: ")
                if choice == "1":
                            print("Neues Spiel wird gestartet...")
                            print("Das Abenteuer beginnt!")
                elif choice == "2":
                    filename = input("Geben Sie den Dateinamen des Spielstands ein: ")
                    self.load_game_menu()
                elif choice == "3":
                    print("Das Spiel wurde beendet.")
                    break
                else:
                    print("Ungültige Option. Bitte wählen Sie erneut.")
    
    def load_game_menu(self):
        print("Spielstand laden...")
        filename = input("Geben Sie den Dateinamen des Spielstands ein (oder 'zurück' zum Hauptmenü): ")
        if filename.lower() == "zurück":
            return  # Zurück zum Hauptmenü
        loaded_game = self.load_game(filename)
        if loaded_game:
            # Das Spiel wurde erfolgreich geladen
            self.menu_stack.append(self.loaded_game_menu)  # Wechsel zum Menü für geladene Spiele

    def initialize_characters(self):
        characters = [
            Character("Daisy", 4, "Rauhaardackel-Terrier Mix", "Nahkampf-Spezialist", is_enemy=False),
            Character("Bruno", 3, "Bernhardiner", "Fernkampf-Spezialist", is_enemy=False),
            Character("Leika", 5, "Pudel-Yorkshire Mix", "Nahkampf-Spezialistin", is_enemy=False),
            Character("Jack", 6, "Pudel", "Heiler", is_enemy=False),
            Character("Leo", 12, "Maltester", "Magier", is_enemy=False),
            Character("Hubertus Snickers", 30, "Chihuahua", "Höllenhund aus dem Chihuahuareich", is_enemy=True),
        ]
        return characters

    def start_adventure(self):
        print("Das Abenteuer beginnt!")
    
    def start_battle(self, characters, monsters):
        print("Ein Kampf beginnt!")
        while True:
            for character in characters + monsters:
                if character.is_alive():
                    if isinstance(character, Character):
                        # Spielercharakter ist dran
                        self.player_turn(characters, monsters)
                    else:
                        # Monster ist dran
                        self.monster_turn(character, characters)
                    # Überprüfe, ob der Kampf vorbei ist
                    if not self.check_battle_over(characters, monsters):
                        return

    def select_character(self, characters):
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

    
    def player_turn(self, characters, monsters):
        print("Dein Zug:")
        
        # Zeige dem Spieler die verfügbaren Charaktere im Team
        print("Wähle einen Charakter:")
        for i, character in enumerate(characters):
            print(f"{i + 1}. {character.name}")
        
        # Lass den Spieler einen Charakter auswählen
        while True:
            try:
                choice = int(input("Gib die Nummer des Charakters ein: ")) - 1
                if 0 <= choice < len(characters):
                    selected_character = characters[choice]
                    break
                else:
                    print("Ungültige Auswahl. Bitte wähle erneut.")
            except ValueError:
                print("Ungültige Eingabe. Bitte gib eine Nummer ein.")
        
        # Hier kannst du die Aktionen für den ausgewählten Charakter implementieren
        # Z.B. Angriff, Heilung, Auswahl einer Aktion, etc.
        print(f"{selected_character.name} ist an der Reihe!")

        # Implementiere hier die Aktionen für den ausgewählten Charakter
        # Du kannst hier den Angriff, Heilung usw. hinzufügen

    def monster_turn(self, monster, characters):
        monster_attack, attack_description = monster.attack()
        selected_character = random.choice(characters)
        
        damage, status_message = selected_character.take_damage(monster_attack)
        print(f"{monster.name} kontert mit einem Angriff von {attack_description}.")
        print(f"{selected_character.name} erleidet {damage} Schaden.")
        print(f"Die Gesundheit von {selected_character.name}: {selected_character.health}")
        
        if not selected_character.is_alive():
            print(f"{selected_character.name} wurde besiegt!")
            characters.remove(selected_character)

        if not characters:
            print("Alle deine Charaktere wurden besiegt! Du hast verloren.")
      
    def check_battle_over(self, characters, monsters):
        # Überprüfe, ob alle Monster besiegt sind
        if all(not monster.is_alive() for monster in monsters):
            print("Du hast den Kampf gewonnen!")
            return True

        # Überprüfe, ob alle Spielercharaktere besiegt sind
        if all(not character.is_alive() for character in characters):
            print("Du hast den Kampf verloren!")
            return True

        return False
        pass   
