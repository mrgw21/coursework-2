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
            "Game Sound:          ",
            "Screen Mode: ",
        ]
        self.text_positions = []
        self.calculate_text_positions()

        self.audio_on_image = pygame.image.load("assets/icons/audio_on.png")
        self.audio_off_image = pygame.image.load("assets/icons/audio_off.png")
        self.audio_on = True
        self.fullscreen = False  # Default to windowed mode

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
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.is_audio_toggle_clicked(mouse_pos):
                        self.audio_on = not self.audio_on
                        if self.audio_on:
                             pygame.mixer.music.unpause()  #Resume music
                        else:
                            pygame.mixer.music.pause()
                    elif self.is_screen_mode_toggle_clicked(mouse_pos):
                        self.toggle_screen_mode()

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
        sidebar_width = self.sidebar.width if self.sidebar.visible else 0
        center_x = self.screen.get_width() // 2 + (sidebar_width // 2)

        self.screen.fill((255, 255, 255))  # Background
        title_text = self.title_font.render("Settings", True, (0, 0, 0))
        self.screen.blit(title_text, title_text.get_rect(center=(center_x, self.title_position[1])))

        for i, line in enumerate(self.settings_lines):
            text = self.text_font.render(line, True, (0, 0, 0))
            self.screen.blit(text, text.get_rect(center=(self.text_positions[i][0], self.text_positions[i][1])))

        # Draw audio toggle button
        audio_image = self.audio_on_image if self.audio_on else self.audio_off_image
        audio_rect = audio_image.get_rect(center=(self.text_positions[0][0] + 50, self.text_positions[0][1]))
        self.screen.blit(audio_image, audio_rect)

        # Draw screen mode toggle button
        screen_mode_text = "Fullscreen" if self.fullscreen else "Windowed"
        screen_mode_rendered = self.text_font.render(screen_mode_text, True, (0, 0, 255))  # Highlight in blue
        screen_mode_rect = screen_mode_rendered.get_rect(center=(self.text_positions[1][0] + 120, self.text_positions[1][1]))
        self.screen.blit(screen_mode_rendered, screen_mode_rect)

        if self.sidebar.visible:
            self.sidebar.draw(self.screen, "Settings")

    def toggle_screen_mode(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.screen = pygame.display.set_mode(self.screen.get_size(), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.screen.get_size(), pygame.RESIZABLE)

    def is_audio_toggle_clicked(self, mouse_pos):
        audio_image = self.audio_on_image if self.audio_on else self.audio_off_image
        audio_rect = audio_image.get_rect(center=(self.text_positions[0][0] + 50, self.text_positions[0][1]))
        return audio_rect.collidepoint(mouse_pos)

    def is_screen_mode_toggle_clicked(self, mouse_pos):
        screen_mode_text = "Fullscreen" if self.fullscreen else "Windowed"
        screen_mode_rendered = self.text_font.render(screen_mode_text, True, (0, 0, 255))
        screen_mode_rect = screen_mode_rendered.get_rect(center=(self.text_positions[1][0] + 120, self.text_positions[1][1]))
        return screen_mode_rect.collidepoint(mouse_pos)

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