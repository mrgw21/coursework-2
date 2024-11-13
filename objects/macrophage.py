import pygame

class Macrophage:
    
    def __init__(self):
        self.image = pygame.image.load("assets/images/macrophage_placehoder.png")
        img = self.image
        self.image = pygame.transform.scale(img, (img.get_width() * 0.3, img.get_height() * 0.3))
        self.speed = 5
        self.rect = self.image.get_rect()
        self.rect.center = (300, 300)  # Initial position for windowed mode

    def reposition(self, screen_width, screen_height):
        if screen_width == 800 and screen_height == 600:
            self.rect.center = (300, 300)  # Windowed mode
        else:
            self.rect.center = (screen_width // 2 - 100, screen_height // 2)
    
    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
    
    def eat(self, pathogen):
        # Logic to "eat" an enemy, making the macrophage stronger
        if pathogen.alive == False:
            pathogen.alive = True
    
    def update(self):
        self.handle_input()
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)

