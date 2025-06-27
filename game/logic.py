import pygame
import random
import math
import time

class CloudLadderGame:
    def __init__(self, num_players=1):
        pygame.init()
        self.BOARD_SIZE = 10
        self.CELL_SIZE = 60
        self.WINDOW_WIDTH = 800
        self.WINDOW_HEIGHT = 700
        
        # Marwadi colors
        self.RED = (220, 20, 60)
        self.GOLD = (255, 215, 0)
        self.BEIGE = (245, 245, 220)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.DARK_RED = (139, 0, 0)
        self.GREEN = (34, 139, 34)
        self.SHADOW = (200, 200, 200)
        
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Cloud Ladder - AWS Edition")
        self.font = pygame.font.Font(None, 24)
        self.big_font = pygame.font.Font(None, 36)
        
        # Game state
        self.num_players = num_players
        self.current_player = 0
        self.player_positions = [1] * num_players
        self.player_colors = [self.DARK_RED, self.GREEN]
        self.dice_value = 1
        self.game_over = False
        self.winner = None
        self.waiting_for_question = False
        self.scores = [0] * num_players
        
        # Animation state
        self.animating = False
        self.animation_start_pos = 1
        self.animation_target_pos = 1
        self.animation_current_pos = 1.0
        self.animation_speed = 3.0
        
        # Dice animation
        self.dice_rolling = False
        self.dice_roll_timer = 0
        self.dice_roll_duration = 30
        
        # Snakes and Ladders positions
        self.ladders = {4: 14, 9: 31, 20: 38, 28: 84, 40: 59, 51: 67, 63: 81, 71: 91}
        self.snakes = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
        
    def get_board_position(self, number):
        """Convert board number to screen coordinates"""
        if number < 1 or number > 100:
            return 50, 50
            
        row = (number - 1) // self.BOARD_SIZE
        col = (number - 1) % self.BOARD_SIZE
        
        # Reverse direction for odd rows (snake pattern)
        if row % 2 == 1:
            col = self.BOARD_SIZE - 1 - col
            
        x = 50 + col * self.CELL_SIZE + self.CELL_SIZE // 2
        y = 550 - row * self.CELL_SIZE + self.CELL_SIZE // 2
        return x, y
    
    def draw_rounded_rect(self, surface, color, rect, radius):
        """Draw a rounded rectangle"""
        pygame.draw.rect(surface, color, rect, border_radius=radius)
    
    def draw_snake(self, start_pos, end_pos):
        """Draw a curved snake between two positions"""
        start_x, start_y = start_pos
        end_x, end_y = end_pos
        
        # Calculate control points for bezier curve
        mid_x = (start_x + end_x) // 2
        mid_y = min(start_y, end_y) - 30
        
        # Draw snake body with multiple segments
        points = []
        for t in range(21):
            t = t / 20.0
            # Quadratic bezier curve
            x = (1-t)**2 * start_x + 2*(1-t)*t * mid_x + t**2 * end_x
            y = (1-t)**2 * start_y + 2*(1-t)*t * mid_y + t**2 * end_y
            points.append((int(x), int(y)))
        
        # Draw snake segments
        for i in range(len(points)-1):
            pygame.draw.line(self.screen, self.RED, points[i], points[i+1], 8)
        
        # Draw snake head and tail
        pygame.draw.circle(self.screen, self.DARK_RED, start_pos, 12)
        pygame.draw.circle(self.screen, self.RED, end_pos, 8)
    
    def draw_ladder(self, start_pos, end_pos):
        """Draw a ladder between two positions"""
        start_x, start_y = start_pos
        end_x, end_y = end_pos
        
        # Draw ladder sides
        pygame.draw.line(self.screen, (139, 69, 19), (start_x-8, start_y), (end_x-8, end_y), 6)
        pygame.draw.line(self.screen, (139, 69, 19), (start_x+8, start_y), (end_x+8, end_y), 6)
        
        # Draw ladder rungs
        steps = 5
        for i in range(steps + 1):
            t = i / steps
            rung_x = int(start_x + (end_x - start_x) * t)
            rung_y = int(start_y + (end_y - start_y) * t)
            pygame.draw.line(self.screen, (139, 69, 19), 
                           (rung_x-8, rung_y), (rung_x+8, rung_y), 4)
    
    def draw_board(self):
        """Draw the game board with enhanced UI"""
        self.screen.fill(self.BEIGE)
        
        # Draw board squares with shadows and rounded corners
        for i in range(100):
            row = i // self.BOARD_SIZE
            col = i % self.BOARD_SIZE
            
            if row % 2 == 1:
                col = self.BOARD_SIZE - 1 - col
                
            x = 50 + col * self.CELL_SIZE
            y = 550 - row * self.CELL_SIZE
            
            # Draw shadow
            shadow_rect = pygame.Rect(x + 2, y + 2, self.CELL_SIZE - 4, self.CELL_SIZE - 4)
            self.draw_rounded_rect(self.screen, self.SHADOW, shadow_rect, 8)
            
            # Draw main tile
            tile_rect = pygame.Rect(x, y, self.CELL_SIZE - 4, self.CELL_SIZE - 4)
            color = self.WHITE if (row + col) % 2 == 0 else self.GOLD
            self.draw_rounded_rect(self.screen, color, tile_rect, 8)
            
            # Draw enhanced border
            pygame.draw.rect(self.screen, self.BLACK, tile_rect, 2, border_radius=8)
            
            # Draw number (centered)
            number = i + 1
            text = self.font.render(str(number), True, self.BLACK)
            text_rect = text.get_rect(center=(x + self.CELL_SIZE//2, y + self.CELL_SIZE//2))
            self.screen.blit(text, text_rect)
        
        # Draw ladders with enhanced graphics
        for start, end in self.ladders.items():
            start_pos = self.get_board_position(start)
            end_pos = self.get_board_position(end)
            self.draw_ladder(start_pos, end_pos)
            
        # Draw snakes with enhanced graphics
        for start, end in self.snakes.items():
            start_pos = self.get_board_position(start)
            end_pos = self.get_board_position(end)
            self.draw_snake(start_pos, end_pos)
    
    def draw_players(self):
        """Draw all player tokens"""
        for player_id in range(self.num_players):
            if self.animating and player_id == self.current_player:
                pos = self.animation_current_pos
            else:
                pos = self.player_positions[player_id]
                
            x, y = self.get_board_position(int(pos))
            
            # If animating between positions, interpolate coordinates
            if self.animating and player_id == self.current_player and pos != int(pos):
                next_pos = int(pos) + 1
                if next_pos <= 100:
                    next_x, next_y = self.get_board_position(next_pos)
                    fraction = pos - int(pos)
                    x = x + (next_x - x) * fraction
                    y = y + (next_y - y) * fraction
            
            # Offset players if on same tile
            offset = 0
            if self.num_players == 2:
                for other_id in range(player_id):
                    if int(self.player_positions[other_id]) == int(pos):
                        offset = 15
            
            color = self.player_colors[player_id]
            
            # Draw player shadow
            pygame.draw.circle(self.screen, self.SHADOW, (int(x + 2 + offset), int(y + 2)), 18)
            # Draw player token
            pygame.draw.circle(self.screen, color, (int(x + offset), int(y)), 18)
            pygame.draw.circle(self.screen, self.WHITE, (int(x + offset), int(y)), 18, 4)
            # Draw inner circle
            pygame.draw.circle(self.screen, self.GOLD, (int(x + offset), int(y)), 8)
    
    def draw_dice(self):
        """Draw animated dice"""
        dice_x, dice_y = 650, 100
        
        # Draw dice shadow
        pygame.draw.rect(self.screen, self.SHADOW, (dice_x + 3, dice_y + 3, 80, 80), border_radius=10)
        # Draw dice
        self.draw_rounded_rect(self.screen, self.WHITE, pygame.Rect(dice_x, dice_y, 80, 80), 10)
        pygame.draw.rect(self.screen, self.BLACK, (dice_x, dice_y, 80, 80), 3, border_radius=10)
        
        # Show random value if rolling, otherwise show actual value
        display_value = random.randint(1, 6) if self.dice_rolling else self.dice_value
        
        # Draw dice dots
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
    
    def draw_ui(self):
        """Draw enhanced game UI"""
        # Title with shadow
        title_shadow = self.big_font.render("Cloud Ladder - AWS Edition", True, self.SHADOW)
        self.screen.blit(title_shadow, (52, 12))
        title = self.big_font.render("Cloud Ladder - AWS Edition", True, self.DARK_RED)
        self.screen.blit(title, (50, 10))
        
        # Current player turn
        if self.num_players > 1 and not self.game_over:
            turn_text = f"Player {self.current_player + 1}'s Turn"
            turn_color = self.player_colors[self.current_player]
            turn = self.font.render(turn_text, True, turn_color)
            self.screen.blit(turn, (650, 180))
        
        # Player positions and scores
        y_offset = 200
        for i in range(self.num_players):
            player_text = f"Player {i+1}: {self.player_positions[i]}"
            score_text = f"Score: {self.scores[i]}"
            color = self.player_colors[i]
            
            pos_surface = self.font.render(player_text, True, color)
            score_surface = self.font.render(score_text, True, color)
            
            self.screen.blit(pos_surface, (650, y_offset))
            self.screen.blit(score_surface, (650, y_offset + 20))
            y_offset += 50
        
        # Instructions
        if not self.waiting_for_question and not self.animating and not self.game_over:
            instruction = self.font.render("Press SPACE to roll dice", True, self.BLACK)
            self.screen.blit(instruction, (650, y_offset + 20))
        elif self.animating:
            instruction = self.font.render("Moving...", True, self.GOLD)
            self.screen.blit(instruction, (650, y_offset + 20))
        
        if self.game_over:
            # Game over screen with winner and final scores
            overlay = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(self.BLACK)
            self.screen.blit(overlay, (0, 0))
            
            if self.winner is not None:
                win_text = f"Player {self.winner + 1} Wins! 🎉"
                win_color = self.player_colors[self.winner]
            else:
                win_text = "Congratulations! 🎉"
                win_color = self.GOLD
                
            win_surface = self.big_font.render(win_text, True, win_color)
            win_rect = win_surface.get_rect(center=(self.WINDOW_WIDTH//2, 300))
            self.screen.blit(win_surface, win_rect)
            
            # Show final scores
            for i in range(self.num_players):
                final_score = self.font.render(f"Player {i+1} Score: {self.scores[i]}", True, self.WHITE)
                score_rect = final_score.get_rect(center=(self.WINDOW_WIDTH//2, 350 + i * 30))
                self.screen.blit(final_score, score_rect)
    
    def roll_dice(self):
        """Start dice roll animation"""
        self.dice_rolling = True
        self.dice_roll_timer = 0
        self.dice_value = random.randint(1, 6)
        return self.dice_value
    
    def update_dice_animation(self):
        """Update dice roll animation"""
        if self.dice_rolling:
            self.dice_roll_timer += 1
            if self.dice_roll_timer >= self.dice_roll_duration:
                self.dice_rolling = False
    
    def start_player_animation(self, target_position):
        """Start smooth player movement animation"""
        self.animating = True
        self.animation_start_pos = self.player_positions[self.current_player]
        self.animation_target_pos = target_position
        self.animation_current_pos = float(self.player_positions[self.current_player])
    
    def update_player_animation(self):
        """Update player movement animation"""
        if self.animating:
            # Move towards target
            if self.animation_current_pos < self.animation_target_pos:
                self.animation_current_pos += self.animation_speed / 60.0
                if self.animation_current_pos >= self.animation_target_pos:
                    self.animation_current_pos = self.animation_target_pos
                    self.animating = False
                    self.player_positions[self.current_player] = self.animation_target_pos
    
    def move_player(self, steps):
        """Move current player with animation"""
        new_position = self.player_positions[self.current_player] + steps
        
        if new_position > 100:
            return False
            
        # Start animation to new position
        self.start_player_animation(new_position)
        
        # Handle snakes/ladders after animation completes
        final_position = new_position
        if final_position in self.ladders:
            final_position = self.ladders[final_position]
        elif final_position in self.snakes:
            final_position = self.snakes[final_position]
            
        # Update target if there's a snake or ladder
        if final_position != new_position:
            self.animation_target_pos = final_position
            
        # Check win condition
        if final_position >= 100:
            self.game_over = True
            self.winner = self.current_player
            
        return True
    
    def next_turn(self):
        """Switch to next player"""
        if self.num_players > 1:
            self.current_player = (self.current_player + 1) % self.num_players
    
    def update(self):
        """Update game animations"""
        self.update_dice_animation()
        self.update_player_animation()
    
    def draw(self):
        """Main draw function"""
        self.draw_board()
        self.draw_players()
        self.draw_dice()
        self.draw_ui()
        pygame.display.flip()