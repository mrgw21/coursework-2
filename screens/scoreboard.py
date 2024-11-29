import pygame
from screens.screen_manager import BaseScreen
from ui.sidebar import Sidebar

class ScoreboardScreen(BaseScreen):
    def __init__(self, screen, manager):
        super().__init__(screen)
        self.manager = manager
        self.title_font = pygame.font.SysFont("Arial", 40)
        self.text_font = pygame.font.SysFont("Arial", 25)

        # Sidebar setup
        self.sidebar = Sidebar()
        self.sidebar.visible = True

        # Dummy scores for demonstration
        self.scores = {
            1: 1500,
            2: 2700,
            3: 3500,
        }

        # Initialize title and row positions
        self.title_position = [screen.get_width() // 2, 50]
        self.row_positions = []
        self.calculate_row_positions()

        self.running = True

    def calculate_row_positions(self):
        sidebar_width = self.sidebar.width if self.sidebar.visible else 0
        center_x = self.screen.get_width() // 2 + (sidebar_width // 2)
        self.row_positions = [
            [center_x - 150, 160 + i * 60] for i in range(len(self.scores))
        ]
        self.title_position[0] = center_x

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_m:  # Toggle sidebar
                        self.sidebar.toggle()
                        self.handle_sidebar_toggle()

                elif event.type == pygame.VIDEORESIZE:
                    self.reposition_elements(event.w, event.h)

                if self.sidebar and self.sidebar.visible and self.sidebar.handle_event(event):
                    mouse_pos = pygame.mouse.get_pos()
                    option_clicked = self.get_sidebar_option(mouse_pos, self.sidebar.options)
                    if option_clicked:
                        self.running = False
                        self.manager.set_active_screen(option_clicked)
                        return

            self.draw()
            pygame.display.flip()

    def draw(self):
        # Determine sidebar width
        sidebar_width = self.sidebar.width if self.sidebar.visible else 0
        center_x = self.screen.get_width() // 2 + (sidebar_width // 2)  # Adjusted center

        # Background
        self.screen.fill((0, 0, 0))  # Black background

        # Title
        title_text = self.title_font.render("Scoreboard", True, (255, 255, 255))
        self.screen.blit(
            title_text,
            title_text.get_rect(center=(center_x, self.title_position[1]))
        )

        # Table headers
        header_font = pygame.font.Font(None, 28)
        level_header = header_font.render("Level", True, (255, 255, 255))
        score_header = header_font.render("Score", True, (255, 255, 255))
        self.screen.blit(level_header, (center_x - 150, 120))
        self.screen.blit(score_header, (center_x + 150, 120))

        # Draw rows for each level
        for idx, (level, score) in enumerate(self.scores.items()):
            row_x = center_x - 150  # Start point adjusted for sidebar
            row_y = 160 + idx * 60  # Dynamic vertical spacing
            level_text = self.text_font.render(f"Level {level}", True, (255, 255, 255))
            score_text = self.text_font.render(str(score), True, (255, 255, 255))

            # Render text
            self.screen.blit(level_text, (row_x, row_y))
            self.screen.blit(score_text, (row_x + 300, row_y))

            # Draw row separator
            pygame.draw.line(
                self.screen,
                (50, 50, 50),
                (row_x - 50, row_y + 40),
                (row_x + 350, row_y + 40),
                2
            )

        # Draw sidebar if visible
        if self.sidebar.visible:
            self.sidebar.draw(self.screen)

    def handle_sidebar_toggle(self):
        self.calculate_row_positions()

    def reposition_elements(self, new_width, new_height):
        self.screen = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)
        self.calculate_row_positions()

    def get_sidebar_option(self, mouse_pos, options):
        y_offset = 120  # Adjust to the starting Y position of options
        spacing = 50  # Space between each option
        for i, option in enumerate(options):
            option_rect = pygame.Rect(20, y_offset + i * spacing, 360, 40)  # Match the sidebar dimensions
            if option_rect.collidepoint(mouse_pos):
                return option
        return None