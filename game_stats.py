class GameStats():
    """Track statistics for Mindspin"""
    
    def __init__(self):
        """Initialize statistics"""
        
        # game_active = True when player can make moves
        # game_active = False between mazes
        self.game_active = False
        
        self.game_over = False
        self.score = 0
        self.level = 1
        
        # Stores time when player activates each maze
        self.start_time = None
