import pygame
from screens.screen_manager import BaseScreen
from ui.sidebar import Sidebar 

class Intro1(BaseScreen):
    def __init__(self, screen, pdf_images, manager):
        super().__init__(screen)  # Initialize BaseScreen
        self.pdf_images = pdf_images
        self.current_page = 0
        self.running = True
        self.manager = manager

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

        # Placeholder sidebar for compatibility
        self.sidebar = Sidebar()

        self.sidebar.visible = False

    def run(self):
        clock = pygame.time.Clock()

        while self.running:
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.VIDEORESIZE:
                    # Handle screen resizing
                    width_ratio = event.w / self.previous_width
                    height_ratio = event.h / self.previous_height
                    self.update_positions(width_ratio, height_ratio)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        if self.current_page < len(self.pdf_images) - 1:
                            self.current_page += 1
                    elif event.key == pygame.K_LEFT:
                        if self.current_page > 0:
                            self.current_page -= 1
                    elif event.key == pygame.K_RETURN and self.current_page == len(self.pdf_images) - 1:
                        self.running = False
                        self.manager.set_active_screen("Level 1")
                    
                    if event.key == pygame.K_m:
                        if self.sidebar:
                            self.sidebar.toggle()
                            self.handle_sidebar_toggle()

                # Pass individual events to the sidebar handler
                if self.sidebar and self.sidebar.visible and self.sidebar.handle_event(event):
                    mouse_pos = pygame.mouse.get_pos()
                    option_clicked = self.get_sidebar_option(mouse_pos, self.sidebar.options)
                    if option_clicked:
                        self.running = False
                        self.manager.set_active_screen(option_clicked)
                        return

            # Handle all events for this screen
            self.handle_event(events)

            # Clear the screen and draw the current state
            self.screen.fill(self.WHITE)
            self.draw()

            # Update the display
            pygame.display.flip()
            clock.tick(60)
    
    def update_positions(self, width_ratio, height_ratio):
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        sidebar_width = self.sidebar.width if self.sidebar and self.sidebar.visible else 0

        # Adjust the center for the image and text based on the screen size and sidebar
        self.center_x = (screen_width - sidebar_width) // 2
        self.center_y = screen_height // 2

        # Adjust icon positions if necessary (scaled proportionally)
        self.left_arrow = pygame.transform.scale(
            self.left_arrow,
            (int(self.left_arrow.get_width() * width_ratio), int(self.left_arrow.get_height() * height_ratio))
        )
        self.right_arrow = pygame.transform.scale(
            self.right_arrow,
            (int(self.right_arrow.get_width() * width_ratio), int(self.right_arrow.get_height() * height_ratio))
        )
        self.enter_icon = pygame.transform.scale(
            self.enter_icon,
            (int(self.enter_icon.get_width() * width_ratio), int(self.enter_icon.get_height() * height_ratio))
        )

    def load_and_scale_icon(self, path, scale_factor=15):
        image = pygame.image.load(path)
        return pygame.transform.scale(
            image, (image.get_width() // scale_factor, image.get_height() // scale_factor)
        )

    def draw(self):
        # Get the screen dimensions and sidebar width
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        sidebar_width = self.sidebar.width if self.sidebar and self.sidebar.visible else 0

        # Scale the current image to fit the available screen space
        scaled_image = pygame.transform.scale(
            self.pdf_images[self.current_page],
            (screen_width - sidebar_width, screen_height)
        )
        self.screen.blit(scaled_image, (sidebar_width, 0))

        # Set the y-position for the guidance text and icons
        text_y_position = screen_height - 20  # Adjust this value for spacing from the bottom
        center_x = (screen_width - sidebar_width) // 2  # Center horizontally, accounting for sidebar

        # Draw guidance arrows and text based on the current page
        if self.current_page == len(self.pdf_images) - 1:  # Last page
            self.draw_text_with_two_texts_and_icons(
                "Press",
                self.left_arrow,
                "to return to tutorial. Press RETURN/ENTER",
                self.enter_icon,
                "to play game!",
                self.screen,
                center_x,
                text_y_position,
                spacing=10
            )
        elif self.current_page == 0:  # First page
            self.draw_text_with_icon_and_following_text(
                "Press right arrow",
                self.right_arrow,
                "to continue.",
                self.screen,
                center_x,
                text_y_position
            )
        else:  # Middle pages
            self.draw_text_with_two_icons_and_following_text(
                "Use arrows",
                self.left_arrow,
                self.right_arrow,
                "to navigate.",
                self.screen,
                center_x,
                text_y_position,
                spacing=10
            )

        if self.sidebar and self.sidebar.visible:
            self.sidebar.draw(self.screen)

    def draw_text_with_icon_and_following_text(self, text, icon, following_text, surface, x, y):
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
    
    def handle_sidebar_toggle(self):
        # Adjust the layout depending on sidebar visibility
        sidebar_width = self.sidebar.width if self.sidebar and self.sidebar.visible else 0
        self.center_x = (self.screen.get_width() - sidebar_width) // 2
        self.center_y = self.screen.get_height() // 2
        self.draw()  # Redraw elements to reflect the changes
    
    def get_sidebar_option(self, mouse_pos, options):
        y_offset = 120  # Adjust to the starting Y position of options
        spacing = 50  # Space between each option
        for i, option in enumerate(options):
            option_rect = pygame.Rect(20, y_offset + i * spacing, 360, 40)  # Match the sidebar dimensions
            if option_rect.collidepoint(mouse_pos):
                return option
        return None

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