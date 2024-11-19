import pygame 
import math

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