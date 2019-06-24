import pygame
from pygame.sprite import Sprite

class Tile(Sprite):
    """Generate a tile"""    
    def __init__(self, ref_row, ref_col, screen = None, settings = None, 
                 color = None, direction = None):
        super(Tile, self).__init__()
        self.screen = screen
        self.color = color
        
        # Tile located one move from the ref_row/col
        # in the given direction
        if direction == 'N':
            self.row = ref_row - 1
            self.col = ref_col
        elif direction == 'S':
            self.row = ref_row + 1
            self.col = ref_col
        elif direction == 'E':
            self.row = ref_row
            self.col = ref_col + 1
        elif direction == 'W':
            self.row = ref_row
            self.col = ref_col - 1
        else:
            self.row = ref_row
            self.col = ref_col
        
        if settings != None:
            self.rect = pygame.Rect(
                self.col * settings.tile_size + settings.border_x,
                self.row * settings.tile_size + settings.border_y,
                settings.tile_size,
                settings.tile_size)
        else:
            self.rect = None
                                
    def draw_tile(self):
        """Draw the tile to the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)
