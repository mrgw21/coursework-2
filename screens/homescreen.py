import pygame
import sys

class HomeScreen:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Screen dimensions
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("INSIDE IMMUNE")

        # Colors
        self.WHITE = (255, 255, 255)
        self.GRAY = (200, 200, 200)
        self.BLACK = (0, 0, 0)
        self.BLUE = (100, 149, 237)

        # Fonts
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 72)

        # Background image
        self.background_image = pygame.image.load("../assets/images/homebg2.webp").convert()
        self.background_image = pygame.transform.scale(self.background_image, (self.WIDTH, self.HEIGHT))

        # Buttons
        self.buttons = {
            "Levels": {"rect": pygame.Rect(self.WIDTH // 2 - 100, self.HEIGHT // 3 - 50, 200, 50), "color": self.GRAY,
                       "options": ["Introduction 1", "Level 1", "Introduction 2", "Level 2"]},
            "Scoreboard": {"rect": pygame.Rect(self.WIDTH // 2 - 100, self.HEIGHT // 3 + 100, 200, 50), "color": self.GRAY,
                           "options": ["Statistics", "Scoreboard"]}
        }

        # Track which menu is open
        self.current_menu = None

    def draw_button(self, button_text, rect, color):
        """Draw a button with text."""
        pygame.draw.rect(self.screen, color, rect)
        text_surface = self.font.render(button_text, True, self.BLACK)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)

    def draw_background(self):
        """Draw the background image."""
        self.screen.blit(self.background_image, (0, 0))

    def draw_main_buttons(self):
        """Draw the main menu buttons."""
        for button_text, button_data in self.buttons.items():
            self.draw_button(button_text, button_data["rect"], button_data["color"])

    def draw_sub_options(self):
        """Draw sub-options for the current menu."""
        if self.current_menu:
            options = self.buttons[self.current_menu]["options"]
            for i, option in enumerate(options):
                option_rect = pygame.Rect(self.WIDTH // 2 - 150, self.HEIGHT // 3 + 200 + i * 50, 300, 40)
                pygame.draw.rect(self.screen, self.BLUE, option_rect)
                option_text = self.font.render(option, True, self.WHITE)
                option_text_rect = option_text.get_rect(center=option_rect.center)
                self.screen.blit(option_text, option_text_rect)

    def draw_text(self, text, font, color, x, y):
        """Draw text on the screen."""
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)

    def handle_events(self):
        """Handle events such as button clicks."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                mouse_pos = event.pos

                # Check for main button clicks
                for button_text, button_data in self.buttons.items():
                    if button_data["rect"].collidepoint(mouse_pos):
                        if self.current_menu == button_text:
                            self.current_menu = None  # Close menu if clicked again
                        else:
                            self.current_menu = button_text

                # Check for sub-option clicks if a menu is open
                if self.current_menu:
                    options = self.buttons[self.current_menu]["options"]
                    for i, option in enumerate(options):
                        option_rect = pygame.Rect(self.WIDTH // 2 - 150, self.HEIGHT // 3 + 200 + i * 50, 300, 40)
                        if option_rect.collidepoint(mouse_pos):
                            print(f"Selected: {option}")

    def run(self):
        """Main loop for the home screen."""
        while True:
            self.handle_events()

            # Draw everything
            self.draw_background()
            self.draw_text("Welcome to the Game!", self.title_font, self.BLACK, self.WIDTH // 2, 50)
            self.draw_text("Choose an option below:", self.font, self.BLACK, self.WIDTH // 2, 120)
            self.draw_main_buttons()
            self.draw_sub_options()

            pygame.display.flip()

# Main execution
if __name__ == "__main__":
    home_screen = HomeScreen()
    home_screen.run()