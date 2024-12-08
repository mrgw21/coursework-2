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
        self.font = pygame.font.SysFont("Arial", 20)
        self.title_font = pygame.font.SysFont("Arial", 36, bold=True)
        self.oracle = Oracle(self.sidebar_width)

        # Load the tutorial-specific image
        self.original_image = pygame.image.load("assets/tutorials/macrophage.png")

        # Load and scale the star icons
        self.original_star_image = pygame.image.load("assets/icons/star.png")
        self.grey_star_image = pygame.image.load("assets/icons/grey_star.png")
        self.star_image = pygame.transform.scale(self.original_star_image, (50, 50))
        self.grey_star_image = pygame.transform.scale(self.grey_star_image, (50, 50))

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
            {
                "relative_position": (600, 535),
                "context": "Once broken down, the material is then expelled from the cell.",
                "clicked": False,
            },
            {
                "relative_position": (800, 205),
                "context": "This forms a ‘phagosome’, inside the cytoplasm of the phagocyte.​",
                "clicked": False,
            },
        ]
        self.clicked_button_index = None
        self.pulse_start_time = None

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

    def wrap_text(self, text, font, max_width):
        words = text.split(' ')
        lines = []
        current_line = words[0]

        for word in words[1:]:
            if font.size(current_line + ' ' + word)[0] <= max_width:
                current_line += ' ' + word
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)
        return lines

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # Check if the modal is open and the click is outside the modal
            if self.clicked_button_index is not None:
                modal_width = self.image_rect.width
                modal_height = 100
                modal_x = (self.screen.get_width() - modal_width) // 2
                modal_y = self.screen.get_height() - modal_height - 50

                # If click is outside the modal
                if not (modal_x <= mouse_pos[0] <= modal_x + modal_width and
                        modal_y <= mouse_pos[1] <= modal_y + modal_height):
                    self.clicked_button_index = None  # Close the modal
                    return

            # Check for star button clicks
            for i, button in enumerate(self.buttons):
                button_rect = pygame.Rect(button["position"], (50, 50))
                if button_rect.collidepoint(mouse_pos):
                    if self.clicked_button_index != i:  # New context
                        self.pulse_start_time = pygame.time.get_ticks()  # Restart pulse timer
                    self.clicked_button_index = i
                    button["clicked"] = True

                    # If all buttons are clicked, show the continue button
                    if all(b["clicked"] for b in self.buttons):
                        self.show_continue_button = True

            # Check if the continue button is clicked
            if self.show_continue_button and self.continue_button_rect.collidepoint(mouse_pos):
                self.completed = True
                self.running = False

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

    def draw_modal_with_pulsing_context(self):
        if self.clicked_button_index is None:
            return

        # Get the current button context
        context = self.buttons[self.clicked_button_index]["context"]

        # Set modal dimensions
        modal_width = self.image_rect.width
        base_font_size = 20
        max_font_size = 24
        pulse_duration = 1000  # Slower pulse duration
        total_pulses = 2  # Number of pulses

        # Handle pulsing effect
        if self.pulse_start_time is not None:
            elapsed_time = pygame.time.get_ticks() - self.pulse_start_time
            current_pulse = elapsed_time // pulse_duration

            if current_pulse < total_pulses:
                pulse_progress = (elapsed_time % pulse_duration) / pulse_duration
                scale_factor = 1 + 0.2 * math.sin(pulse_progress * math.pi)
                font_size = min(int(base_font_size * scale_factor), max_font_size)
                pulsing_font = pygame.font.SysFont("Arial", font_size)
            else:
                pulsing_font = pygame.font.SysFont("Arial", base_font_size)
                self.pulse_start_time = None
        else:
            pulsing_font = pygame.font.SysFont("Arial", base_font_size)

        # Wrap text and calculate required height
        wrapped_text = self.wrap_text(context, pulsing_font, modal_width - 20)
        text_height = sum(pulsing_font.size(line)[1] + 5 for line in wrapped_text)  # Add 5 for line spacing
        modal_height = max(100, text_height + 40)  # Ensure a minimum modal height

        # Keep the modal lower on the screen
        modal_x = (self.screen.get_width() - modal_width) // 2
        modal_y = self.screen.get_height() - modal_height - 50  # Original lower position

        # Draw modal background (white) and border
        pygame.draw.rect(self.screen, (255, 255, 255), (modal_x, modal_y, modal_width, modal_height))
        pygame.draw.rect(self.screen, (0, 0, 0), (modal_x, modal_y, modal_width, modal_height), 3)

        # Render the wrapped text inside the modal
        y_offset = modal_y + 20  # Padding at the top of the modal
        for line in wrapped_text:
            text_surface = pulsing_font.render(line, True, (0, 0, 0))
            self.screen.blit(text_surface, (modal_x + 10, y_offset))
            y_offset += pulsing_font.get_height() + 5  # Add line spacing

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

        # Draw the modal with pulsing context
        self.draw_modal_with_pulsing_context()

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