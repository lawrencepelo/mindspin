class GameStats():
    """Track statistics for Mindspin"""
    
    def __init__(self, settings):
        """Initialize statistics"""
        self.settings = settings
        self.reset_stats()
        
        # Start in an inactive state
        self.game_active = False
        
        self.high_score = 0
        
    def reset_stats(self):
        """Initialize statistics that can change during the game"""
        self.score = 0
        self.level = 1
        self.start_time = None
        self.finish_time = None
