import pygame

class Cell:
    def __init__(self, position, center_pos=(400, 300)):
        self.image = pygame.image.load("assets/images/uninfected_cell.png")

        # Resize the cell image to 10 times smaller
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 2.5, self.image.get_height() // 2.5))

        self.rect = self.image.get_rect()  # Simplified positioning for now
        # uninfected / infected
        self.state = True

        # Store the position of the cell
        self.position = position

        # Set initial position of the cell
        self.reposition(center_pos)

    def reposition(self, center_pos, spacing=15):
        row = [3, 5, 7, 7, 7, 5, 3]
        
        y_offset = -3.5 * spacing
        idx = 0 
        
        for i, count in enumerate(row):
            x_offset = -(count // 2) * spacing - 5
            for j in range(count):
                if idx == self.position:
                    self.rect.x = center_pos[0] + x_offset + j * spacing
                    self.rect.y = center_pos[1] + y_offset + i * spacing
                    return
                idx += 1

    def die(self):
        self.state = False
        self.image = pygame.image.load("assets/images/infected_cell.png")
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 2.5, self.image.get_height() // 2.5))

    def draw(self, screen):
        screen.blit(self.image, self.rect)