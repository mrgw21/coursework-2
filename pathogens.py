import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set up screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Multiple Pathogen Images Moving Towards Central Cell")

# Define colors
WHITE = (255, 255, 255)

# Central cell properties
center_x = SCREEN_WIDTH // 2
center_y = SCREEN_HEIGHT // 2

# Load pathogen images and scale them
pathogen_images = [
    pygame.transform.scale(pygame.image.load("bacteria_placeholder.png"), (30, 30)),
    pygame.transform.scale(pygame.image.load("macrophage_placehoder.png"), (30, 30)),
    pygame.transform.scale(pygame.image.load("virus_placeholder.png"), (30, 30))
]

# Load the central cell image and scale it
central_cell_image = pygame.transform.scale(pygame.image.load("cell.png"), (100, 100))

# Pathogen class
class Pathogen:
    def __init__(self):
        # Start at a random position on the screen
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)
        # Randomly select one of the three pathogen images
        self.image = random.choice(pathogen_images)
        self.speed = random.uniform(1, 3)

    def move_towards_center(self):
        # Calculate the direction vector towards the central cell
        dx = center_x - self.x
        dy = center_y - self.y
        distance = math.hypot(dx, dy)

        # Normalize the direction vector and update the position
        if distance != 0:
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed

    def draw(self, surface):
        # Draw the pathogen image on the screen
        surface.blit(self.image, (int(self.x), int(self.y)))

# Create a list of pathogens
num_pathogens = 20
pathogens = [Pathogen() for _ in range(num_pathogens)]

# Main game loop flag
running = True
clock = pygame.time.Clock()

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with a white background
    screen.fill(WHITE)

    # Draw the central cell image
    screen.blit(central_cell_image, (center_x - 50, center_y - 50))

    # Move and draw each pathogen
    for pathogen in pathogens:
        pathogen.move_towards_center()
        pathogen.draw(screen)

    # Update the display
    pygame.display.flip()
    clock.tick(60)  # Cap the frame rate at 60 FPS

# Quit Pygame
pygame.quit()