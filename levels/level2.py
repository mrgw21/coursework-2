import pygame
import math
import random
import platform
import os
import sys
from datetime import datetime
from objects.cell import Cell
from objects.macrophage import Macrophage
from objects.pathogen import Pathogen
from data.quizzes import quizzes
from ui.sidebar import Sidebar
from ui.timer import Timer
from objects.oracle import Oracle
from screens.screen_manager import BaseScreen
from data.leaderboard_manager import LeaderboardManager

class Level2(BaseScreen):
    def __init__(self, screen, manager, tutorial_phase, tutorial_step):
        super().__init__(screen)  # Initialize BaseScreen
        self.manager = manager    # Add this line
        self.screen = screen   # Assign the actual screen surface
        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False
        self.fullscreen = False

        self.sidebar_width = 400
        self.sidebar = Sidebar()
        self.sidebar.visible = True

        self.body_image = pygame.image.load(self.resource_path('assets/images/final/body.png'))
        screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h
        self.macrophage = Macrophage(screen_width, screen_height, sidebar_width=self.sidebar_width)
        self.colliding_pathogens = {}

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
        self.tutorial_pathogens = []  # Special pathogens for the tutorial phase
        self.tutorial_phase = tutorial_phase
        self.tutorial_step = tutorial_step
        self.tutorial_start_time = pygame.time.get_ticks()

        self.spawn_timer = 0
        self.spawn_interval = 2000
        self.resize_pause_timer = 0
        self.resize_pause_duration = 2000 
        self.counter = 0

        self.start_time = pygame.time.get_ticks()
        self.pause_start = None  # To track when the game was paused
        self.total_paused_time = 0  # Total time paused
        self.win_time = 90000  # 90 seconds in milliseconds
        self.remaining_time = self.win_time // 1000

        self.points = 0  # Add points tracking
        self.leaderboard = LeaderboardManager(filepath="data/leaderboards/level2_leaderboard.json")

        self.game_over = False
        self.win = True

        self.timer = Timer(font=pygame.font.SysFont("Arial", 24))

        # Use `pygame.display` to get screen dimensions
        self.previous_width, self.previous_height = screen.get_width(), screen.get_height()
        

    def run(self):
        while self.tutorial_phase:
            # Tutorial logic
            self.clock.tick(60)  # Ensure consistent 60 FPS for the tutorial
            self.spawn_tutorial_pathogens()
            if self.tutorial_step == 2 or self.tutorial_step == 4:
                self.macrophage.update(
                    self.screen.get_width(),
                    self.screen.get_height(),
                    self.sidebar.width if self.sidebar.visible else 25
                )
            self.handle_tutorial_clicks()  # Handle mouse clicks during the tutorial
            self.check_collisions()
            # Move enemies towards the center and cells
            if self.counter < len(self.cells):
                current_cell = self.cells[self.counter]
                for enemy in self.enemies:
                    if enemy.move_towards_target(self.cells):
                        self.counter += 1
            self.draw()  # Draw the updated state for the tutorial
            pygame.display.flip()  # Update the screen
                

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    exit()
                """
                if event.type == pygame.FULLSCREEN:
                    pygame.display.flip()
                """

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        self.toggle_fullscreen()
                    elif event.key == pygame.K_m:  # Toggle sidebar
                        self.sidebar.toggle()
                        self.handle_sidebar_toggle()
                    elif event.key == pygame.K_p:  # Toggle sidebar
                        self.paused = not self.paused
                    if event.key == pygame.K_ESCAPE and self.paused:
                        for cell in self.cells:
                            if cell.show_modal:
                                cell.reset_quiz_state()
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

                    # Handle sidebar clicks first, if the sidebar is visible
                    if self.sidebar and self.sidebar.visible:
                        option_clicked = self.sidebar.handle_event(event)
                        if option_clicked:
                            self.running = False
                            if option_clicked == "Introduction":
                                option_clicked = "Preliminary"
                            self.manager.set_active_screen(option_clicked)
                            return  # Exit after handling sidebar click

                    modal_active = any(cell.show_modal for cell in self.cells)
                    pause_button_rect = pygame.Rect(self.screen.get_width() - 60, 20, 40, 40)

                    # Pause/Play Button Handling
                    if pause_button_rect.collidepoint(mouse_pos):
                        self.paused = not self.paused

                        # Close all modals if unpausing
                        if not self.paused and modal_active:
                            for cell in self.cells:
                                cell.show_modal = False
                        continue  # Skip further processing for this click

                    # If a quiz modal is open, prioritize modal interactions
                    if modal_active:
                        for cell in self.cells:
                            if cell.show_modal:
                                cell.handle_radio_button_click(self.screen, mouse_pos, self.cells, self)
                                break  # Stop further processing for this click
                        continue  # Skip further processing for this click

                    # Allow Oracle interaction when not paused
                    """
                    if not self.paused:
                        self.oracle.handle_click(mouse_pos, self.cells, self)
                    """

                    # Handle cell clicks
                    for cell in self.cells:
                        if cell.rect.collidepoint(mouse_pos):
                            # Open the modal only for infected cells
                            if not self.paused:
                                if cell.health == "infected":
                                    cell.show_modal = True
                                    self.paused = True  # Pause the game when a modal is active
                            break

            # Check if the game is over
            if not self.paused and self.game_over:
                if self.win:
                    self.leaderboard.update_leaderboard("Level2", self.points)
                self.check_game_over()

            # Timer handling
            if self.paused:
                if self.pause_start is None:
                    self.pause_start = pygame.time.get_ticks()
            else:
                if self.pause_start is not None:
                    self.total_paused_time += pygame.time.get_ticks() - self.pause_start
                    self.pause_start = None

            # Main game logic
            if not self.paused and not self.game_over:
                self.check_game_over()
                current_time = pygame.time.get_ticks()
                elapsed_time = current_time - self.start_time - self.total_paused_time
                self.remaining_time = max(0, (self.win_time - elapsed_time) // 1000)

                if self.remaining_time <= 0:
                    self.game_over = True
                    self.paused = True

            if not self.paused and not self.game_over:
                # Dynamically calculate the center of the screen
                self.game_center_x = (self.game_width // 2) + (self.sidebar_width // 2)

                self.screen.fill((255, 255, 255))
                self.clock.tick(60)

                # Update cells and pathogens
                for cell in self.cells:
                    cell.update_infection(self)

                if not self.tutorial_phase:
                    self.spawn_enemy()
                    self.replicate_pathogens()
                    self.update_replica_positions()

                self.macrophage.update(self.screen.get_width(), self.screen.get_height(), self.sidebar.width if self.sidebar.visible else 25)
                self.check_collisions()

                # Move enemies towards the dynamically calculated center and the current cell
                if self.counter < len(self.cells):
                    current_cell = self.cells[self.counter]
                    for enemy in self.enemies:
                        if enemy.move_towards_target(self.cells):
                            self.counter += 1

            # Handle feedback closures for modals
            self.handle_feedback_closure()

            # Draw game elements
            self.draw()

            if self.game_over:
                for cell in self.cells:
                    if cell.show_modal:
                        cell.show_modal = False
                if self.win:
                    self.leaderboard.update_leaderboard("Level2", self.points)
                self.show_game_over_screen()

            # Update the screen
            pygame.display.flip()
    
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
        if self.tutorial_phase:  # Skip spawning during tutorial phase
            return
        
        if pygame.time.get_ticks() - self.resize_pause_timer < self.resize_pause_duration:
            return
        
        if pygame.time.get_ticks() - self.spawn_timer > self.spawn_interval:
            spawn_location = self.generate_spawn_location()
            if random.choice([True, False]):
                # Bacteria
                self.enemies.append(Pathogen(spawn_location[0], spawn_location[1], "bacteria"))
                self.enemies[-1].speed = 0.6
            else:
                # Virus
                self.enemies.append(Pathogen(spawn_location[0], spawn_location[1], "virus"))
                self.enemies[-1].speed = 0.6
            self.spawn_timer = pygame.time.get_ticks()
    
    def replicate_pathogens(self):
        current_time = pygame.time.get_ticks()
        for enemy in list(self.enemies):  # Use a copy to avoid modifying the list during iteration
            if enemy.can_replicate and enemy.replicas < 2 and current_time - enemy.spawn_time >= 4000:  # 4 seconds after spawn
                target_cell = enemy.find_closest_uninfected_cell(self.cells)  # Assuming cells are available
                if target_cell:
                    target_x, target_y = target_cell.rect.center
                    direction_x = target_x - enemy.x
                    direction_y = target_y - enemy.y
                    distance = math.hypot(direction_x, direction_y)

                    if distance != 0:
                        direction_x /= distance
                        direction_y /= distance

                    launch_direction_x = -direction_x
                    launch_direction_y = -direction_y

                    for i in range(2 - enemy.replicas):  # Create up to 2 replicas
                        # Randomized offsets for distinct launch positions
                        offset_x = random.choice([-20, 20]) * (i + 1)
                        offset_y = random.choice([-20, 20]) * (i + 1)

                        replica = Pathogen(
                            enemy.x + offset_x,
                            enemy.y + offset_y,
                            enemy.type,
                            can_replicate=False  # Replicas cannot replicate
                        )
                        replica.speed = 0.6
                        replica.launching = True
                        replica.launch_start_time = pygame.time.get_ticks()  # Set launch start time
                        replica.launch_velocity = (launch_direction_x * 1.5, launch_direction_y * 1.5)  # Adjust scale
                        self.enemies.append(replica)

                    enemy.replicas = 2  # Mark as fully replicated
    
    def update_replica_positions(self):
        for enemy in self.enemies:
            enemy.update_position(self.cells)

    def spawn_tutorial_pathogens(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.tutorial_start_time

        if self.tutorial_step == 0:
            self.oracle.display_message("Click on the Macrophage!", self.screen)
            self.handle_tutorial_clicks()

        if self.tutorial_step == 1:
            # Spawn the virus at a random location using generate_spawn_location
            if not any(p.type == "virus" for p in self.enemies):
                x, y = self.generate_spawn_location()
                virus = Pathogen(x, y, "virus")
                virus.is_tutorial = True
                virus.speed = 0.1
                self.enemies.append(virus)
                self.tutorial_pathogens.append(virus)
                self.handle_tutorial_clicks()

            if elapsed_time >= 2000 and elapsed_time < 5000:
                self.oracle.display_message("Take a look at the coming phatogen, it's a virus!", self.screen)

            # Pause the game after 5 seconds to ensure the virus is visible
            if elapsed_time >= 5000:  # Wait 5 seconds
                self.paused = True
                self.tutorial_pathogens[0].speed = 0
                self.oracle.display_message("Click on the virus to learn about it!", self.screen)

        elif self.tutorial_step == 2:
            if not any(p.type == "virus" for p in self.enemies):
                x, y = self.generate_spawn_location()
                virus = Pathogen(x, y, "virus")
                virus.is_tutorial = True
                virus.speed = 0.1
                self.enemies.append(virus)
                self.tutorial_pathogens.append(virus)

            self.oracle.display_message("Use WASD to move the macrophage and kill a virus.", self.screen)
            if elapsed_time >= 5000:
                self.tutorial_pathogens[0].speed = 0

        elif self.tutorial_step == 3 and not any(p.type == "virus" for p in self.enemies):
            # Spawn the bacteria after the virus is killed
            if not any(p.type == "bacteria" for p in self.enemies):
                x, y = self.generate_spawn_location()
                bacteria = Pathogen(x, y, "bacteria")
                bacteria.is_tutorial = True
                bacteria.speed = 0.1
                self.enemies.append(bacteria)
                self.tutorial_pathogens.append(bacteria)
            
            if elapsed_time >= 2000 and elapsed_time < 5000:
                self.oracle.display_message("Look at another phatogen coming, it's a bacteria!", self.screen)
            elif elapsed_time >= 5000:
                self.tutorial_pathogens[0].speed = 0
                self.oracle.display_message("Click on the bacteria to learn about it.", self.screen)

        elif self.tutorial_step == 4:
            if not any(p.type == "bacteria" for p in self.enemies):
                x, y = self.generate_spawn_location()
                virus = Pathogen(x, y, "bacteria")
                virus.is_tutorial = True
                virus.speed = 0.1
                self.enemies.append(virus)
                self.tutorial_pathogens.append(virus)
            
            self.oracle.display_message("Kill a bacteria!", self.screen)
            if elapsed_time >= 5000:
                self.tutorial_pathogens[0].speed = 0

        elif self.tutorial_step == 5 and not self.enemies:
            # Tutorial is over
            self.tutorial_phase = False
            self.tutorial_completed = True  # Mark tutorial as completed
            self.oracle.display_message("Tutorial completed! Protect the cells!", self.screen)

            # Reset game timer
            if self.tutorial_completed:
                self.start_time = pygame.time.get_ticks()  # Reset start time
                self.total_paused_time = 0  # Reset paused time
                self.tutorial_completed = False  # Ensure this logic runs only once

    def handle_tutorial_clicks(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            """
            if event.type == pygame.FULLSCREEN:
                pygame.display.flip()
            """

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    self.toggle_fullscreen()
                elif event.key == pygame.K_m:  # Toggle sidebar
                    self.sidebar.toggle()
                    self.handle_sidebar_toggle()
                if event.key == pygame.K_ESCAPE and self.paused:
                    for cell in self.cells:
                        if cell.show_modal:
                            cell.reset_quiz_state()
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

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                pause_button_rect = pygame.Rect(self.screen.get_width() - 60, 20, 40, 40)

                # Pause/Play Button Handling
                if pause_button_rect.collidepoint(mouse_pos):
                    self.paused = not self.paused

                if self.macrophage.rect.collidepoint(mouse_pos):
                    self.running = False
                    self.tutorial_phase = False
                    self.manager.set_active_screen("macrophage_tutorial") 
                    return

                # Check if a sidebar option is clicked
                if self.sidebar and self.sidebar.visible and self.sidebar.handle_event(event):
                    option_clicked = self.get_sidebar_option(mouse_pos, self.sidebar.options)
                    if option_clicked:
                        self.running = False
                        self.tutorial_phase = False
                        if option_clicked == "Introduction":
                            option_clicked = "Preliminary"
                        self.manager.set_active_screen(option_clicked)
                        return

                # Check clicks on tutorial pathogens
                for pathogen in self.tutorial_pathogens:
                    if pathogen.get_collision_rect().collidepoint(mouse_pos):
                        if pathogen.type == "virus":
                            self.running = False
                            self.tutorial_phase = False
                            self.manager.set_active_screen("virus_tutorial")  # Switch to virus tutorial
                            return
                        elif pathogen.type == "bacteria":
                            self.running = False
                            self.tutorial_phase = False
                            self.manager.set_active_screen("bacteria_tutorial")  # Switch to bacteria tutorial
                            return

    def show_oracle_instructions(self):
        instructions = {
            0: "Click on the virus to learn about it.",
            2: "Use WASD to move the macrophage and kill the virus.",
            4: "Click on the bacteria to learn about it.",
            6: "Protect the cells from enemies!",
        }
        if self.tutorial_step in instructions:
            self.oracle.display_message(instructions[self.tutorial_step])

    def check_collisions(self):
        current_time = pygame.time.get_ticks()

        # Check collisions with the macrophage
        for enemy in list(self.enemies):  # Work on a copy of the enemies list
            if self.macrophage.get_collision_rect().collidepoint(enemy.get_collision_rect().center):
                if enemy not in self.colliding_pathogens:
                    # Start tracking collision time and trigger animation
                    self.colliding_pathogens[enemy] = current_time
                    self.macrophage.handle_collision([enemy])  # Trigger animation
                else:
                    # Check if the collision duration has exceeded the kill delay
                    collision_duration = current_time - self.colliding_pathogens[enemy]
                    if collision_duration >= 600:  # 0.6 second delay
                        if enemy in self.enemies:
                            self.enemies.remove(enemy)  # Safely remove the enemy
                            self.add_points(100)
                        if enemy in self.colliding_pathogens:
                            del self.colliding_pathogens[enemy]  # Stop tracking this pathogen
                        # Handle tutorial-specific logic
                        if self.tutorial_phase:
                            self.tutorial_step += 1
                            if enemy in self.tutorial_pathogens:
                                self.tutorial_pathogens.remove(enemy)
            else:
                # Remove pathogen from tracking if no longer colliding with the macrophage
                if enemy in self.colliding_pathogens:
                    del self.colliding_pathogens[enemy]

        # Check collisions with cells
        for enemy in list(self.enemies):  # Work on a copy of the enemies list
            for cell in self.cells:
                if cell.state and enemy.get_collision_rect().colliderect(cell.get_collision_rect()):
                    cell.die()  # Infect the cell
                    if enemy in self.enemies:
                        self.enemies.remove(enemy)  # Safely remove the pathogen
                    self.add_points(-10)
                    if enemy in self.colliding_pathogens:
                        del self.colliding_pathogens[enemy]  # Stop tracking this pathogen
                    break  # Stop checking other cells for this pathogen
    
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
            if self.win:
                self.leaderboard.update_leaderboard("Level2", self.points)

    def show_game_over_screen(self):
        sidebar_width = self.sidebar.width if self.sidebar.visible else 25
        game_width = self.screen.get_width() - sidebar_width
        game_center_x = sidebar_width + game_width // 2
        game_center_y = self.screen.get_height() // 2

        modal_width, modal_height = 700, 600
        modal_x = game_center_x - modal_width // 2
        modal_y = game_center_y - modal_height // 2

        # Draw modal background
        pygame.draw.rect(self.screen, (220, 220, 220), (modal_x, modal_y, modal_width, modal_height))
        pygame.draw.rect(self.screen, (0, 0, 0), (modal_x, modal_y, modal_width, modal_height), 5)

        font_large = pygame.font.SysFont('Arial', 48)
        font_mid = pygame.font.SysFont('Arial', 36)

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

            line3_text = font_mid.render(f"Your Score: {self.points}", True, (0, 0, 0))
            line3_rect = line3_text.get_rect(center=(modal_x + modal_width // 2, current_y))
            self.screen.blit(line3_text, line3_rect)
        else:
            line1_text = font_large.render("Game Over!", True, (0, 0, 0))
            line1_rect = line1_text.get_rect(center=(modal_x + modal_width // 2, current_y))
            self.screen.blit(line1_text, line1_rect)
            current_y += 60

            line2_text = font_large.render("You Lost!", True, (0, 0, 0))
            line2_rect = line2_text.get_rect(center=(modal_x + modal_width // 2, current_y))
            self.screen.blit(line2_text, line2_rect)
            current_y += 80

            line3_text = font_mid.render(f"Your Score: {self.points}", True, (0, 0, 0))
            line3_rect = line3_text.get_rect(center=(modal_x + modal_width // 2, current_y))
            self.screen.blit(line3_text, line3_rect)

        # Display top 3 scores
        font_small = pygame.font.SysFont('Arial', 24)
        leaderboard = self.leaderboard.get_leaderboard("Level2") or []

        # Fill with placeholder entries if less than 3
        while len(leaderboard) < 3:
            leaderboard.append({"score": 0})

        top_scores = leaderboard[:3]  # Get the top 3 scores

        current_y += 50  # Add some space below "Your Score"
        title_text = "Level 2 - Top 3 Scores:"
        title_rendered = font_small.render(title_text, True, (0, 0, 0))
        margin_left = modal_x + modal_width // 3 - 50  # Start near the center but slightly to the left
        self.screen.blit(title_rendered, (margin_left, current_y))
        current_y += 40  # Add some space below the title

        margin_left = modal_x + modal_width // 3 - 50  # Start near the center but slightly to the left

        for i, entry in enumerate(top_scores):
            score_text = f"{i + 1}. {entry['score']}"
            score_rendered = font_small.render(score_text, True, (0, 0, 0))
            self.screen.blit(score_rendered, (margin_left, current_y))
            current_y += 30  # Space between each score

        if not top_scores:  # If no scores exist, show a placeholder
            placeholder_text = "No scores available"
            placeholder_rendered = font_small.render(placeholder_text, True, (0, 0, 0))
            self.screen.blit(placeholder_rendered, (margin_left, current_y))
            current_y += 30

        # Button setup
        button_radius = 50
        button_spacing = 200
        button_y = modal_y + modal_height - 130
        button_centers = [
            (game_center_x - button_spacing, button_y),  # "Home"
            (game_center_x, button_y),  # "Leaderboards"
            (game_center_x + button_spacing, button_y),  # "Restart"
        ]

        buttons = [
            {"label": "Home", "action": "Home"},
            {"label": "Leaderboards", "action": "Leaderboards"},
            {"label": "Restart", "action": "Restart"},
        ]

        # Draw buttons and render text
        button_font = pygame.font.SysFont("Arial", int(button_radius * 0.25), bold=True)
        for center, button in zip(button_centers, buttons):
            x, y = center
            pygame.draw.circle(self.screen, (255, 255, 255), (x, y), button_radius)  # Button background
            pygame.draw.circle(self.screen, (0, 0, 139), (x, y), button_radius, 3)  # Button border

            label_text = button_font.render(button["label"], True, (0, 0, 139))
            label_rect = label_text.get_rect(center=(x, y))
            self.screen.blit(label_text, label_rect)

        pygame.display.flip()

        # Event handling for buttons
        while True:  # Event loop for the game-over screen
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    # Handle sidebar clicks first, if the sidebar is visible
                    if self.sidebar and self.sidebar.visible:
                        option_clicked = self.sidebar.handle_event(event)
                        if option_clicked:
                            self.running = False
                            if option_clicked == "Introduction":
                                option_clicked = "Preliminary"
                            self.manager.set_active_screen(option_clicked)
                            return  # Exit after handling sidebar click

                    for center, button in zip(button_centers, buttons):
                        x, y = center
                        distance = ((mouse_pos[0] - x) ** 2 + (mouse_pos[1] - y) ** 2) ** 0.5
                        if distance <= button_radius:  # Button click detection
                            if button["action"] == "Home":
                                self.running = False
                                self.manager.set_active_screen("Home")
                                return
                            elif button["action"] == "Leaderboards":
                                self.running = False
                                self.manager.set_active_screen("Leaderboard Level 2")
                                return
                            elif button["action"] == "Restart":
                                self.reset_game()
                                return
                            
                elif event.type == pygame.K_SPACE and self.game_over:
                    self.reset_game()

    def add_points(self, amount):
        self.points += amount
        # Prevent score from dropping below 0
        if self.points < 0:
            self.points = 0
    
    def reset_game(self):
        # Reset cells
        self.cells = [Cell(i) for i in range(37)]
        self.assign_neighbors()

        # Clear existing enemies
        self.enemies = []
        self.points = 0

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
            cell.image = pygame.image.load(self.resource_path("assets/images/final/uninfected_cell.png"))
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
        current_time = pygame.time.get_ticks()  # Get the current time
        for cell in self.cells:
            if cell.show_modal and hasattr(cell, "feedback_timer") and cell.feedback_timer:
                if current_time - cell.feedback_timer > 1200:
                    cell.show_modal = False  # Close modal
                    cell.feedback_timer = None  # Reset the timer
                    # Update paused state
                    if self.pause_start is not None:
                        self.total_paused_time += pygame.time.get_ticks() - self.pause_start
                        self.pause_start = None
                    self.paused = False  # Unpause the game
    
    def get_sidebar_option(self, mouse_pos, options_mapping):
        x, y = mouse_pos
        sidebar_width = 400  # Ensure this matches your actual sidebar width
        y_offset = 120  # Starting Y position of the first option
        spacing = 50  # Spacing between each option in the sidebar

        if x < sidebar_width:  # Check if the click is within the sidebar area
            for index, option_text in enumerate(options_mapping):
                # Define the rectangle for each option
                option_rect = pygame.Rect(20, y_offset + index * spacing, sidebar_width - 40, 30)
                if option_rect.collidepoint(x, y):  # Check if the mouse is within this option's rectangle
                    return option_text
        return None  # Return None if no option was clicked
        
    def draw(self):
        # Determine sidebar width dynamically
        sidebar_width = self.sidebar.width if self.sidebar.visible else 25

        # Adjust the center and game area for the sidebar
        game_width = self.screen.get_width() - sidebar_width
        center_x = sidebar_width + game_width // 2  # Center within the adjusted game area
        center_y = self.screen.get_height() // 2

        # Fill the screen background
        self.screen.fill((255, 255, 255))

        if self.tutorial_phase:
            self.sidebar.draw(self.screen, "Introduction")
        else:
            self.sidebar.draw(self.screen, "Level 2")

        # Adjust body image placement
        img = self.body_image
        img = pygame.transform.scale(img, (img.get_width() * 0.7, img.get_height() * 0.7))
        body_rect = img.get_rect(center=(center_x, center_y))
        self.screen.blit(img, body_rect)
        
        if self.tutorial_phase:
            """
            for pathogen in self.tutorial_pathogens:
                pygame.draw.rect(self.screen, (0, 255, 0), pathogen.get_collision_rect(), 2)
            self.oracle.draw_message(self.screen)
            """

        # Draw cells
        for cell in self.cells:
            cell.reposition(center_pos=(center_x, center_y))
            cell.draw(self.screen, sidebar_width, self.cells, self)
        
        # Draw pathogens first (behind macrophage)
        for enemy in self.enemies:
            enemy.draw(self.screen)

        # Draw macrophage (in front of pathogens)
        self.macrophage.draw(self.screen)

        # Draw cell modals if active
        for cell in self.cells:
            if cell.show_modal:
                cell.draw_modal(self.screen, self.sidebar.width if self.sidebar.visible else 25, self.cells, self)

        # Draw timer and pause/play button
        if not self.tutorial_phase:
            self.timer.draw(self.screen, self.remaining_time, self.paused)
            button_icon = "assets/icons/pause.png" if not self.paused else "assets/icons/play.png"
            pause_button = pygame.image.load(self.resource_path(button_icon))
            pause_button = pygame.transform.scale(pause_button, (40, 40))
            button_position = (self.screen.get_width() - 60, 22)
            self.screen.blit(pause_button, button_position)
        
            font = pygame.font.SysFont("Arial", 24)
            score_text = font.render(f"Score: {self.points}", True, (0, 0, 0))
            sidebar_width = self.sidebar.width if self.sidebar.visible else 0
            self.screen.blit(score_text, (sidebar_width + 20, 30))

        self.oracle.draw(self.screen)
        self.oracle.draw_message(self.screen)
    
    @staticmethod
    def resource_path(relative_path):
        try:
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)