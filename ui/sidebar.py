import pygame

class Sidebar:
    def __init__(self, options, font):
        self.width = 400
        self.options = options
        self.visible = True
        self.font = font
        self.title_font = pygame.font.SysFont("Arial", 40, bold=True)
        self.menu_font = pygame.font.SysFont("Arial", 25, bold=True)

    def draw(self, screen):
        if not self.visible:
            return

        # Background
        pygame.draw.rect(screen, (0, 153, 153), (0, 0, self.width, screen.get_height()))

        # Title
        title = self.title_font.render("Inside Immune", True, (255, 255, 255))
        screen.blit(title, (20, 20))

        menu_title = self.menu_font.render("Menu", True, (255, 255, 255))
        screen.blit(menu_title, (20, 70))  # Add some padding below the first title

        # Options
        y_offset = 120  # Start below the titles with some padding
        spacing = 50  # Space between each menu option
        for i, option in enumerate(self.options):
            color = (255, 255, 255)
            text = self.font.render(option, True, color)
            screen.blit(text, (20, y_offset + i * spacing))

    def toggle(self):
        self.visible = not self.visible

    def handle_event(self, event):
        if not self.visible:
            return False  # Sidebar is hidden, so don't handle the event

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if mouse_pos[0] < self.width:  # Click is inside the sidebar
                y_offset = 100
                for i, option in enumerate(self.options):
                    option_rect = pygame.Rect(20, y_offset + i * 40, self.width - 40, 30)
                    if option_rect.collidepoint(mouse_pos):
                        # Handle sidebar actions here
                        return True  # Event handled by the sidebar
        return False  # Sidebar didn't handle the event