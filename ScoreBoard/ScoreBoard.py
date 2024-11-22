import pygame

# Initialize Pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Scoreboard Table")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)

# Define the ScoreboardScreen class
class ScoreboardScreen:
    def __init__(self, scores, font_size=36):
        """
        Initialize the scoreboard screen.
        :param scores: A dictionary with levels and corresponding scores.
        :param font_size: Size of the font for the text.
        """
        self.scores = scores
        self.font = pygame.font.Font(None, font_size)

    def draw(self, surface):
        """
        Draw the scoreboard table on the given surface.
        :param surface: The Pygame surface to draw on (e.g., the screen).
        """
        surface.fill(BLACK)  # Clear the screen with black

        # Title
        title_text = self.font.render("Scoreboard", True, WHITE)
        surface.blit(title_text, (300, 50))  # Center the title

        # Table headers
        header_font = pygame.font.Font(None, 28)
        level_header = header_font.render("Level", True, WHITE)
        score_header = header_font.render("Score", True, WHITE)
        surface.blit(level_header, (200, 120))
        surface.blit(score_header, (500, 120))

        # Draw rows for each level
        row_y = 160
        for level, score in self.scores.items():
            level_text = self.font.render(f"Level {level}", True, WHITE)
            score_text = self.font.render(str(score), True, WHITE)

            surface.blit(level_text, (200, row_y))
            surface.blit(score_text, (500, row_y))

            # Draw row separator
            pygame.draw.line(surface, GRAY, (150, row_y + 40), (650, row_y + 40), 2)

            row_y += 60

        # Back button
        back_text = header_font.render("Press 'B' to return to game", True, WHITE)
        surface.blit(back_text, (300, 500))


# Dummy scores for demonstration
scores = {
    1: 1500,
    2: 2700,
    3: 3500,
}

# Create the scoreboard screen instance
scoreboard_screen = ScoreboardScreen(scores)

# Main game loop
running = True
show_scoreboard = True  # Toggle to show the scoreboard
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Check for key press to toggle scoreboard
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:  # Return to game
                show_scoreboard = False

    if show_scoreboard:
        scoreboard_screen.draw(screen)
    else:
        screen.fill(BLACK)
        back_text = pygame.font.Font(None, 36).render(
            "Game Screen: Press 'S' to view scoreboard", True, WHITE
        )
        screen.blit(back_text, (100, 250))

        # Toggle back to scoreboard
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:  # Show scoreboard
                show_scoreboard = True

    pygame.display.flip()
    clock.tick(60)

pygame.quit()