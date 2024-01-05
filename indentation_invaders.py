import sys
import pygame
from settings import Settings

class IndentationInvaders:
    """Main game class to manage game behavior"""
    def __init__(self):
        """Initialize the game"""
        pygame.init()
        """clock for frame rate"""
        self.clock = pygame.time.Clock(60)
        self.settings = Settings()
        self.screen = pygame.display.set_mode(self.settings.screen_width, self.settings.screen_height)
        pygame.display.set_caption("Indentation Invaders")
        # background color
        self.screen.fill(self.settings.bg_color)

    def run_game(self):
        """Start game loop"""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            # redraw background color when screen refreshes
            self.screen.fill(self.bg_color)
            # display most recently drawn screen
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == '__main__':
    ii = IndentationInvaders()
    ii.run_game()
