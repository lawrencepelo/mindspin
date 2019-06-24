import itertools
import random
import pygame
from pygame.sprite import Group
from tile import Tile

class Maze():
    """Generate a random maze and edit its values"""
    
    def __init__(self, settings):
        self.rows = settings.rows
        self.cols = settings.cols
        self.start_side = settings.start_side
        self.end_side = settings.end_side
        self.wall_value = settings.wall_value
        self.path_value = settings.path_value
        self.start_value = settings.start_value
        self.end_value = settings.end_value
        
        # no_more_X variables, when True, prevent path tiles from
        # being placed on edges, keeping the edges of the maze as solid
        # walls except for Start and End tiles
        if self.start_side == 'T' or self.end_side == 'T':
            self.no_more_top = False
        else:
            self.no_more_top = True
        if self.start_side == 'B' or self.end_side == 'B':
            self.no_more_bottom = False
        else:
            self.no_more_bottom = True
        if self.start_side == 'R' or self.end_side == 'R':
            self.no_more_right = False
        else:
            self.no_more_right = True
        if self.start_side == 'L' or self.end_side == 'L':
            self.no_more_left = False
        else:
            self.no_more_left = True
        
        # Initialize values_array to all wall tiles
        self.values_array = []
        initial_row = list(itertools.repeat(self.wall_value,
                                            self.cols))
        for _ in range(0, self.rows):
            self.values_array.append(initial_row.copy())
            
        # Picks first path tile and sends to extend_path function
        initial_tile = Tile(self.rows // 2 + 1, self.cols // 2 + 1)
        self.set_value(initial_tile, self.path_value)
        self.extend_path(initial_tile)
            
    def is_inside_maze(self, tile):
        """"Returns True if tile is inside maze, otherwise False"""
        return (tile.row >= 0 and tile.row < self.rows and 
                tile.col >= 0 and tile.col < self.cols)
    
    def get_value(self, tile):
        """Returns value from values_array at location of given tile"""
        return self.values_array[tile.row][tile.col]
        
    def set_value(self, tile, val):
        """Edits value in values_array at location of given tile"""
        self.values_array[tile.row][tile.col] = val
        

    def can_move_to_tile(self, tile):
        """Returns True if extend_path function can move to given tile,
           otherwise False"""
        # Can't move outside maze
        if not self.is_inside_maze(tile):
            return False
            
        # Prevents inappropriate move to edge of maze
        if tile.row == 0 and self.no_more_top:
            return False
        if tile.row == self.rows - 1 and self.no_more_bottom:
            return False
        if tile.col == 0 and self.no_more_left:
            return False
        if tile.col == self.cols - 1 and self.no_more_right:
            return False

        # Prevents move to tile adjacent to existing path tile
        used_tiles = 0
        # 'N'=up(north), 'S'=down(south),'E'=right(east), 'W'=left(west)
        for direction in ['N', 'S', 'E', 'W']:
            check_tile = Tile(tile.row, tile.col, direction = direction)
            if self.is_inside_maze(check_tile):
                if self.get_value(check_tile) == self.path_value:
                    used_tiles += 1  

        return used_tiles == 1
        
    def extend_path(self, tile):
        """Recursive function that extends existing maze path
           from given tile"""
        # 'N'=up(north), 'S'=down(south),'E'=right(east), 'W'=left(west)
        direction_shuffle = random.sample(['N', 'S', 'E', 'W'], 4)
    
        # function attempts to extend path in all 4 directions
        # in random order, but calls itself as soon as it finds
        # a legal direction to move in
        for direction in direction_shuffle:
            next_tile = Tile(tile.row, tile.col, direction = direction)
            if self.can_move_to_tile(next_tile):
                self.set_value(next_tile, self.path_value)
                
                # If move to edge is legal, no_more_X variable
                # set to prevent future move to edge
                # and start/end tile is defined
                if next_tile.row == 0:
                    self.no_more_top = True
                    if self.start_side == 'T':
                        self.set_value(next_tile, self.start_value)
                    elif self.end_side == 'T':
                        self.set_value(next_tile, self.end_value)
                if next_tile.row == self.rows - 1:
                    self.no_more_bottom = True
                    if self.start_side == 'B':
                        self.set_value(next_tile, self.start_value)
                    elif self.end_side == 'B':
                        self.set_value(next_tile, self.end_value)
                if next_tile.col == 0:
                    self.no_more_left = True
                    if self.start_side == 'L':
                        self.set_value(next_tile, self.start_value)
                    elif self.end_side == 'L':
                        self.set_value(next_tile, self.end_value)
                if next_tile.col == self.cols - 1:
                    self.no_more_right = True
                    if self.start_side == 'R':
                        self.set_value(next_tile, self.start_value)
                    elif self.end_side == 'R':
                        self.set_value(next_tile, self.end_value)
                    
                # Recursive call to extend path from next_tile
                self.extend_path(next_tile)
                
    def text_display(self):
        """Displays maze in terminal as 2D text array"""
        for i in range(0, self.rows):
            for j in range(0, self.cols):
                print(self.values_array[i][j], end = '')
            print('\r')

    def draw(self, screen, settings):
        """Displays maze in pygame display"""
        tiles = Group()
        for row in range(0, self.rows):
            for col in range(0, self.cols):
                new_tile = Tile(row, col, 
                                screen = screen, 
                                settings = settings)
                
                if self.get_value(new_tile) == self.wall_value:
                    new_tile.color = settings.wall_color
                elif self.get_value(new_tile) == self.path_value:
                    new_tile.color = settings.path_color
                elif self.get_value(new_tile) == self.start_value:
                    new_tile.color = settings.start_color
                elif self.get_value(new_tile) == self.end_value:
                    new_tile.color = settings.end_color
                
                tiles.add(new_tile)
                
        for tile in tiles:
            tile.draw_tile()
                
                
