import pygame

class Macrophage:
    
    def __init__(self):
        self.image = pygame.image.load("assets/images/macrophage_placehoder.png")
        img = self.image
        self.image = pygame.transform.scale(img, (img.get_width() * 0.3, img.get_height() * 0.3))
        self.speed = 5
        self.rect = self.image.get_rect()  # Get the rect of the image
        self.rect.center = (300, 350)  # Set the center to the desired position
        # self.strength = 0
    
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