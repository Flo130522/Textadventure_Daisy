class Character:
    def __init__(self, name, age, breed, role, is_enemy=False):
        self.name = name
        self.age = age
        self.breed = breed
        self.role = role
        self.health = 100  # Startgesundheit
        self.attack = 0  # Angriffskraft
        self.level = 1
        self.experience_points = 0
        self.inventory = []
        self.inventory_limit = 20
        self.skills = []
        self.is_enemy = is_enemy
        self.current_location = None
        self.in_battle = False
        self.is_blocked = False
        self.team = []

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

    def block(self):
        self.is_blocked = True

    def unblock(self):
        self.is_blocked = False

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0

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

class Monster(Character):
    def __init__(self, name, level, breed, role, health, attack, attacks=None, current_location=None):
        super().__init__(name, level, breed, role, health, attack)
        self.attacks = attacks if attacks is not None else []
        self.current_location = current_location


    def generate_monster_attacks(self, name, level):
        attacks = {}
        if self.breed == "Spinne":
                attacks["Seidenfaden"] = {"damage": level * 2, "description": "Umwickelt den Gegner komplett ein."}
                attacks["Giftzahn"] = {"damage": level * 3, "description": "Beißt den Gegner mit vergifteten Zähnen an."}
                attacks["Turbosprung"] = {"damage": level * 2, "description": "Springt auf den Gegner und fügt zufälligen Schaden zu."}
                
        elif self.breed == "Wildschwein":
                attacks["Rammbock"] = {"damage": level * 2, "description": "Rennt mit schnellen Schritten auf den Gegner zu und fügt ihm zufälligen Schaden zu (Gegner ist verwirrt)."}
                attacks["Stoßzahn"] = {"damage": level * 3, "description": "Der Gegner wird im Nahkampf durch Stoßzähne verletzt."}
                attacks["Teleportation"] = {"damage": level * 2, "description": "Kann sich weg teleportieren und greift in der nächsten Runde an (Gegner kann ihn nicht angreifen)."}

        elif self.breed == "Wolf":
                attacks["Hyperstrahl"] =  {"damage": level * 2, "description": "Schießt einen Strahl aus der Schnauze."},
                attacks["Mega-Biss"] = {"damage": level * 3, "description": "Beißt sich am Gegner fest und fügt zufälligen Schaden zu."},
                attacks["Riesenklaue"] = {"damage": level * 2, "description": "Greift mit seinen Klauen an und fügt zufällig starken hinzu."}

        elif self.breed == "Troll":
                attacks["Keulenschlag"] = {"damage": level * 2, "description": "Umwickelt den Gegner komplett ein."},
                attacks["Giftzahn"] = {"damage": level * 3, "description": "Beißt den Gegner mit vergifteten Zähnen an."},
                attacks["Turbosprung"] = {"damage": level * 2, "description": "Springt auf den Gegner und fügt zufälligen Schaden zu."}
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
