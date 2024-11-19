import pygame 
import math

"""
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
"""

# Target settings (central cell area)
class Pathogen:
    def __init__(self, x, y, type, screen_width=800, screen_height=600):
        self.x = x
        self.y = y
        self.speed = 2
        self.alive = False
        self.type = type

        if self.type == "bacteria":
            self.image = pygame.image.load("assets/images/bacteria_placeholder.png")
        else:
            self.image = pygame.image.load("assets/images/virus_placeholder.png")
        
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        self.adjust_initial_position(screen_width, screen_height)

    def adjust_initial_position(self, screen_width, screen_height):
        if screen_width != 800 or screen_height != 600:
            self.rect.x = screen_width // 2 + (self.rect.x - 400)
            self.rect.y = screen_height // 2 + (self.rect.y - 300)

    def move_towards_target(self, center_x, center_y, cell=None):
        if not self.alive:
            dx, dy = center_x - self.x, center_y - self.y
            distance = math.hypot(dx, dy)
            if distance > 30:
                dx, dy = dx / distance, dy / distance
                self.x += dx * self.speed
                self.y += dy * self.speed
                self.rect.center = (self.x, self.y)
            else:
                self.alive = True
                if cell:
                    cell.die()
                return True
        return False

    def draw(self, screen):
        if not self.alive:
            screen.blit(self.image, self.rect)
    
    def reposition(self, width_ratio, height_ratio):
        self.rect.centerx = int(self.rect.centerx * width_ratio)
        self.rect.centery = int(self.rect.centery * height_ratio)


"""
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
    pygame.draw.circle(screen, GREEN if not pathogen.alive else (255, 0, 0), target_position, target_radius)

    # Update the display
    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()
"""
