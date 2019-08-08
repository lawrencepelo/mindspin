import random

class Settings():
    """A class to store all sets for Mindspin"""
    
    def __init__(self, stats):
        """Initialize the game's sets"""        
        # Number of rows and columns in maze for each level.
        self.rows_list = [15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
        self.cols_list = [15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
        
        # Maximum number of rows and columns,
        # used to determined screen size
        self.max_rows = 25
        self.max_cols = 24
        
        # Sides that the maze starts and ends on,
        # actual values determined randomly in calculate function.
        self.start_side = None
        self.end_side = None
        
        # Tiles are square, so tile_size is length of tile edge.
        # For best results, tile_size + tile_border should be even
        self.tile_size = 19
        # Size of blank border around each tile.
        self.tile_border = 1
        
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
        
        # Location of pygame display on monitor
        self.screen_x = 50
        self.screen_y = 50
        
        # Blank space around maze
        self.border_x = 25
        self.border_y = 25
        
        # Background color on pygame display
        self.bg_color = (230, 230, 230) #gray
        
        # sets for message telling player
        # how to activate game
        self.button_width = 425
        self.button_height = 50
        self.button_color = (0, 255, 0)
        self.button_text_color = (0, 0, 0)
        self.button_font = 'ocr a extended'
        self.button_font_size = 18
        self.button_message = 'PRESS ANY ARROW KEY TO START LEVEL '
        
        # Scoreboard font sets
        self.sb_font_color = (30, 30, 30)
        self.sb_font = 'ocr a extended'
        self.sb_font_size = 20
        
        # List of congratulatory messages for when player solves maze
        self.solved_msgs = ['GREAT JOB!',
                            'FANTASTIC!',
                            "YOU'RE A GENIUS!",
                            'HOLY SMOKES!',
                            'GOODNESS GRACIOUS!',
                            'UNBELIEVABLE!',
                            'OUTTA SIGHT!',
                            'CONGRATULATIONS!',
                            'WOWIE ZOWIE!',
                            'GREAT GOOGLY MOOGLY!',
                            'COWABUNGA!',
                            'YOU CRUSHED IT!',
                            'DY-NO-MITE!']         
        
        # Initial movement directions assigned to arrow keys
        self.initial_arrow_north = 'U'
        self.initial_arrow_south = 'D'
        self.initial_arrow_west = 'L'
        self.initial_arrow_east = 'R'
        
        # delay between displaying new tiles during maze build
        # set to 0 if you don't want to display maze build
        self.maze_build_delay = 0
        
        # Time (in seconds) when timer bonus reaches zero
        self.time_limit = 1200
        # Starting value of timer bonus
        self.bonus_start = 1000
        
        # Length of pause (in seconds) between 'solved' messages
        self.solve_pause = 2
        
        # Difficulty bonus is number of tiles on solution path
        # multiplied by diff_bonus_multiplier
        self.diff_bonus_multiplier = 10
        
        # Number of each type of special tile for each level.
        self.rotate_cw_list =  [0, 1, 1, 1, 1, 2, 2, 2, 3, 3]
        self.rotate_ccw_list = [0, 0, 1, 1, 1, 1, 2, 2, 2, 3]
        self.reflect_x_list =  [0, 0, 0, 1, 0, 1, 0, 1, 1, 1]
        self.reflect_y_list =  [0, 0, 0, 0, 1, 0, 1, 1, 1, 1]
        
        # Points for landing on a special tile.
        self.special_tile_bonus = 100
        
        # Calculates sets that depend on other sets
        self.calculate(stats)

    def calculate(self, stats):
        """ Calculates sets that depend on other sets/stats """        
        # Determine number of rows/columns depending on level.
        self.rows = self.rows_list[stats.level - 1]
        self.cols = self.cols_list[stats.level - 1]

        # Coordinates where maze will begin to draw
        self.initial_tile_row = self.rows // 2
        self.initial_tile_col = self.cols // 2
        
        # Randomly select start and end sides for maze,
        # notice they are always opposite each other.
        self.start_side = random.choice(['U', 'D', 'L', 'R'])
        if self.start_side == 'U':
            self.end_side = 'D'
        elif self.start_side == 'D':
            self.end_side = 'U'
        elif self.start_side == 'L':
            self.end_side = 'R'
        elif self.start_side == 'R':
            self.end_side = 'L'
        
        # Total size of each tile is sum of size and border.
        self.tile_total_size = self.tile_size + self.tile_border
        
        # Build list of special tile colors to be randomly
        # distributed on maze solution path.
        self.special_tile_colors = []
        for _ in range(0, self.rotate_cw_list[stats.level - 1]):
            self.special_tile_colors.append(self.rotate_cw_color)
        for _ in range(0, self.rotate_ccw_list[stats.level - 1]):
            self.special_tile_colors.append(self.rotate_ccw_color)
        for _ in range(0, self.reflect_x_list[stats.level - 1]):
            self.special_tile_colors.append(self.reflect_x_color)
        for _ in range(0, self.reflect_y_list[stats.level - 1]):
            self.special_tile_colors.append(self.reflect_y_color)
        
        # Size and background color of screen
        self.screen_width = (self.max_cols * self.tile_total_size +
                             4 * self.border_x +
                             2 * self.sb_font_size)
        self.screen_height = (self.max_rows * self.tile_total_size +
                              6 * self.border_y +
                              4 * self.sb_font_size)
                              
        # Find top left corner of maze.
        self.maze_topleft_x = ((self.screen_width -
                                self.cols * self.tile_total_size) // 2)
        self.maze_topleft_y = ((self.screen_height -
                                self.rows * self.tile_total_size) // 2)
                              
        # Value of timer bonus is a quadratic function of time
        # self.bonus_coeff is the coefficient of the time^2 term
        self.bonus_coeff = -self.bonus_start / (self.time_limit ** 2)
