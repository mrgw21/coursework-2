import pygame

class HomeScreen:
    def __init__(self, screen, manager):
        self.screen = screen
        self.manager = manager
        self.running = True

        # Colors
        self.WHITE = (255, 255, 255)
        self.GRAY = (200, 200, 200)
        self.BLACK = (0, 0, 0)
        self.BLUE = (100, 149, 237)

        # Fonts
        self.font = pygame.font.SysFont("Arial", 36)
        self.title_font = pygame.font.SysFont("Arial", 72, bold=True)

        # Background image
        self.background_image = pygame.image.load("assets/images/homebg2.webp").convert()
        self.background_image = pygame.transform.scale(self.background_image, screen.get_size())

        # Buttons with their corresponding options mapped to registered screens
        self.buttons = {
            "Levels": {
                "rect": pygame.Rect(screen.get_width() // 2 - 100, screen.get_height() // 3 - 50, 200, 50),
                "color": self.GRAY,
                "options": ["Introduction", "Level 1"]
            },
            "Scoreboard": {
                "rect": pygame.Rect(screen.get_width() // 2 - 100, screen.get_height() // 3 + 100, 200, 50),
                "color": self.GRAY,
                "options": ["Scoreboard"]#Removed statistics option
            }
        }

        self.current_menu = None  # Track which menu is open

    def reposition_elements(self):
        screen_width, screen_height = self.screen.get_size()

        # Rescale background
        self.background_image = pygame.transform.scale(self.background_image, (screen_width, screen_height))

        # Adjust button positions dynamically
        self.buttons["Levels"]["rect"] = pygame.Rect(
            screen_width // 2 - 100, screen_height // 3 - 50, 200, 50
        )
        self.buttons["Scoreboard"]["rect"] = pygame.Rect(
            screen_width // 2 - 100, screen_height // 3 + 100, 200, 50
        )

    def draw_button(self, button_text, rect, color):
        pygame.draw.rect(self.screen, color, rect)
        text_surface = self.font.render(button_text, True, self.BLACK)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)

    def draw_background(self):
        self.screen.blit(self.background_image, (0, 0))

    def draw_main_buttons(self):
        for button_text, button_data in self.buttons.items():
            self.draw_button(button_text, button_data["rect"], button_data["color"])

    def draw_sub_options(self):
        if self.current_menu:
            options = self.buttons[self.current_menu]["options"]
            for i, option in enumerate(options):
                option_rect = pygame.Rect(self.screen.get_width() // 2 - 150,
                                          self.screen.get_height() // 3 + 200 + i * 50,
                                          300, 40)
                pygame.draw.rect(self.screen, self.BLUE, option_rect)
                option_text = self.font.render(option, True, self.WHITE)
                option_text_rect = option_text.get_rect(center=option_rect.center)
                self.screen.blit(option_text, option_text_rect)

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
            mouse_pos = event.pos
            for button_text, button_data in self.buttons.items():
                if button_data["rect"].collidepoint(mouse_pos):
                    if self.current_menu == button_text:
                        self.current_menu = None
                    else:
                        self.current_menu = button_text
            if self.current_menu:
                options = self.buttons[self.current_menu]["options"]
                for i, option in enumerate(options):
                    option_rect = pygame.Rect(self.screen.get_width() // 2 - 150,
                                              self.screen.get_height() // 3 + 200 + i * 50,
                                              300, 40)
                    if option_rect.collidepoint(mouse_pos):
                        self.manager.set_active_screen(option)
                        self.running = False  # Exit the loop and hand over to the next screen

    def draw_text(self, text, font, color, x, y):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)
    
    def draw(self):
        self.run()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)

            self.draw_background()
            self.draw_text("Welcome to Inside Immune!", self.title_font, self.BLACK, self.screen.get_width() // 2, 50)
            self.draw_text("Choose an option below:", self.font, self.BLACK, self.screen.get_width() // 2, 120)
            self.draw_main_buttons()
            self.draw_sub_options()

            pygame.display.flip()