import pygame
import math
from ui.sidebar import Sidebar
from screens.screen_manager import BaseScreen
from objects.oracle import Oracle


class VirusScreen(BaseScreen):
    def __init__(self, screen, manager):
        super().__init__(screen)
        self.manager = manager
        self.running = True
        self.completed = False
        self.step = 1
        self.sidebar = Sidebar()
        self.sidebar.visible = False
        self.sidebar_width = 400
        self.font = pygame.font.SysFont("Arial", 20)
        self.title_font = pygame.font.SysFont("Arial", 36, bold=True)
        self.semi_title_font = pygame.font.SysFont("Arial", 24, bold=True)
        self.oracle = Oracle(self.sidebar_width)
        self.oracle.display_message("Click on the stars!", self.screen)

        # Load the tutorial-specific image
        self.original_image = pygame.image.load("assets/tutorials/virus.png")

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
                "relative_position": (600, 250),
                "context": "Viral genetic information is stored within a protein capsid.",
                "clicked": False,
            },
            {
                "relative_position": (500, 350),
                "context": "Viruses tend to be small ~ 20-800nm.",
                "clicked": False,
            },
            {
                "relative_position": (400, 200),
                "context": "Viruses reproduce using infected cell machinery. Either using reverse transcriptase (to turn the viral RNA into nascent DNA) or the RNA is structured similarly to host RNA so is treated as normal mRNA.",
                "clicked": False,
            },
            {
                "relative_position": (540, 230),
                "context": "Viral genetic information is stored as RNA. It makes use of the infected cells' machinery (ribosomes) for protein production and replication. The virus genome tends to be very small, containing only enough information to code for the assembly of more viral particles.",
                "clicked": False,
            },
            {
                "relative_position": (425, 300),
                "context": "Viral particles have external ‘binding proteins’ that lead to attachment and promote insertion of the contents of the virus into target cells.",
                "clicked": False,
            },
        ]

        # Prepend "Dr. Tomato:" to all contexts
        for button in self.buttons:
            button["context"] = f"Dr. Tomato: {button['context']}"

        self.clicked_button_index = None
        self.pulse_start_time = None

        # Initialize positions
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

        # Separate "Dr. Tomato:" and the rest of the context
        speaker = "Dr. Tomato:"
        message = context.replace(speaker, "").strip()

        # Set modal dimensions
        modal_width = self.image_rect.width
        base_font_size = 20
        max_font_size = 24
        pulse_duration = 1000
        total_pulses = 2

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

        # Wrap the message text to fit within modal width
        wrapped_message = self.wrap_text(message, pulsing_font, modal_width - 20)
        text_height = pulsing_font.size(speaker)[1] + sum(
            pulsing_font.size(line)[1] + 5 for line in wrapped_message
        )
        modal_height = max(100, text_height + 40)

        # Keep the modal lower on the screen
        modal_x = (self.screen.get_width() - modal_width) // 2
        modal_y = self.screen.get_height() - modal_height - 50

        # Draw modal background and border
        pygame.draw.rect(self.screen, (255, 255, 255), (modal_x, modal_y, modal_width, modal_height))
        pygame.draw.rect(self.screen, (0, 0, 0), (modal_x, modal_y, modal_width, modal_height), 3)

        # Render the speaker
        speaker_surface = pulsing_font.render(speaker, True, (0, 0, 0))
        self.screen.blit(speaker_surface, (modal_x + 10, modal_y + 10))

        # Render the wrapped message text
        y_offset = modal_y + 20 + pulsing_font.size(speaker)[1]
        for line in wrapped_message:
            text_surface = pulsing_font.render(line, True, (0, 0, 0))
            self.screen.blit(text_surface, (modal_x + 10, y_offset))
            y_offset += pulsing_font.get_height() + 5

    def draw(self):
        self.screen.fill((252, 232, 240))

        # Draw the title
        title_text = self.title_font.render("Virus Information", True, (0, 0, 139))
        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 50))
        self.screen.blit(title_text, title_rect)

        guide_text = self.semi_title_font.render("Click on the stars!", True, (0, 0, 139))
        guide_rect = guide_text.get_rect(center=(self.screen.get_width() // 2, 100))
        self.screen.blit(guide_text, guide_rect)

        # Draw the virus tutorial image
        self.screen.blit(self.image, self.image_rect)

        # Draw the star buttons
        for button in self.buttons:
            self.draw_star_with_gleaming(self.screen, button["position"], button["clicked"])

        # Draw the continue button if applicable
        if self.show_continue_button:
            self.screen.blit(self.continue_button_image, self.continue_button_rect)

        # Draw the modal with pulsing context
        self.draw_modal_with_pulsing_context()

        # Draw the Oracle
        self.oracle.draw(self.screen)
        self.oracle.draw_message(self.screen)

        # Draw the sidebar if visible
        if self.sidebar.visible:
            self.sidebar.draw(self.screen, "Virus Information")

    def draw_star_with_gleaming(self, screen, position, is_clicked):
        if not is_clicked:
            elapsed_time = pygame.time.get_ticks() % 1000
            scale_factor = 1 + 0.1 * math.sin((elapsed_time / 1000) * 2 * math.pi)
            gleaming_star = pygame.transform.scale(
                self.star_image,
                (int(self.star_image.get_width() * scale_factor), int(self.star_image.get_height() * scale_factor)),
            )
            gleaming_rect = gleaming_star.get_rect(center=(position[0] + 28, position[1] + 28))
            screen.blit(gleaming_star, gleaming_rect)
        else:
            screen.blit(self.grey_star_image, position)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)

            self.draw()
            self.manager.draw_active_screen()
            pygame.display.flip()