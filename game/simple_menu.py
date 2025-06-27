import pygame
import math
import random

class SimpleMenu:
    def __init__(self, screen, font, big_font, colors):
        self.screen = screen
        self.font = font
        self.big_font = big_font
        self.colors = colors
        self.selected_option = 0
        self.options = ["1 Player", "2 Players", "3 Players", "4 Players", "Exit Game"]
        
        # Animation variables
        self.time = 0
        self.floating_offset = 0
        self.sparkles = []
        self.init_sparkles()
        
        # Fun messages
        self.fun_messages = [
            "🎲 Roll your way to victory!",
            "🐍 Watch out for sneaky snakes!",
            "🪜 Climb ladders to success!",
            "🏆 Be the first to reach 100!",
            "🎯 Strategy meets luck!",
            "⭐ Classic fun for everyone!"
        ]
        self.current_message = 0
        self.message_timer = 0
        
    def init_sparkles(self):
        for _ in range(15):
            self.sparkles.append({
                'x': random.randint(50, 750),
                'y': random.randint(50, 650),
                'size': random.randint(2, 5),
                'speed': random.uniform(0.5, 2.0),
                'color': random.choice([self.colors['GOLD'], self.colors['WHITE'], (255, 192, 203)])
            })
    
    def update(self):
        self.time += 1
        self.floating_offset = math.sin(self.time * 0.05) * 10
        
        # Update sparkles
        for sparkle in self.sparkles:
            sparkle['y'] -= sparkle['speed']
            if sparkle['y'] < 0:
                sparkle['y'] = 700
                sparkle['x'] = random.randint(50, 750)
        
        # Update fun message
        self.message_timer += 1
        if self.message_timer > 180:  # Change every 3 seconds
            self.current_message = (self.current_message + 1) % len(self.fun_messages)
            self.message_timer = 0
    
    def draw_sparkles(self):
        for sparkle in self.sparkles:
            pygame.draw.circle(self.screen, sparkle['color'], 
                             (int(sparkle['x']), int(sparkle['y'])), sparkle['size'])
    
    def draw_animated_snake(self, x, y, size=30):
        # Animated snake
        snake_offset = math.sin(self.time * 0.1) * 5
        head_x = x + snake_offset
        head_y = y
        
        # Snake body segments
        for i in range(3):
            segment_x = head_x - (i + 1) * 15
            segment_y = head_y + math.sin(self.time * 0.1 + i) * 3
            color = (220 - i * 30, 20, 60 + i * 20)
            pygame.draw.circle(self.screen, color, (int(segment_x), int(segment_y)), size - i * 3)
        
        # Snake head
        pygame.draw.circle(self.screen, self.colors['DARK_RED'], (int(head_x), int(head_y)), size)
        # Eyes
        eye1 = (int(head_x - 8), int(head_y - 5))
        eye2 = (int(head_x + 8), int(head_y - 5))
        pygame.draw.circle(self.screen, self.colors['WHITE'], eye1, 4)
        pygame.draw.circle(self.screen, self.colors['WHITE'], eye2, 4)
        pygame.draw.circle(self.screen, self.colors['BLACK'], eye1, 2)
        pygame.draw.circle(self.screen, self.colors['BLACK'], eye2, 2)
    
    def draw_animated_ladder(self, x, y, height=80):
        # Animated ladder with floating effect
        ladder_offset = math.sin(self.time * 0.08) * 3
        
        # Ladder sides
        side1_top = (x - 15, y + ladder_offset)
        side1_bottom = (x - 15, y + height + ladder_offset)
        side2_top = (x + 15, y + ladder_offset)
        side2_bottom = (x + 15, y + height + ladder_offset)
        
        pygame.draw.line(self.screen, (139, 69, 19), side1_top, side1_bottom, 6)
        pygame.draw.line(self.screen, (139, 69, 19), side2_top, side2_bottom, 6)
        
        # Ladder rungs with slight animation
        for i in range(5):
            rung_y = y + (i + 1) * height // 6 + ladder_offset
            rung_offset = math.sin(self.time * 0.1 + i) * 1
            pygame.draw.line(self.screen, (139, 69, 19), 
                           (x - 15 + rung_offset, rung_y), 
                           (x + 15 + rung_offset, rung_y), 4)
    
    def draw_dice_animation(self, x, y):
        # Rotating dice
        dice_rotation = self.time * 0.1
        dice_size = 40 + math.sin(self.time * 0.15) * 5
        
        # Dice shadow
        pygame.draw.rect(self.screen, (150, 150, 150), 
                        (x - dice_size//2 + 3, y - dice_size//2 + 3, dice_size, dice_size), 
                        border_radius=8)
        
        # Dice body
        dice_rect = pygame.Rect(x - dice_size//2, y - dice_size//2, dice_size, dice_size)
        pygame.draw.rect(self.screen, self.colors['WHITE'], dice_rect, border_radius=8)
        pygame.draw.rect(self.screen, self.colors['BLACK'], dice_rect, 3, border_radius=8)
        
        # Animated dots
        dot_value = int(self.time / 30) % 6 + 1
        dot_positions = {
            1: [(0, 0)],
            2: [(-10, -10), (10, 10)],
            3: [(-10, -10), (0, 0), (10, 10)],
            4: [(-10, -10), (10, -10), (-10, 10), (10, 10)],
            5: [(-10, -10), (10, -10), (0, 0), (-10, 10), (10, 10)],
            6: [(-10, -10), (10, -10), (-10, 0), (10, 0), (-10, 10), (10, 10)]
        }
        
        for dot_x, dot_y in dot_positions[dot_value]:
            pygame.draw.circle(self.screen, self.colors['BLACK'], 
                             (x + dot_x, y + dot_y), 4)
    
    def draw(self):
        # Gradient background
        for y in range(700):
            color_ratio = y / 700
            r = int(245 * (1 - color_ratio) + 200 * color_ratio)
            g = int(245 * (1 - color_ratio) + 220 * color_ratio)
            b = int(220 * (1 - color_ratio) + 255 * color_ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (800, y))
        
        # Draw sparkles
        self.draw_sparkles()
        
        # Animated decorations
        self.draw_animated_snake(150, 100 + self.floating_offset)
        self.draw_animated_ladder(650, 80)
        self.draw_dice_animation(400, 100 + self.floating_offset // 2)
        
        # Main title with shadow and animation
        title_y = 180 + self.floating_offset
        title_shadow = self.big_font.render("🐍 SNAKE & LADDER 🪜", True, (100, 100, 100))
        title_rect_shadow = title_shadow.get_rect(center=(402, title_y + 2))
        self.screen.blit(title_shadow, title_rect_shadow)
        
        title = self.big_font.render("🐍 SNAKE & LADDER 🪜", True, self.colors['DARK_RED'])
        title_rect = title.get_rect(center=(400, title_y))
        self.screen.blit(title, title_rect)
        
        # Fun subtitle with animation
        subtitle_colors = [self.colors['GOLD'], self.colors['RED'], self.colors['DARK_RED']]
        subtitle_color = subtitle_colors[int(self.time / 20) % len(subtitle_colors)]
        subtitle = self.font.render("Classic Board Game Fun!", True, subtitle_color)
        subtitle_rect = subtitle.get_rect(center=(400, title_y + 40))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Fun message rotation
        message = self.font.render(self.fun_messages[self.current_message], True, self.colors['BLACK'])
        message_rect = message.get_rect(center=(400, 260))
        self.screen.blit(message, message_rect)
        
        # Menu options with enhanced styling
        y_start = 320
        for i, option in enumerate(self.options):
            option_y = y_start + i * 60
            option_rect = pygame.Rect(250, option_y, 300, 50)
            
            # Animation for selected option
            if i == self.selected_option:
                scale = 1.1 + math.sin(self.time * 0.2) * 0.05
                option_rect.width = int(300 * scale)
                option_rect.height = int(50 * scale)
                option_rect.center = (400, option_y + 25)
                
                bg_color = self.colors['GOLD']
                text_color = self.colors['BLACK']
                border_width = 4
                
                # Glow effect
                glow_rect = pygame.Rect(option_rect.x - 5, option_rect.y - 5, 
                                      option_rect.width + 10, option_rect.height + 10)
                pygame.draw.rect(self.screen, (255, 255, 0, 100), glow_rect, border_radius=20)
            else:
                bg_color = self.colors['WHITE']
                text_color = self.colors['BLACK']
                border_width = 2
            
            # Shadow
            shadow_rect = pygame.Rect(option_rect.x + 3, option_rect.y + 3, 
                                    option_rect.width, option_rect.height)
            pygame.draw.rect(self.screen, (150, 150, 150), shadow_rect, border_radius=15)
            
            # Main button
            pygame.draw.rect(self.screen, bg_color, option_rect, border_radius=15)
            pygame.draw.rect(self.screen, self.colors['BLACK'], option_rect, border_width, border_radius=15)
            
            # Button text
            if option == "Exit Game":
                text_color = self.colors['RED']
                option_text = "❌ " + option
            else:
                option_text = "🎮 " + option
                
            text_surface = self.font.render(option_text, True, text_color)
            text_rect = text_surface.get_rect(center=option_rect.center)
            self.screen.blit(text_surface, text_rect)
        
        # Instructions with animation
        instruction_y = 650 + math.sin(self.time * 0.1) * 3
        instruction = self.font.render("↑↓ Navigate • ENTER Select • ESC Exit", True, self.colors['BLACK'])
        instruction_rect = instruction.get_rect(center=(400, instruction_y))
        self.screen.blit(instruction, instruction_rect)
        
    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                if self.selected_option == len(self.options) - 1:  # Exit Game
                    return 'exit'
                else:
                    return self.selected_option + 1
        return None