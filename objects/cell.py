import pygame
import random

class Cell:
    def __init__(self, position, center_pos=(400, 300)):
        self.image = pygame.image.load("assets/images/uninfected_cell.png")
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 2.5, self.image.get_height() // 2.5))
        self.rect = self.image.get_rect()
        self.position = position
        self.state = True  # True means uninfected, False means infected
        self.health = "uninfected"  # Health status of the cell
        self.show_modal = False
        self.cell_number = position + 1  # Numbering for cells
        self.quiz = None 
        self.selected_option = None

        self.infection_timer = 0  # Timer for slowing infected cell attacks
        self.neighbors = [] 

        self.option_coords = []

        # Set initial position of the cell
        self.reposition(center_pos)

    def reposition(self, center_pos, spacing=15):
        row = [3, 5, 7, 7, 7, 5, 3]
        y_offset = -3.5 * spacing
        idx = 0 
        
        for i, count in enumerate(row):
            x_offset = -(count // 2) * spacing - 5
            for j in range(count):
                if idx == self.position:
                    self.rect.x = center_pos[0] + x_offset + j * spacing
                    self.rect.y = center_pos[1] + y_offset + i * spacing
                    return
                idx += 1

    def die(self):
        self.state = False
        self.health = "infected"
        self.image = pygame.image.load("assets/images/infected_cell.png")
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 2.5, self.image.get_height() // 2.5))
        self.infection_timer = pygame.time.get_ticks()
    
    def draw(self, screen, sidebar_width, level):
        screen.blit(self.image, self.rect)

        if self.show_modal:
            self.draw_modal(screen, sidebar_width, level)

    def draw_modal(self, screen, sidebar_width, level):
        screen_width = screen.get_width()

        # Determine modal dimensions based on screen size
        if screen_width > 1200:  # Fullscreen mode
            modal_width = 500
            modal_height = 700
        else:
            modal_width = 300
            modal_height = 500

        # Calculate modal position dynamically, respecting the sidebar
        game_width = screen_width - sidebar_width
        modal_x = sidebar_width + (game_width - modal_width) // 2 - 350
        modal_y = (screen.get_height() - modal_height) // 2

        # Draw modal background and border
        pygame.draw.rect(screen, (220, 220, 220), (modal_x, modal_y, modal_width, modal_height))
        pygame.draw.rect(screen, (0, 0, 0), (modal_x, modal_y, modal_width, modal_height), 3)

        # Font for text
        font = pygame.font.SysFont("Arial", 20)

        # Close button
        close_button_width = 90
        close_button_height = 25
        close_button_x = modal_x + modal_width - close_button_width - 10
        close_button_y = modal_y + 10

        # Draw the button background (same as modal color)
        pygame.draw.rect(screen, (220, 220, 220), (close_button_x, close_button_y, close_button_width, close_button_height))
        # Draw button border in red
        pygame.draw.rect(screen, (255, 0, 0), (close_button_x, close_button_y, close_button_width, close_button_height), 2)

        # Render the button text in red
        close_button_text = font.render("X (ESC)", True, (255, 0, 0))
        text_rect = close_button_text.get_rect(
            center=(close_button_x + close_button_width // 2, close_button_y + close_button_height // 2)
        )
        screen.blit(close_button_text, text_rect)

        # Handle close button click detection
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        if (close_button_x <= mouse_pos[0] <= close_button_x + close_button_width and
            close_button_y <= mouse_pos[1] <= close_button_y + close_button_height):
            if mouse_pressed[0]:  # Left mouse button pressed
                self.show_modal = False  # Close the modal
                level.paused = False

        # Display cell information
        cell_number_text = f"Cell #{self.cell_number}"
        health_text = f"Health: {self.health}"
        info_text = self.get_info_text()

        content_start_y = close_button_y + close_button_height + 20

        # Display cell number and health
        screen.blit(font.render(cell_number_text, True, (0, 0, 0)), (modal_x + 10, content_start_y))
        screen.blit(font.render(health_text, True, (0, 0, 0)), (modal_x + 10, content_start_y + 30))

        # Draw cell information with text wrapping
        self.draw_wrapped_text(screen, info_text, font, modal_x + 10, content_start_y + 60, modal_width - 20)

        # Draw cell image
        if self.health == "dead":
            cell_image = pygame.image.load("assets/images/dead_cell_placeholder.png")
            cell_image = pygame.transform.scale(cell_image, (100, 100))
        else:
            cell_image = pygame.image.load("assets/images/infected_cell.png")
            cell_image = pygame.transform.scale(cell_image, (100, 100))
        screen.blit(cell_image, (modal_x + (modal_width // 2) - 50, content_start_y + 115))

        # Draw quiz if applicable
        if self.quiz:
            self.draw_quiz(screen, modal_x, modal_y, content_start_y + 250, modal_width)

        # Draw feedback
        if hasattr(self, "quiz_feedback") and self.quiz_feedback:
            feedback_text = font.render(self.quiz_feedback["message"], True, self.quiz_feedback["color"])
            feedback_rect = feedback_text.get_rect(
                center=(modal_x + modal_width // 2, modal_y + modal_height - 70)
            )
            screen.blit(feedback_text, feedback_rect)
    
    def draw_quiz(self, screen, modal_x, modal_y, start_y, modal_width):
        font = pygame.font.SysFont('Arial', 18)
        quiz = self.quiz

        # Question text
        question_text = self.wrap_text(quiz["question"], font, modal_width - 20)
        current_y = start_y

        # Display the question text
        for line in question_text:
            rendered_text = font.render(line, True, (0, 0, 0))
            screen.blit(rendered_text, (modal_x + 10, current_y))
            current_y += 25  # Line spacing

        # Options (radio buttons with text)
        new_option_coords = []  # Temporary list to store new coordinates
        for i, option in enumerate(quiz["options"]):
            option_y = current_y + 20 + i * 40  # Adjust spacing between options

            # Determine the color based on selection
            if hasattr(self, "selected_option") and self.selected_option == option:
                if option["is_correct"]:
                    circle_color = (0, 255, 0)  # Green for correct
                    text_color = (0, 255, 0)
                else:
                    circle_color = (255, 0, 0)  # Red for incorrect
                    text_color = (255, 0, 0)
            else:
                circle_color = (220, 220, 220)  # Modal background color (default filling)
                text_color = (0, 0, 0)

            # Draw filled circle for radio button
            circle_x = modal_x + 20  # Left margin for radio button
            pygame.draw.circle(screen, circle_color, (circle_x, option_y), 10, 0)  # Filled circle
            pygame.draw.circle(screen, (0, 0, 0), (circle_x, option_y), 10, 1)  # Outline circle

            # Render option text
            rendered_text = font.render(option["text"], True, text_color)
            screen.blit(rendered_text, (circle_x + 20, option_y - 10))  # Adjust text placement

            # Add this option to the clickable areas list
            new_option_coords.append({"circle": (circle_x, option_y), "radius": 10, "option": option})

        # Update `option_coords` only if there's a change
        if not hasattr(self, "option_coords") or self.option_coords != new_option_coords:
            self.option_coords = new_option_coords

    def wrap_text(self, text, font, max_width):
        words = text.split(' ')
        lines = []
        current_line = words[0]

        for word in words[1:]:
            if font.size(current_line + ' ' + word)[0] < max_width:
                current_line += ' ' + word
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)
        return lines

    def handle_quiz_answer(self, selected_option, level):
        for option in self.quiz["options"]:
            if option == selected_option:
                if option["is_correct"]:
                    # Correct answer
                    self.quiz_feedback = {"message": "Congratulations! You got the right answer!", "color": (0, 255, 0)}
                    self.stop_infection_and_neighbors()  # Stop infection and neighbors' spread
                    self.feedback_timer = pygame.time.get_ticks()  # Start feedback timer
                    level.paused = True
                else:
                    # Incorrect answer
                    self.quiz_feedback = {"message": "Wrong answer! Try again!", "color": (255, 0, 0)}

    def draw_wrapped_text(self, screen, text, font, x, y, max_width):
        words = text.split(' ')
        space = font.size(' ')[0]
        line = []
        line_width = 0
        for word in words:
            word_width = font.size(word)[0]
            if line_width + word_width > max_width:
                screen.blit(font.render(' '.join(line), True, (0, 0, 0)), (x, y))
                y += font.get_height()
                line = [word]
                line_width = word_width + space
            else:
                line.append(word)
                line_width += word_width + space
        if line:
            screen.blit(font.render(' '.join(line), True, (0, 0, 0)), (x, y))
    
    def get_info_text(self):
        return "Cells protect the body from pathogens."

    def handle_click(self, mouse_pos, cells, level):
        if self.health == "uninfected" or self.health == "dead":
            return

        # Toggle modal on click
        if self.rect.collidepoint(mouse_pos):
            self.show_modal = True

        """
        # If the modal is not open, check if the infected cell was clicked
        if self.rect.collidepoint(mouse_pos):
            for cell in cells:
                if cell != self:
                    cell.show_modal = False
            self.show_modal = True
            level.paused = True
        """
    
    def handle_radio_button_click(self, screen, mouse_pos, cells, level):
        if not self.show_modal or not hasattr(self, "option_coords"):
            return

        for option_data in self.option_coords:
            circle_x, circle_y = option_data["circle"]
            radius = option_data["radius"]
            distance = ((mouse_pos[0] - circle_x) ** 2 + (mouse_pos[1] - circle_y) ** 2) ** 0.5
            if distance <= radius:
                self.selected_option = option_data["option"]  # Mark the selected option
                self.handle_quiz_answer(option_data["option"], level)
                return

    def infect_neighbors(self):
        neighbors_to_infect = random.sample(self.neighbors, random.randint(0, len(self.neighbors)))
        for neighbor in neighbors_to_infect:
            if neighbor.health == "uninfected":
                neighbor.die()
    
    def update_infection(self):
        if self.health != "infected" or self.infection_timer is None:  # Check if infection spread is stopped
            return
        current_time = pygame.time.get_ticks()
        if current_time - self.infection_timer > 2000:  # Delay of 2 seconds
            self.infect_neighbors()  # Spread infection
            self.infection_timer = current_time  # Reset timer

    def stop_infection(self):
        self.state = False  # Ensure the cell is marked as no longer infectious
        self.health = "dead"  # Update health status
        self.image = pygame.image.load("assets/images/dead_cell_placeholder.png")
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 2.5, self.image.get_height() // 2.5))
        self.infection_timer = None  # Disable infection spread

    def stop_infection_and_neighbors(self):
        self.stop_infection()  # Stop the infection of this cell
        for neighbor in self.neighbors:
            if neighbor.health == "infected":
                # Only stop the spread but do not reset the health or state of infected neighbors
                neighbor.infection_timer = None  # Stop infection spread from this neighbor