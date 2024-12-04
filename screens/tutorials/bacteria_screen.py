import pygame
from ui.sidebar import Sidebar
from screens.screen_manager import BaseScreen
from objects.oracle import Oracle


class BacteriaScreen(BaseScreen):
    def __init__(self, screen, manager):
        super().__init__(screen)
        self.manager = manager
        self.running = True
        self.completed = False
        self.step = 3  # Retaining the `step` instance variable
        self.sidebar = Sidebar()
        self.sidebar.visible = False
        self.sidebar_width = 400
        self.font = pygame.font.SysFont("Arial", 24)
        self.title_font = pygame.font.SysFont("Arial", 36, bold=True)
        self.oracle = Oracle(self.sidebar_width)
        self.modal_active = False

        # Load the tutorial-specific image (keeping original dimensions)
        self.original_image = pygame.image.load("assets/tutorials/bacteria.png")
        self.image = self.original_image
        self.image_rect = self.image.get_rect()  # Keep the original dimensions

        # Load and scale the star icon
        self.original_star_image = pygame.image.load("assets/icons/star.png")
        self.star_image = pygame.transform.scale(self.original_star_image, (30, 30))

        # Define button locations and their corresponding context text
        self.buttons = [
            {
                "relative_position": (60, 120),
                "context": "Bacteria are single-celled microorganisms found almost everywhere on Earth.",
            },
            {
                "relative_position": (140, 350),
                "context": "Some bacteria are beneficial, while others cause diseases like tuberculosis.",
            },
            {
                "relative_position": (400, 200),
                "context": "Bacteria reproduce through binary fission, doubling their population rapidly.",
            },
        ]
        self.clicked_button_index = None  # To track which button is clicked

        # Initialize positions
        self.sidebar_width = self.sidebar.width if self.sidebar.visible else 0
        self.reposition_elements()  # Now called after initializing self.buttons

    def reposition_elements(self):
        screen_width, screen_height = self.screen.get_size()
        self.sidebar_width = self.sidebar.width if self.sidebar.visible else 0

        # Center the image with original dimensions
        self.image = pygame.transform.scale(
            self.original_image,
            (int((screen_width - self.sidebar_width) * 0.4), int(screen_height * 0.6)),
        )
        self.image_rect = self.image.get_rect(
            center=(
                (screen_width - self.sidebar_width) // 2 + self.sidebar_width,
                screen_height // 2,
            )
        )
        self.image_rect.center = (
            (screen_width - self.sidebar_width) // 2 + self.sidebar_width,
            screen_height // 2,
        )

        # Recalculate button positions
        for button in self.buttons:
            relative_x, relative_y = button["relative_position"]
            button["position"] = (self.image_rect.left + relative_x, self.image_rect.top + relative_y)

            # Place the context text closer to the button
            context_offset_x = 50
            context_offset_y = -20
            button["context_position"] = (
                button["position"][0] + context_offset_x,
                button["position"][1] + context_offset_y,
            )

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            clicked_any_button = False
            for i, button in enumerate(self.buttons):
                button_rect = pygame.Rect(button["position"], (30, 30))
                if button_rect.collidepoint(mouse_pos):
                    clicked_any_button = True
                    if self.clicked_button_index == i:
                        # Hide context and modal if the same button is clicked again
                        self.clicked_button_index = None
                        self.oracle.show_modal = False
                    else:
                        # Show context and modal for the clicked button
                        self.clicked_button_index = i
                        self.oracle.tutorial_handle_click(button["context"])

            # If no button was clicked, close the modal
            if not clicked_any_button and self.oracle.show_modal:
                self.clicked_button_index = None
                self.oracle.show_modal = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
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
        title_text = self.title_font.render("Bacteria Information", True, (0, 0, 0))
        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 50))
        self.screen.blit(title_text, title_rect)

        guide_text = self.font.render("Click on the stars!", True, (0, 0, 0))
        guide_rect = guide_text.get_rect(center=(self.screen.get_width() // 2, 100))
        self.screen.blit(guide_text, guide_rect)

        # Draw the bacteria tutorial image at its original size
        self.screen.blit(self.image, self.image_rect)

        # Draw the star buttons
        for button in self.buttons:
            self.screen.blit(self.star_image, button["position"])

        # Draw the Oracle and its modal
        self.oracle.draw(self.screen)
        self.oracle.draw_message(self.screen)

        # Draw the sidebar if visible
        if self.sidebar.visible:
            self.sidebar.draw(self.screen, "Bacteria Information")

    def run(self):
        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)

            self.draw()
            pygame.display.flip()