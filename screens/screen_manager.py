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
        print(f"[DEBUG] Registered screen: {name}")

    def set_active_screen(self, name):
        if name in self.screens:
            screen_class, args, kwargs = self.screens[name]
            print(f"[DEBUG] Switching to screen: {name}")
            self.active_screen = screen_class(self.screen, *args, **kwargs)
            if hasattr(self.active_screen, "run"):
                print(f"[DEBUG] Active screen set to: {type(self.active_screen).__name__}")
            else:
                print(f"[ERROR] Screen '{name}' does not have a 'run' method.")
        elif name == "Exit Game":
            print("[DEBUG] Exiting game.")
        else:
            raise ValueError(f"Screen '{name}' is not registered.")

    def run_active_screen(self):
        if self.active_screen:
            print(f"[DEBUG] Running screen: {type(self.active_screen).__name__}")
            self.active_screen.run()

    def draw_active_screen(self):
        if self.active_screen:
            print(f"[DEBUG] Drawing screen: {type(self.active_screen).__name__}")
            self.active_screen.draw()

    def handle_event(self, event):
        if self.active_screen:
            print(f"[DEBUG] Handling event in screen: {type(self.active_screen).__name__}")
            self.active_screen.handle_event(event)

    def reposition_active_screen(self):
        if self.active_screen:
            print(f"[DEBUG] Repositioning elements in screen: {type(self.active_screen).__name__}")
            self.active_screen.reposition_elements()