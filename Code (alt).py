import random

# Globale Daten für das Spiel
item_descriptions = {
    "Trank (20 HP)": "Ein Trank, der 20 Gesundheitspunkte wiederherstellt.",
    "Trank (40 HP)": "Ein stärkerer Trank, der 40 Gesundheitspunkte wiederherstellt.",
    "Schwert": "Ein scharfes Schwert, das mehr Schaden im Kampf verursacht.",
}

skills_descriptions = {
    "Kratzattacke": "Eine einfache Kratzattacke, die wenig Schaden verursacht.",
}

attacks = [
    {"name": "Kratzattacke", "min_damage": 1, "max_damage": 10},
    {"name": "Biss", "min_damage": 5, "max_damage": 15},
    {"name": "Trickser", "min_damage": 10, "max_damage": 20},
]

potions = [
    "Trank (20 HP)",
    "Trank (40 HP)",
    "Trank (60 HP)",
    "Trank (100 HP)",
]

available_skills = {
    "Schwertkampf": "Erlernbar, wenn ein Schwert im Inventar ist.",
    "Feuerball": "Erlernbar ab Level 5.",
    "Tarnung": "Erlernbar ab Level 3.",
}


class Character:
    def __init__(self, name, age, breed, role, is_enemy=True, home=None):
        self.name = name
        self.age = age
        self.breed = breed
        self.role = role
        self.health = 100
        self.level = 1
        self.inventory = []
        self.skills = ["Kratzattacke"]  # Startfähigkeit
        self.is_enemy = is_enemy
        self.current_location = None
        self.home = home

    def add_item_to_inventory(self, item_name, item_description):
        if len(self.inventory) < 20:
            self.inventory.append((item_name, item_description))
            print(f"{self.name} hat {item_name} gefunden.")
        else:
            print(
                f"{self.name} hat zu viele Elemente im Inventar und kann {item_name} nicht aufnehmen."
            )

    def learn_skill(self, skill_name, description):
        if len(self.skills) >= 3:
            replace_skill = input(
                "Du hast bereits 3 Fähigkeiten. Welche möchtest du ersetzen? "
            )
            if replace_skill in self.skills:
                self.skills.remove(replace_skill)
                print(f"{replace_skill} wurde ersetzt.")

        self.skills.append(skill_name)
        print(f"{self.name} hat eine neue Fähigkeit gelernt: {skill_name}")

    def is_skill_unlocked(self, skill_name):
        if skill_name in self.skills:
            return True
        return False

    def display_inventory_and_skills(self):
        print(f"Inventar von {self.name}:")
        for item, description in self.inventory:
            if "Trank" in item:
                description = f"Heilt {int(item.split()[0])} HP"
            else:
                description = item_descriptions.get(
                    item, "Beschreibung nicht verfügbar"
                )
            print(f"- {item}: {description}")

        print(f"Fähigkeiten von {self.name}:")
        for skill in self.skills:
            description = skills_descriptions.get(skill, "Beschreibung nicht verfügbar")
            print(f"- {skill}: {description}")

    def move_to_location(self, location):
        self.current_location = location

    def go_home(self):
        if self.home:
            self.move_to_location(self.home)
        else:
            print(f"{self.name} hat keinen Zuhause-Ort festgelegt.")

    def is_alive(self):
        return self.health > 0

    def take_damage(self, damage):
        self.health -= damage

    def attack(self, enemy):
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

    def level_up(self):
        self.level += 1
        print(f"{self.name} hat Level {self.level} erreicht!")
        if self.level % 2 == 0:
            self.learn_random_skill()

    def find_item(self, item_name, item_description):
        if len(self.inventory) < 20:
            self.inventory.append((item_name, item_description))
            print(f"{self.name} hat {item_name} gefunden.")
        else:
            print(
                f"{self.name} hat zu viele Elemente im Inventar und kann {item_name} nicht aufnehmen."
            )

    def choose_attack(self, enemy):
        if self.is_enemy:
            # Gegner können immer angreifen
            damage = random.randint(1, 10)  # Angriffsschaden anpassen
            enemy.take_damage(damage)
            print(f"{self.name} greift {enemy.name} an und fügt {damage} Schaden zu.")
        else:
            print(f"{self.name}s verfügbare Angriffe:")
            attacks = ["Kratzattacke"]
            if self.is_skill_unlocked("Schwertkampf"):
                attacks.append("Schwertangriff")
            if self.is_skill_unlocked("Feuerball"):
                attacks.append("Feuerball")
            if self.is_skill_unlocked("Tarnung"):
                attacks.append("Tarnangriff")

            for i, attack in enumerate(attacks, start=1):
                print(f"{i}. {attack}")

            while True:
                choice = input("Wähle einen Angriff (1/2/3): ")
                if choice.isdigit():
                    choice = int(choice)
                if 1 <= choice <= len(attacks):
                    attack = attacks[choice - 1]
                    damage = random.randint(1, 10)  # Angriffsschaden anpassen
                    enemy.take_damage(damage)
                    print(
                        f"{self.name} führt {attack} aus und fügt {enemy.name} {damage} Schaden zu."
                    )
                    break
                else:
                    print("Ungültige Auswahl. Bitte wähle einen Angriff (1/2/3).")

    def learn_random_skill(self):
        # Hier können Sie Code hinzufügen, um zufällig eine neue Fähigkeit zu lernen
        pass

    def display_inventory(self):
        print(f"{self.name}s Inventar:")
        for item, description in self.inventory:
            print(f"{item}: {description}")

    def travel(self, destination):
        self.move_to_location(destination)

    def zeige_inventar_und_faehigkeiten(charakter):
        print(f"Inventar von {charakter.name}:")
        for item in charakter.inventar:
            if "Trank" in item:
                beschreibung = f"Heilt {item.split()[0]} HP"
            else:
                beschreibung = "Waffe"
        print(f"- {item}: {beschreibung}")

        print(f"Fähigkeiten von {charakter.name}:")
        for faehigkeit, beschreibung in charakter.faehigkeiten.items():
            print(f"- {faehigkeit}: {beschreibung}")


class Location:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.enemies = []
        self.friends = []
        self.in_battle = False
        self.inventory = {}

    def display_inventory(self):
        print(f"{self.name}s Inventar:")
        for item, description in self.inventory.items():
            print(f"{item}: {description}")

    def add_enemy(self, enemy):
        self.enemies.append(enemy)

    def add_friend(self, friend):
        self.friends.append(friend)

    def display_inventory(self):
        print(f"{self.name}s Inventar:")
        for item in self.inventory:
            description = item_descriptions.get(item, "Beschreibung nicht verfügbar")
            print(f"{item}: {description}")

    def learn_skill(self, skill_name, description):
        if len(self.skills) >= 3:
            replace_skill = input(
                "Du hast bereits 3 Fähigkeiten. Welche möchtest du ersetzen? "
            )
            if replace_skill in self.skills:
                self.skills.remove(replace_skill)
                print(f"{replace_skill} wurde ersetzt.")

        self.skills.append(skill_name)
        self.skills_descriptions[skill_name] = description
        print(f"{self.name} hat eine neue Fähigkeit gelernt: {skill_name}")

    def display_skills_descriptions(self):
        for skill in self.skills:
            print(f"{skill}: {skills_descriptions[skill]}")


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
    # Backstory
    print(
        "Huberus Snickers schickt sein Gefolge los, um das Schutzgeld aus Grauholz und anderen Dörfern einzutreiben."
    )
    print(
        "Daisys Eltern haben nicht genug Geld, um das Schutzgeld zu bezahlen. Sie verstecken Daisy, werden jedoch nach einem angespannten Gespräch mit dem Gefolge getötet."
    )
    print("Daisy bekommt alles mit und schwört sich Rache.")

    daisy = Character("Daisy", 4, "Rauhaardackel-Terrier Mix", "Main", is_enemy=False)
    bruno = Character(
        "Bruno", 3, "Bernhardiner", "Fernkampf-Spezialist", is_enemy=False
    )
    leika = Character(
        "Leika", 5, "Pudel-Yorkshire Mix", "Nahkampf-Spezialistin", is_enemy=False
    )
    jack = Character("Jack", 6, "Pudel", "Heiler", is_enemy=False)
    leo = Character("Leo", 12, "Maltester", "Magier", is_enemy=False)
    hubertus = Character(
        "Hubertus Snickers",
        30,
        "Chihuahua",
        "Höllenhund aus dem Chihuahuareich",
        is_enemy=True,
    )

    village = Location("Grauholz", "Ein friedliches Dorf, in dem alles begann.")
    forest = Location("Finsterwald", "Ein dunkler Wald, der viele Gefahren birgt.")
    city = Location("Hundewacht", "Eine belebte Stadt mit vielen Menschen.")
    endgame = Location(
        "Chihuahua-Höllenreich",
        "Das dunkle Reich, in dem der Höllenhund Hubertus Snickers sein Unwesen treibt",
    )
    home = Location("Zuhause", "Daisys gemütliches Zuhause.")
    dock = Location("Bootssteg", "Der Bootssteg am Flussufer.")
    market = Location(
        "Dorfmarkt", "Der belebte Dorfmarkt, auf dem viele Geschäfte sind."
    )

    daisy.home = home
    bruno.home = home
    leika.home = home
    jack.home = home
    leo.home = home

    daisy.move_to_location(village)

    village.add_friend(bruno)
    village.add_friend(leika)
    village.add_friend(daisy)
    forest.add_friend(leo)
    city.add_friend(jack)
    city.add_friend(daisy)
    endgame.add_enemy(hubertus)

    current_location = village

    while daisy.is_alive():
        print("\nAktueller Ort:", current_location.name)
        print(current_location.description)
        action = input(
            "Was möchtest du tun? (Angriff / Inventar anzeigen / Fähigkeiten anzeigen / Reisen): "
        ).lower()

        if action == "reisen":
            destination = input(
                "Wohin möchtest du reisen? (Nach Hause / Zum Bootssteg / Zum Dorfmarkt): "
            ).lower()
            if destination == "nach hause":
                daisy.travel(home)
            elif destination == "zum bootssteg":
                daisy.travel(dock)
            elif destination == "zum dorfmarkt":
                daisy.travel(market)
            else:
                print(
                    "Ungültiges Reiseziel. Wähle Nach Hause, Zum Bootssteg oder Zum Dorfmarkt."
                )
            current_location = (
                daisy.current_location
            )  # Aktualisiere den aktuellen Ort nach dem Reisen

        elif action == "nach hause gehen":
            daisy.go_home()
            current_location = daisy.current_location  # Aktualisiere den aktuellen Ort

        elif action == "zum bootssteg":
            daisy.move_to_location(dock)
            current_location = daisy.current_location  # Aktualisiere den aktuellen Ort

        elif action == "zum dorfmarkt":
            daisy.move_to_location(market)
            current_location = daisy.current_location  # Aktualisiere den aktuellen Ort

        else:
            if current_location.in_battle:
                print("Feindliche Charaktere im aktuellen Ort:")
                for enemy in current_location.enemies:
                    if enemy.is_alive():
                        print(
                            f"{enemy.name} ({enemy.age} Jahre, {enemy.breed}) - Rolle: {enemy.role} - Gesundheit: {enemy.health}"
                        )

                print("Freundliche Charaktere im aktuellen Ort:")
                for friend in current_location.friends:
                    if friend.is_alive():
                        print(
                            f"{friend.name} ({friend.age} Jahre, {friend.breed}) - Rolle: {friend.role} - Gesundheit: {friend.health}"
                        )

                battle_action = input(
                    "Was möchtest du tun? (Angriff / Inventar anzeigen): "
                ).lower()

                if battle_action == "angriff":
                    target_name = input("Mit welchem Charakter möchtest du angreifen? ")
                    attacker = None
                    for friend in current_location.friends:
                        if (
                            friend.name.lower() == target_name.lower()
                            and friend.is_alive()
                        ):
                            attacker = friend
                            break
                    if attacker:
                        target = random.choice(
                            [c for c in current_location.enemies if c.is_alive()]
                        )
                        attacker.choose_attack(
                            target
                        )  # Hier wird die neue Methode verwendet
                    else:
                        print("Ungültiger Charaktername.")

        # Zufällige Ereignisse
        if random.randint(1, 6) == 1:
            print("Ein unerwartetes Ereignis tritt ein!")

            event = random.randint(1, 3)

            if event == 1:
                print("Du findest einen wertvollen Gegenstand!")
                item = input("Was möchtest du dem Inventar hinzufügen? ")
                item_description = input("Beschreibung des Gegenstands: ")
                daisy.add_item_to_inventory(item, item_description)

            elif event == 2:
                print("Ein Monster greift an!")
                monster = Character(
                    "Wildes Monster", random.randint(50, 100), "Unbekannt", "Monster"
                )
                damage = daisy.attack(monster)
                print(
                    f"{daisy.name} greift das wilde Monster an und fügt {damage} Schaden zu."
                )
                if not monster.is_alive():
                    print(f"{monster.name} wurde besiegt!")

            else:
                print("Du findest ein altes Buch und lernst eine neue Fertigkeit!")
                skill = input("Welche Fertigkeit möchtest du lernen? ")
                skill_description = input("Beschreibung der Fertigkeit: ")
                daisy.learn_skill(skill, skill_description)

    print(
        "Daisy wurde besiegt. Hubertus Snickers triumphiert und das Dorf bleibt in Angst."
    )


def explore_home():
    print(
        "Daisy lebt mit ihren Eltern in Grauholz. Es ist ein Tag wie jeder andere, die Sonne scheint und es ist angenehm warm."
    )

    while True:
        print("\nDu befindest dich im Wohnzimmer von Daisys Zuhause.")
        print("1. Mit deinem Papa reden")
        print("2. Mit deiner Mama reden")
        print("3. Zurück zum Hauptmenü")

        choice = input("Bitte wählen Sie eine Option: ")

        if choice == "1":
            print(
                "Dein Papa ist in seine Zeitung vertieft und sagt, 'Guten Morgen, kleines.'"
            )
        elif choice == "2":
            print(
                "Deine Mama lächelt und sagt, 'Guten Morgen Daisylein, iss dein Frühstück bevor es kalt wird!'"
            )
        elif choice == "3":
            break
        else:
            print("Ungültige Option. Bitte wählen Sie 1, 2 oder 3.")


if __name__ == "__main__":
    main()
