import pygame
import sys
import math

pygame.init()

#display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("pathogen popup")

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
font = pygame.font.Font(None, 36)

class ClickPathogen(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)  # Transparent surface
        pygame.draw.circle(self.image, RED, (25, 25), 25)  # Draw a red circle
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.target = (WIDTH // 2, HEIGHT // 2)

    def update(self):
        # Move toward the target (center of the screen)
        dx, dy = self.target[0] - self.rect.centerx, self.target[1] - self.rect.centery
        distance = math.hypot(dx, dy)
        if distance > self.speed:  # Avoid jittering when close
            dx, dy = dx / distance, dy / distance  # Normalize
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Function to show a popup message
def show_popup(message, duration=2000):
    popup_start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - popup_start_time < duration:
        screen.fill(WHITE)
        
        # Draw popup box
        popup_rect = pygame.Rect(WIDTH // 4, HEIGHT // 3, WIDTH // 2, HEIGHT // 3)
        pygame.draw.rect(screen, BLACK, popup_rect)
        pygame.draw.rect(screen, WHITE, popup_rect, 3)
        
        # PopUptext
        text = font.render(message, True, WHITE)
        text_rect = text.get_rect(center=popup_rect.center)
        screen.blit(text, text_rect)
        
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

clock = pygame.time.Clock()
pathogen = ClickPathogen(100, 100, speed=3)
all_sprites = pygame.sprite.Group(pathogen)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if pathogen.is_clicked(event.pos):
                    show_popup("Congo you have clicked a virus.", duration=2000)

    # Update
    all_sprites.update()

    # Draw
    screen.fill(WHITE)
    all_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()