import pygame

class Macrophage:
    
    def __init__(self, screen_width, screen_height):
        self.image = pygame.image.load("assets/images/macrophage_placeholder.png")
        img = self.image
        self.image = pygame.transform.scale(img, (img.get_width() * 0.4, img.get_height() * 0.4))
        self.speed = 5
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2 - 100, screen_height // 2)

    def reposition(self, screen_width, screen_height):
        if screen_width == 800 and screen_height == 600:
            self.rect.center = (300, 300)
        else:
            self.rect.center = (screen_width // 2 - 100, screen_height // 2)
    
    def handle_input(self, screen_width, screen_height):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.bottom < screen_height:
            self.rect.y += self.speed
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.right < screen_width:
            self.rect.x += self.speed
    
    def eat(self, pathogen):
        # Logic to "eat" an enemy, making the macrophage stronger
        if pathogen.alive == False:
            pathogen.alive = True
    
    def update(self, screen_width, screen_height):
        self.handle_input(screen_width, screen_height)
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)

