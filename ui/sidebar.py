import pygame

class Sidebar:
    def __init__(self):
        self.width = 400
        self.options = ["Home", "Introduction", "Level 1", "Quizzes", "Statistics", "Scoreboard", "Settings", "Controls", "About", "Exit Game"]
        self.visible = True
        self.title_font = pygame.font.SysFont("Arial", 40, bold=True)
        self.menu_font = pygame.font.SysFont("Arial", 25, bold=True)
        self.font = pygame.font.SysFont("Arial", 24)

    def draw(self, screen, current_screen, clicked_option=None):
        if not self.visible:
            return

        # Background
        pygame.draw.rect(screen, (0, 153, 153), (0, 0, self.width, screen.get_height()))

        # Title
        title = self.title_font.render("Inside Immune", True, (255, 255, 255))
        screen.blit(title, (20, 40))

        # menu_title = self.menu_font.render("Menu", True, (255, 255, 255))
        # screen.blit(menu_title, (20, 70))  # Add some padding below the first title

        # Options
        y_offset = 120  # Start below the titles with some padding
        spacing = 50  # Space between each menu option
        for i, option in enumerate(self.options):
            if option == clicked_option:
                font = self.menu_font  # Use bold font for clicked option
                color = (255, 215, 0)  # Golden yellow for clicked option
            elif option == current_screen:
                font = self.menu_font  # Bold the current screen
                color = (0, 0, 0)  # Black for current screen
            else:
                font = self.font  # Regular font for others
                color = (255, 255, 255)  # White for others

            text = font.render(option, True, color)
            screen.blit(text, (20, y_offset + i * spacing))

    def toggle(self):
        self.visible = not self.visible

    def handle_event(self, event):
        if not self.visible or event.type != pygame.MOUSEBUTTONDOWN:
            return None
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_x < self.width:  # Check if the click is within the sidebar
            y_offset = 120  # Starting Y position of options
            for i, option in enumerate(self.options):
                option_rect = pygame.Rect(20, y_offset + i * 50, self.width - 40, 30)
                if option_rect.collidepoint(mouse_x, mouse_y):
                    return option  # Return the clicked option text
        return None