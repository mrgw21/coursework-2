import pygame
import sys
import math
from objects import Cell

pygame.init()

# display
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("pathogen popup")

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
font = pygame.font.Font(None, 36)

class ClickPathogen(pygame.sprite.Sprite, Cell):  # Inherit from Cell
    def __init__(self, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        Cell.__init__(self, x, y)  # Initialize Cell
        self.image = pygame.image.load("assets/images/bacteria_placeholder.png")
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.target = (screen_width // 2, screen_height // 2)

    def update(self):
        # move to center
        dx, dy = self.target[0] - self.rect.centerx, self.target[1] - self.rect.centery
        distance = math.hypot(dx, dy)
        if distance > self.speed:
            dx, dy = dx / distance, dy / distance
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Image - popup
virus_popup_image = pygame.image.load("assets/introduction-materials/virusinfo.jpg").convert_alpha()
virus_popup_image = pygame.transform.scale(virus_popup_image, (200, 200))

bacteria_popup_image = pygame.image.load("assets/introduction-materials/bacteriainfo.jpg").convert_alpha()
bacteria_popup_image = pygame.transform.scale(bacteria_popup_image, (200, 200))

# show a popup
def show_popup(duration=2000):
    popup_start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - popup_start_time < duration:
        screen.fill(WHITE)
        # popup image
        popup_image_rect = virus_popup_image.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
        screen.blit(virus_popup_image, popup_image_rect)
        
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

clock = pygame.time.Clock()
pathogen = ClickPathogen(100, 100, speed=3)
all_sprites = pygame.sprite.Group(pathogen)

# Display message
background_text = "Click on the moving virus"
text_surface = font.render(background_text, True, BLACK)
text_rect = text_surface.get_rect(topleft=(10, 10))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if pathogen.is_clicked(event.pos):
                    show_popup()
        elif event.type == pygame.VIDEORESIZE:
            screen_width, screen_height = event.w, event.h

    # Update
    all_sprites.update()

    # Draw
    screen.fill(WHITE)
    all_sprites.draw(screen)
    screen.blit(text_surface, text_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()