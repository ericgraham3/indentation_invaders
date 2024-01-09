class GameStats:
    """Track stats for indentation_invaders"""

    def __init__(self, ii):
        """Initialize stats"""
        self.settings = ii.settings
        self.reset_stats()

    def reset_stats(self):
        """initialize stats that can change during game"""
        self.ships_left = self.settings.ship_limit
