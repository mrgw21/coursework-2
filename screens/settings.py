import pygame

from screens.screen_manager import BaseScreen
from ui.sidebar import Sidebar

class SettingsScreen(BaseScreen):
    def __init__(self, screen, manager):
        super().__init__(screen)
        self.manager = manager
        self.title_font = pygame.font.SysFont("Arial", 40, bold=True)
        self.text_font = pygame.font.SysFont("Arial", 25)
        self.sidebar = Sidebar()
        self.sidebar.visible = True

        self.title_position = [screen.get_width() // 2, 100]
        self.settings_lines = [
            "Audio: On/Off",
            "Screen Mode: Fullscreen/Windowed",
        ]
        self.text_positions = []
        self.calculate_text_positions()

        self.running = True

    def calculate_text_positions(self):
        sidebar_width = self.sidebar.width if self.sidebar.visible else 0
        center_x = self.screen.get_width() // 2 + (sidebar_width // 2)

        self.title_position[0] = center_x
        self.text_positions = [
            [center_x, 200 + i * 40] for i in range(len(self.settings_lines))
        ]

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_m:
                        self.sidebar.toggle()
                        self.handle_sidebar_toggle()

                elif event.type == pygame.VIDEORESIZE:
                    self.reposition_elements(event.w, event.h)

                if self.sidebar and self.sidebar.visible and self.sidebar.handle_event(event):
                    mouse_pos = pygame.mouse.get_pos()
                    option_clicked = self.get_sidebar_option(mouse_pos, self.sidebar.options)
                    if option_clicked:
                        self.running = False
                        if option_clicked == "Introduction":
                            option_clicked = "Preliminary"
                        self.manager.set_active_screen(option_clicked)
                        return

            self.draw()
            pygame.display.flip()

    def draw(self):
        sidebar_width = self.sidebar.width if self.sidebar.visible else 0
        center_x = self.screen.get_width() // 2 + (sidebar_width // 2)

        self.screen.fill((255, 255, 255))  # Background
        title_text = self.title_font.render("Settings", True, (0, 0, 0))
        self.screen.blit(title_text, title_text.get_rect(center=(center_x, self.title_position[1])))

        for i, line in enumerate(self.settings_lines):
            text = self.text_font.render(line, True, (0, 0, 0))
            self.screen.blit(text, text.get_rect(center=(self.text_positions[i][0], self.text_positions[i][1])))

        if self.sidebar.visible:
            self.sidebar.draw(self.screen, "Settings")

    def handle_sidebar_toggle(self):
        self.calculate_text_positions()

    def reposition_elements(self, new_width, new_height):
        old_width, old_height = self.screen.get_size()
        width_ratio = new_width / old_width
        height_ratio = new_height / old_height

        self.screen = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)

        self.title_position[0] = int(self.title_position[0] * width_ratio)
        self.title_position[1] = int(self.title_position[1] * height_ratio)

        self.text_positions = [
            [int(pos[0] * width_ratio), int(pos[1] * height_ratio)]
            for pos in self.text_positions
        ]
    
    def get_sidebar_option(self, mouse_pos, options):
        y_offset = 120  # Adjust to the starting Y position of options
        spacing = 50  # Space between each option
        for i, option in enumerate(options):
            option_rect = pygame.Rect(20, y_offset + i * spacing, 360, 40)  # Match the sidebar dimensions
            if option_rect.collidepoint(mouse_pos):
                return option
        return None