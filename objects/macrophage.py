import pygame

class Macrophage:
    
    def __init__(self, screen_width, screen_height, sidebar_width=400):
        self.image = pygame.image.load("assets/images/macrophage_placeholder.png")
        img = self.image
        self.image = pygame.transform.scale(img, (img.get_width() * 0.4, img.get_height() * 0.4))
        self.speed = 5
        self.rect = self.image.get_rect()
        self.sidebar_width = sidebar_width
        self.set_initial_position(screen_width, screen_height, self.sidebar_width)
    
    def set_initial_position(self, screen_width, screen_height, sidebar_width):
        # Set the initial position, center x adjusted by -100
        game_width = screen_width - sidebar_width
        if sidebar_width == 400:
            center_x = self.sidebar_width + game_width // 2 - 100
        else:
            center_x = self.sidebar_width + game_width // 2 - 525
        center_y = screen_height // 2
        self.rect.center = (center_x, center_y)

    def reposition(self, screen_width, screen_height):
        self.set_initial_position(screen_width, screen_height)
    
    def handle_input(self, screen_width, screen_height, sidebar_width):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] and self.rect.top > 0:  # Move up
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.bottom < screen_height:  # Move down
            self.rect.y += self.speed
        if keys[pygame.K_a] and self.rect.left > sidebar_width:  # Move left, not crossing sidebar
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.right < screen_width:  # Move right
            self.rect.x += self.speed
    
    @staticmethod
    def eat(pathogen):
        if pathogen.alive == False:
            pathogen.alive = True
    
    def update(self, screen_width, screen_height, sidebar_width):
        self.handle_input(screen_width, screen_height, sidebar_width)
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)

