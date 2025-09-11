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
        self.in_battle = False  # Neue Variable für den Kampfstatus

    def is_alive(self):
        return self.health > 0

    def take_damage(self, damage):
        self.health -= damage

    def attack(self, enemy):
        if self.in_battle:
            if self.role == "Fernkampf-Spezialist":
                damage = random.randint(10, 20)
            elif self.role == "Nahkampf-Spezialistin":
                damage = random.randint(15, 25)
            elif self.role == "Heiler":
                damage = 0
            elif self.role == "Magier":
                damage = random.randint(5, 15)
            else:
                damage = random.randint(1, 10)
            enemy.take_damage(damage)
            return damage
        else:
            print(f"{self.name} ist nicht im Kampf und kann nicht angreifen.")

    def level_up(self):
        self.level += 1
        print(f"{self.name} hat Level {self.level} erreicht!")

    def learn_skill(self, skill):
        self.skills.append(skill)

    def add_item_to_inventory(self, item):
        self.inventory.append(item)

    def display_inventory(self):
        print(f"{self.name}s Inventar:")
        for item in self.inventory:
            print(item)

    def travel_and_encounter(self, destination):
        self.current_location = destination
        print(f"{self.name} reist nach {destination.name}.")

        if random.randint(1, 3) == 1:
            enemy_strength = random.randint(10, 30)
            enemy = Character("Gefolgsmann", enemy_strength, "Unbekannt", "Gefolgsmann", is_enemy=True)
            print(f"{self.name} wird von einem Gefolgsmann mit Stärke {enemy_strength} angegriffen!")
            damage = self.attack(enemy)
            print(f"{self.name} greift den Gefolgsmann an und fügt {damage} Schaden zu.")
            if not enemy.is_alive():
                print(f"Der Gefolgsmann wurde besiegt!")

class Location:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.enemies = []
        self.friends = []
        self.in_battle = False

    def add_enemy(self, enemy):
        self.enemies.append(enemy)

    def add_friend(self, friend):
        self.friends.append(friend)

def main():
    print("Das Abenteuer des Rache-Dackels: Daisy gegen Huberus Snickers")
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
def start_adventure():
        # Erstelle Charaktere
    daisy = Character("Daisy", 4, "Rauhaardackel-Terrier Mix", "Main", is_enemy=False)
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

    current_location = home

    while daisy.is_alive():
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

        action = input("Was möchtest du tun? (Angriff / Inventar anzeigen / Reisen): ").lower()

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

        elif action == "reisen":
            destination = input("Wohin möchtest du reisen? (Nach Hause / Zum Bootssteg / Zum Dorfmarkt): ").lower()
            if destination == "nach hause":
                daisy.travel(home)
            elif destination == "zum bootssteg":
                daisy.travel(dock)
            elif destination == "zum dorfmarkt":
                daisy.travel(market)
            else:
                print("Ungültiges Reiseziel. Wähle Nach Hause, Zum Bootssteg oder Zum Dorfmarkt.")
            current_location = daisy.current_location  # Aktualisiere den aktuellen Ort nach dem Reisen

        else:
            print("Ungültige Aktion. Wähle Angriff, Inventar anzeigen oder Reisen.")

    print("Daisy wurde besiegt. Hubertus Snickers triumphiert und das Dorf bleibt in Angst.")

def explore_home():
    print("Daisy lebt mit ihren Eltern in Grauholz. Es ist ein Tag wie jeder andere, die Sonne scheint und es ist angenehm warm.")

    while True:
        print("\nDu befindest dich im Wohnzimmer von Daisys Zuhause.")
        print("1. Mit deinem Papa reden")
        print("2. Mit deiner Mama reden")
        print("3. Zurück zum Hauptmenü")

        choice = input("Bitte wählen Sie eine Option: ")

        if choice == "1":
            print("Dein Papa ist in seine Zeitung vertieft und sagt, 'Guten Morgen, kleines.'")
        elif choice == "2":
            print("Deine Mama lächelt und sagt, 'Guten Morgen Daisylein, iss dein Frühstück bevor es kalt wird!'")
        elif choice == "3":
            break
        else:
            print("Ungültige Option. Bitte wählen Sie 1, 2 oder 3.")

if __name__ == "__main__":
    main()
