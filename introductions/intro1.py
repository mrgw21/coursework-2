import pygame   
# image = pygame.image.load("assets/backgrounds/control_screen.png").convert()
# WIDTH, HEIGHT = 0, 0  # Replace with your desired screen dimensions
# image = pygame.transform.scale(image, (WIDTH, HEIGHT))
class Intro1:
    def __init__(self, screen, pdf_images):
        self.screen = screen
        self.next_screen = None
        
        self.pdf_images = pdf_images
        self.current_page = 0
        self.running = True

        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)

        # Fonts
        self.TITLE_FONT = pygame.font.Font(None, 80)
        self.TEXT_FONT = pygame.font.Font(None, 40)

        # Load and resize icons (15x smaller)
        self.left_arrow = pygame.transform.scale(
            pygame.image.load("assets/icons/arrow-left.png"), 
            (pygame.image.load("assets/icons/arrow-left.png").get_width() // 15, 
            pygame.image.load("assets/icons/arrow-left.png").get_height() // 15)
        )
        self.right_arrow = pygame.transform.scale(
            pygame.image.load("assets/icons/arrow-right.png"), 
            (pygame.image.load("assets/icons/arrow-right.png").get_width() // 15, 
            pygame.image.load("assets/icons/arrow-right.png").get_height() // 15)
        )
        self.enter_icon = pygame.transform.scale(
            pygame.image.load("assets/icons/computer.png"), 
            (pygame.image.load("assets/icons/computer.png").get_width() // 15, 
            pygame.image.load("assets/icons/computer.png").get_height() // 15)
        )

    def run(self):
        clock = pygame.time.Clock()

        while self.running:
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            self.handle_events(events)
            self.screen.fill(self.WHITE)  # Clear the screen
            self.draw(self.screen)

            # Update the display
            pygame.display.flip()
            clock.tick(60)
        
        if self.next_screen == "control":
            self.run_control_screen()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    # Go to the next page
                    if self.current_page < len(self.pdf_images) - 1:
                        self.current_page += 1
                elif event.key == pygame.K_LEFT:
                    # Go to the previous page
                    if self.current_page > 0:
                        self.current_page -= 1
                elif event.key == pygame.K_RETURN and self.current_page == len(self.pdf_images) - 1:
                    # Transition to the Control Screen
                    self.running = False
                    self.next_screen = "control"

    def draw(self, surface):
        # Get the screen dimensions
        screen_width = surface.get_width()
        screen_height = surface.get_height()

        # Scale the current image to fit the full screen
        scaled_image = pygame.transform.scale(self.pdf_images[self.current_page], (screen_width, screen_height))
        surface.blit(scaled_image, (0, 0))

        # Set the y-position for the guidance text and icons
        text_y_position = screen_height - 22  # Adjust this value for spacing from the bottom

        # Draw guidance arrows and text
        if self.current_page == len(self.pdf_images) - 1:  # Last page
            # Text: "Press [icon] to return to tutorial. Press [icon] to play game!"
            self.draw_text_with_two_texts_and_icons(
                "Press",
                self.left_arrow,
                "to return to tutorial. Press RETURN/ENTER",
                self.enter_icon,
                "to play game!",
                surface,
                screen_width // 2,
                text_y_position,
                spacing=10
            )
        elif self.current_page == 0:  # First page
            # Text: "Press [icon] to continue."
            self.draw_text_with_icon_and_following_text(
                "Press right arrow",
                self.right_arrow,
                "to continue.",
                surface,
                screen_width // 2,
                text_y_position
            )
        else:  # Middle pages
            # Text: "Press [icon1] [icon2] to navigate."
            self.draw_text_with_two_icons_and_following_text(
                "Use arrows",
                self.left_arrow,
                self.right_arrow,
                "to navigate.",
                surface,
                screen_width // 2,
                text_y_position,
                spacing=10
            )

    def draw_text_with_icon_and_following_text(self, text, icon, following_text, surface, x, y):
        """Draws text with a single icon followed by more text."""
        # Render the first part of the text
        text_obj = self.TEXT_FONT.render(text, True, self.BLACK)
        text_rect = text_obj.get_rect(midright=(x - 10, y))  # Adjust position to the left of the icon

        # Resize icon and set its position
        icon_rect = icon.get_rect(midleft=(x, y))

        # Render the following text
        following_text_obj = self.TEXT_FONT.render(following_text, True, self.BLACK)
        following_text_rect = following_text_obj.get_rect(midleft=(icon_rect.right + 10, y))

        # Draw text, icon, and following text
        surface.blit(text_obj, text_rect)
        surface.blit(icon, icon_rect)
        surface.blit(following_text_obj, following_text_rect)

    def draw_text_with_two_icons_and_following_text(self, text, icon1, icon2, following_text, surface, x, y, spacing=20):
        # Render the first part of the text
        text_obj = self.TEXT_FONT.render(text, True, self.BLACK)
        text_rect = text_obj.get_rect(midright=(x - 60, y))  # Adjust position for the first icon

        # Resize and position the icons
        icon1_rect = icon1.get_rect(midleft=(x - 50, y))
        icon2_rect = icon2.get_rect(midleft=(icon1_rect.right + spacing, y))

        # Render the following text
        following_text_obj = self.TEXT_FONT.render(following_text, True, self.BLACK)
        following_text_rect = following_text_obj.get_rect(midleft=(icon2_rect.right + spacing, y))

        # Draw text, icons, and following text
        surface.blit(text_obj, text_rect)
        surface.blit(icon1, icon1_rect)
        surface.blit(icon2, icon2_rect)
        surface.blit(following_text_obj, following_text_rect)

    def draw_text_with_two_texts_and_icons(self, text1, icon1, text2, icon2, text3, surface, x, y, spacing=10):
        # Render the first part of the text
        text1_obj = self.TEXT_FONT.render(text1, True, self.BLACK)
        text1_rect = text1_obj.get_rect(midright=(x - 380, y))

        # Position the first icon
        icon1_rect = icon1.get_rect(midleft=(text1_rect.right + spacing, y))

        # Render the second part of the text
        text2_obj = self.TEXT_FONT.render(text2, True, self.BLACK)
        text2_rect = text2_obj.get_rect(midleft=(icon1_rect.right + spacing, y))

        # Position the second icon
        icon2_rect = icon2.get_rect(midleft=(text2_rect.right + spacing, y))

        # Render the third part of the text
        text3_obj = self.TEXT_FONT.render(text3, True, self.BLACK)
        text3_rect = text3_obj.get_rect(midleft=(icon2_rect.right + spacing, y))

        # Draw all elements
        surface.blit(text1_obj, text1_rect)
        surface.blit(icon1, icon1_rect)
        surface.blit(text2_obj, text2_rect)
        surface.blit(icon2, icon2_rect)
        surface.blit(text3_obj, text3_rect)

    @staticmethod
    def draw_text(text, font, color, surface, x, y):
        text_obj = font.render(text, True, color)
        text_rect = text_obj.get_rect(center=(x, y))
        surface.blit(text_obj, text_rect)

    @staticmethod
    def run_control_screen():
        screen = pygame.display.get_surface()
        clock = pygame.time.Clock()
        running = True
        next_screen = None  # Add transition attribute
        
        # Load image locally
        control_image = pygame.image.load("assets/backgrounds/control_screen2.png").convert()
        control_image = pygame.transform.scale(control_image, (screen.get_width(), screen.get_height()))

        while running:
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        running = False
                        next_screen = "game"  # Indicate transition to game screen

            # Draw control screen
            screen.fill((0, 0, 0))  # Black background
            
            screen.blit(control_image, (0, 0))
            
            Intro1.draw_text("Controls Screen", pygame.font.Font(None, 40), (255, 255, 255), screen, screen.get_width() // 2, screen.get_height() // 2)
            Intro1.draw_text("Press RETURN/ENTER to start the game", pygame.font.Font(None, 40), (255, 255, 255), screen, screen.get_width() // 2, screen.get_height() // 2 + 150)

            pygame.display.flip()
            clock.tick(60)

        # Handle transition
        if next_screen == "game":
            Intro1.run_game_screen()

    @staticmethod
    def run_game_screen():
        screen = pygame.display.get_surface()
        clock = pygame.time.Clock()
# Load image locally
        control_image = pygame.image.load("assets/backgrounds/game_screen2.png").convert()
        control_image = pygame.transform.scale(control_image, (screen.get_width(), screen.get_height()))
        running = True
        while running:
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        running = False

            # Draw game screen
            screen.fill((0, 0, 0))  # Black background
            
            screen.blit(control_image, (0, 0))
            Intro1.draw_text("Game Screen", pygame.font.Font(None, 40), (255, 255, 255), screen, screen.get_width() // 2, screen.get_height() // 2)
            Intro1.draw_text("Press RETURN/ENTER to start Level 1", pygame.font.Font(None, 40), (255, 255, 255), screen, screen.get_width() // 2, screen.get_height() // 2 + 50)

            pygame.display.flip()
            clock.tick(60)