import itertools
import random
from tile import Tile

class Maze():
    """Generate a random maze and edit its values"""
    
    def __init__(self, rows = 20, cols = 20, start_side = 'B', end_side = 'T'):
        self.rows = rows
        self.cols = cols
        self.start_side = start_side
        self.end_side = end_side
        
        if start_side == 'T' or end_side == 'T':
            self.no_more_top = False
        else:
            self.no_more_top = True
        if start_side == 'B' or end_side == 'B':
            self.no_more_bottom = False
        else:
            self.no_more_bottom = True
        if start_side == 'R' or end_side == 'R':
            self.no_more_right = False
        else:
            self.no_more_right = True
        if start_side == 'L' or end_side == 'L':
            self.no_more_left = False
        else:
            self.no_more_left = True
        
        self.values_array = []
        initial_row = list(itertools.repeat('#', cols))
        for _ in range(0, rows):
            self.values_array.append(initial_row.copy())
            
        self.generate()
            
    def is_inside_maze(self, tile):
        return (tile.row >= 0 and tile.row < self.rows and 
                tile.col >= 0 and tile.col < self.cols)
                
    def get_value(self, tile):
        return self.values_array[tile.row][tile.col]
        
    def set_value(self, tile, val):
        self.values_array[tile.row][tile.col] = val
        
    def can_move_to_tile(self, tile):
        if not self.is_inside_maze(tile):
            return False
            
        if tile.row == 0 and self.no_more_top:
            return False
        if tile.row == self.rows - 1 and self.no_more_bottom:
            return False
        if tile.col == 0 and self.no_more_left:
            return False
        if tile.col == self.cols - 1 and self.no_more_right:
            return False

        used_tiles = 0
        for direction in ['N', 'S', 'E', 'W']:
            check_tile = Tile(tile.row, tile.col, direction)
            if self.is_inside_maze(check_tile):
                if self.get_value(check_tile) == ' ':
                    used_tiles += 1  
                     
        return used_tiles == 1
        
    def generate(self):
        initial_tile = Tile(self.rows // 2, self.cols // 2)
        self.set_value(initial_tile, ' ')
        self.extend_path(initial_tile)
        
    def extend_path(self, tile):
        direction_shuffle = random.sample(['N', 'S', 'E', 'W'], 4)
    
        for direction in direction_shuffle:
            next_tile = Tile(tile.row, tile.col, direction)
            if self.can_move_to_tile(next_tile):
                self.set_value(next_tile, ' ')
                
                if next_tile.row == 0:
                    self.no_more_top = True
                    if self.start_side == 'T':
                        self.set_value(next_tile, 'S')
                    elif self.end_side == 'T':
                        self.set_value(next_tile, 'E')
                if next_tile.row == self.rows - 1:
                    self.no_more_bottom = True
                    if self.start_side == 'B':
                        self.set_value(next_tile, 'S')
                    elif self.end_side == 'B':
                        self.set_value(next_tile, 'E')
                if next_tile.col == 0:
                    self.no_more_left = True
                    if self.start_side == 'L':
                        self.set_value(next_tile, 'S')
                    elif self.end_side == 'L':
                        self.set_value(next_tile, 'E')
                if next_tile.col == self.cols - 1:
                    self.no_more_right = True
                    if self.start_side == 'R':
                        self.set_value(next_tile, 'S')
                    elif self.end_side == 'R':
                        self.set_value(next_tile, 'E')
                    
                self.extend_path(next_tile)
                
    def display(self):
        for i in range(0, self.rows):
            for j in range(0, self.cols):
                print(self.values_array[i][j], end = '')
            print('\r')
