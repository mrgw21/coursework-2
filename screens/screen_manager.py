import pygame

class BaseScreen:
    def __init__(self, screen):
        self.screen = screen
        self.previous_width = screen.get_width()
        self.previous_height = screen.get_height()

    def run(self):
        raise NotImplementedError("Each screen must implement its own 'run' method.")

    def draw(self):
        raise NotImplementedError("Each screen must implement its own 'draw' method.")

    def handle_event(self, event):
        pass

    def reposition_elements(self):
        new_width = self.screen.get_width()
        new_height = self.screen.get_height()

        width_ratio = new_width / self.previous_width
        height_ratio = new_height / self.previous_height

        self.update_positions(width_ratio, height_ratio)
        self.previous_width = new_width
        self.previous_height = new_height

    def update_positions(self, width_ratio, height_ratio):
        pass


class ScreenManager:
    def __init__(self, screen):
        self.screen = screen
        self.screens = {}
        self.active_screen = None

    def register_screen(self, name, screen_class, *args, **kwargs):
        self.screens[name] = (screen_class, args, kwargs)

    def set_active_screen(self, name):
        if name in self.screens:
            screen_class, args, kwargs = self.screens[name]
            self.active_screen = screen_class(self.screen, *args, **kwargs)
        elif name == "Exit Game":
            pygame.quit()
            exit()
        else:
            raise ValueError(f"Screen '{name}' is not registered.")

    def run_active_screen(self):
        if self.active_screen:
            self.active_screen.run()

    def draw_active_screen(self):
        if self.active_screen:
            self.active_screen.draw()

    def handle_event(self, event):
        if self.active_screen:
            self.active_screen.handle_event(event)

    def reposition_active_screen(self):
        if self.active_screen:
            self.active_screen.reposition_elements()