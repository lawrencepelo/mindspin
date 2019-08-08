class GameStats():
    """Track statistics for Mindspin"""
    
    def __init__(self):
        """Initialize statistics"""
        
        # maze_status = 'before' when game is waiting for player to
        #               activate the next maze.
        # maze_status = 'during' while player attempting to solve maze.
        # maze_status = 'after' when player has just solved maze
        #               and before player can activate new maze.
        self.maze_status = 'before'

        self.score = 0
        self.level = 1
        
        # Stores time when player activates each maze
        self.start_time = None
