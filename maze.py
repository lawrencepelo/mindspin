import itertools
import random
import pygame
import time
import datetime
from pygame.sprite import Group
from tile import Tile

class Maze():
    """Generate a random maze and edit its values"""
    
    def __init__(self, screen, settings):
        # no_more_X variables, when True, prevent path tiles from
        # being placed on edges, keeping the edges of the maze as solid
        # walls except for Start and End tiles
        if settings.start_side == 'N' or settings.end_side == 'N':
            self.no_more_north = False
        else:
            self.no_more_north = True
        if settings.start_side == 'S' or settings.end_side == 'S':
            self.no_more_south = False
        else:
            self.no_more_south = True
        if settings.start_side == 'E' or settings.end_side == 'E':
            self.no_more_east = False
        else:
            self.no_more_east = True
        if settings.start_side == 'W' or settings.end_side == 'W':
            self.no_more_west = False
        else:
            self.no_more_west = True
            
        # Tiles where the maze starts and ends    
        self.start_tile = None
        self.end_tile = None
        
        self.wall_rect = pygame.Rect(
            settings.maze_topleft_x,
            settings.maze_topleft_y,
            settings.cols * settings.tile_total_size,
            settings.rows * settings.tile_total_size)
        
        # values_array is a 2D list that holds maze tile values
        # in text form.
        # All maze tile values are initalized to wall values.
        self.values_array = []
        initial_row = list(itertools.repeat(settings.wall_value,
                                            settings.cols))
        for _ in range(0, settings.rows):
            self.values_array.append(initial_row.copy())
            
        # Picks first path tile and sends to extend_path function
        initial_tile = Tile(settings.initial_tile_row,
                            settings.initial_tile_col)
        self.set_value(initial_tile, settings.path_value)
        self.extend_path(screen, settings, initial_tile)
        
        # solve_tiles Group contains tiles on the solution path
        self.solve_tiles = Group()
        # self.solved = True when the maze solution has been found
        self.solved = False
        # Solves the maze and populates the solve_tiles Group
        self.solve(screen, settings, self.start_tile)
        
        self.choose_special_tiles(settings)
        
        self.path_tiles = Group()
        self.create_path_tiles_group(screen, settings)        
            
    def is_inside_maze(self, settings, tile):
        """"Returns True if tile is inside maze, otherwise False"""
        return (tile.row >= 0 and tile.row < settings.rows and 
                tile.col >= 0 and tile.col < settings.cols)
    
    def get_value(self, settings, tile):
        """Returns value from values_array at location of given tile"""
        if self.is_inside_maze(settings, tile):
            return self.values_array[tile.row][tile.col]
        else:
            return None
        
    def set_value(self, tile, val):
        """Edits value in values_array at location of given tile"""
        self.values_array[tile.row][tile.col] = val
        
    def can_move_to_tile(self, settings, tile):
        """Returns True if given tile is on path, otherwise False"""
        for path_tile in self.path_tiles:
            if tile.same_location_as(path_tile):
                return True
        return False

    def can_extend_path_to_tile(self, settings, tile):
        """
        Returns True if extend_path function can move to given tile,
        otherwise False
        """
        # Can't extend path outside maze
        if not self.is_inside_maze(settings, tile):
            return False
            
        # Prevents inappropriate path extension to edge of maze
        if tile.row == 0 and self.no_more_north:
            return False
        if tile.row == settings.rows - 1 and self.no_more_south:
            return False
        if tile.col == 0 and self.no_more_west:
            return False
        if tile.col == settings.cols - 1 and self.no_more_east:
            return False

        # Prevents path extension to tile adjacent to existing path tile
        used_tiles = 0
        for direction in ['U', 'D', 'L', 'R']:
            check_tile = Tile(tile.row, tile.col, direction = direction)
            if self.is_inside_maze(settings, check_tile):
                check_value = self.get_value(settings, check_tile)
                if check_value in settings.all_path_values:
                    used_tiles += 1  
        # Returns True if tile adjacent to only one path tile
        # (that is, the tile the path is extending from)
        return used_tiles == 1
        
    def extend_path(self, screen, settings, tile):
        """
        Recursive function that extends existing maze path
        from given tile
        """
        # Displays maze after each path extension
        if settings.maze_build_delay > 0:
            time.sleep(settings.maze_build_delay)
            self.draw_from_text(screen, settings)
            pygame.display.flip()
           
        # From each path tile, path extensions attempted in a
        # random sequence of directions
        direction_shuffle = random.sample(['U', 'D', 'L', 'R'], 4)
    
        # function attempts to extend path in all 4 directions
        # in random order, but calls itself as soon as it finds
        # a legal direction to move in
        for direction in direction_shuffle:
            next_tile = Tile(tile.row, tile.col, direction = direction)
            if self.can_extend_path_to_tile(settings, next_tile):
                #next_tile_value = self.choose_path_tile(settings)
                self.set_value(next_tile, settings.path_value)
                
                # If path extended to edge, update edge variables
                # (that is, no_more_X variables)
                if (next_tile.row in [0, settings.rows - 1] or
                    next_tile.col in [0, settings.cols - 1]):

                    self.update_edge_vars(settings, next_tile)
                    
                # Recursive call to extend path from next_tile
                self.extend_path(screen, settings, next_tile)
                
    def update_edge_vars(self, settings, tile):
        """
        If path extension to edge X is legal, no_more_X variable
        set to True to prevent future path extension to that edge
        and start_tile or end_tile is defined
        """
        if tile.row == 0:
            self.no_more_north = True
            if settings.start_side == 'N':
                self.set_value(tile, settings.start_value)
                self.start_tile = tile
            elif settings.end_side == 'N':
                self.set_value(tile, settings.end_value)
                self.end_tile = tile
        if tile.row == settings.rows - 1:
            self.no_more_south = True
            if settings.start_side == 'S':
                self.set_value(tile, settings.start_value)
                self.start_tile = tile
            elif settings.end_side == 'S':
                self.set_value(tile, settings.end_value)
                self.end_tile = tile
        if tile.col == settings.cols - 1:
            self.no_more_east = True
            if settings.start_side == 'E':
                self.set_value(tile, settings.start_value)
                self.start_tile = tile
            elif settings.end_side == 'E':
                self.set_value(tile, settings.end_value)
                self.end_tile = tile
        if tile.col == 0:
            self.no_more_west = True
            if settings.start_side == 'W':
                self.set_value(tile, settings.start_value)
                self.start_tile = tile
            elif settings.end_side == 'W':
                self.set_value(tile, settings.end_value)
                self.end_tile = tile

    def choose_path_tile(self, settings):
        roll = random.uniform(0, 1)
        if roll <= settings.rotate_cw_prob:
            return settings.rotate_cw_value
        elif roll <= settings.rotate_cw_prob + settings.rotate_ccw_prob:
            return settings.rotate_ccw_value
        else:
            return settings.path_value
                
    def text_display(self):
        """Displays maze in terminal as 2D text array"""
        for i in range(0, settings.rows):
            for j in range(0, settings.cols):
                print(self.values_array[i][j], end = '')
            print('\r')

    def draw_from_text(self, screen, settings):
        """Displays maze in pygame display"""
        for row in range(0, settings.rows):
            for col in range(0, settings.cols):
                new_tile = Tile(row, col, 
                                screen = screen, 
                                settings = settings)
                new_tile_value = self.get_value(settings, new_tile)
                new_tile.color = settings.tile_colors[new_tile_value]                
                new_tile.draw()
                
    def draw_from_group(self, screen, settings):
        pygame.draw.rect(screen, settings.wall_color, self.wall_rect)
        for path_tile in self.path_tiles:
            path_tile.draw()
                
    def create_path_tiles_group(self, screen, settings):
        for row in range(0, settings.rows):
            for col in range(0, settings.cols):
                new_tile = Tile(row, col, 
                                screen = screen, 
                                settings = settings)
                new_tile_value = self.get_value(settings, new_tile)
                if new_tile_value != settings.wall_value:
                    new_tile.color = settings.tile_colors[new_tile_value]
                    self.path_tiles.add(new_tile)          

    def solve(self, screen, settings, tile):
        """Solves the maze from given tile using recursive algorithm"""
        # Display attempted solution path after each step
        if settings.maze_build_delay > 0:
            time.sleep(settings.maze_build_delay)
            self.draw_from_text(screen, settings)
            for solve_tile in self.solve_tiles:
                solve_tile.draw()
            pygame.display.flip()
            
        # Maze is solved when solution path is adjacent to end_tile    
        if self.is_adjacent_to_end(tile):
            self.solved = True
            
        # Attempts to extend solution path in each direction
        # using recursive algorithm similar to extend_path function.
        # Note that if maze is solved, solution path stops extending.
        for direction in ['U', 'D', 'L', 'R']:
            if not self.solved:
                next_tile = Tile(tile.row, tile.col, screen, settings,
                                 settings.solve_color, direction)
                next_value = self.get_value(settings, next_tile)
                
                # Consider extending solution path only to path tiles
                # that are not the start tile
                if (next_value in settings.all_path_values and
                    next_value != settings.start_value):

                    # Loops through solve_tiles to see if next_tile
                    # is already on solution path
                    already_solve_tile = False
                    for solve_tile in self.solve_tiles:
                        if next_tile.same_location_as(solve_tile):
                            already_solve_tile = True
                            
                    # If next_tile not on solution path, it is added
                    # to solve tiles and recursive call made
                    # to solve function.
                    if not already_solve_tile:
                        self.solve_tiles.add(next_tile)
                        self.solve(screen, settings, next_tile)
                        
        # If solution path can't be extended from tile,
        # it's removed from solve_tiles
        if not self.solved:
            for solve_tile in self.solve_tiles.copy():
                if tile.same_location_as(solve_tile):
                    self.solve_tiles.remove(solve_tile)

    def is_adjacent_to_end(self, tile):
        """Returns True iff given tile is adjacent to end_tile"""
        for direction in ['U', 'D', 'L', 'R']:
            next_tile = Tile(tile.row, tile.col, direction = direction)
            if next_tile.same_location_as(self.end_tile):
                return True
        return False

    def choose_special_tiles(self, settings):
        special_prob = len(settings.special_tiles) / len(self.solve_tiles)
        for row in range(0, settings.rows):
            for col in range(0, settings.cols):
                new_tile = Tile(row, col)
                new_tile_value = self.get_value(settings, new_tile)
                if (new_tile_value != settings.wall_value and
                    new_tile_value != settings.start_value and
                    new_tile_value != settings.end_value):

                    roll = random.uniform(0, 1)
                    if roll <= special_prob:
                        special_value = random.choice(settings.special_tiles)
                        self.set_value(new_tile, special_value)
                        
        solve_tile_list = list(range(0, len(self.solve_tiles)))        
        solve_tile_shuffle = random.sample(solve_tile_list,
                                           len(settings.special_tiles))
        special_shuffle = random.sample(settings.special_tiles, 
                                        len(settings.special_tiles))
                                           
        i = 0
        for solve_tile in self.solve_tiles:
            if i in solve_tile_shuffle:
                self.set_value(solve_tile, special_shuffle.pop())
            else:
                self.set_value(solve_tile, settings.path_value)
            i += 1
