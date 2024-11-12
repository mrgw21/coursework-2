import pygame
import random
from objects.cell import Cell
from objects.macrophage import Macrophage
from objects.pathogen import Pathogen

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
        self.counter = 0
    

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

            self.spawn_enemy()
        
            self.macrophage.update()
            self.draw()

            if self.counter < len(self.cells):
                for enemy in self.enemies:
                    if enemy.move_towards_target(400, 300, self.cells[self.counter]):
                        self.counter += 1

            self.check_collisions() 

    
    def generate_spawn_location(self):
        side_pick = random.randint(1, 4)

        if side_pick == 1:
            x = random.randint(0, 800)
            y = random.randint(1, 10)
            return [x, y]
        elif side_pick == 2:
            x = random.randint(1, 10)
            y = random.randint(0, 600)
            return [x, y]
        elif side_pick == 3:
            x = random.randint(0, 800)
            y = random.randint(590, 600)
            return [x, y]
        else:
            x = random.randint(790, 800)
            y = random.randint(0, 600)
            return [x, y]

    def spawn_enemy(self):
        if pygame.time.get_ticks() - self.spawn_timer > self.spawn_interval:
            spawn_location = self.generate_spawn_location()
            if pygame.time.get_ticks() % 2 == 0:
                # Bacteria
                self.enemies.append(Pathogen(spawn_location[0], spawn_location[1], "bacteria"))
            else:
                # Virus
                self.enemies.append(Pathogen(spawn_location[0], spawn_location[1], "virus"))
            self.spawn_timer = pygame.time.get_ticks()
    
    def check_collisions(self):

        for enemy in self.enemies[:]:
            if self.macrophage.rect.colliderect(enemy.rect):
                self.enemies.remove(enemy)

            # Check if enemy reached the cells
            for cell in self.cells:
                if enemy.rect.colliderect(cell.rect) and cell.alive:
                    cell.die()
                    self.enemies.remove(enemy)
                    break

    def draw(self):   

        img = self.body_image
        img = pygame.transform.scale(img, (img.get_width() * 0.32, img.get_height() * 0.32))
        body_rect = img.get_rect(center=(400, 300)) 

        self.screen.blit(img, body_rect)
        
        for cell in self.cells:
            cell.draw(self.screen)

        self.macrophage.draw(self.screen)

        for enemy in self.enemies:
            enemy.draw(self.screen)
        pygame.display.flip()  # Update the screen with the new drawing