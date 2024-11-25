import pygame

class Sidebar:
    def __init__(self, options, font):
        self.width = 400
        self.options = options
        self.visible = True
        self.font = font
        self.title_font = pygame.font.SysFont("Arial", 30, bold=True)

    def draw(self, screen):
        if not self.visible:
            return
        # Background
        pygame.draw.rect(screen, (220, 220, 220), (0, 0, self.width, screen.get_height()))
        # Title
        title = self.title_font.render("Inside Immune", True, (0, 0, 0))
        screen.blit(title, (20, 20))
        title = self.title_font.render("Menu", True, (0, 0, 0))
        screen.blit(title, (20, 60))
        # Options
        y_offset = 100
        for i, option in enumerate(self.options):
            color = (0, 0, 0)
            text = self.font.render(option, True, color)
            screen.blit(text, (20, y_offset + i * 40))

    def toggle(self):
        self.visible = not self.visible