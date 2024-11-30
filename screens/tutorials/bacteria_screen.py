# screens/tutorials/bacteria_screen.py
import pygame
from screens.screen_manager import BaseScreen


class BacteriaScreen(BaseScreen):
    def __init__(self, screen, manager):
        super().__init__(screen)
        self.manager = manager
        self.running = True

        # Background color or image
        self.background_color = (230, 230, 250)  # Light lavender background
        self.title_font = pygame.font.SysFont("Arial", 36)
        self.content_font = pygame.font.SysFont("Arial", 20)

        # Button for returning to the game
        self.button_font = pygame.font.SysFont("Arial", 24)
        self.button_text = "Back to Game"
        self.button_width = 200
        self.button_height = 50
        self.button_color = (200, 50, 50)
        self.button_hover_color = (255, 80, 80)
        self.button_rect = pygame.Rect(
            (self.screen.get_width() - self.button_width) // 2,
            self.screen.get_height() - 100,
            self.button_width,
            self.button_height,
        )

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.manager.set_active_screen("level1")  # Return to the game
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.button_rect.collidepoint(mouse_pos):
                self.manager.set_active_screen("level1")  # Return to the game

    def draw(self):
        # Background
        self.screen.fill(self.background_color)

        # Title
        title_text = self.title_font.render("Bacteria Tutorial", True, (50, 50, 50))
        self.screen.blit(
            title_text,
            ((self.screen.get_width() - title_text.get_width()) // 2, 50),
        )

        # Content
        content_lines = [
            "Bacteria are single-celled microorganisms.",
            "Some bacteria are harmful and can cause infections.",
            "Others are beneficial and help with digestion and immunity.",
            "In this game, bacteria are oval-shaped pathogens.",
        ]
        y_offset = 150
        for line in content_lines:
            content_text = self.content_font.render(line, True, (50, 50, 50))
            self.screen.blit(content_text, (50, y_offset))
            y_offset += 30

        # Button
        mouse_pos = pygame.mouse.get_pos()
        if self.button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, self.button_hover_color, self.button_rect)
        else:
            pygame.draw.rect(self.screen, self.button_color, self.button_rect)

        button_text = self.button_font.render(self.button_text, True, (255, 255, 255))
        self.screen.blit(
            button_text,
            (
                self.button_rect.centerx - button_text.get_width() // 2,
                self.button_rect.centery - button_text.get_height() // 2,
            ),
        )

    def run(self):
        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)

            self.draw()
            pygame.display.flip()