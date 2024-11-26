import pygame
import random
import platform
from objects.cell import Cell
from objects.macrophage import Macrophage
from objects.pathogen import Pathogen
from data.quizzes import quizzes
from ui.sidebar import Sidebar
from ui.timer import Timer
from objects.oracle import Oracle

class Level1:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False
        self.fullscreen = False

        self.sidebar_width = 400
        self.sidebar = Sidebar(options=["Introduction", "Level 1", "Level 2", "Level 3", "Quizzes", "Statistics", "Settings", "Controls", "About"], font=pygame.font.SysFont("Arial", 24))

        self.body_image = pygame.image.load('assets/images/final/body.png')
        screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h
        self.macrophage = Macrophage(screen_width, screen_height, sidebar_width=self.sidebar_width)

        self.game_width = screen_width - self.sidebar_width
        self.game_center_x = self.game_width // 2 + self.sidebar_width // 2
        self.cells = [Cell(i) for i in range(37)] 

        self.oracle = Oracle(self.sidebar_width)

        random.shuffle(quizzes)
        quiz_index = 0
        for cell in self.cells:
            cell.quiz = quizzes[quiz_index]
            quiz_index += 1
            if quiz_index >= len(quizzes):
                quiz_index = 0

        self.assign_neighbors()

        self.enemies = []

        self.spawn_timer = 0
        self.spawn_interval = 2000
        self.resize_pause_timer = 0
        self.resize_pause_duration = 2000 
        self.counter = 0

        self.start_time = pygame.time.get_ticks()
        self.pause_start = None  # To track when the game was paused
        self.total_paused_time = 0  # Total time paused
        self.win_time = 30000  # 30 seconds in milliseconds

        self.game_over = False
        self.win = True

        self.timer = Timer(font=pygame.font.SysFont("Arial", 24))

        self.previous_width, self.previous_height = screen.get_width(), screen.get_height()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                """
                if event.type == pygame.FULLSCREEN:
                    pygame.display.flip()
                """

                # Pass event to sidebar first if it's visible
                if self.sidebar.visible and self.sidebar.handle_event(event):
                    continue  # Skip other event handling if the sidebar handles the event

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        self.toggle_fullscreen()
                    elif event.key == pygame.K_m:  # Toggle sidebar
                        self.sidebar.toggle()
                        self.handle_sidebar_toggle()
                    if event.key == pygame.K_ESCAPE and self.paused:
                        for cell in self.cells:
                            if cell.show_modal:
                                cell.show_modal = False
                        self.paused = False
                    if event.key == pygame.K_SPACE and self.game_over:
                        self.reset_game()
                
                if event.type == pygame.VIDEORESIZE:
                    if not self.fullscreen:
                        self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                        self.reposition_macrophage()
                        self.reposition_pathogens()
                        self.resize_pause_timer = pygame.time.get_ticks()
                
                if event.type == pygame.MOUSEMOTION:
                    mouse_pos = pygame.mouse.get_pos()
                    self.oracle.handle_hover(mouse_pos)
                
                if event.type == pygame.MOUSEBUTTONUP:
                    self.oracle.reset_image()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    modal_active = any(cell.show_modal for cell in self.cells)
                    pause_button_rect = pygame.Rect(self.screen.get_width() - 60, 20, 40, 40)

                    # Pause/Play Button Handling
                    if pause_button_rect.collidepoint(mouse_pos):
                        # Toggle pause state
                        self.paused = not self.paused

                        # Close all modals if unpausing
                        if not self.paused and modal_active:
                            for cell in self.cells:
                                if cell.show_modal:
                                    cell.show_modal = False
                                    break

                        continue  # Skip further processing for this click

                    # Block all interactions if paused, except with the pause/play button and opening oracle
                    if self.paused and not modal_active:
                        self.oracle.handle_click(mouse_pos, self.cells, self)
                        continue  # Ignore all other clicks while paused

                    # If a quiz modal is open, prioritize modal interactions
                    if modal_active:
                        for cell in self.cells:
                            if cell.show_modal:
                                cell.handle_radio_button_click(self.screen, mouse_pos, self.cells, self)
                        continue  # Skip further processing for this click

                    # Allow Oracle interaction only if no quiz modal is open
                    self.oracle.handle_click(mouse_pos, self.cells, self)

                    # Handle cell clicks
                    for cell in self.cells:
                        cell.handle_click(mouse_pos, self.cells, self)

                    # Update paused state based on active modals
                    self.paused = any(cell.show_modal for cell in self.cells)
            
            if not self.paused and self.game_over:
                self.check_game_over()

            if self.paused:
                if self.pause_start is None:
                    self.pause_start = pygame.time.get_ticks()
            else:
                if self.pause_start is not None:
                    # Account for modal pause duration in total paused time
                    self.total_paused_time += pygame.time.get_ticks() - self.pause_start
                    self.pause_start = None

            if not self.paused and not self.game_over:
                self.check_game_over()
                # Dynamically calculate the center of the screen
                self.game_center_x = (self.game_width // 2) + (self.sidebar_width // 2)

                self.screen.fill((255, 255, 255))
                self.clock.tick(60)

                for cell in self.cells:
                    cell.update_infection()

                # Spawn enemies
                self.spawn_enemy()
                self.macrophage.update(self.screen.get_width(), self.screen.get_height(), self.sidebar.width if self.sidebar.visible else 25)
                self.check_collisions()

                # Move enemies towards the dynamically calculated center and the current cell
                if self.counter < len(self.cells):
                    current_cell = self.cells[self.counter]
                    for enemy in self.enemies:
                        # Pass center coordinates and the current cell as arguments
                        if enemy.move_towards_target(self.game_center_x, self.screen.get_height() // 2, current_cell):
                            self.counter += 1
            
            if self.paused:
                if self.pause_start is None:
                    self.pause_start = pygame.time.get_ticks()
            else:
                if self.pause_start is not None:
                    self.total_paused_time += pygame.time.get_ticks() - self.pause_start
                    self.pause_start = None

            self.handle_feedback_closure()

            self.draw()

            if self.game_over:
                self.show_game_over_screen()
            
            pygame.display.flip()  # Update the screen with the new drawing
    
    def assign_neighbors(self):
        # Diamond layout (row-based)
        row_layout = [3, 5, 7, 7, 7, 5, 3]  # Rows of cells
        grid = []  # Flattened grid of cells for indexing
        index = 0

        for row_count in row_layout:
            grid.append(self.cells[index:index + row_count])
            index += row_count

        for row_idx, row in enumerate(grid):
            for col_idx, cell in enumerate(row):
                neighbors = []
                # Define potential neighbor directions in diamond pattern
                directions = [
                    (-1, -1), (-1, 0), (0, -1), (0, 1), (1, 0), (1, 1)
                ]

                for dr, dc in directions:
                    r, c = row_idx + dr, col_idx + dc
                    if 0 <= r < len(grid) and 0 <= c < len(grid[r]):
                        neighbors.append(grid[r][c])
                
                cell.neighbors = neighbors

    def handle_sidebar_toggle(self):
        sidebar_width = self.sidebar.width if self.sidebar.visible else 25
        self.game_width = self.screen.get_width() - sidebar_width
        self.game_center_x = sidebar_width + self.game_width // 2
        
        self.reposition_macrophage()
        self.reposition_pathogens()
        self.oracle.set_position()

        # Ensure any open modals are correctly repositioned
        for cell in self.cells:
            if cell.show_modal:
                cell.modal_position_updated = True  # Add flag to trigger reposition logic in draw_modal

        self.draw() # Redraw elements with updated positions

    def toggle_fullscreen(self):
        if platform.system() == "Darwin":
            # For macOS, handle fullscreen with NOFRAME to avoid issues
            flags = pygame.FULLSCREEN | pygame.NOFRAME if not self.fullscreen else pygame.RESIZABLE
        else:
            flags = pygame.FULLSCREEN if not self.fullscreen else pygame.RESIZABLE
        self.screen = pygame.display.set_mode((0, 0), flags)
        self.fullscreen = not self.fullscreen
    
    def reposition_macrophage(self):
        sidebar_width = self.sidebar.width if self.sidebar.visible else 25
        new_game_width = self.screen.get_width() - sidebar_width
        new_screen_height = self.screen.get_height()

        # Calculate relative position within the old dimensions
        old_game_width = self.previous_width - self.sidebar_width
        old_screen_height = self.previous_height

        # Ensure the old dimensions are non-zero to prevent division errors
        if old_game_width > 0 and old_screen_height > 0:
            relative_x = (self.macrophage.rect.centerx - self.sidebar_width) / old_game_width
            relative_y = self.macrophage.rect.centery / old_screen_height

            # Adjust the new position relative to the resized game area
            self.macrophage.rect.centerx = int(sidebar_width + relative_x * new_game_width)
            self.macrophage.rect.centery = int(relative_y * new_screen_height)
        else:
            # Fallback to center the macrophage if old dimensions are zero (initialization case)
            self.macrophage.rect.centerx = sidebar_width + new_game_width // 2
            self.macrophage.rect.centery = new_screen_height // 2

        # Update previous dimensions
        self.previous_width = self.screen.get_width()
        self.previous_height = self.screen.get_height()
        self.sidebar_width = sidebar_width

    def reposition_pathogens(self):
        sidebar_width = self.sidebar.width if self.sidebar.visible else 25
        new_game_width = self.screen.get_width() - sidebar_width
        new_screen_height = self.screen.get_height()

        old_game_width = self.previous_width - self.sidebar_width
        old_screen_height = self.previous_height

        if old_game_width > 0 and old_screen_height > 0:
            width_ratio = new_game_width / old_game_width
            height_ratio = new_screen_height / old_screen_height

            for pathogen in self.enemies:
                # Dynamically reposition each pathogen
                pathogen.reposition(sidebar_width, width_ratio, height_ratio)

        # Ensure pathogens outside bounds after repositioning are adjusted
        for pathogen in self.enemies:
            if pathogen.rect.left < sidebar_width:
                pathogen.rect.left = sidebar_width + 20  # Offset slightly outside the sidebar

        # Update previous dimensions
        self.previous_width = self.screen.get_width()
        self.previous_height = self.screen.get_height()
    
    def generate_spawn_location(self):
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        # Define padding for edges
        edge_padding = 100
        sidebar_width = self.sidebar.width if self.sidebar.visible else 25

        # Dynamically calculate gray area dimensions based on screen size
        modal_width = int(screen_width * 0.6)  # Adjusted to 60% of screen width
        modal_height = int(screen_height * 0.6)  # Adjusted to 60% of screen height
        center_x = sidebar_width + (screen_width - sidebar_width) // 2
        center_y = screen_height // 2

        # Gray area boundaries
        gray_left = center_x - modal_width // 2
        gray_right = center_x + modal_width // 2
        gray_top = center_y - modal_height // 2
        gray_bottom = center_y + modal_height // 2

        while True:
            # Generate a random spawn location within the valid game bounds
            x = random.randint(sidebar_width + edge_padding, screen_width - edge_padding)
            y = random.randint(edge_padding, screen_height - edge_padding)

            # Ensure spawn location is outside the gray center area and sidebar
            if not (gray_left <= x <= gray_right and gray_top <= y <= gray_bottom):
                return [x, y]

    def spawn_enemy(self):
        if pygame.time.get_ticks() - self.resize_pause_timer < self.resize_pause_duration:
            return
        
        if pygame.time.get_ticks() - self.spawn_timer > self.spawn_interval:
            spawn_location = self.generate_spawn_location()
            if random.choice([True, False]):
                # Bacteria
                self.enemies.append(Pathogen(spawn_location[0], spawn_location[1], "bacteria"))
            else:
                # Virus
                self.enemies.append(Pathogen(spawn_location[0], spawn_location[1], "virus"))
            self.spawn_timer = pygame.time.get_ticks()
    
    def check_collisions(self):
        for enemy in self.enemies[:]:
            # Check collision with macrophage
            if self.macrophage.get_collision_rect().colliderect(enemy.get_collision_rect()):
                if enemy.target_cell and not enemy.target_cell.state:  # Attacking an infected cell
                    if enemy.attack_infected_cell():  # Delay attacks
                        self.enemies.remove(enemy)  # Remove pathogen after attack
                else:
                    self.enemies.remove(enemy)  # Normal attack speed for healthy cells

            # Check collision with cells
            for cell in self.cells:
                if enemy.get_collision_rect().colliderect(cell.rect) and cell.state:
                    cell.die()  # Infect the cell
                    self.enemies.remove(enemy)
                    break
    
    def check_for_open_modal(self):
        for cell in self.cells:
            if cell.show_modal:
                return True
        return False

    def check_game_over(self):
        # Calculate elapsed time considering paused duration
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.start_time - self.total_paused_time

        # Check if the game timer has run out
        time_up = elapsed_time >= self.win_time

        # Check if all cells are infected
        all_infected = all(not cell.state for cell in self.cells)

        # Determine win or lose based on the above conditions
        if all_infected:
            # Player loses if all cells are infected
            self.game_over = True
            self.win = False
        elif time_up:
            # Player wins if time is up and at least one cell is healthy
            self.game_over = True
            self.win = True

        # Pause the game if it's over
        if self.game_over:
            self.paused = True

    def show_game_over_screen(self):
        sidebar_width = self.sidebar.width if self.sidebar.visible else 25
        game_width = self.screen.get_width() - sidebar_width
        game_center_x = sidebar_width + game_width // 2
        game_center_y = self.screen.get_height() // 2

        modal_width, modal_height = 700, 300
        modal_x = game_center_x - modal_width // 2
        modal_y = game_center_y - modal_height // 2

        pygame.draw.rect(self.screen, (220, 220, 220), (modal_x, modal_y, modal_width, modal_height))
        pygame.draw.rect(self.screen, (0, 0, 0), (modal_x, modal_y, modal_width, modal_height), 5)

        font_large = pygame.font.SysFont('Arial', 48)
        font_small = pygame.font.SysFont('Arial', 24)

        current_y = modal_y + 50

        if self.win:
            line1_text = font_large.render("Congratulations!", True, (0, 0, 0))
            line1_rect = line1_text.get_rect(center=(modal_x + modal_width // 2, current_y))
            self.screen.blit(line1_text, line1_rect)
            current_y += 60

            line2_text = font_large.render("You Won!", True, (0, 0, 0))
            line2_rect = line2_text.get_rect(center=(modal_x + modal_width // 2, current_y))
            self.screen.blit(line2_text, line2_rect)
            current_y += 80
        else:
            line1_text = font_large.render("Game Over!", True, (0, 0, 0))
            line1_rect = line1_text.get_rect(center=(modal_x + modal_width // 2, current_y))
            self.screen.blit(line1_text, line1_rect)
            current_y += 60

            line2_text = font_large.render("You Lost!", True, (0, 0, 0))
            line2_rect = line2_text.get_rect(center=(modal_x + modal_width // 2, current_y))
            self.screen.blit(line2_text, line2_rect)
            current_y += 80

        restart_text = font_small.render("Press SPACE to restart", True, (0, 0, 0))
        restart_text_rect = restart_text.get_rect(center=(modal_x + modal_width // 2, current_y))
        self.screen.blit(restart_text, restart_text_rect)

        pygame.display.flip()

    
    def reset_game(self):
        # Reset cells
        self.cells = [Cell(i) for i in range(37)]
        self.assign_neighbors()

        # Clear existing enemies
        self.enemies = []

        # Reset quizzes for cells
        random.shuffle(quizzes)
        quiz_index = 0
        for cell in self.cells:
            cell.quiz = quizzes[quiz_index]
            quiz_index += 1
            if quiz_index >= len(quizzes):
                quiz_index = 0

        # Reset infection state
        for cell in self.cells:
            cell.state = True
            cell.health = "uninfected"
            cell.image = pygame.image.load("assets/images/final/uninfected_cell.png")
            cell.image = pygame.transform.scale(cell.image, (cell.image.get_width() // 20, cell.image.get_height() // 20))
            cell.infection_timer = 0  # Reset infection timer

        # Reset sidebar and game center
        sidebar_width = self.sidebar.width if self.sidebar.visible else 25
        self.game_width = self.screen.get_width() - sidebar_width
        self.game_center_x = sidebar_width + self.game_width // 2

        # Reset macrophage position
        self.macrophage.set_initial_position(self.screen.get_width(), self.screen.get_height(), sidebar_width)

        # Reset game timers and state
        self.start_time = pygame.time.get_ticks()
        self.total_paused_time = 0
        self.pause_start = None
        self.spawn_timer = 0
        self.counter = 0
        self.game_over = False
        self.win = True
        self.paused = False
        self.remaining_time = self.win_time // 1000

    def countdown_before_resume(self):
        font = pygame.font.SysFont('Arial', 48)
        for i in range(3, 0, -1):
            self.screen.fill((255, 255, 255))
            text = font.render(str(i), True, (255, 0, 0))
            self.screen.blit(text, (self.screen.get_width() // 2, 50))
            pygame.display.flip()
            pygame.time.delay(500)
        self.paused = False

    def handle_feedback_closure(self):
        current_time = pygame.time.get_ticks()
        for cell in self.cells:
            if cell.show_modal and hasattr(cell, "feedback_timer") and cell.feedback_timer:
                if current_time - cell.feedback_timer > 1200:  # 1.2 seconds
                    cell.show_modal = False  # Close modal
                    cell.feedback_timer = None  # Reset timer
                    # Update total paused time to exclude the modal duration
                    if self.pause_start is not None:
                        self.total_paused_time += pygame.time.get_ticks() - self.pause_start
                        self.pause_start = None
                    self.paused = False  # Unpause game
        
    def draw(self):
        # Determine sidebar width dynamically
        sidebar_width = self.sidebar.width if self.sidebar.visible else 25

        # Adjust the center and game area for the sidebar
        game_width = self.screen.get_width() - sidebar_width
        center_x = sidebar_width + game_width // 2  # Center within the adjusted game area
        center_y = self.screen.get_height() // 2

        # Fill the screen background
        self.screen.fill((255, 255, 255))

        # Adjust body image placement
        img = self.body_image
        img = pygame.transform.scale(img, (img.get_width() * 0.7, img.get_height() * 0.7))
        body_rect = img.get_rect(center=(center_x, center_y))
        self.screen.blit(img, body_rect)

        # Draw cells, macrophages, and enemies
        for cell in self.cells:
            cell.reposition(center_pos=(center_x, center_y))
            cell.draw(self.screen, sidebar_width, self)

        self.macrophage.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)

        # Draw cell modals if active
        for cell in self.cells:
            if cell.show_modal:
                cell.draw_modal(self.screen, self.sidebar.width if self.sidebar.visible else 25, self)

        # Update the timer only if the game is running and not paused
        if not self.paused and not self.game_over:
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - self.start_time - self.total_paused_time
            self.remaining_time = max(0, (self.win_time - elapsed_time) // 1000)

            if self.remaining_time <= 0:
                self.game_over = True
                self.paused = True

        # Draw timer and pause/play button
        self.timer.draw(self.screen, self.remaining_time, self.paused)

        button_icon = "assets/icons/pause.png" if not self.paused else "assets/icons/play.png"
        pause_button = pygame.image.load(button_icon)
        pause_button = pygame.transform.scale(pause_button, (40, 40))
        button_position = (self.screen.get_width() - 60, 22)
        self.screen.blit(pause_button, button_position)

        # Finally, draw the sidebar on top of everything
        self.sidebar.draw(self.screen)
        self.oracle.draw(self.screen)