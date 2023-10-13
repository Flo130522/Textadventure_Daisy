
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

def random_encounter(character):
    if random.random() < 0.5:
        encounter = random.choice(characters['enemies'])
        print(f"Du triffst auf {encounter['name']} und es kommt zu einem Kampf!")

        while is_alive(character) and is_alive(encounter):
            print("\nWas möchtest du im Kampf tun?")
            print("1. Angreifen")
            print("2. Verteidigen")
            print("3. Fliehen")
            battle_choice = input("Bitte wähle eine Option: ")

            if battle_choice == "1":
                damage_dealt = attack(character, encounter)
                print(f"Du greifst {encounter['name']} an und verursachst {damage_dealt} Schaden.")
                print(f"{encounter['name']} hat noch {encounter['health']} Gesundheit.")
                if not is_alive(encounter):
                    print(f"{encounter['name']} wurde besiegt! Du hast gewonnen.")
                    break
                else:
                    damage_taken = attack(encounter, character)
                    print(f"{encounter['name']} kontert und verursacht {damage_taken} Schaden.")
                    print(f"Deine Gesundheit: {character['health']}")
                    if not is_alive(character):
                        print(f"{encounter['name']} hat dich besiegt! Du hast verloren.")
                        break
            elif battle_choice == "2":
                # Hier könntest du die Verteidigung implementieren
                pass
            elif battle_choice == "3":
                print(f"Du fliehst aus dem Kampf gegen {encounter['name']}.")
                break
            else:
                print("Ungültige Option. Bitte wähle erneut.")
    else:
        if random.random() < 0.7:
            print("Du hast ein seltenes Item gefunden!")
            # Hier kannst du die Logik für das Finden von Items implementieren
            # Beispiel: find_item()
        else:
            print("Du entdeckst eine mysteriöse Höhle.")
            # Hier kannst du die Logik für das Entdecken einer Höhle implementieren
            # Beispiel: enter_cave()


if __name__ == "__main__":
    main()
