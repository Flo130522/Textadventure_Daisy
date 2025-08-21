from Klassen.Character import *
from Klassen.Monsters import *
from Klassen.item import *
from Klassen.Game import *


class Location:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.friends = []
        self.enemies = []
        self.hidden_location= []

    def add_friend(self, character):
        self.friends.append(character)

    def add_enemy(self, character):
        self.enemies.append(character)

    def initialize_locations():
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

    def explore_location(self):
        """
        Erkundet den aktuellen Ort und führt Ereignisse aus.
        """
        print(
            f"Du erkundest {self.name}: {self.description}")

        # Überprüfe, ob es Feinde gibt
        if self.enemies:
            print("Feinde nähern sich!")
            self.start_battle(self.current_character.team,
                              self.enemies)
        else:
            print("Es gibt keine Feinde hier.")

        # Überprüfe, ob es Gegenstände gibt
        if self.current_character.items:
            print("Du findest Gegenstände:")
            for item in self.items:
                print(f"- {item.name}: {item.description}")
            self.current_character.add_items(self.items)
            self.items = []  # Entferne die aufgesammelten Gegenstände

        # Überprüfe, ob es versteckte Orte gibt
        if self.hidden_locations:
            print("Du entdeckst versteckte Orte:")
            for location_name in self.hidden_locations:
                print(f"- {location_name}")
            hidden_location_choice = input(
                "Möchtest du einen versteckten Ort erkunden? (Ja/Nein): ")
            if hidden_location_choice.lower() == "ja":
                self.explore_hidden_location()

    def explore_hidden_location(self):
        """
        Erkundet einen versteckten Ort und führt Ereignisse aus.

        Args:
            current_location (Location): Der aktuelle Ort, der den versteckten Ort enthält.
        """
        hidden_location_name = input(
            "Gib den Namen des versteckten Ortes ein, den du erkunden möchtest: ")
        if hidden_location_name in self.hidden_locations:
            hidden_location = self.locations[hidden_location_name]
            print(
                f"Du erkundest den versteckten Ort {hidden_location.name}: {hidden_location.description}")

            # Überprüfe, ob es Feinde gibt
            if hidden_location.enemies:
                print("Feinde nähern sich!")
                self.start_battle(self.current_character.team,
                                  hidden_location.enemies)
            else:
                print("Es gibt keine Feinde hier.")

            # Überprüfe, ob es Gegenstände gibt
            if hidden_location.items:
                print("Du findest Gegenstände:")
                for item in hidden_location.items:
                    print(f"- {item.name}: {item.description}")
                self.current_character.add_items(hidden_location.items)
                hidden_location.items = []  # Entferne die aufgesammelten Gegenstände
        else:
            print(
                "Ungültiger Ort. Bitte gib den Namen eines versteckten Ortes ein, den du erkunden möchtest.")
