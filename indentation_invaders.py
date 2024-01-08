import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet


class IndentationInvaders:
    """Main game class to manage game behavior"""

    def __init__(self):
        """Initialize the game"""
        pygame.init()
        """clock for frame rate"""
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("__indentation__: invaders")
        pygame.display.set_icon(pygame.image.load("images/icon.png"))
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()

    def run_game(self):
        """Start main game loop"""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_screen()
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
        # press spacebar to fire a bullt
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Respond to key releases"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """create new bullet and add to bullets group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """update position of bullets and get rid of old bullets"""
        # update movement of bullets
        self.bullets.update()
        # get rid of bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _update_screen(self):
        """Update images on screen"""
        # redraw background color when scree       n refreshes
        self.screen.fill(self.settings.bg_color)
        # draw bullets to screen
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        # draw ship to screen
        self.ship.blitme()
        # display most recently drawn screen
        pygame.display.flip()


if __name__ == '__main__':
    ii = IndentationInvaders()
    ii.run_game()
