import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """Class to manage bullets fired from ship"""

    def __init__(self, ii):
        """create bullet object at ship's current position"""
        super().__init__()
        self.screen = ii.screen
        self.settings = ii.settings
        self.color = self.settings.bullet_color

        # create bullet rect at (0, 0) and set correct position
        self.rect = pygame.Rect(
            0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ii.ship.rect.midtop

        # store bullet's position as a float
        self.y = float(self.rect.y)

    def update(self):
        """update position of bullet and rect to move it up the screen"""
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        """draw bullet to the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)
