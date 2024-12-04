import pygame
from screens.screen_manager import ScreenManager
from introductions.intro1 import Intro1
from levels.level1 import Level1
from screens.controls import ControlsScreen
from screens.about import AboutScreen
from screens.homescreen import HomeScreen
from screens.quizzes import QuizzesScreen
from screens.statistics import StatisticsScreen
from screens.settings import SettingsScreen
from screens.scoreboard import ScoreboardScreen
import os


def main():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
    pygame.display.set_caption("Inside Immune")

    pdf_images = load_pdf_images("assets/introduction-materials/")

    # Create ScreenManager and register all screens
    manager = ScreenManager(screen)
    manager.register_screen("Home", HomeScreen, manager)
    manager.register_screen("Introduction", Intro1, pdf_images, manager)
    manager.register_screen("Level 1", Level1, manager)
    manager.register_screen("Quizzes", QuizzesScreen, manager)
    manager.register_screen("Statistics", StatisticsScreen, manager)
    manager.register_screen("Scoreboard", ScoreboardScreen, manager)
    manager.register_screen("Settings", SettingsScreen, manager)
    manager.register_screen("Controls", ControlsScreen, manager)
    manager.register_screen("About", AboutScreen, manager)

    # Set the starting screen
    manager.set_active_screen("Home")

    sidebar_options = {
        "Introduction": "Introduction",
        "Level 1": "Level 1",
        "Quizzes": "Quizzes",
        "Statistics": "Statistics",
        "Scoreboard": "Scoreboard",
        "Settings": "Settings",
        "Controls": "Controls",
        "About": "About",
    }

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                manager.reposition_active_screen()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    active_screen = manager.active_screen
                    if hasattr(active_screen, "sidebar") and active_screen.sidebar:
                        active_screen.sidebar.toggle()
                        if hasattr(active_screen, "handle_sidebar_toggle"):
                            active_screen.handle_sidebar_toggle()  # Adjust elements for sidebar
            else:
                active_screen = manager.active_screen
                if active_screen:
                    # Check if sidebar is visible and handle option clicks
                    if hasattr(active_screen, "sidebar") and active_screen.sidebar.visible:
                        clicked_option = active_screen.sidebar.handle_event(event)
                        if clicked_option:
                            if clicked_option == "Exit Game":
                                active_screen.sidebar.draw(active_screen.screen, "Exit Game")
                                pygame.display.flip()
                                pygame.time.delay(500)
                                pygame.quit()
                                exit()
                            elif clicked_option in sidebar_options:
                                # Switch to a valid screen
                                manager.set_active_screen(sidebar_options[clicked_option])
                                break
                    else:
                        # Pass event to the active screen if the sidebar isn't handling it
                        active_screen.handle_event(event)

        # Update and draw the active screen
        if manager.active_screen:
            manager.run_active_screen()
            screen.fill((255, 255, 255))  # Clear the screen
            manager.draw_active_screen()

        pygame.display.flip()  # Update the display
        clock.tick(60)

    pygame.quit()
    exit()


def get_sidebar_option(mouse_pos, options_mapping):
    x, y = mouse_pos
    sidebar_width = 400  # Ensure this matches your actual sidebar width
    y_offset = 120  # Starting Y position of the first option
    spacing = 50  # Spacing between each option in the sidebar

    if x < sidebar_width:  # Check if the click is within the sidebar area
        for index, (option_text, screen_name) in enumerate(options_mapping.items()):  # Correct unpacking
            # Define the rectangle for each option
            option_rect = pygame.Rect(20, y_offset + index * spacing, sidebar_width - 40, 30)
            if option_rect.collidepoint(x, y):  # Check if the mouse is within this option's rectangle
                return screen_name
    return None  # Return None if no option was clicked


def load_pdf_images(folder):
    images = []
    for filename in sorted(os.listdir(folder)):
        if filename.endswith(".jpg"):
            image = pygame.image.load(os.path.join(folder, filename)).convert()
            images.append(image)
    return images


if __name__ == "__main__":
    main()