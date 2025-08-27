class GameStats:
    """Track statistics for Alien Invasion"""

    def __init__(self, ai_game):
        """Initialize statistics"""
        self.settings= ai_game.settings
        self.reset_stats()

    def reset_stats(self):
        """Initialize statistice that can change during the game"""
        self.ships_left = self.settings.ship_limit # limit the number of ships each player has. After each resurrection, a new ship will appear and the statistices of the game will reset. The number of ships will depend on the numberof lives each player gets after losing.
