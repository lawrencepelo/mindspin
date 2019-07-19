import sys
import pygame
import datetime
import random
from tile import Tile
import time

def update_screen(settings, screen, maze, player_tile,
                  stats, play_button, sb):
    """Update images on the screen and flip to the new screen"""
    # Redraw the screen during each pass through the loop
    screen.fill(settings.bg_color)
    # Only draws player tile in 'before' status
    # Only draws maze & player tile if not in 'before' status
    if stats.maze_status == 'before':
        play_button.draw_button()
    else:
        maze.draw(screen, settings)
        player_tile.draw()
        
    sb.prep_bonus(settings, stats)
    sb.draw_scoreboard()
    pygame.display.flip()
    
def check_events(settings, screen, maze, player_tile, arrows,
                 stats, play_button, sb):
    """Respond to keypresses and mouse events"""
    for event in pygame.event.get():
        # Close window if user clicks 'X' box
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(settings, screen, event,
                                 maze, player_tile, arrows, stats, sb)
            
def check_keydown_events(settings, screen, event, maze, player_tile,
                         arrows, stats, sb):
    """Respond to keypresses"""
    arrow_keys = [pygame.K_UP, pygame.K_DOWN, 
                  pygame.K_LEFT, pygame.K_RIGHT]
    # If 'q' key pressed, game quits
    if event.key == pygame.K_q:
        sys.exit()
    # If 'before' status, an arrow keypress activates maze
    elif stats.maze_status == 'before' and event.key in arrow_keys:
        stats.maze_status = 'during'
        sb.prep_message(settings, '')
        stats.start_time = datetime.datetime.now()
    # If 'during' status (maze is activated and player can move),
    # arrow keypress is interpreted based on arrows object
    elif stats.maze_status == 'during' and event.key in arrow_keys:
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
            # take action based on next tile, such as update arrows
            call_tile_event(settings, arrows, new_tile_value, stats)

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
        
def player_solved_maze(settings, screen, maze, player_tile,
                       stats, play_button, sb):
    """
    When player solves maze, update settings/stats
    and prepare for next level
    """
    # Choose & display a random congratulatory message
    # Note pauses between message changes
    solved_msg = random.choice(settings.solved_msgs)
    sb.prep_message(settings, solved_msg)
    update_screen(settings, screen, maze, player_tile,
                  stats, play_button, sb)
    time.sleep(settings.solve_pause)
    
    # Status change placed after congratulatory message
    # because 'solved' status sets bonus timer to 0
    stats.maze_status = 'solved'
    
    # Timer bonus added to score
    stats.score += sb.bonus
    sb.prep_score(settings, stats)
    sb.prep_message(settings, 'TIME BONUS: ' + str(sb.bonus))
    update_screen(settings, screen, maze, player_tile,
                  stats, play_button, sb)
    time.sleep(settings.solve_pause)
    
    # Calculate/display difficulty bonus and add to score
    diff_bonus = len(maze.solve_tiles) * settings.diff_bonus_multiplier
    stats.score += diff_bonus
    sb.prep_score(settings, stats)
    sb.prep_message(settings, 'DIFFICULTY BONUS: ' + str(diff_bonus))
    update_screen(settings, screen, maze, player_tile,
                  stats, play_button, sb)
    time.sleep(settings.solve_pause)
    
    # Increment level
    stats.level += 1
    # Increase difficulty of next maze
    settings.rows += 1
    settings.cols += 2
    # Recalculate settings based on changed settings
    settings.calculate()
    # Change status so player can start next maze
    stats.maze_status = 'before'
