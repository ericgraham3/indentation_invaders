import pygame


class Ship:

    def __init__(self, ii):
        """initialize the ship and set starting position"""
        self.screen = ii.screen
        self.screen_rect = ii.screen.get_rect()

        # load ship image and get its rect.
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # start each new ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

    def blitme(self):
        """draw the ship on the screen at its current position"""
        self.screen.blit(self.image, self.rect)
