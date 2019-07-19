import pygame
from pygame.sprite import Sprite
import datetime

class Tile(Sprite):
    """Generate a tile"""
    # All tiles have a location (row & col) but only tiles intended
    # to be drawn need screen, settings, color.
    def __init__(self, ref_row, ref_col, screen = None, settings = None, 
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
        if settings != None:
            self.rect = pygame.Rect(
                self.col * settings.tile_size + settings.border_x,
                self.row * settings.tile_size + settings.border_y + 
                           settings.scoreboard_height,
                settings.tile_size,
                settings.tile_size)
        else:
            self.rect = None
            
    def move(self, settings, direction):
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
            self.rect = pygame.Rect(
                self.col * settings.tile_size + settings.border_x,
                self.row * settings.tile_size + settings.border_y + 
                           settings.scoreboard_height,
                settings.tile_size,
                settings.tile_size)    
        
    def same_location_as(self, other_tile):
        """Returns true iff tile and other_tile share same row, col"""
        if self.row == other_tile.row and self.col == other_tile.col:
            return True
        else:
            return False
    
    def draw(self):
        """Draw the tile to the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)
