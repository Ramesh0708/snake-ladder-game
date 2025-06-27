import pygame
import sys
from game.simple_game import SnakeLadderGame
from game.simple_menu import SimpleMenu

class GameController:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 700))
        pygame.display.set_caption("Snake and Ladder Game")
        self.font = pygame.font.Font(None, 24)
        self.big_font = pygame.font.Font(None, 36)
        self.clock = pygame.time.Clock()
        
        self.colors = {
            'RED': (220, 20, 60),
            'GOLD': (255, 215, 0),
            'BEIGE': (245, 245, 220),
            'WHITE': (255, 255, 255),
            'BLACK': (0, 0, 0),
            'DARK_RED': (139, 0, 0)
        }
        
        self.menu = SimpleMenu(self.screen, self.font, self.big_font, self.colors)
        self.game = None
        self.game_state = 'menu'
    
    def init_game(self, num_players):
        self.game = SnakeLadderGame(num_players)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()
                elif event.key == pygame.K_ESCAPE and self.game_state == 'menu':
                    return False
            
            if self.game_state == 'menu':
                result = self.menu.handle_input(event)
                if result == 'exit':
                    return False
                elif result:
                    self.init_game(result)
                    self.game_state = 'playing'
            
            elif self.game_state == 'playing':
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not self.game.animating and not self.game.game_over:
                        dice_roll = self.game.roll_dice()
                        self.game.move_player(dice_roll)
                        if not self.game.game_over:
                            self.game.next_turn()
                    elif event.key == pygame.K_ESCAPE:
                        self.game_state = 'menu'
        
        return True
    
    def update(self):
        if self.game:
            self.game.update()
        if self.menu:
            self.menu.update()
    
    def draw(self):
        if self.game_state == 'menu':
            self.menu.draw()
        elif self.game_state == 'playing':
            self.game.draw()
        
        pygame.display.flip()
    
    def run(self):
        print('🐍 Snake and Ladder Game - Fun & Engaging! 🪜')
        print('Press ESC in menu to exit')
        
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    controller = GameController()
    controller.run()