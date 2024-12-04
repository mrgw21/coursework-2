import pygame
import math
from objects.oracle import Oracle
from ui.sidebar import Sidebar
from screens.screen_manager import BaseScreen


class MacrophageScreen(BaseScreen):
    def __init__(self, screen, manager):
        super().__init__(screen)
        self.manager = manager
        self.running = True
        self.completed = False
        self.step = 0
        self.sidebar = Sidebar()
        self.sidebar.visible = False
        self.sidebar_width = 400
        self.font = pygame.font.SysFont("Arial", 24)
        self.title_font = pygame.font.SysFont("Arial", 36, bold=True)
        self.oracle = Oracle(self.sidebar_width)

        # Load the tutorial-specific image
        self.original_image = pygame.image.load("assets/tutorials/macrophage.png")

        # Load and scale the star icons
        self.original_star_image = pygame.image.load("assets/icons/star.png")
        self.grey_star_image = pygame.image.load("assets/icons/grey_star.png")
        self.star_image = pygame.transform.scale(self.original_star_image, (30, 30))
        self.grey_star_image = pygame.transform.scale(self.grey_star_image, (30, 30))

        # Load and set up the continue button
        self.continue_button_image = pygame.image.load("assets/icons/continue.png")
        self.continue_button_image = pygame.transform.scale(self.continue_button_image, (100, 50))
        self.continue_button_rect = self.continue_button_image.get_rect(
            topright=(self.screen.get_width() - 20, 20)
        )
        self.show_continue_button = False  # Flag to display the continue button

        # Define button locations and their corresponding context text
        self.buttons = [
            {
                "relative_position": (70, 100),
                "context": "The macrophage is one of your first lines of defense against pathogens.",
                "clicked": False,
            },
            {
                "relative_position": (100, 400),
                "context": "Vesicles, called lysosomes, containing hydrolytic enzymes merge with the phagosome, causing the degradation of the pathogen.",
                "clicked": False,
            },
            {
                "relative_position": (415, 250),
                "context": "The macrophage can recognize, bind to, and engulf foreign pathogens.",
                "clicked": False,
            },
        ]
        self.clicked_button_index = None

        self.sidebar_width = self.sidebar.width if self.sidebar.visible else 0
        self.reposition_elements()

    def reposition_elements(self):
        screen_width, screen_height = self.screen.get_size()
        self.sidebar_width = self.sidebar.width if self.sidebar.visible else 0

        # Resize the image dynamically
        self.image = pygame.transform.scale(
            self.original_image,
            (int((screen_width - self.sidebar_width) * 0.6), int(screen_height * 0.6)),
        )
        self.image_rect = self.image.get_rect(
            center=(
                (screen_width - self.sidebar_width) // 2 + self.sidebar_width,
                screen_height // 2,
            )
        )

        # Recalculate button positions
        for button in self.buttons:
            relative_x, relative_y = button["relative_position"]
            button["position"] = (self.image_rect.left + relative_x, self.image_rect.top + relative_y)

        # Adjust the continue button position
        self.continue_button_rect = self.continue_button_image.get_rect(
            topright=(self.screen.get_width() - 20, 20)
        )

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # Check for star button clicks
            clicked_any_button = False
            for i, button in enumerate(self.buttons):
                button_rect = pygame.Rect(button["position"], (30, 30))
                if button_rect.collidepoint(mouse_pos) and not button["clicked"]:
                    clicked_any_button = True
                    button["clicked"] = True  # Mark the button as clicked
                    self.manager.show_modal(button["context"])

                    # If all buttons are clicked, show the continue button
                    if all(b["clicked"] for b in self.buttons):
                        self.show_continue_button = True

            # Check if the continue button is clicked
            if self.show_continue_button and self.continue_button_rect.collidepoint(mouse_pos):
                # Close the modal before transitioning
                if self.manager.modal_active:
                    self.manager.close_modal()
                self.completed = True
                self.running = False

            # Close the modal if no button was clicked
            if not clicked_any_button and self.manager.modal_active:
                self.manager.close_modal()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # Close the modal before transitioning
                if self.manager.modal_active:
                    self.manager.close_modal()
                self.completed = True
                self.running = False
            elif event.key == pygame.K_m:
                self.sidebar.toggle()
                self.reposition_elements()
        elif event.type == pygame.QUIT:
            pygame.quit()
            exit()

    def draw(self):
        self.screen.fill((200, 200, 200))

        # Draw the title
        effective_center_x = (
            (self.screen.get_width() - (self.sidebar.width if self.sidebar.visible else 0)) // 2
            + (self.sidebar.width if self.sidebar.visible else 0)
        )
        title_text = self.title_font.render("Macrophage Information", True, (0, 0, 0))
        title_rect = title_text.get_rect(center=(effective_center_x, 50))
        self.screen.blit(title_text, title_rect)

        guide_text = self.font.render("Click on the stars!", True, (0, 0, 0))
        guide_rect = guide_text.get_rect(center=(effective_center_x, 100))
        self.screen.blit(guide_text, guide_rect)

        # Draw the macrophage tutorial image
        self.screen.blit(self.image, self.image_rect)

        # Draw the star buttons
        for button in self.buttons:
            star_image = self.grey_star_image if button["clicked"] else self.star_image
            self.screen.blit(star_image, button["position"])

        # Draw the continue button if applicable
        if self.show_continue_button:
            self.screen.blit(self.continue_button_image, self.continue_button_rect)

        # Draw the Oracle
        self.oracle.draw(self.screen)

        # Draw the sidebar if visible
        if self.sidebar.visible:
            self.sidebar.draw(self.screen, "Macrophage Information")

    def run(self):
        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)

            self.draw()
            self.manager.draw_active_screen()
            pygame.display.flip()