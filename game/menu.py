import pygame

class StartMenu:
    def __init__(self, screen, font, big_font, colors):
        self.screen = screen
        self.font = font
        self.big_font = big_font
        self.colors = colors
        self.selected_option = 0
        self.options = ["Single Player", "Two Players"]
        
    def draw_rounded_rect(self, surface, color, rect, radius):
        """Draw a rounded rectangle"""
        pygame.draw.rect(surface, color, rect, border_radius=radius)
        
    def draw(self):
        """Draw the start menu"""
        self.screen.fill(self.colors['BEIGE'])
        
        # Title with shadow
        title_shadow = self.big_font.render("Cloud Ladder", True, (150, 150, 150))
        title_rect_shadow = title_shadow.get_rect(center=(402, 152))
        self.screen.blit(title_shadow, title_rect_shadow)
        
        title = self.big_font.render("Cloud Ladder", True, self.colors['DARK_RED'])
        title_rect = title.get_rect(center=(400, 150))
        self.screen.blit(title, title_rect)
        
        subtitle = self.font.render("AWS Edition", True, self.colors['GOLD'])
        subtitle_rect = subtitle.get_rect(center=(400, 190))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Menu options
        y_start = 300
        for i, option in enumerate(self.options):
            # Option container
            option_rect = pygame.Rect(250, y_start + i * 80, 300, 60)
            shadow_rect = pygame.Rect(252, y_start + i * 80 + 2, 300, 60)
            
            # Colors based on selection
            if i == self.selected_option:
                bg_color = self.colors['GOLD']
                border_color = self.colors['DARK_RED']
                text_color = self.colors['BLACK']
                border_width = 4
            else:
                bg_color = self.colors['WHITE']
                border_color = self.colors['BLACK']
                text_color = self.colors['BLACK']
                border_width = 2
            
            # Draw shadow and option box
            self.draw_rounded_rect(self.screen, (200, 200, 200), shadow_rect, 15)
            self.draw_rounded_rect(self.screen, bg_color, option_rect, 15)
            pygame.draw.rect(self.screen, border_color, option_rect, border_width, border_radius=15)
            
            # Option text
            option_text = self.font.render(option, True, text_color)
            text_rect = option_text.get_rect(center=option_rect.center)
            self.screen.blit(option_text, text_rect)
        
        # Instructions
        instruction = self.font.render("Use ↑↓ arrows to select, ENTER to start", True, self.colors['BLACK'])
        instruction_rect = instruction.get_rect(center=(400, 500))
        self.screen.blit(instruction, instruction_rect)
        
    def handle_input(self, event):
        """Handle menu input"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                return self.selected_option + 1  # Return 1 for single, 2 for two players
        return None