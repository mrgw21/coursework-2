import pygame

class Cell:
    def __init__(self, position, center_pos=(400, 300), spacing=15):
        self.image = pygame.image.load("assets/images/uninfected_cell.png")

        # Resize the cell image to 10 times smaller
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 2.5, self.image.get_height() // 2.5))

        self.rect = self.image.get_rect()  # Simplified positioning for now
        self.alive = True
         

        # Diamond positioning
        row = [3, 5, 7, 7, 7, 5, 3]  # Number of cells in each row
        total_rows = len(row)
        
        # Calculate the top-left starting offset for the diamond pattern
        y_offset = -3.5 * spacing # Start the top row at -4*spacing from the center vertically

        idx = 0  # Track the cell index
        
        for i, count in enumerate(row):
            x_offset = -(count // 2) * spacing - 5  # Center each row horizontally
            for j in range(count):
                if idx == position:
                    # Center each cell in the diamond pattern around center_pos
                    self.rect.x = center_pos[0] + x_offset + j * spacing
                    self.rect.y = center_pos[1] + y_offset + i * spacing
                    return
                idx += 1



    def die(self):
        self.alive = False
        self.image = pygame.image.load("assets/images/infected_cell.png")


    def draw(self, screen):
        if self.alive:
            screen.blit(self.image, self.rect)