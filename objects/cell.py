import pygame

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
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if self.show_modal:
            self.draw_modal(screen)

    def draw_modal(self, screen):
        """Draw a modal with cell information."""
        screen_width = screen.get_width()
        screen_height = screen.get_height()

        if screen_width > 1200:  # Fullscreen mode
            modal_width = 500
            modal_height = 700
            modal_x = 200
        else:
            modal_width = 300
            modal_height = 500
            modal_x = 20
        modal_y = (screen.get_height() - modal_height) // 2

        # Draw modal background and border
        pygame.draw.rect(screen, (220, 220, 220), (modal_x, modal_y, modal_width, modal_height))
        pygame.draw.rect(screen, (0, 0, 0), (modal_x, modal_y, modal_width, modal_height), 3)

        # Font for text
        font = pygame.font.SysFont('Arial', 20)
        
        # Adjust button size and spacing
        close_button_width = 90
        close_button_height = 25
        close_button_x = modal_x + modal_width - close_button_width - 10
        close_button_y = modal_y + 10

        # Draw the "X (ESC)" text centered within the button area
        close_button_text = font.render("X (ESC)", True, (255, 0, 0))
        text_rect = close_button_text.get_rect(center=(close_button_x + close_button_width // 2, close_button_y + close_button_height // 2))
        screen.blit(close_button_text, text_rect)

        # Draw a red rectangle for visual feedback (optional)
        pygame.draw.rect(screen, (255, 0, 0), (close_button_x, close_button_y, close_button_width, close_button_height), 2)

        # Draw cell information below the close button with spacing
        cell_number_text = f"Cell #{self.cell_number}"
        health_text = f"Health: {self.health}" if self.state else "infected"
        info_text = self.get_info_text()

        # Adjust the starting y-position for content
        content_start_y = close_button_y + close_button_height + 20
        
        # Display cell number, health status, and information with proper spacing
        screen.blit(font.render(cell_number_text, True, (0, 0, 0)), (modal_x + 10, content_start_y))
        screen.blit(font.render(health_text, True, (0, 0, 0)), (modal_x + 10, content_start_y + 30))
        
        # Use text wrapping function to fit info text within the modal
        self.draw_wrapped_text(screen, info_text, font, modal_x + 10, content_start_y + 60, modal_width - 20)

    def draw_wrapped_text(self, screen, text, font, x, y, max_width):
        """Render wrapped text within the specified width."""
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
        """Return cell information for educational purposes."""
        return "Cells protect the body from pathogens."

    def handle_click(self, mouse_pos, cells, level):
        """Check if the cell is clicked and toggle the modal."""
        if self.rect.collidepoint(mouse_pos):
            # Close all other cells' modals
            for cell in cells:
                if cell != self:
                    cell.show_modal = False

            self.show_modal = not self.show_modal
            level.paused = self.show_modal  # Pause the game if the modal is open

    def handle_modal_close(self, mouse_pos, level):
        """Close modal if the close button is clicked."""
        modal_width = 300
        modal_height = 500
        modal_x = 20
        modal_y = (pygame.display.get_surface().get_height() - modal_height) // 2

        close_button_width = 90
        close_button_height = 25
        close_button_x = modal_x + modal_width - close_button_width - 10
        close_button_y = modal_y + 10

        # Check if the mouse click is within the close button area
        if close_button_x <= mouse_pos[0] <= close_button_x + close_button_width and \
        close_button_y <= mouse_pos[1] <= close_button_y + close_button_height:
            self.show_modal = False
            level.paused = False

    def handle_keydown(self, key, level):
        if key == pygame.K_ESCAPE and self.show_modal:
            self.show_modal = False
            # Only unpause if the game was paused because of the modal
            if level.paused:
                level.paused = False