import pygame
from ui.sidebar import Sidebar
from screens.screen_manager import BaseScreen

class BacteriaScreen(BaseScreen):
    def __init__(self, screen, manager):
        super().__init__(screen)
        self.manager = manager
        self.running = True
        self.completed = False  # To indicate when to switch back
        self.step = 3
        self.sidebar = Sidebar()
        self.font = pygame.font.SysFont("Arial", 24)
        self.title_font = pygame.font.SysFont("Arial", 36, bold=True)

        # Tutorial-specific content
        self.content = [
            "Bacteria are single-celled microorganisms.",
        ]
        self.current_index = 0  # Start with the first page of content

        # Dynamic centering variables
        self.sidebar_width = self.sidebar.width if self.sidebar.visible else 0
        self.content_center = self.calculate_center()

    def calculate_center(self):
        sidebar_width = self.sidebar.width if self.sidebar.visible else 0
        return (
            (self.screen.get_width() - sidebar_width) // 2 + sidebar_width,
            self.screen.get_height() // 2,
        )

    def handle_sidebar_toggle(self):
        self.sidebar_width = self.sidebar.width if self.sidebar.visible else 0
        self.content_center = self.calculate_center()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.completed = True  # Mark as completed to trigger screen switch
                self.running = False
            elif event.key == pygame.K_RIGHT:
                self.current_index = min(self.current_index + 1, len(self.content) - 1)
            elif event.key == pygame.K_LEFT:
                self.current_index = max(self.current_index - 1, 0)
            elif event.key == pygame.K_m:
                self.sidebar.toggle()
                self.handle_sidebar_toggle()  # Adjust content position dynamically
        elif event.type == pygame.MOUSEBUTTONDOWN and self.sidebar.visible:
            option = self.sidebar.get_option_clicked(event.pos)
            if option:
                self.manager.set_active_screen(option)
                self.running = False

    def draw(self):
        self.screen.fill((200, 200, 200))

        # Draw title
        title_text = self.title_font.render("Bacteria Information", True, (0, 0, 0))
        title_rect = title_text.get_rect(center=(self.content_center[0], 100))
        self.screen.blit(title_text, title_rect)

        # Draw content
        content_text = self.font.render(self.content[self.current_index], True, (0, 0, 0))
        content_rect = content_text.get_rect(center=self.content_center)
        self.screen.blit(content_text, content_rect)

        # Draw navigation hints
        nav_hint = self.font.render(
            "Use LEFT/RIGHT arrows to navigate. Press ENTER to return.",
            True,
            (50, 50, 50),
        )
        nav_hint_rect = nav_hint.get_rect(
            center=(self.content_center[0], self.screen.get_height() - 50)
        )
        self.screen.blit(nav_hint, nav_hint_rect)

        # Draw the sidebar if visible
        if self.sidebar.visible:
            self.sidebar.draw(self.screen, "Bacteria Information")

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                self.handle_event(event)

            self.draw()
            pygame.display.flip()