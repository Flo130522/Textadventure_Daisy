import random
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
