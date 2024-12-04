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
        self.step = 3
        self.sidebar = Sidebar()
        self.sidebar.visible = False
        self.sidebar_width = 400
        self.font = pygame.font.SysFont("Arial", 24)
        self.title_font = pygame.font.SysFont("Arial", 36, bold=True)
        self.oracle = Oracle(self.sidebar_width)

        # Load the tutorial-specific image
        self.original_image = pygame.image.load("assets/tutorials/bacteria.png")
        self.image = self.original_image
        self.image_rect = self.image.get_rect()

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
        self.clicked_button_index = None

        # Initialize positions
        self.sidebar_width = self.sidebar.width if self.sidebar.visible else 0
        self.reposition_elements()

    def reposition_elements(self):
        screen_width, screen_height = self.screen.get_size()
        self.sidebar_width = self.sidebar.width if self.sidebar.visible else 0

        # Center the image with adjusted dimensions
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

        # Recalculate button positions
        for button in self.buttons:
            relative_x, relative_y = button["relative_position"]
            button["position"] = (self.image_rect.left + relative_x, self.image_rect.top + relative_y)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            clicked_any_button = False
            for i, button in enumerate(self.buttons):
                button_rect = pygame.Rect(button["position"], (30, 30))
                if button_rect.collidepoint(mouse_pos):
                    clicked_any_button = True
                    if self.clicked_button_index == i:
                        # Hide modal if the same button is clicked again
                        self.clicked_button_index = None
                        self.manager.close_modal()
                    else:
                        # Show modal with the button's context
                        self.clicked_button_index = i
                        self.manager.show_modal(button["context"])

            if not clicked_any_button:
                # Close modal if clicking outside any buttons
                self.clicked_button_index = None
                self.manager.close_modal()

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

        # Draw the bacteria tutorial image
        self.screen.blit(self.image, self.image_rect)

        # Draw the star buttons
        for button in self.buttons:
            self.screen.blit(self.star_image, button["position"])

        # Draw the Oracle
        self.oracle.draw(self.screen)

        # Draw the sidebar if visible
        if self.sidebar.visible:
            self.sidebar.draw(self.screen, "Bacteria Information")

    def run(self):
        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)

            self.draw()
            self.manager.draw_active_screen()  # Ensure modal is drawn
            pygame.display.flip()