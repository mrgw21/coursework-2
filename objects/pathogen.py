import pygame
import math

class Pathogen:
    def __init__(self, x, y, type, screen_width=None, screen_height=None):
        self.x = x
        self.y = y
        self.speed = 2
        self.alive = False
        self.type = type

        # Set target cell and attack timer
        self.target_cell = None
        self.attack_timer = 0  # For delayed attacks

        if self.type == "bacteria":
            self.image = pygame.image.load("assets/images/bacteria_placeholder.png")
        else:
            self.image = pygame.image.load("assets/images/virus_placeholder.png")
        
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        # Adjust initial position dynamically based on screen dimensions
        if screen_width and screen_height:
            self.adjust_initial_position(screen_width, screen_height)

    def adjust_initial_position(self, screen_width, screen_height):
        # Centerize position dynamically based on current screen size
        self.rect.x = screen_width // 2 + (self.rect.x - screen_width // 2)
        self.rect.y = screen_height // 2 + (self.rect.y - screen_height // 2)

    def move_towards_target(self, center_x, center_y, cell=None):
        if not self.alive:
            target_x, target_y = (cell.rect.center if cell else (center_x, center_y))

            dx, dy = target_x - self.x, target_y - self.y
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

    def attack_infected_cell(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.attack_timer > 1500:  # Attack delay of 1.5 seconds
            self.attack_timer = current_time  # Reset the attack timer
            return True
        return False

    def draw(self, screen):
        if not self.alive:
            screen.blit(self.image, self.rect)
    
    def reposition(self, width_ratio, height_ratio):
        # Dynamically adjust position based on screen resize ratios
        self.rect.centerx = int(self.rect.centerx * width_ratio)
        self.rect.centery = int(self.rect.centery * height_ratio)