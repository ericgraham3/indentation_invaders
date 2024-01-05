import sys
import pygame

class IndentationInvaders:
    """Main game class to manage game behavior"""
    def __init__(self):
        """Initialize the game"""
        pygame.init()

        self.screen = pygame.display.set_mode((1200,800))

    def run_game(self):
        """Start game loop"""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # display most recently drawn screen
            pygame.display.flip()

if __name__ == '__main__':
    ii = IndentationInvaders()
    ii.run_game()
