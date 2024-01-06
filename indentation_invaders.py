import sys
import pygame
from settings import Settings
from ship import Ship


class IndentationInvaders:
    """Main game class to manage game behavior"""
    def __init__(self):
        """Initialize the game"""
        pygame.init()
        """clock for frame rate"""
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("__indentation__: invaders")
        pygame.display.set_icon(pygame.image.load("images/icon.png"))
        self.ship = Ship(self)

    def run_game(self):
        """Start main game loop"""
        while True:
            # check for keyboard and mouse events
            self._check_events()
            # update movement status
            self.ship.update()
            # update images on screen
            self._update_screen()
            # tick clock for refresh rate
            self.clock.tick(60)

    def _check_events(self):
        """Respond to keyboard and mouse events"""
        # check for quit, keypress (passes to _check_keydown_events) or key release (passes to _check_keyup_events)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Respond to keypresses"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        # press q to quit game
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        """Respond to key releases"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _update_screen(self):
        """Update images on screen"""
        # redraw background color when screen refreshes
        self.screen.fill(self.settings.bg_color)
        # draw ship to screen
        self.ship.blitme()
        # display most recently drawn screen
        pygame.display.flip()


if __name__ == '__main__':
    ii = IndentationInvaders()
    ii.run_game()
