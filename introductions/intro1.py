import pygame

class Intro1:
    def __init__(self, screen, pdf_images):
        self.screen = screen
        self.pdf_images = pdf_images
        self.current_page = 0
        self.running = True

        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)

        # Fonts
        self.TITLE_FONT = pygame.font.Font(None, 80)
        self.TEXT_FONT = pygame.font.Font(None, 40)

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

        # Centerize the scaled image (by blitting at the top-left corner of the screen)
        surface.blit(scaled_image, (0, 0))

        if self.current_page == len(self.pdf_images) - 1:
            guidance_text = "Press [<-] to return to intro. Hit RETURN/ENTER to play game!"
        elif self.current_page == 0:
            guidance_text = "Press [->] to continue!"
        else:
            guidance_text = "Press [<-] [->] to navigate."

        self.draw_text(
            guidance_text,
            self.TEXT_FONT,
            self.BLACK,
            surface,
            screen_width // 2,
            screen_height - 20
        )

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
            Intro1.draw_text("Game Screen", pygame.font.Font(None, 40), (255, 255, 255), screen, screen.get_width() // 2, screen.get_height() // 2)
            Intro1.draw_text("Press RETURN/ENTER to start Level 1", pygame.font.Font(None, 40), (255, 255, 255), screen, screen.get_width() // 2, screen.get_height() // 2 + 50)

            pygame.display.flip()
            clock.tick(60)