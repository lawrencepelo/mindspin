import sys
import pygame
import datetime
from tile import Tile

def update_screen(settings, screen, maze, player_tile):
    """Update images on the screen and flip to the new screen"""
    # Redraw the screen during each pass through the loop
    screen.fill(settings.bg_color)
    maze.draw(screen, settings)
    player_tile.draw()
    pygame.display.flip()
    
def check_events(settings, screen, maze, player_tile, arrows):
    """Respond to keypresses and mouse events"""
    for event in pygame.event.get():
        # Close window if user clicks 'X' box
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(settings, screen, event,
                                 maze, player_tile, arrows)
            
def check_keydown_events(settings, screen, event, maze, player_tile,
                         arrows):
    """Respond to keypresses"""
    # If arrow key pressed, player tile moves if possible
    if event.key in [pygame.K_UP, pygame.K_DOWN,
                     pygame.K_LEFT, pygame.K_RIGHT]:
        if event.key == pygame.K_UP:
            direction = arrows.up
        elif event.key == pygame.K_DOWN:
            direction = arrows.down
        elif event.key == pygame.K_LEFT:
            direction = arrows.left
        elif event.key == pygame.K_RIGHT:
            direction = arrows.right
            
        next_tile = Tile(player_tile.row, player_tile.col,
                         direction = direction)
        if maze.can_move_to_tile(settings, next_tile):
            player_tile.move(settings, direction)
            # take action based on next tile, such as updating arrows
            call_tile_event(settings, arrows, 
                            maze.get_value(settings, player_tile))
    
    # If 'q' key pressed, game quits
    elif event.key == pygame.K_q:
        sys.exit()

def call_tile_event(settings, arrows, tile_value):
    """Implements event based on tile value"""
    if tile_value == settings.rotate_cw_value:
        arrows.rotate_cw()
    elif tile_value == settings.rotate_ccw_value:
        arrows.rotate_ccw()
    elif tile_value == settings.reflect_x_value:
        arrows.reflect_x()
    elif tile_value == settings.reflect_y_value:
        arrows.reflect_y()
    elif tile_value == settings.end_value:
        print('You solved the maze!!!')
