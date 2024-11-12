import pygame
from objects.cell import Cell
from objects.macrophage import Macrophage

class Level1:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.body_image = pygame.image.load('assets/images/body_placeholder.png')

        self.macrophage = Macrophage()
        self.cells = [Cell(i) for i in range(37)] 

        self.enemies = []

        self.spawn_timer = 0
        self.spawn_interval = 2000

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                """
                if event.type == pygame.FULLSCREEN:
                    pygame.display.flip()
                """
            self.screen.fill((255, 255, 255))
            self.clock.tick(60)
            self.draw()

    def spawn_enemy(self):
        if pygame.time.get_ticks() - self.spawn_timer > self.spawn_interval:
            if pygame.time.get_ticks() % 2 == 0:
                # Bacteria
                self.enemies.append(None)
            else:
                # Virus
                self.enemies.append(None)
            self.spawn_timer = pygame.time.get_ticks()
    
    def check_collisions(self):
        for enemy in self.enemies[:]:
            if self.macrophage.rect.colliderect(enemy.rect):
                self.macrophage.eat(enemy)
                self.enemies.remove(enemy)

            # Check if enemy reached the cells
            for cell in self.cells:
                if enemy.rect.colliderect(cell.rect):
                    cell.die()
                    self.enemies.remove(enemy)
                    break

    def draw(self):

        self.macrophage.update()

        img = self.body_image
        img = pygame.transform.scale(img, (img.get_width() * 0.32, img.get_height() * 0.32))
        body_rect = img.get_rect(center=(400, 300)) 
        self.screen.blit(img, body_rect)
        for cell in self.cells:
            cell.draw(self.screen)
        self.macrophage.draw(self.screen)
        pygame.display.flip()  # Update the screen with the new drawing