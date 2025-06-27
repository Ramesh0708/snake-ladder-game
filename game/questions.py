import json
import random
import pygame

class QuestionManager:
    def __init__(self, questions_file):
        self.all_questions = []
        self.unused_questions = []
        self.used_questions = []
        self.current_question = None
        self.load_questions(questions_file)
        self.shuffle_questions()
        
    def load_questions(self, filename):
        """Load questions from JSON file"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                self.all_questions = data['questions']
        except FileNotFoundError:
            print(f"Questions file {filename} not found!")
            self.all_questions = []
    
    def shuffle_questions(self):
        """Shuffle questions at game start"""
        self.unused_questions = self.all_questions.copy()
        random.shuffle(self.unused_questions)
        self.used_questions = []
    
    def get_random_question(self):
        """Get next unused question"""
        if not self.unused_questions:
            return None  # All questions exhausted
            
        self.current_question = self.unused_questions.pop()
        self.used_questions.append(self.current_question)
        return self.current_question
    
    def has_more_questions(self):
        """Check if there are more unused questions"""
        return len(self.unused_questions) > 0
    
    def check_answer(self, selected_option):
        """Check if the selected answer is correct"""
        if not self.current_question:
            return False
        return selected_option == self.current_question['answer']

class QuestionScreen:
    def __init__(self, screen, font, big_font, colors):
        self.screen = screen
        self.font = font
        self.big_font = big_font
        self.colors = colors
        self.selected_option = 0
        self.show_result = False
        self.result_correct = False
        self.result_timer = 0
        
    def draw_rounded_rect(self, surface, color, rect, radius):
        """Draw a rounded rectangle"""
        pygame.draw.rect(surface, color, rect, border_radius=radius)
        
    def draw_question(self, question_data):
        """Draw the enhanced question screen"""
        if not question_data:
            # Show "all questions exhausted" message
            self.screen.fill(self.colors['BEIGE'])
            
            title = self.big_font.render("🎉 AWS Master! 🎉", True, self.colors['GOLD'])
            title_rect = title.get_rect(center=(400, 200))
            self.screen.blit(title, title_rect)
            
            message = self.font.render("You've mastered all AWS questions!", True, self.colors['DARK_RED'])
            message_rect = message.get_rect(center=(400, 250))
            self.screen.blit(message, message_rect)
            
            continue_text = self.font.render("Press SPACE to continue playing", True, self.colors['BLACK'])
            continue_rect = continue_text.get_rect(center=(400, 300))
            self.screen.blit(continue_text, continue_rect)
            return
            
        self.screen.fill(self.colors['BEIGE'])
        
        # Question container with shadow and rounded corners
        container_rect = pygame.Rect(50, 80, 700, 500)
        shadow_rect = pygame.Rect(53, 83, 700, 500)
        self.draw_rounded_rect(self.screen, (200, 200, 200), shadow_rect, 15)
        self.draw_rounded_rect(self.screen, self.colors['WHITE'], container_rect, 15)
        pygame.draw.rect(self.screen, self.colors['DARK_RED'], container_rect, 3, border_radius=15)
        
        # Title
        title = self.big_font.render("AWS Quiz Question", True, self.colors['DARK_RED'])
        title_rect = title.get_rect(center=(400, 120))
        self.screen.blit(title, title_rect)
        
        # Question text with better formatting
        question_lines = self.wrap_text(question_data['question'], 70)
        y_offset = 170
        for line in question_lines:
            text = self.font.render(line, True, self.colors['BLACK'])
            text_rect = text.get_rect(center=(400, y_offset))
            self.screen.blit(text, text_rect)
            y_offset += 30
        
        # Options with enhanced styling
        y_offset += 20
        for i, option in enumerate(question_data['options']):
            # Option container
            option_rect = pygame.Rect(80, y_offset, 640, 45)
            shadow_rect = pygame.Rect(82, y_offset + 2, 640, 45)
            
            # Colors based on selection
            if i == self.selected_option:
                bg_color = self.colors['GOLD']
                border_color = self.colors['DARK_RED']
                border_width = 3
            else:
                bg_color = self.colors['WHITE']
                border_color = self.colors['BLACK']
                border_width = 2
            
            # Draw shadow and option box
            self.draw_rounded_rect(self.screen, (220, 220, 220), shadow_rect, 10)
            self.draw_rounded_rect(self.screen, bg_color, option_rect, 10)
            pygame.draw.rect(self.screen, border_color, option_rect, border_width, border_radius=10)
            
            # Option text
            option_text = self.font.render(f"{chr(65+i)}. {option}", True, self.colors['BLACK'])
            text_rect = option_text.get_rect(center=option_rect.center)
            self.screen.blit(option_text, text_rect)
            
            y_offset += 55
        
        # Instructions
        if not self.show_result:
            instruction = self.font.render("Use ↑↓ arrows to select, ENTER to confirm", True, self.colors['DARK_RED'])
            instruction_rect = instruction.get_rect(center=(400, y_offset + 20))
            self.screen.blit(instruction, instruction_rect)
        
        # Show result with enhanced styling
        if self.show_result:
            result_rect = pygame.Rect(100, y_offset + 10, 600, 120)
            result_color = self.colors['GOLD'] if self.result_correct else self.colors['RED']
            
            self.draw_rounded_rect(self.screen, result_color, result_rect, 10)
            pygame.draw.rect(self.screen, self.colors['BLACK'], result_rect, 2, border_radius=10)
            
            result_text = "✓ Correct! You can move." if self.result_correct else "✗ Wrong! Try again next turn."
            result = self.big_font.render(result_text, True, self.colors['WHITE'])
            result_rect_center = result.get_rect(center=(400, y_offset + 40))
            self.screen.blit(result, result_rect_center)
            
            # Show explanation
            if question_data.get('explanation'):
                exp_lines = self.wrap_text(question_data['explanation'], 80)
                exp_y = y_offset + 70
                for line in exp_lines:
                    exp_text = self.font.render(line, True, self.colors['WHITE'])
                    exp_rect = exp_text.get_rect(center=(400, exp_y))
                    self.screen.blit(exp_text, exp_rect)
                    exp_y += 20
            
            continue_text = self.font.render("Press SPACE to continue", True, self.colors['BLACK'])
            continue_rect = continue_text.get_rect(center=(400, 580))
            self.screen.blit(continue_text, continue_rect)
    
    def wrap_text(self, text, max_chars):
        """Wrap text to fit within specified character limit"""
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            if len(current_line + word) <= max_chars:
                current_line += word + " "
            else:
                if current_line:
                    lines.append(current_line.strip())
                current_line = word + " "
        
        if current_line:
            lines.append(current_line.strip())
        
        return lines
    
    def handle_input(self, event, question_data):
        """Handle input for question screen"""
        if not question_data:
            # Handle "all questions exhausted" screen
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return 'continue'
            return None
            
        if self.show_result:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return 'continue'
            return None
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(question_data['options'])
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(question_data['options'])
            elif event.key == pygame.K_RETURN:
                selected_answer = question_data['options'][self.selected_option]
                self.result_correct = (selected_answer == question_data['answer'])
                self.show_result = True
                return 'answered'
        
        return None
    
    def reset(self):
        """Reset question screen state"""
        self.selected_option = 0
        self.show_result = False
        self.result_correct = False