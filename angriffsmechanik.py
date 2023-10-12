import random
import json

# region load data
#Locations aus JSON Datei laden
with open(r"json\locations.json") as fd:
    locations = json.load(fd)

#Charaktere aus JSON Datei laden
with open(r"json\characters.json") as fd:
    characters = json.load(fd)
    friends = characters["friends"]
    enemys = characters["enemies"]
# endregion load data

def is_alive(character):
        return character.health > 0

def take_damage(character, damage):
    character.health -= damage
def attack(character, enemy):
    if character.in_battle:
        if character.role == "Fernkampf-Spezialist":
            damage = random.randint(10, 20)
        elif character.role == "Nahkampf-Spezialistin":
            damage = random.randint(15, 25)
        elif character.role == "Heiler":
            damage = 0
        elif character.role == "Magier":
            damage = random.randint(5, 15)
        else:
            damage = random.randint(1, 10)
        enemy.take_damage(damage)
        return damage
    else:
        print(f"{character.name} ist nicht im Kampf und kann nicht angreifen.")

#Schaden berechnen   
def calculate_damage(character):
    if character.role == "Fernkampf-Spezialist":
        return random.randint(10, 20)
    elif character.role == "Nahkampf-Spezialistin":
        return random.randint(15, 25)
    elif character.role == "Heiler":
        return 0
    elif character.role == "Magier":
        return random.randint(5, 15)
    else:
        return random.randint(1, 10)
    
#Mob-Angriff ausführen    
def perform_attack(character, enemys):
    if character.role == "Spinnen":
        if random.randint(1, 2) == 1:
            print(f"{[character].name} führt Seidenfaden aus und kann sich nicht mehr bewegen!")
            character.can_attack = False
        else:
            print(f"{enemys.name} führt Giftzahn aus und vergiftet {friends.name}!")
            friends.poisoned = True
    elif character.role == "Wildschwein":
        if random.randint(1, 2) == 1:
            print(f"{enemys.name} führt Rammbock aus und verwirrt {friends.name}!")
            friends.confused = True
        else:
            print(f"{character.name} führt Teleportation aus und greift in der nächsten Runde an (Gegner kann ihn nicht angreifen).")
            
def battle_monster(character, monster):
    print(f"Du trittst in den Kampf gegen {monster.name} ein!")
    while True:
        print("\nWas möchtest du im Kampf tun?")
        print("1. Angreifen")
        print("2. Verteidigen")
        print("3. Fliehen")
        battle_choice = input("Bitte wähle eine Option: ")
        if battle_choice == "1":
        # Hier implementieren Sie den Angriff auf das Monster
            character_attack = character.attack()  # Angriff des Spielers
        monster_health = monster.take_damage(character_attack)  # Das Monster erleidet Schaden
        print(f"Du greifst {monster.name} mit {character_attack} an.")
        print(f"{monster.name} hat noch {monster_health} Gesundheit.")
        if monster_health <= 0:
            print(f"{monster.name} wurde besiegt! Du hast gewonnen.")
            break
        # Das Monster kontert
        monster_attack = monster.attack()
        character_health = character.take_damage(monster_attack)
        print(f"{monster.name} kontert mit einem Angriff von {monster_attack}.")
        print(f"Deine Gesundheit: {character_health}")
        
        if character_health <= 0:
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
        
def heal(character, amount):
    character.health += amount
    if character.health > 100:
        character.health = 100
    print(f"{character.name} hat {amount} Gesundheit erhalten.")
    
def encounter(character, locations):
    current_location = locations.get(character['location'])

    if current_location.get('enemies'):
        print("Feindliche Charaktere nähern sich!")
        character['in_battle'] = True
        while character['in_battle']:
            # Überprüfen Sie, ob es noch lebende Feinde in der aktuellen Location gibt
            living_enemies = [enemy for enemy in current_location['enemies'] if isinstance(enemy, dict) and enemy['is_alive']]
            if not living_enemies:
                character['in_battle'] = False
                break  # Beenden Sie den Kampf, wenn keine lebenden Feinde mehr vorhanden sind
            pass  # Hier geht der Kampf weiter