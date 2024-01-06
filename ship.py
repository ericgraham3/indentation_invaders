import pygame


class Ship:

    def __init__(self, ii):
        """initialize the ship and set starting position"""
        self.screen = ii.screen
        self.settings = ii.settings
        self.screen_rect = ii.screen.get_rect()

        # load ship image and get its rect.
        self.image = pygame.image.load("images/ship.bmp")
        self.rect = self.image.get_rect()

        # start each new ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        # store a float for ship's exact horizontal position
        self.x = float(self.rect.x)

        # movement flags, start ship with no movement
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update the ship's position based on the movement flag"""
        # update ship's x value, which is a float, not the rect, which is an int
        # don't let it slip off the left or right edge of the screen
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # update the rect based on self.x
        self.rect.x = self.x

    def blitme(self):
        """draw the ship on the screen at its current position"""
        self.screen.blit(self.image, self.rect)
