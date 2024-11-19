import pygame
import random
from objects.cell import Cell
from objects.macrophage import Macrophage
from objects.pathogen import Pathogen

class Level1:
    def __init__(self, screen):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False

        self.body_image = pygame.image.load('assets/images/body_placeholder.png')
        screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h
        self.macrophage = Macrophage(screen_width, screen_height)
        self.cells = [Cell(i) for i in range(37)] 

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

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        self.toggle_fullscreen()

                    if event.key == pygame.K_SPACE and self.game_over:
                        self.reset_game()
                
                if event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    self.reposition_macrophage()
                    self.reposition_pathogens()
                    self.resize_pause_timer = pygame.time.get_ticks()

                if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                    mouse_pos = pygame.mouse.get_pos()
                    for cell in self.cells:
                        if cell.show_modal:
                            cell.handle_modal_close(self.screen, mouse_pos, self)
                        else:
                            cell.handle_click(mouse_pos, self.cells, self)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        for cell in self.cells:
                            if cell.show_modal:
                                cell.handle_keydown(event.key, self)
            
            if not self.paused and self.game_over:
                self.check_game_over()

            if self.paused:
                if self.pause_start is None:
                    self.pause_start = pygame.time.get_ticks()  # Start tracking pause time
            else:
                if self.pause_start is not None:
                    # Calculate total paused duration and reset the pause_start
                    self.total_paused_time += pygame.time.get_ticks() - self.pause_start
                    self.pause_start = None

            if not self.paused and not self.game_over:
                # Dynamically calculate the center of the screen
                center_x = self.screen.get_width() // 2
                center_y = self.screen.get_height() // 2

                self.screen.fill((255, 255, 255))
                self.clock.tick(60)

                # Spawn enemies
                self.spawn_enemy()
                self.macrophage.update(self.screen.get_width(), self.screen.get_height())
                self.check_collisions()

                # Move enemies towards the dynamically calculated center and the current cell
                if self.counter < len(self.cells):
                    current_cell = self.cells[self.counter]
                    for enemy in self.enemies:
                        # Pass center coordinates and the current cell as arguments
                        if enemy.move_towards_target(center_x, center_y, current_cell):
                            self.counter += 1
            
            if self.paused:
                if self.pause_start is None:
                    self.pause_start = pygame.time.get_ticks()
            else:
                if self.pause_start is not None:
                    self.total_paused_time += pygame.time.get_ticks() - self.pause_start
                    self.pause_start = None

            self.draw()

            if self.game_over:
                self.show_game_over_screen()
            
            pygame.display.flip()  # Update the screen with the new drawing
    
    def toggle_fullscreen(self):
        if self.fullscreen:
            self.screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        else:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    def recenter_elements(self):
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        self.macrophage.reposition(screen_width, screen_height)
    
    def reposition_macrophage(self):
        screen_info = pygame.display.Info()
        screen_width, screen_height = screen_info.current_w, screen_info.current_h

        width_ratio = screen_width / self.previous_width
        height_ratio = screen_height / self.previous_height

        self.macrophage.rect.centerx = int(self.macrophage.rect.centerx * width_ratio)
        self.macrophage.rect.centery = int(self.macrophage.rect.centery * height_ratio)

        self.previous_width, self.previous_height = screen_width, screen_height

    def reposition_pathogens(self):
        screen_info = pygame.display.Info()
        screen_width, screen_height = screen_info.current_w, screen_info.current_h

        width_ratio = screen_width / self.previous_width
        height_ratio = screen_height / self.previous_height

        for pathogen in self.enemies:
            pathogen.reposition(width_ratio, height_ratio)

        self.previous_width, self.previous_height = screen_width, screen_height
    
    def generate_spawn_location(self):
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        # Define padding for edges
        edge_padding = 100

        # Dynamically calculate gray area dimensions based on screen size
        modal_width = int(screen_width * 0.8)  # 60% of screen width
        modal_height = int(screen_height * 0.8)  # 40% of screen height
        center_x = screen_width // 2
        center_y = screen_height // 2

        # Gray area boundaries
        gray_left = center_x - modal_width // 2
        gray_right = center_x + modal_width // 2
        gray_top = center_y - modal_height // 2
        gray_bottom = center_y + modal_height // 2

        # Ensure valid spawn location outside the gray center area
        while True:
            # Generate a random spawn location within the screen bounds
            x = random.randint(edge_padding, screen_width - edge_padding)
            y = random.randint(edge_padding, screen_height - edge_padding)

            # Check if the location is outside the dynamically calculated gray area
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
            if self.macrophage.rect.colliderect(enemy.rect):
                self.enemies.remove(enemy)

            # Check if enemy reached the cells
            for cell in self.cells:
                if enemy.rect.colliderect(cell.rect) and cell.state:
                    cell.die()
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
        modal_width = 700
        modal_height = 300
        modal_x = (self.screen.get_width() - modal_width) // 2
        modal_y = (self.screen.get_height() - modal_height) // 2

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
        self.cells = [Cell(i) for i in range(37)]
        self.enemies = []
        
        screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h
        self.macrophage = Macrophage(screen_width, screen_height)
        self.recenter_elements()
        
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
        
    def draw(self):   
        center_x = self.screen.get_width() // 2
        center_y = self.screen.get_height() // 2

        self.screen.fill((255, 255, 255))

        img = self.body_image
        img = pygame.transform.scale(img, (img.get_width() * 0.32, img.get_height() * 0.32))
        body_rect = img.get_rect(center=(center_x, center_y))
        self.screen.blit(img, body_rect)
        
        # Draw cells, macrophages, and enemies
        for cell in self.cells:
            cell.reposition(center_pos=(center_x, center_y))
            cell.draw(self.screen)

        self.macrophage.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)

        # Draw cell modal on top of everything else
        for cell in self.cells:
            if cell.show_modal:
                cell.draw_modal(self.screen)

        # Update timer only if game is running and not paused
        if not self.paused and not self.game_over:
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - self.start_time - self.total_paused_time
            self.remaining_time = max(0, (self.win_time - elapsed_time) // 1000)

            if self.remaining_time <= 0:
                self.game_over = True
                self.paused = True
        else:
            pass

        # Draw the timer
        font = pygame.font.SysFont('Arial', 24)
        time_text = font.render(f"Time Left: {self.remaining_time}s", True, (0, 0, 0))
        self.screen.blit(time_text, (10, 10))

        if self.paused and not self.game_over:
            paused_font = pygame.font.SysFont('Arial', 24, bold=True)
            paused_text = paused_font.render("Paused", True, (255, 0, 0))
            text_rect = paused_text.get_rect(topright=(self.screen.get_width() - 10, 10))
            self.screen.blit(paused_text, text_rect)