import sys
import pygame
import datetime
from tile import Tile
import time

def update_screen(settings, screen, maze, player_tile,
                  stats, play_button):
    """Update images on the screen and flip to the new screen"""
    # Redraw the screen during each pass through the loop
    screen.fill(settings.bg_color)
    if stats.game_active:
        maze.draw(screen, settings)
        player_tile.draw()
    else:
        play_button.draw_button()
        
    pygame.display.flip()
    
def check_events(settings, screen, maze, player_tile, arrows,
                 stats, play_button):
    """Respond to keypresses and mouse events"""
    for event in pygame.event.get():
        # Close window if user clicks 'X' box
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(settings, screen, event,
                                 maze, player_tile, arrows, stats)
            
def check_keydown_events(settings, screen, event, maze, player_tile,
                         arrows, stats):
    """Respond to keypresses"""
    # If arrow key pressed, player tile moves if possible
    if event.key in [pygame.K_UP, pygame.K_DOWN,
                     pygame.K_LEFT, pygame.K_RIGHT]:
        if stats.game_active:
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
                new_tile_value = maze.get_value(settings, player_tile)
                # take action based on next tile, such as updating arrows
                call_tile_event(settings, arrows, new_tile_value, stats)
        else: # not stats.game_active
            stats.game_active = True
            stats.start_time = datetime.datetime.now()
                
    # If 'q' key pressed, game quits
    elif event.key == pygame.K_q:
        sys.exit()

def call_tile_event(settings, arrows, tile_value, stats):
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
        stats.finish_time = datetime.datetime.now()
        
def player_solved_maze(settings, stats):
    stats.game_active = False
    time_delta = stats.finish_time - stats.start_time
    time_secs = time_delta.total_seconds()
    bonus = settings.bonus_coeff * time_secs ** 2 + settings.bonus_start
    print(bonus)
    time.sleep(settings.solve_pause)
