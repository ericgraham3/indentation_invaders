class GameStats:
    """Track stats for indentation_invaders"""

    def __init__(self, ii):
        """Initialize stats"""
        self.settings = ii.settings
        self.reset_stats()
        self.score = 0
        # high score should never be reset
        self.high_score = 0

    def reset_stats(self):
        """initialize stats that can change during game"""
        self.ships_left = self.settings.ship_limit
        self.level = 1
