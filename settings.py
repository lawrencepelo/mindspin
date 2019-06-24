class Settings():
    """A class to store all settings for Mindspin"""
    
    def __init__(self):
        """Initialize the game's settings"""        
        # Number of rows and columns in maze
        self.rows = 21
        self.cols = 21
        
        # Sides that the maze starts and ends on
        # 'T'=top, 'B'=bottom, 'R'=right, 'L'=left 
        self.start_side = 'B'
        self.end_side = 'T'
        
        # Tiles are square, so tile_size in length of tile edge
        self.tile_size = 20
        self.wall_color = (0, 0, 0)
        self.path_color = (255, 255, 0)
        self.start_color = (0, 255, 0)
        self.end_color = (255, 0, 0)
        
        self.border_x = 25
        self.border_y = 25
        self.screen_width = (self.cols * self.tile_size +
                             2 * self.border_x)
        self.screen_height = (self.rows * self.tile_size +
                             2 * self.border_y)
        self.bg_color = (230, 230, 230)
        
        # These values will be stored in maze.values_array
        self.wall_value = '#'
        self.path_value = ' '
        self.start_value = 'S'
        self.end_value = 'E'
