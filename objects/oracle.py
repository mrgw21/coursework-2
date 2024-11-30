import pygame

class Oracle:
    def __init__(self, sidebar_width):
        # Load Oracle images
        self.image_default = pygame.image.load("assets/images/dr_tomato.png")  # Default image
        self.image_hover = pygame.image.load("assets/images/dr_tomato.png")  # Hover image
        self.image_click = pygame.image.load("assets/images/dr_tomato.png")  # Click image
        self.image = pygame.transform.scale(self.image_default, (250, 200))  # Adjusted size
        self.rect = self.image.get_rect()

        # Sidebar reference for positioning
        self.sidebar_width = sidebar_width

        # Initialize modal properties
        self.modal_rect = pygame.Rect(0, 0, 400, 300)  # Modal dimensions: 600x600
        self.show_modal = False

        # Set Oracle's initial position and modal position
        self.set_position()

        # Initialize message attributes
        self.message_surface = None
        self.message_rect = None
        self.message_bg_rect = None  # Background rect for the message
        self.font = pygame.font.SysFont("Arial", 24)  # Font for messages
        self.message = ""  # Default empty message

    def set_position(self):
        # Adjust Oracle position within the sidebar
        screen_height = pygame.display.get_surface().get_height()
        self.rect.bottom = screen_height - 20  # Margin from the bottom
        self.rect.x = self.sidebar_width // 2 - self.rect.width // 2  # Center horizontally in sidebar

        # Dynamically position modal (top right of Oracle)
        self.modal_rect.topleft = (
            self.rect.right + 10,  # Slight padding to the right of Oracle
            self.rect.top - self.modal_rect.height  # Align modal top-right
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
            self.image = pygame.transform.scale(self.image_hover, (250, 200))
        else:
            self.image = pygame.transform.scale(self.image_default, (250, 200))

    def handle_click(self, mouse_pos, cells, level):
        if any(cell.show_modal for cell in cells):
            return
        # Change image to click state and toggle modal visibility
        if self.rect.collidepoint(mouse_pos):
            self.image = pygame.transform.scale(self.image_click, (250, 200))
            self.show_modal = not self.show_modal  # Toggle modal visibility

            # Pause the game if Oracle's modal is opened
            if self.show_modal:
                level.paused = True
            else:
                level.paused = False

    def reset_image(self):
        # Reset to default image after a click
        self.image = pygame.transform.scale(self.image_default, (250, 200))

    def display_message(self, message, screen):
        self.message = message

        # Create the text surface
        self.message_surface = self.font.render(self.message, True, (0, 0, 0))  # Black text
        self.message_rect = self.message_surface.get_rect()
        
        # Position the text above the Oracle
        self.message_rect.topleft = (self.rect.x - 40, self.rect.top - 35)  # Display above Oracle

        # Create an oval background shape for the message
        padding = 30  # Padding around the text
        self.message_bg_rect = pygame.Rect(
            self.message_rect.x - padding,  # Left side with padding
            self.message_rect.y - padding,  # Top side with padding
            self.message_rect.width + padding * 2,  # Width with padding
            self.message_rect.height + padding * 2  # Height with padding
        )

    def draw_message(self, screen):
        if self.message_surface and self.message_bg_rect:
            # Draw the message background
            pygame.draw.ellipse(screen, (255, 255, 255), self.message_bg_rect)  # White background
            pygame.draw.ellipse(screen, (0, 0, 0), self.message_bg_rect, 2)  # Black border

            # Draw the message text
            screen.blit(self.message_surface, self.message_rect)