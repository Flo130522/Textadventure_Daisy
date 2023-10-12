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