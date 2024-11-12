import pygame 
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Pathogen with Image")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Target settings (central cell area)
target_radius = 30
target_position = (WIDTH // 2, HEIGHT // 2)


class Pathogen:
    def __init__(self, x, y, speed, image_path):
        self.x = x
        self.y = y
        self.speed = speed
        self.infected = False
        self.image = pygame.image.load(image_path)  # Load the image
        self.image = pygame.transform.scale(self.image, (20, 20))  # Scale image to desired size

    def move_towards_target(self, target_x, target_y):
        if not self.infected:  # Only move if not yet infected
            dx, dy = target_x - self.x, target_y - self.y
            distance = math.hypot(dx, dy)
            if distance > target_radius:  # Move pathogen if it hasn't reached the target
                dx, dy = dx / distance, dy / distance  # Normalize vector
                self.x += dx * self.speed
                self.y += dy * self.speed
            else:
                self.infected = True  # Pathogen has infected the target

    def draw(self, screen):
        # Draw the pathogen image
        screen.blit(self.image, (int(self.x), int(self.y)))

# Game loop setup
pathogen = Pathogen(100, 100, 2, 'virus_placeholder.png')  # Replace 'pathogen.png' with your image path
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(WHITE)

    # Move and draw the pathogen
    pathogen.move_towards_target(*target_position)
    pathogen.draw(screen)

    # Draw the target (central cell group)
    pygame.draw.circle(screen, GREEN if not pathogen.infected else (255, 0, 0), target_position, target_radius)

    # Update the display
    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()