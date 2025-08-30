#1 
<<<<<<< deepsource-autofix-a7b9832d


        # Füge die Standardangriffe hinzu
        attacks["Biss"] = {"damage": level * 2, "description": "Ein kräftiger Biss."}
        attacks["Kratzer"] = {"damage": level * 3, "description": "Ein scharfer Kratzer mit den Pfoten."}
        attacks["Bellender Angriff"] = {"damage": level * 2, "description": "Ein lauter bellender Angriff."}
        attacks["Sprung"] = {"damage": level * 3, "description": "Ein mutiger Sprung auf den Feind."}

        # Attacks zufällig auswählen
        selected_attacks = random.sample(attacks.items(), 3)
        self.attacks = {}
        for attack in selected_attacks:
            self.attacks[attack[0]] = attack[1]

        return self.attacks

=======
    
>>>>>>> Refactoring