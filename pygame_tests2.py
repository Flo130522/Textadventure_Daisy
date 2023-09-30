import pygame
import sys

# Initialisiere Pygame
pygame.init()

# Bildschirmgröße und -titel
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Textadventure mit Pygame')

# Farben
black = (0, 0, 0)
white = (255, 255, 255)

# Schriftart und Schriftgröße
font = pygame.font.Font(None, 36)

# Variablen für den Spielzustand
current_room = "start"

# Spielzustände und Handlungsoptionen
rooms = {
    "start": {
        "description": "Du befindest dich in einem dunklen Raum. Vor dir siehst du zwei Türen. Welche nimmst du?",
        "options": {
            "links": "Gehe zur linken Tür",
            "rechts": "Gehe zur rechten Tür"
        }
    },
    "links": {
        "description": "Du betrittst einen schmalen Flur. Vor dir liegt eine Schatztruhe.",
        "options": {
            "öffne Truhe": "Du findest einen Schlüssel.",
            "zurück": "Gehe zurück in den dunklen Raum."
        }
    },
    "rechts": {
        "description": "Du stehst vor einem Abgrund. Du kannst nicht weitergehen.",
        "options": {
            "zurück": "Gehe zurück in den dunklen Raum."
        }
    }
}

# Hauptspiel-Schleife
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    current_room_data = rooms[current_room]
    description_text = font.render(current_room_data["description"], True, white)
    option_texts = [font.render(f"{option}: {description}", True, white) for option, description in current_room_data["options"].items()]

    screen.fill(black)
    screen.blit(description_text, (20, 20))
    for i, option_text in enumerate(option_texts):
        screen.blit(option_text, (20, 100 + i * 40))

    pygame.display.update()
