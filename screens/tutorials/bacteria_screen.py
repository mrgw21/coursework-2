import pygame
import math
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
        self.font = pygame.font.SysFont("Arial", 20)
        self.title_font = pygame.font.SysFont("Arial", 36, bold=True)
        self.oracle = Oracle(self.sidebar_width)

        # Load the tutorial-specific image
        self.original_image = pygame.image.load("assets/tutorials/bacteria.png")
        self.image = self.original_image
        self.image_rect = self.image.get_rect()

        # Load and scale the star icons
        self.original_star_image = pygame.image.load("assets/icons/star.png")
        self.grey_star_image = pygame.image.load("assets/icons/grey_star.png")
        self.star_image = pygame.transform.scale(self.original_star_image, (40, 40))
        self.grey_star_image = pygame.transform.scale(self.grey_star_image, (40, 40))

        # Load and set up the continue button
        self.continue_button_image = pygame.image.load("assets/icons/continue.png")
        self.continue_button_image = pygame.transform.scale(self.continue_button_image, (100, 50))
        self.continue_button_rect = self.continue_button_image.get_rect(
            topright=(self.screen.get_width() - 20, 20)
        )
        self.show_continue_button = False  # Flag to display the button

        # Define button locations and their corresponding context text
        self.buttons = [
            {"relative_position": (400, 250), "context": "Ribosomes, used for protein production. (little orange circles)​", "clicked": False},
            {"relative_position": (400, 300), "context": "Cytoplasm​​", "clicked": False},
            {"relative_position": (400, 325), "context": "Circular DNA​.​​", "clicked": False},
            {"relative_position": (400, 360), "context": "Cell membrane​.​​​", "clicked": False},
            {"relative_position": (425, 380), "context": "Bacteria do not need to enter your cell to cause an infection, unlike Viruses. In addition, they can play useful roles, such as in your gut microbiome and in plants during nitrogen fixation.​​​​", "clicked": False},
            {"relative_position": (400, 400), "context": "Bacteria are larger than viruses, around 1-2μm.​", "clicked": False},
            {"relative_position": (295, 360), "context": "Protein Capsid, additional DNA that can be passed by a process known as ‘horizontal transfer,’ the main reason for antibiotic resistance amongst bacterial populations.", "clicked": False},
            {"relative_position": (285, 450), "context": "Pilli, used for attachment to other cells.​​​", "clicked": False},
            {"relative_position": (275, 215), "context": "Membrane invaginations, used for a variety of processes such as photosynthesis and nitrogen fixation.​​​", "clicked": False},
            {"relative_position": (313, 100), "context": "Flagellum, used for movement.​​​​", "clicked": False},
            {"relative_position": (275, 160), "context": "Capsule, used for protection​​​​", "clicked": False},
            {"relative_position": (385, 160), "context": "Peptidoglycan cell wall, like plant cells enables cell ‘turgidness.​​​", "clicked": False},
        ]
        self.clicked_button_index = None
        self.pulse_start_time = None  # For pulsing effect

        # Prepend "Dr. Tomato:" to all contexts
        for button in self.buttons:
            button["context"] = f"Dr. Tomato: {button['context']}"

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
                button_rect = pygame.Rect(button["position"], (40, 40))
                if button_rect.collidepoint(mouse_pos):
                    if self.clicked_button_index != i:  # New context
                        self.pulse_start_time = pygame.time.get_ticks()  # Restart pulse timer
                    self.clicked_button_index = i
                    button["clicked"] = True

                    # Check if all stars are clicked to show the continue button
                    if all(b["clicked"] for b in self.buttons):
                        self.show_continue_button = True

            # Handle the continue button click
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

        # Wrap the message text to fit within modal width
        wrapped_message = self.wrap_text(message, pulsing_font, modal_width - 20)
        text_height = pulsing_font.size(speaker)[1] + sum(
            pulsing_font.size(line)[1] + 5 for line in wrapped_message
        )  # Add spacing for lines
        modal_height = max(100, text_height + 40)  # Ensure a minimum modal height

        # Keep the modal lower on the screen
        modal_x = (self.screen.get_width() - modal_width) // 2
        modal_y = self.screen.get_height() - modal_height - 50  # Original lower position

        # Draw modal background (white) and border
        pygame.draw.rect(self.screen, (255, 255, 255), (modal_x, modal_y, modal_width, modal_height))
        pygame.draw.rect(self.screen, (0, 0, 0), (modal_x, modal_y, modal_width, modal_height), 3)

        # Render the speaker ("Dr. Tomato:") at the top of the modal
        speaker_surface = pulsing_font.render(speaker, True, (0, 0, 0))
        self.screen.blit(speaker_surface, (modal_x + 10, modal_y + 10))

        # Render the wrapped message text
        y_offset = modal_y + 20 + pulsing_font.size(speaker)[1]  # Below the speaker
        for line in wrapped_message:
            text_surface = pulsing_font.render(line, True, (0, 0, 0))
            self.screen.blit(text_surface, (modal_x + 10, y_offset))
            y_offset += pulsing_font.get_height() + 5  # Add line spacing

    def draw(self):
        self.screen.fill((252, 232, 240))

        # Draw the title
        title_text = self.title_font.render("Bacteria Information", True, (0, 0, 0))
        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 50))
        self.screen.blit(title_text, title_rect)

        guide_text = self.font.render("Click on the stars!", True, (0, 0, 0))
        guide_rect = guide_text.get_rect(center=(self.screen.get_width() // 2, 100))
        self.screen.blit(guide_text, guide_rect)

        # Draw the bacteria tutorial image with a black border
        border_thickness = 5
        border_rect = self.image_rect.inflate(border_thickness * 2, border_thickness * 2)
        pygame.draw.rect(self.screen, (0, 0, 0), border_rect)  # Draw the black border
        self.screen.blit(self.image, self.image_rect)  # Blit the original image on top

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

        # Draw the sidebar if visible
        if self.sidebar.visible:
            self.sidebar.draw(self.screen, "Bacteria Information")

    def draw_star_with_gleaming(self, screen, position, is_clicked):
        if not is_clicked:
            # Create a pulsing effect for the star
            elapsed_time = pygame.time.get_ticks() % 1000  # Repeat every 1000ms
            scale_factor = 1 + 0.1 * math.sin((elapsed_time / 1000) * 2 * math.pi)
            gleaming_star = pygame.transform.scale(
                self.star_image, 
                (int(self.star_image.get_width() * scale_factor), int(self.star_image.get_height() * scale_factor))
            )
            gleaming_rect = gleaming_star.get_rect(center=(position[0] + 20, position[1] + 20))
            screen.blit(gleaming_star, gleaming_rect)
        else:
            # Draw a grey star if clicked
            screen.blit(self.grey_star_image, position)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)

            self.draw()
            self.manager.draw_active_screen()
            pygame.display.flip()