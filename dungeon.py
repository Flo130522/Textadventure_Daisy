import random
import json
def enter_dungeon(self, dungeon, locations):
    if dungeon in locations:
        dungeon_location = locations[dungeon]
        if isinstance(dungeon_location, Dungeon):
            # TODO: Implement dungeon logic
            print(f"Du betrittst das {dungeon_location.name}.")
            monsters = dungeon_location.monsters
            if monsters:
                self.in_battle = True
                self.can_attack = True
                print("Du trittst in einen Kampf ein!")

def fight_monsters_in_dungeon(self, dungeon):
        if self.in_battle:
            print("Du befindest dich bereits im Kampf.")
            return

        if not dungeon.monsters:
            print("Es gibt keine Monster im Dungeon.")
            return

        selected_monster = random.choice(dungeon.monsters)
        print(f"Du triffst auf eine Level {selected_monster.level} {selected_monster.name} im Dungeon!")
        
def add_monster(self, monster):
    """
    Füge ein Monster zum Dungeon hinzu.
    """
    self.monsters.append(monster)
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