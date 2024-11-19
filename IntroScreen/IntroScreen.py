import pygame
import sys
import os

pygame.init()

#ScreenSettings
WIDTH, HEIGHT = 800, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Inside Immunity")

#Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#Fonts
TITLE_FONT = pygame.font.Font(None, 80)
TEXT_FONT = pygame.font.Font(None, 40)

# IntroScreen Slides
def load_pdf_images(folder):
    images = []
    for filename in sorted(os.listdir(folder)):
        if filename.endswith(".jpg"):
            image = pygame.image.load(os.path.join(folder, filename)).convert()
            image = pygame.transform.scale(image, (WIDTH, HEIGHT))
            images.append(image)
    return images

pdf_images = load_pdf_images(".")

class Screen:
    def __init__(self):
        self.next_screen = None

    def handle_events(self, events):
        pass

    def update(self):
        pass

    def draw(self, surface):
        pass

#Screen 1 - Intro Screen
class IntroScreen(Screen):
    def __init__(self, pdf_images):
        super().__init__()
        self.pdf_images = pdf_images
        self.current_page = 0

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    # Go to the next page
                    if self.current_page < len(self.pdf_images) - 1:
                        self.current_page += 1
                elif event.key == pygame.K_LEFT:
                    # Go to the previous page
                    if self.current_page > 0:
                        self.current_page -= 1
                elif event.key == pygame.K_RETURN:
                    self.next_screen = ControlsScreen()

    def draw(self, surface):
        surface.blit(self.pdf_images[self.current_page], (0, 0))
        draw_text("Use LEFT/RIGHT arrows to navigate", TEXT_FONT, BLACK, surface, WIDTH // 2, HEIGHT - 50)
        draw_text("Press ENTER to continue", TEXT_FONT, BLACK, surface, WIDTH // 2, HEIGHT - 20)

#Screen 2 - Controls Screen
class ControlsScreen(Screen):
    def __init__(self):
        super().__init__()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.next_screen = GameScreen()

    def draw(self, surface):
        surface.fill(BLACK)
        draw_text("Controls Screen", TEXT_FONT, WHITE, surface, WIDTH // 2, HEIGHT // 2)
        draw_text("Use [W] [A] [S] [D]", TEXT_FONT, WHITE, surface, WIDTH // 2, HEIGHT // 2 + 50)
        draw_text("Use POINTER to click on the INFECTED Cells ", TEXT_FONT, WHITE, surface, WIDTH // 2, HEIGHT // 2 + 100)
        draw_text("Press ENTER to start the game", TEXT_FONT, WHITE, surface, WIDTH // 2, HEIGHT // 2 + 150)

#Screen 3 - Game Code
class GameScreen(Screen):
    def __init__(self):
        super().__init__()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    def draw(self, surface):
        surface.fill(BLACK)
        draw_text("Game Screen", TEXT_FONT, WHITE, surface, WIDTH // 2, HEIGHT // 2)
        draw_text("Press ESC to quit", TEXT_FONT, WHITE, surface, WIDTH // 2, HEIGHT // 2 + 50)

# Helper function to draw text
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

#Main
class Game:
    def __init__(self, pdf_images):
        self.current_screen = IntroScreen(pdf_images)

    def run(self):
        clock = pygame.time.Clock()

        while True:
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.current_screen.handle_events(events)
            self.current_screen.update()
            self.current_screen.draw(SCREEN)

            if self.current_screen.next_screen:
                self.current_screen = self.current_screen.next_screen

            # Update the display
            pygame.display.flip()
            clock.tick(60)

#Run
if __name__ == "__main__":
    pdf_images = load_pdf_images(".")
    game = Game(pdf_images)
    game.run()