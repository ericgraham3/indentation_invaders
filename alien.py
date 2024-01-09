import pygame
from pygame.sprite import Sprite


class Alien (Sprite):
    """A class to represent a single alien"""

    def __init__(self, ii):
        """Initialize alien and starting"""
        super().__init__()
        self.screen = ii.screen
        self.settings = ii.settings

        # Load alien image and set rect attribute
        self.image = pygame.image.load("images/alien.bmp")
        self.rect = self.image.get_rect()

        # Start each new alien at top left of screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store alien's exact horizontal position
        self.x = float(self.rect.x)

    def update(self):
        """move alien right or left"""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x

    def check_edges(self):
        """return true if alien is at edge of screen"""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)
