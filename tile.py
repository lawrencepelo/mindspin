import pygame
from pygame.sprite import Sprite
import datetime

class Tile(Sprite):
    """Generate a tile"""
    # All tiles have a location (row & col) but only tiles intended
    # to be drawn need screen, sets, color.
    def __init__(self, ref_row, ref_col, screen = None, sets = None, 
                 color = None, direction = None):
        super(Tile, self).__init__()
        self.screen = screen
        self.color = color
        
        # Tile located one move from the ref_row/col
        # in the given direction
        if direction == 'U':
            self.row = ref_row - 1
            self.col = ref_col
        elif direction == 'D':
            self.row = ref_row + 1
            self.col = ref_col
        elif direction == 'L':
            self.row = ref_row
            self.col = ref_col - 1
        elif direction == 'R':
            self.row = ref_row
            self.col = ref_col + 1
        else:
            self.row = ref_row
            self.col = ref_col
        
        # If tile is to be drawn, create its rect
        if sets != None:
            self.create_rect(sets)
        else:
            self.rect = None
            
    def move(self, sets, direction):
        """Move given tile one space in given direction"""
        if direction == 'U':
            self.row -= 1
        elif direction == 'D':
            self.row += 1
        elif direction == 'L':
            self.col -= 1
        elif direction == 'R':
            self.col += 1
        
        if self.rect != None:
            self.create_rect(sets)
        
    def same_location_as(self, other_tile):
        """Returns true iff tile and other_tile share same row, col"""
        if self.row == other_tile.row and self.col == other_tile.col:
            return True
        else:
            return False
    
    def draw(self):
        """Draw the tile to the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)
        
    def create_rect(self, sets):
        """ Create rect for tiles intended to be displayed """
        self.rect = pygame.Rect(
            sets.maze_topleft_x +
                self.col * sets.tile_total_size +
                sets.tile_border,
            sets.maze_topleft_y +
                self.row * sets.tile_total_size + 
                sets.tile_border,
            sets.tile_size,
            sets.tile_size)
            
    def rotate_cw(self, sets):
        """ Change tile coordinates after maze rotates clockwise """
        temp = self.row
        self.row = self.col
        self.col = sets.rows - temp - 1
        self.create_rect(sets)
        
    def rotate_ccw(self, sets):
        """ Change tile coords after maze rotates counter-clockwise """
        temp = self.row
        self.row = sets.cols - self.col - 1
        self.col = temp
        self.create_rect(sets)
        
    def reflect_x(self, sets):
        """ Change tile coordinates after maze
            reflects around x-axis """
        self.row = sets.rows - self.row - 1
        self.create_rect(sets)

    def reflect_y(self, sets):
        """ Change tile coordinates after maze
            reflects around y-axis """
        self.col = sets.cols - self.col - 1
        self.create_rect(sets)
