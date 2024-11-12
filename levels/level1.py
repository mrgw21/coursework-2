import pygame

class Level1:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.body_image = pygame.image.load('assets/images/body_placeholder.png')  

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                """
                if event.type == pygame.FULLSCREEN:
                    pygame.display.flip()
                """
            self.screen.fill((0, 0, 0))
            self.clock.tick(60)
            self.draw()
    
    def draw(self):
        # Get the rect for positioning the image (you can adjust position and size here)
        # Center the image at (400, 300)
        
        # Blit the image to the screen at the given position
        img = self.body_image
        img = pygame.transform.scale(img, (img.get_width() * 0.3, img.get_height() * 0.3))
        body_rect = img.get_rect(center=(400, 300)) 
        self.screen.blit(img, body_rect)
        pygame.display.flip()  # Update the screen with the new drawing