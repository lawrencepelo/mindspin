class Settings():
    """A class to store all settings for Mindspin"""
    
    def __init__(self):
        """Initialize the game's settings"""        
        # Number of rows and columns in maze
        self.rows = 22
        self.cols = 25
        
        # Coordinates where maze will begin to draw
        self.initial_tile_row = self.rows // 2
        self.initial_tile_col = self.cols // 2
        
        # Sides that the maze starts and ends on
        # 'T'=top, 'B'=bottom, 'R'=right, 'L'=left 
        self.start_side = 'W'
        self.end_side = 'E'
        
        # These values denote different types of maze tiles and
        # are stored in maze.values_array
        self.wall_value = 0
        self.path_value = 1
        self.start_value = 2
        self.end_value = 3
        self.rotate_cw_value = 4
        self.rotate_ccw_value = 5
        self.reflect_x_value = 6
        self.reflect_y_value = 7
        # List of tile values that player can move to
        self.all_path_values = [self.path_value, 
                                self.start_value, 
                                self.end_value,
                                self.rotate_cw_value, 
                                self.rotate_ccw_value,
                                self.reflect_x_value,
                                self.reflect_y_value]
        
        # Tiles are square, so tile_size is length of tile edge
        self.tile_size = 20
        
        # Colors assigned to tile types
        self.player_color = (255, 0, 255) #purple        
        self.wall_color = (0, 0, 0) #black
        self.path_color = (255, 255, 255) #white
        self.start_color = (0, 255, 0) #green
        self.end_color = (255, 0, 0) #red
        self.rotate_cw_color = (135, 206, 235) #blue
        self.rotate_ccw_color = (255, 140, 0) #orange
        self.reflect_x_color = (255, 182, 193) #pink
        self.reflect_y_color = (255, 255, 0) #yellow 
        self.solve_color = (255, 255, 0) #yellow
        
        # Important! These colors must be in same order
        # as the tile values listed above,
        # i.e., wall_value == 0 --> tile_colors[0] == wall_color
        self.tile_colors = [self.wall_color,
                            self.path_color,
                            self.start_color,
                            self.end_color,
                            self.rotate_cw_color,
                            self.rotate_ccw_color,
                            self.reflect_x_color,
                            self.reflect_y_color,
                            self.solve_color]
        
        # Location of screen on monitor
        self.screen_x = 50
        self.screen_y = 50
        
        # Blank space around maze
        self.border_x = 25
        self.border_y = 25
        
        # Size and background color of screen
        self.screen_width = (self.cols * self.tile_size +
                             2 * self.border_x)
        self.screen_height = (self.rows * self.tile_size +
                              2 * self.border_y)
        self.bg_color = (230, 230, 230) #gray
        
        self.rotate_cw_prob = .05
        self.rotate_ccw_prob = .05
        self.reflect_x_prob = .05
        
        # Initial movement directions assigned to arrow keys
        self.initial_arrow_up = 'U'
        self.initial_arrow_down = 'D'
        self.initial_arrow_left = 'L'
        self.initial_arrow_right = 'R'
        
        # delay between displaying new tiles during maze build
        # set to 0 if you don't want to display maze build
        self.maze_build_delay = 0.001
