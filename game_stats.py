class GameStats():
    """Track statistics for Mindspin"""
    
    def __init__(self):
        """Initialize statistics"""
        
        # game_active = True when player can make moves
        # game_active = False between mazes
        self.maze_status = 'before'

        self.score = 0
        self.level = 1
        
        # Stores time when player activates each maze
        self.start_time = None
