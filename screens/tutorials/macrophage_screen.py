import pygame
import math
from ui.sidebar import Sidebar
from screens.screen_manager import BaseScreen


class MacrophageScreen(BaseScreen):
    def __init__(self, screen, manager):
        super().__init__(screen)
        self.manager = manager
        self.running = True
        self.completed = False
        self.step = 0  # Retaining the `step` instance variable
        self.sidebar = Sidebar()
        self.sidebar.visible = False
        self.font = pygame.font.SysFont("Arial", 24)
        self.title_font = pygame.font.SysFont("Arial", 36, bold=True)

        # Load the tutorial-specific image
        self.original_image = pygame.image.load("assets/tutorials/macrophage.png")

        # Load and scale the star icon
        self.original_star_image = pygame.image.load("assets/icons/star.png")
        self.star_image = pygame.transform.scale(self.original_star_image, (30, 30))

        # Define button locations and their corresponding context text
        self.buttons = [
            {
                "relative_position": (70, 100),  # Relative to the image top-left
                "context": "The macrophage is one of your first lines of defense against pathogens.",
            },
            {
                "relative_position": (100, 70),  # Relative to the image top-left
                "context": "The macrophage can recognize, bind to, and engulf foreign pathogens.",
            },
            {
                "relative_position": (150, 300),  # Relative to the image top-left
                "context": "Vesicles merge with the pathogen to degrade it.",
            },
        ]
        self.clicked_button_index = None  # To track which button is clicked

        # Initialize positions
        self.sidebar_width = self.sidebar.width if self.sidebar.visible else 0
        self.reposition_elements()  # Now called after initializing self.buttons

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

            # Context position (to the right of the image or dynamically adjust)
            context_offset = 50 if not self.sidebar.visible else self.sidebar_width + 50
            button["context_position"] = (
                self.image_rect.right + context_offset,
                self.image_rect.top + relative_y,
            )

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for i, button in enumerate(self.buttons):
                button_rect = pygame.Rect(button["position"], (30, 30))
                if button_rect.collidepoint(mouse_pos):
                    self.clicked_button_index = i  # Set the clicked button
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.completed = True  # Mark as completed to trigger screen switch
                self.running = False
            elif event.key == pygame.K_m:
                self.sidebar.toggle()
                self.reposition_elements()  # Adjust layout based on sidebar visibility
        elif event.type == pygame.QUIT:
            pygame.quit()
            exit()

    def draw_arrow(self, start, end, color=(0, 0, 0), width=2):
        # Shorten the arrow length further
        shorten_factor = 0.6  # Reduce the arrow length to 60% of the original
        dx, dy = end[0] - start[0], end[1] - start[1]
        shortened_end = (start[0] + dx * shorten_factor, start[1] + dy * shorten_factor)

        # Draw the shortened main line
        pygame.draw.line(self.screen, color, start, shortened_end, width)

        # Calculate the angle and draw the arrowhead
        arrow_size = 10
        angle = math.atan2(dy, dx)
        arrow_head_points = [
            shortened_end,
            (
                shortened_end[0] - arrow_size * math.cos(angle - math.pi / 6),
                shortened_end[1] - arrow_size * math.sin(angle - math.pi / 6),
            ),
            (
                shortened_end[0] - arrow_size * math.cos(angle + math.pi / 6),
                shortened_end[1] - arrow_size * math.sin(angle + math.pi / 6),
            ),
        ]
        pygame.draw.polygon(self.screen, color, arrow_head_points)

    def draw(self):
        self.screen.fill((200, 200, 200))

        # Draw the title
        title_text = self.title_font.render("Macrophage Information", True, (0, 0, 0))
        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 50))
        self.screen.blit(title_text, title_rect)

        # Draw the macrophage tutorial image
        self.screen.blit(self.image, self.image_rect)

        # Draw the star buttons
        for button in self.buttons:
            self.screen.blit(self.star_image, button["position"])

        # If a button is clicked, display its context and draw an arrow
        if self.clicked_button_index is not None:
            button = self.buttons[self.clicked_button_index]
            context_text = self.font.render(button["context"], True, (0, 0, 0))
            context_rect = context_text.get_rect(topleft=button["context_position"])

            # Draw background for text
            pygame.draw.rect(self.screen, (255, 255, 255), context_rect.inflate(10, 10))
            pygame.draw.rect(self.screen, (0, 0, 0), context_rect.inflate(10, 10), 2)
            self.screen.blit(context_text, context_rect)

            # Draw an arrow from the button to the context
            self.draw_arrow(
                (button["position"][0] + 15, button["position"][1] + 15),  # Center of star
                context_rect.topleft,
            )

        # Draw the sidebar if visible
        if self.sidebar.visible:
            self.sidebar.draw(self.screen, "Macrophage Information")

    def run(self):
        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)

            self.draw()
            pygame.display.flip()