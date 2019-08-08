import itertools
import random
import pygame
import time
import datetime
from pygame.sprite import Group
from tile import Tile

class Maze():
    """Generate a random maze and edit its values"""
    
    def __init__(self, screen, sets):
        # no_more_X variables, when True, prevent path tiles from
        # being placed on edges, keeping the edges of the maze as solid
        # walls except for Start and End tiles
        if sets.start_side == 'U' or sets.end_side == 'U':
            self.no_more_up = False
        else:
            self.no_more_up = True
        if sets.start_side == 'D' or sets.end_side == 'D':
            self.no_more_down = False
        else:
            self.no_more_down = True
        if sets.start_side == 'R' or sets.end_side == 'R':
            self.no_more_right = False
        else:
            self.no_more_right = True
        if sets.start_side == 'L' or sets.end_side == 'L':
            self.no_more_left = False
        else:
            self.no_more_left = True

        # wall_rect is a blank rectangle that outlines the maze,
        # the path tiles will be drawn on top of it.
        self.wall_rect = pygame.Rect(
            sets.maze_topleft_x,
            sets.maze_topleft_y,
            sets.cols * sets.tile_total_size,
            sets.rows * sets.tile_total_size)
            
        # Picks first path tile and sends to extend_path function
        initial_tile = Tile(sets.initial_tile_row,
                            sets.initial_tile_col,
                            screen, sets, sets.path_color)
        self.path_tiles = Group()
        self.path_tiles.add(initial_tile)
        self.extend_path(screen, sets, initial_tile)
        
        # solve_tiles Group contains tiles on the solution path
        self.solve_tiles = Group()
        # self.solved = True when the maze solution has been found
        self.solved = False
        # Solves the maze and populates the solve_tiles Group
        self.solve(screen, sets, self.get_start_tile(sets))
        
        # Chooses types and locations of special tiles.
        self.choose_special_tiles(sets)    
            
    def is_inside_maze(self, sets, tile):
        """"Returns True if tile is inside maze, otherwise False"""
        return (tile.row >= 0 and tile.row < sets.rows and 
                tile.col >= 0 and tile.col < sets.cols)
                
    def is_path_tile(self, tile):
        """Returns True if location of given tile is on the maze path,
           returns False otherwise"""
        for path_tile in self.path_tiles:
            if tile.same_location_as(path_tile):
                return True
        return False
        
    def is_solve_tile(self, tile):
        """Returns True if location of given tile is on solution path,
           returns False otherwise"""
        for solve_tile in self.solve_tiles:
            if tile.same_location_as(solve_tile):
                return True
        return False
        
    def is_adjacent_to_end(self, sets, tile):
        """Returns True iff given tile is adjacent to end_tile"""
        for direction in ['U', 'D', 'L', 'R']:
            next_tile = Tile(tile.row, tile.col, direction = direction)
            if next_tile.same_location_as(self.get_end_tile(sets)):
                return True
        return False
        
    def can_move_to_tile(self, sets, tile):
        """Returns True if given tile is on path, otherwise False"""
        for path_tile in self.path_tiles:
            if tile.same_location_as(path_tile):
                return True
        return False
        
    def get_start_tile(self, sets):
        """Returns start tile"""
        for path_tile in self.path_tiles:
            if path_tile.color == sets.start_color:
                return path_tile
        return None
        
    def get_end_tile(self, sets):
        """Returns end tile"""
        for path_tile in self.path_tiles:
            if path_tile.color == sets.end_color:
                return path_tile
        return None
        
    def get_tile_color(self, tile):
        """Returns color of given tile"""
        for path_tile in self.path_tiles:
            if tile.same_location_as(path_tile):
                return path_tile.color
        return None
        
    def get_path_tile(self, tile):
        """Returns path tile at same location as given tile"""
        for path_tile in self.path_tiles:
            if tile.same_location_as(path_tile):
                return path_tile
        return None

    def can_extend_path_to_tile(self, sets, tile):
        """
        Returns True if extend_path function can move to given tile,
        otherwise False
        """
        # Can't extend path outside maze
        if not self.is_inside_maze(sets, tile):
            return False
            
        # Prevents inappropriate path extension to edge of maze
        if tile.row == 0 and self.no_more_up:
            return False
        if tile.row == sets.rows - 1 and self.no_more_down:
            return False
        if tile.col == 0 and self.no_more_left:
            return False
        if tile.col == sets.cols - 1 and self.no_more_right:
            return False

        # Prevents path extension to tile adjacent to existing path tile
        used_tiles = 0
        for direction in ['U', 'D', 'L', 'R']:
            check_tile = Tile(tile.row, tile.col, direction = direction)
            if (self.is_inside_maze(sets, check_tile) and
                self.is_path_tile(check_tile)):

               used_tiles += 1
               
        # Returns True if tile adjacent to only one path tile
        # (that is, the tile the path is extending from)
        return used_tiles == 1
        
    def extend_path(self, screen, sets, tile):
        """
        Recursive function that extends existing maze path
        from given tile
        """
        # Displays maze after each path extension
        if sets.maze_build_delay > 0:
            time.sleep(sets.maze_build_delay)
            self.draw_maze(screen, sets)
            pygame.display.flip()
           
        # From each path tile, path extensions attempted in a
        # random sequence of directions
        direction_shuffle = random.sample(['U', 'D', 'L', 'R'], 4)
    
        # function attempts to extend path in all 4 directions
        # in random order, but calls itself as soon as it finds
        # a legal direction to move in
        for direction in direction_shuffle:
            next_tile = Tile(tile.row, tile.col, screen, sets, 
                             sets.path_color, direction)
            if self.can_extend_path_to_tile(sets, next_tile):
                self.path_tiles.add(next_tile)
                
                # If path extended to edge, update edge variables
                # (that is, no_more_X variables)
                if (next_tile.row in [0, sets.rows - 1] or
                    next_tile.col in [0, sets.cols - 1]):

                    self.update_edge_vars(sets, next_tile)
                    
                # Recursive call to extend path from next_tile
                self.extend_path(screen, sets, next_tile)
                
    def update_edge_vars(self, sets, tile):
        """
        If path extension to edge X is legal, no_more_X variable
        set to True to prevent future path extension to that edge
        and start_tile or end_tile is defined
        """
        if tile.row == 0:
            self.no_more_up = True
            if sets.start_side == 'U':
                tile.color = sets.start_color
            elif sets.end_side == 'U':
                tile.color = sets.end_color
        if tile.row == sets.rows - 1:
            self.no_more_down = True
            if sets.start_side == 'D':
                tile.color = sets.start_color
            elif sets.end_side == 'D':
                tile.color = sets.end_color
        if tile.col == sets.cols - 1:
            self.no_more_right = True
            if sets.start_side == 'R':
                tile.color = sets.start_color
            elif sets.end_side == 'R':
                tile.color = sets.end_color
        if tile.col == 0:
            self.no_more_left = True
            if sets.start_side == 'L':
                tile.color = sets.start_color
            elif sets.end_side == 'L':
                tile.color = sets.end_color
                
    def draw_maze(self, screen, sets):
        """ Draws all path tiles """
        pygame.draw.rect(screen, sets.wall_color, self.wall_rect)
        for path_tile in self.path_tiles:
            path_tile.draw()
                
    def solve(self, screen, sets, tile):
        """Solves the maze from given tile using recursive algorithm"""
        # Display attempted solution path after each step
        if sets.maze_build_delay > 0:
            time.sleep(sets.maze_build_delay)
            self.draw_maze(screen, sets)
            for solve_tile in self.solve_tiles:
                solve_tile.draw()
            pygame.display.flip()
            
        # Maze is solved when solution path is adjacent to end_tile    
        if self.is_adjacent_to_end(sets, tile):
            self.solved = True
            
        # Attempts to extend solution path in each direction
        # using recursive algorithm similar to extend_path function.
        # Note that if maze is solved, solution path stops extending.
        for direction in ['U', 'D', 'L', 'R']:
            if not self.solved:
                next_tile = Tile(tile.row, tile.col, screen, sets,
                                 sets.solve_color, direction)
                
                # Consider extending solution path only to path tiles
                # that are not the start tile
                if (self.is_path_tile(next_tile) and
                    not next_tile.same_location_as(self.get_start_tile(sets)) and
                    not self.is_solve_tile(next_tile)):
                            
                    # If next_tile not on solution path, it is added
                    # to solve tiles and recursive call made
                    # to solve function.
                    self.solve_tiles.add(next_tile)
                    self.solve(screen, sets, next_tile)
                        
        # If solution path can't be extended from tile,
        # it's removed from solve_tiles
        if not self.solved:
            for solve_tile in self.solve_tiles.copy():
                if tile.same_location_as(solve_tile):
                    self.solve_tiles.remove(solve_tile)

    def choose_special_tiles(self, sets):
        """Chooses types and locations of special tiles"""
        # Probability that a tile not on the solution path
        # will be a special tile.
        special_prob = (len(sets.special_tile_colors) / 
                        len(self.solve_tiles))
        s_tile = self.get_start_tile(sets)
        e_tile = self.get_end_tile(sets)
        # Loop through path tiles, each one has special_prob
        # probability of being a special tile.
        for path_tile in self.path_tiles:
            if not(path_tile.same_location_as(s_tile) or
                   path_tile.same_location_as(e_tile)):

                    roll = random.uniform(0, 1)
                    if roll <= special_prob:
                        c = random.choice(sets.special_tile_colors)
                        path_tile.color = c
                            
        # Get random sample of solve tiles (represented by numbers)
        # that will become special tiles
        # and shuffle list of special tile colors.                 
        solve_tile_list = list(range(0, len(self.solve_tiles))) 
        num_specs = len(sets.special_tile_colors)
        solve_tile_shuffle = random.sample(solve_tile_list, num_specs)
        special_shuffle = random.sample(sets.special_tile_colors, 
                                        num_specs)
        
        # Loop through solve tiles, if counter matches random sample
        # in solve_tile_shuffle, that solve tile will become a
        # special tile, otherwise it is an ordinary path tile,
        # even if it was designated a special tile earlier in
        # this function.                       
        i = 0
        for solve_tile in self.solve_tiles:
            path_tile = self.get_path_tile(solve_tile)
            if i in solve_tile_shuffle:
                path_tile.color = special_shuffle.pop()
            else:
                path_tile.color = sets.path_color
            i += 1
