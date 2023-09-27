class Location:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.friends = []
        self.enemies = []

    def add_friend(self, character):
        self.friends.append(character)

    def add_enemy(self, character):
        self.enemies.append(character)
