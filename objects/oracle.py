import pygame

class Oracle:
    def __init__(self, sidebar_width):
        # Load Oracle images
        self.image_default = pygame.image.load("assets/images/dr_tomato.png")  # Default image
        self.image_hover = pygame.image.load("assets/images/dr_tomato.png")  # Hover image
        self.image_click = pygame.image.load("assets/images/dr_tomato.png")  # Click image
        self.image = pygame.transform.scale(self.image_default, (400, 400))  # Adjusted size
        self.rect = self.image.get_rect()

        # Sidebar reference for positioning
        self.sidebar_width = sidebar_width

        # Initialize modal properties
        self.modal_rect = pygame.Rect(0, 0, 400, 400)  # Modal dimensions: 600x600
        self.show_modal = False

        # Set Oracle's initial position and modal position
        self.set_position()

    def set_position(self):
        # Adjust Oracle position within the sidebar
        screen_height = pygame.display.get_surface().get_height()
        self.rect.bottom = screen_height - 20  # Margin from the bottom
        self.rect.x = self.sidebar_width // 2 - self.rect.width // 2  # Center horizontally in sidebar

        # Dynamically position modal (top right of Oracle)
        self.modal_rect.topleft = (
            self.rect.right + 10,  # Slight padding to the right of Oracle
            self.rect.top - self.modal_rect.height // 2  # Align modal top-right
        )

    def draw(self, screen):
        # Draw Oracle image
        screen.blit(self.image, self.rect)

        # Draw modal if active
        if self.show_modal:
            pygame.draw.rect(screen, (220, 220, 220), self.modal_rect)  # White background
            pygame.draw.rect(screen, (0, 0, 0), self.modal_rect, 3)    # Black border

    def handle_hover(self, mouse_pos):
        # Change image to hover state if mouse is over Oracle
        if self.rect.collidepoint(mouse_pos):
            self.image = pygame.transform.scale(self.image_hover, (400, 400))
        else:
            self.image = pygame.transform.scale(self.image_default, (400, 400))

    def handle_click(self, mouse_pos):
        # Change image to click state and toggle modal visibility
        if self.rect.collidepoint(mouse_pos):
            self.image = pygame.transform.scale(self.image_click, (400, 400))
            self.show_modal = not self.show_modal  # Toggle modal visibility

    def reset_image(self):
        # Reset to default image after a click
        self.image = pygame.transform.scale(self.image_default, (400, 400))