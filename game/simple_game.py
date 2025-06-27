import pygame
import random
import math

class SnakeLadderGame:
    def __init__(self, num_players=1):
        pygame.init()
        self.BOARD_SIZE = 10
        self.CELL_SIZE = 60
        self.WINDOW_WIDTH = 800
        self.WINDOW_HEIGHT = 700
        
        # Colors
        self.RED = (220, 20, 60)
        self.GOLD = (255, 215, 0)
        self.BEIGE = (245, 245, 220)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.DARK_RED = (139, 0, 0)
        self.GREEN = (34, 139, 34)
        self.BLUE = (30, 144, 255)
        self.PURPLE = (128, 0, 128)
        self.SHADOW = (200, 200, 200)
        self.LIGHT_BLUE = (173, 216, 230)
        self.ORANGE = (255, 165, 0)
        
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Snake and Ladder Game")
        self.font = pygame.font.Font(None, 24)
        self.big_font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 20)
        
        # Game state
        self.num_players = num_players
        self.current_player = 0
        self.player_positions = [1] * num_players
        self.player_colors = [self.DARK_RED, self.GREEN, self.BLUE, self.PURPLE]
        self.player_names = ["Red", "Green", "Blue", "Purple"]
        self.dice_value = 1
        self.game_over = False
        self.winner = None
        
        # Animation
        self.animating = False
        self.animation_steps = []
        self.animation_current_step = 0
        self.animation_timer = 0
        self.animation_delay = 20
        
        # Message system
        self.show_message = False
        self.message_text = ""
        self.message_timer = 0
        self.message_color = self.BLACK
        
        # Dice animation
        self.dice_rolling = False
        self.dice_roll_timer = 0
        
        # Social awareness messages for snakes
        self.snake_messages = [
            "Don't pollute! 🌍 Keep Earth clean!",
            "Say NO to plastic! ♻️ Go green!",
            "Plant trees! 🌳 Save the planet!",
            "Save water! 💧 Every drop counts!",
            "Reduce, Reuse, Recycle! 🔄",
            "Choose renewable energy! ⚡",
            "Protect wildlife! 🦋 They need us!",
            "Walk or cycle! 🚲 Reduce pollution!"
        ]
        
        # Positive messages for ladders
        self.ladder_messages = [
            "Great job! 🌟 Keep climbing!",
            "Education lifts you up! 📚",
            "Kindness is your ladder! ❤️",
            "Hard work pays off! 💪",
            "Dream big, achieve bigger! 🚀",
            "Helping others helps you! 🤝"
        ]
        
        # Snakes and Ladders
        self.ladders = {4: 14, 9: 31, 20: 38, 28: 84, 40: 59, 51: 67, 63: 81, 71: 91}
        self.snakes = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
        
    def get_board_position(self, number):
        if number < 1 or number > 100:
            return 50, 50
            
        row = (number - 1) // self.BOARD_SIZE
        col = (number - 1) % self.BOARD_SIZE
        
        if row % 2 == 1:
            col = self.BOARD_SIZE - 1 - col
            
        x = 50 + col * self.CELL_SIZE + self.CELL_SIZE // 2
        y = 550 - row * self.CELL_SIZE + self.CELL_SIZE // 2
        return x, y
    
    def draw_rounded_rect(self, surface, color, rect, radius):
        pygame.draw.rect(surface, color, rect, border_radius=radius)
    
    def draw_snake(self, start_pos, end_pos):
        start_x, start_y = start_pos
        end_x, end_y = end_pos
        
        # Curved snake body with multiple control points
        mid_x = (start_x + end_x) // 2
        mid_y = min(start_y, end_y) - 40
        
        points = []
        for t in range(31):
            t = t / 30.0
            x = (1-t)**2 * start_x + 2*(1-t)*t * mid_x + t**2 * end_x
            y = (1-t)**2 * start_y + 2*(1-t)*t * mid_y + t**2 * end_y
            points.append((int(x), int(y)))
        
        # Draw snake body with pattern
        for i in range(len(points)-1):
            # Varying thickness
            thickness = 12 - int(abs(i - len(points)//2) * 4 / len(points))
            thickness = max(thickness, 6)
            
            # Alternating colors for pattern
            if i % 3 == 0:
                color = self.RED
            elif i % 3 == 1:
                color = self.DARK_RED
            else:
                color = (180, 30, 70)
            
            pygame.draw.line(self.screen, color, points[i], points[i+1], thickness)
        
        # Enhanced snake head
        pygame.draw.circle(self.screen, self.DARK_RED, start_pos, 15)
        pygame.draw.circle(self.screen, (100, 0, 0), start_pos, 15, 3)
        # Snake eyes
        eye1_pos = (start_x - 5, start_y - 3)
        eye2_pos = (start_x + 5, start_y - 3)
        pygame.draw.circle(self.screen, self.WHITE, eye1_pos, 3)
        pygame.draw.circle(self.screen, self.WHITE, eye2_pos, 3)
        pygame.draw.circle(self.screen, self.BLACK, eye1_pos, 2)
        pygame.draw.circle(self.screen, self.BLACK, eye2_pos, 2)
        
        # Snake tail
        pygame.draw.circle(self.screen, self.RED, end_pos, 10)
        pygame.draw.circle(self.screen, self.DARK_RED, end_pos, 10, 2)
    
    def draw_ladder(self, start_pos, end_pos):
        start_x, start_y = start_pos
        end_x, end_y = end_pos
        
        # Calculate ladder angle and length
        dx = end_x - start_x
        dy = end_y - start_y
        length = math.sqrt(dx*dx + dy*dy)
        
        # Ladder sides with better positioning
        side_offset = 10
        pygame.draw.line(self.screen, (139, 69, 19), 
                        (start_x - side_offset, start_y), 
                        (end_x - side_offset, end_y), 8)
        pygame.draw.line(self.screen, (139, 69, 19), 
                        (start_x + side_offset, start_y), 
                        (end_x + side_offset, end_y), 8)
        
        # Enhanced ladder rungs with proper spacing
        num_rungs = max(3, int(length / 25))
        for i in range(num_rungs + 1):
            t = i / num_rungs if num_rungs > 0 else 0
            rung_x = int(start_x + dx * t)
            rung_y = int(start_y + dy * t)
            
            # Rung with shadow effect
            pygame.draw.line(self.screen, (100, 50, 10), 
                           (rung_x - side_offset + 1, rung_y + 1), 
                           (rung_x + side_offset + 1, rung_y + 1), 5)
            pygame.draw.line(self.screen, (160, 82, 45), 
                           (rung_x - side_offset, rung_y), 
                           (rung_x + side_offset, rung_y), 5)
    
    def draw_board(self):
        self.screen.fill(self.BEIGE)
        
        # Draw tiles
        for i in range(100):
            row = i // self.BOARD_SIZE
            col = i % self.BOARD_SIZE
            
            if row % 2 == 1:
                col = self.BOARD_SIZE - 1 - col
                
            x = 50 + col * self.CELL_SIZE
            y = 550 - row * self.CELL_SIZE
            
            # Shadow
            shadow_rect = pygame.Rect(x + 2, y + 2, self.CELL_SIZE - 4, self.CELL_SIZE - 4)
            self.draw_rounded_rect(self.screen, self.SHADOW, shadow_rect, 8)
            
            # Main tile
            tile_rect = pygame.Rect(x, y, self.CELL_SIZE - 4, self.CELL_SIZE - 4)
            color = self.WHITE if (row + col) % 2 == 0 else self.GOLD
            self.draw_rounded_rect(self.screen, color, tile_rect, 8)
            pygame.draw.rect(self.screen, self.BLACK, tile_rect, 2, border_radius=8)
            
            # Number
            number = i + 1
            text = self.font.render(str(number), True, self.BLACK)
            text_rect = text.get_rect(center=(x + self.CELL_SIZE//2, y + self.CELL_SIZE//2))
            self.screen.blit(text, text_rect)
        
        # Draw ladders and snakes
        for start, end in self.ladders.items():
            self.draw_ladder(self.get_board_position(start), self.get_board_position(end))
            
        for start, end in self.snakes.items():
            self.draw_snake(self.get_board_position(start), self.get_board_position(end))
    
    def draw_players(self):
        for player_id in range(self.num_players):
            # Get current position (animated or static)
            if self.animating and player_id == self.current_player and self.animation_current_step < len(self.animation_steps):
                pos = self.animation_steps[self.animation_current_step]
            else:
                pos = self.player_positions[player_id]
                
            x, y = self.get_board_position(pos)
            
            # Offset for multiple players
            offset_x = (player_id % 2) * 15 - 7
            offset_y = (player_id // 2) * 15 - 7
            
            color = self.player_colors[player_id]
            
            # Shadow
            pygame.draw.circle(self.screen, self.SHADOW, (int(x + offset_x + 2), int(y + offset_y + 2)), 15)
            # Player token
            pygame.draw.circle(self.screen, color, (int(x + offset_x), int(y + offset_y)), 15)
            pygame.draw.circle(self.screen, self.WHITE, (int(x + offset_x), int(y + offset_y)), 15, 3)
    
    def draw_scoreboard(self):
        # Scoreboard background
        board_rect = pygame.Rect(650, 50, 140, 200)
        shadow_rect = pygame.Rect(653, 53, 140, 200)
        
        self.draw_rounded_rect(self.screen, self.SHADOW, shadow_rect, 15)
        self.draw_rounded_rect(self.screen, self.WHITE, board_rect, 15)
        pygame.draw.rect(self.screen, self.DARK_RED, board_rect, 3, border_radius=15)
        
        # Scoreboard title
        title = self.font.render("SCOREBOARD", True, self.DARK_RED)
        title_rect = title.get_rect(center=(720, 70))
        self.screen.blit(title, title_rect)
        
        # Dice value with icon
        dice_bg = pygame.Rect(660, 90, 120, 30)
        self.draw_rounded_rect(self.screen, self.LIGHT_BLUE, dice_bg, 8)
        dice_text = f"🎲 Dice: {self.dice_value}"
        dice_surface = self.small_font.render(dice_text, True, self.BLACK)
        self.screen.blit(dice_surface, (665, 97))
        
        # Current player turn
        if self.num_players > 1 and not self.game_over:
            turn_bg = pygame.Rect(660, 125, 120, 25)
            turn_color = self.player_colors[self.current_player]
            self.draw_rounded_rect(self.screen, turn_color, turn_bg, 8)
            turn_text = f"{self.player_names[self.current_player]}'s Turn"
            turn_surface = self.small_font.render(turn_text, True, self.WHITE)
            self.screen.blit(turn_surface, (665, 130))
        
        # Player positions
        y_offset = 160
        for i in range(self.num_players):
            # Player info background
            player_bg = pygame.Rect(660, y_offset, 120, 20)
            player_color = self.player_colors[i]
            
            # Highlight current player
            if i == self.current_player and not self.game_over:
                self.draw_rounded_rect(self.screen, player_color, player_bg, 5)
                text_color = self.WHITE
            else:
                self.draw_rounded_rect(self.screen, (240, 240, 240), player_bg, 5)
                text_color = player_color
            
            player_text = f"{self.player_names[i]}: {self.player_positions[i]}"
            pos_surface = self.small_font.render(player_text, True, text_color)
            self.screen.blit(pos_surface, (665, y_offset + 2))
            y_offset += 25
    
    def draw_dice(self):
        dice_x, dice_y = 650, 270
        
        # Shadow
        pygame.draw.rect(self.screen, self.SHADOW, (dice_x + 3, dice_y + 3, 80, 80), border_radius=10)
        # Dice
        self.draw_rounded_rect(self.screen, self.WHITE, pygame.Rect(dice_x, dice_y, 80, 80), 10)
        pygame.draw.rect(self.screen, self.BLACK, (dice_x, dice_y, 80, 80), 3, border_radius=10)
        
        display_value = random.randint(1, 6) if self.dice_rolling else self.dice_value
        
        # Dice dots
        dot_positions = {
            1: [(40, 40)],
            2: [(20, 20), (60, 60)],
            3: [(20, 20), (40, 40), (60, 60)],
            4: [(20, 20), (60, 20), (20, 60), (60, 60)],
            5: [(20, 20), (60, 20), (40, 40), (20, 60), (60, 60)],
            6: [(20, 20), (60, 20), (20, 40), (60, 40), (20, 60), (60, 60)]
        }
        
        for dot_x, dot_y in dot_positions[display_value]:
            pygame.draw.circle(self.screen, self.BLACK, (dice_x + dot_x, dice_y + dot_y), 6)
    
    def draw_message(self):
        if self.show_message:
            # Message background
            msg_rect = pygame.Rect(50, 600, 600, 80)
            shadow_rect = pygame.Rect(53, 603, 600, 80)
            
            self.draw_rounded_rect(self.screen, self.SHADOW, shadow_rect, 15)
            self.draw_rounded_rect(self.screen, self.WHITE, msg_rect, 15)
            pygame.draw.rect(self.screen, self.message_color, msg_rect, 3, border_radius=15)
            
            # Message text
            lines = self.wrap_text(self.message_text, 70)
            y_offset = 620
            for line in lines:
                text = self.font.render(line, True, self.message_color)
                text_rect = text.get_rect(center=(350, y_offset))
                self.screen.blit(text, text_rect)
                y_offset += 25
    
    def wrap_text(self, text, max_chars):
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
    
    def draw_ui(self):
        # Title moved to top-right area
        title_shadow = self.big_font.render("🐍 Snake and Ladder 🪜", True, self.SHADOW)
        self.screen.blit(title_shadow, (652, 12))
        title = self.big_font.render("🐍 Snake and Ladder 🪜", True, self.DARK_RED)
        self.screen.blit(title, (650, 10))
        
        # Instructions
        if not self.animating and not self.game_over:
            instruction = self.font.render("SPACE: Roll | F11: Fullscreen", True, self.BLACK)
            self.screen.blit(instruction, (650, 370))
        elif self.animating:
            instruction = self.font.render("Moving...", True, self.ORANGE)
            self.screen.blit(instruction, (650, 370))
        
        # Game over with beautiful design
        if self.game_over:
            # Celebration overlay
            overlay = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
            overlay.set_alpha(200)
            overlay.fill((0, 0, 50))
            self.screen.blit(overlay, (0, 0))
            
            # Winner card
            card_rect = pygame.Rect(150, 200, 500, 300)
            shadow_rect = pygame.Rect(155, 205, 500, 300)
            
            self.draw_rounded_rect(self.screen, self.SHADOW, shadow_rect, 20)
            self.draw_rounded_rect(self.screen, self.WHITE, card_rect, 20)
            pygame.draw.rect(self.screen, self.GOLD, card_rect, 5, border_radius=20)
            
            # Celebration text
            congrats = self.big_font.render("🎉 CONGRATULATIONS! 🎉", True, self.GOLD)
            congrats_rect = congrats.get_rect(center=(400, 250))
            self.screen.blit(congrats, congrats_rect)
            
            # Winner announcement
            winner_text = f"🏆 {self.player_names[self.winner]} Player Wins! 🏆"
            win_color = self.player_colors[self.winner]
            win_surface = self.big_font.render(winner_text, True, win_color)
            win_rect = win_surface.get_rect(center=(400, 300))
            self.screen.blit(win_surface, win_rect)
            
            # Final positions
            final_text = self.font.render("Final Positions:", True, self.BLACK)
            final_rect = final_text.get_rect(center=(400, 350))
            self.screen.blit(final_text, final_rect)
            
            y_pos = 380
            for i in range(self.num_players):
                pos_text = f"{self.player_names[i]}: {self.player_positions[i]}"
                pos_color = self.player_colors[i]
                pos_surface = self.font.render(pos_text, True, pos_color)
                pos_rect = pos_surface.get_rect(center=(400, y_pos))
                self.screen.blit(pos_surface, pos_rect)
                y_pos += 25
            
            # Play again instruction
            again_text = self.small_font.render("Press ESC to return to menu", True, self.BLACK)
            again_rect = again_text.get_rect(center=(400, 460))
            self.screen.blit(again_text, again_rect)
    
    def show_snake_message(self):
        self.message_text = random.choice(self.snake_messages)
        self.message_color = self.RED
        self.show_message = True
        self.message_timer = 180  # 3 seconds at 60 FPS
    
    def show_ladder_message(self):
        self.message_text = random.choice(self.ladder_messages)
        self.message_color = self.GREEN
        self.show_message = True
        self.message_timer = 180
    
    def roll_dice(self):
        self.dice_rolling = True
        self.dice_roll_timer = 0
        self.dice_value = random.randint(1, 6)
        return self.dice_value
    
    def move_player(self, steps):
        current_pos = self.player_positions[self.current_player]
        new_position = current_pos + steps
        
        if new_position > 100:
            return False
        
        # Create animation steps
        self.animation_steps = []
        for i in range(1, steps + 1):
            self.animation_steps.append(current_pos + i)
        
        # Check for snake or ladder
        final_position = new_position
        if final_position in self.ladders:
            final_position = self.ladders[final_position]
            self.animation_steps.append(final_position)
            self.show_ladder_message()
        elif final_position in self.snakes:
            final_position = self.snakes[final_position]
            self.animation_steps.append(final_position)
            self.show_snake_message()
        
        # Start animation
        self.animating = True
        self.animation_current_step = 0
        self.animation_timer = 0
        
        # Set final position
        self.player_positions[self.current_player] = final_position
        
        if final_position >= 100:
            self.game_over = True
            self.winner = self.current_player
            
        return True
    
    def next_turn(self):
        if self.num_players > 1:
            self.current_player = (self.current_player + 1) % self.num_players
    
    def update(self):
        # Dice animation
        if self.dice_rolling:
            self.dice_roll_timer += 1
            if self.dice_roll_timer >= 30:
                self.dice_rolling = False
        
        # Player animation
        if self.animating:
            self.animation_timer += 1
            if self.animation_timer >= self.animation_delay:
                self.animation_timer = 0
                self.animation_current_step += 1
                if self.animation_current_step >= len(self.animation_steps):
                    self.animating = False
        
        # Message timer
        if self.show_message:
            self.message_timer -= 1
            if self.message_timer <= 0:
                self.show_message = False
    
    def draw(self):
        self.draw_board()
        self.draw_players()
        self.draw_scoreboard()
        self.draw_dice()
        self.draw_message()
        self.draw_ui()
        pygame.display.flip()