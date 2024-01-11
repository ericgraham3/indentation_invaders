import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien


class IndentationInvaders:
    """Main game class to manage game behavior"""

    def __init__(self):
        """Initialize the game"""
        pygame.init()

        # clock for frame rate
        self.clock = pygame.time.Clock()

        # create settings object and set screen size
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("__indentation__: invaders")
        pygame.display.set_icon(pygame.image.load("images/icon.png"))

        # create an instance to store game stats and create a scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        # create ship, bullets, and aliens
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        # set game active flag to True
        self.game_active = False

        # make the Play button
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Start main game loop"""
        while True:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play button"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            # reset game settings
            self.settings.initialize_dynamic_settings()

            # reset game stats
            self.stats.reset_stats()
            self.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # get rid of remaining bullets and aliens
            self.bullets.empty()
            self.aliens.empty()

            # create a new fleet and reset the ship
            self._create_fleet()
            self.ship.center_ship()

            # hide the mouse cursor
            pygame.mouse.set_visible(False)

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
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collission."""
        # check for any bullets that have hit aliens
        # if so, remove bullet and alien
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        # check to see if fleet is empty
        if not self.aliens:
            # if no fleet, destroy existing bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # increase level
            self.stats.level += 1
            self.sb.prep_level()

    def _update_screen(self):
        """Update images on screen"""
        # redraw background color when screen refreshes
        self.screen.fill(self.settings.bg_color)

        # draw bullets to screen
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # draw ship to screen
        self.ship.blitme()

        # draw aliens to screen
        self.aliens.draw(self.screen)

        # Draw the score information
        self.sb.show_score()

        # draw play button if game is inactive
        if not self.game_active:
            self.play_button.draw_button()

        # display most recently drawn screen
        pygame.display.flip()

    def _create_fleet(self):
        """Create the fleet of aliens"""
        # Make an alien, keep adding them until there's no room left
        # Spacing between aliens is one alien width and one alien height
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

            # finished a row; reset x value and increment y
            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self, x_position, y_position):
        """create an alien and place it in the fleet"""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _update_aliens(self):
        """check if the fleet is at an edge, then update positions"""
        self._check_fleet_edges()
        self.aliens.update()
        # look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        # look for aliens hitting bottom of the screen
            self._check_aliens_bottom()

    def _check_fleet_edges(self):
        """respond appropriately if any aliens have reached an edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """drop the entire fleet and change the fleet's direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """respond to the player ship being hit by an alien"""
        if self.stats.ships_left > 0:
            # decrement ships left and update scoreboard
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # get rid of any remaining bullets and aliens
            self.bullets.empty()
            self.aliens.empty()

            # create new fleet and center ship
            self._create_fleet()
            self.ship.center_ship()

            # pause
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """check if any aliens have reached the bottom of the screen"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Treat this the same as if the ship got hit
                self._ship_hit()
                break


if __name__ == '__main__':
    ii = IndentationInvaders()
    ii.run_game()
