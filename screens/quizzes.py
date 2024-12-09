import pygame
import random
from screens.screen_manager import BaseScreen
from ui.sidebar import Sidebar
from data.quizzes import quizzes

class Button:
    def __init__(self, x, y, width, height, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.font = pygame.font.SysFont("Arial", 25)
    def draw(self, screen, colour):
        pygame.draw.rect(screen, colour, self.rect)  # Button background
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        screen.blit(text_surface, (self.rect.centerx - text_surface.get_width() // 2, self.rect.centery - text_surface.get_height() // 2))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class QuizzesScreen(BaseScreen):
    def __init__(self, screen, manager):
        super().__init__(screen)
        self.manager = manager
        self.title_font = pygame.font.SysFont("Arial", 40, bold=True)
        self.text_font = pygame.font.SysFont("Arial", 25)
        self.sidebar = Sidebar()
        self.sidebar.visible = True
        sidebar_width = self.sidebar.width if self.sidebar.visible else 0
        center_x = self.screen.get_width() // 2 + (sidebar_width // 2)
        center_y = self.screen.get_height() // 2
        square_size_x = (self.screen.get_width() - sidebar_width - 300) // 2
        square_size_y = (self.screen.get_height() - 300) // 2

        self.colours = [(0,0,139),(255,140,0),(0,128,128),(255,130,180)]
        button1 = Button(center_x - square_size_x - 10, center_y + 10, square_size_x, square_size_y, "Comparisons", "Comparisons")
        button2 = Button(center_x - square_size_x - 10, center_y - 10 - square_size_y, square_size_x, square_size_y, "Viruses", "Viruses")
        button3 = Button(center_x + 10, center_y + 10, square_size_x, square_size_y, "Bacteria", "Bacteria")
        button4 = Button(center_x + 10, center_y - 10 - square_size_y, square_size_x, square_size_y, "Immune System", "Immune System")
        self.buttons = [button1, button2, button3, button4]

        self.title_position = [screen.get_width() // 2, 100]
        self.quiz_descriptions = [
            "Quiz 1: Bacteria",
            "Quiz 2: Viruses",
            "Quiz 3: The Immune System",
            "Quiz 4: Comparisons"
        ]
        self.text_positions = []
        self.calculate_text_positions()

        self.running = True

            
    def calculate_text_positions(self):
        sidebar_width = self.sidebar.width if self.sidebar.visible else 0
        center_x = self.screen.get_width() // 2 + (sidebar_width // 2)

        self.title_position[0] = center_x
        self.text_positions = [
            [center_x, 200 + i * 40] for i in range(len(self.quiz_descriptions))
        ]

    def draw(self, screen):
        pygame.draw.rect(screen, (200, 200, 200), self.rect)  # Button background
        text_surface = self.text_font.render(self.text, True, (0, 0, 0))
        screen.blit(text_surface, (self.rect.centerx - text_surface.get_width() // 2, self.rect.centery - text_surface.get_height() // 2))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def run_quiz(self, category):
        category_questions = [q for q in quizzes if q["category"] == category]

        correct_answers = 0
        quiz_index = 0
        while quiz_index < 10 and quiz_index < len(category_questions):

            active_question = category_questions[quiz_index]
            active_question_text = active_question["question"]
            active_question_options = active_question["options"]
            random.shuffle(active_question_options)
            self.screen.fill((255, 255, 255))  # Clear screen

            x = self.screen.get_width()//2 - 250
            option_buttons = []
            y_offset = 250
            i = 0
            
            # Display question
            question_surface = self.title_font.render(active_question_text, True, (0, 0, 0))
            text_width = question_surface.get_width()
            x_question = (self.screen.get_width() - text_width) // 2

            self.screen.blit(question_surface, (x_question, 50))

            for option in active_question_options:
                button = Button(500, y_offset, x, 100, option["text"], option["is_correct"])
                button.draw(self.screen, self.colours[i])
                option_buttons.append(button)
                y_offset += 130
                i += 1

            pygame.display.flip()

            answered = False
            while not answered:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        for button in option_buttons:
                            if button.is_clicked(mouse_pos):
                                if button.action:  # Check if the answer is correct
                                    correct_answers += 1
                                quiz_index += 1
                                answered = True
                                break

    # Display score at the end of quiz
        self.screen.fill((255, 255, 255))  # Clear screen
        score_text = f"Your score: {correct_answers}/10"
        score_surface = self.title_font.render(score_text, True, (0, 0, 0))
        self.screen.blit(score_surface, (self.screen.get_width() // 2 - score_surface.get_width() // 2, self.screen.get_height() // 2))
        pygame.display.flip()

        pygame.time.wait(2000)

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
                        self.manager.set_active_screen(option_clicked)
                        return
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for button in self.buttons:
                        if button.is_clicked(mouse_pos):
                            self.run_quiz(button.action)  # Launch quiz for selected category
                            break

            self.draw()
            pygame.display.flip()

    def draw(self):
        sidebar_width = self.sidebar.width if self.sidebar.visible else 0
        center_x = self.screen.get_width() // 2 + (sidebar_width // 2)
        
        self.screen.fill((255, 255, 255))  # Background
        title_text = self.title_font.render("Quizzes", True, (0, 0, 0))
        self.screen.blit(title_text, title_text.get_rect(center=(center_x, self.title_position[1])))
    

        if self.sidebar.visible:
            self.sidebar.draw(self.screen, "Quizzes")

        i = 0
        for button in self.buttons:
            button.draw(self.screen,self.colours[i])
            i += 1

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