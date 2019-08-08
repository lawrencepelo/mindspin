import sys
import pygame
import datetime
import random
from tile import Tile
import time

def update_screen(sets, screen, maze, player_tile,
                  stats, play_button, sb, arrows):
    """Update images on the screen and flip to the new screen"""
    # Redraw the screen during each pass through the loop
    screen.fill(sets.bg_color)
    # Only draws maze & player tile if not in 'before' status
    if stats.maze_status == 'before':
        play_button.draw_button()
    else:
        maze.draw_maze(screen, sets)
        player_tile.draw()
        
    sb.prep_bonus(sets, stats)
    sb.prep_compass(sets, maze, arrows)
    sb.draw_scoreboard()
    pygame.display.flip()
    
def check_events(sets, screen, maze, player_tile, arrows,
                 stats, play_button, sb):
    """Respond to keypresses and mouse events"""
    for event in pygame.event.get():
        # Close window if user clicks 'X' box
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(sets, screen, event,
                                 maze, player_tile, arrows, stats, sb)
            
def check_keydown_events(sets, screen, event, maze, player_tile,
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
        sb.prep_message(sets, '')
        stats.start_time = datetime.datetime.now()
    # If 'during' status (maze is activated and player can move),
    # arrow keypress is interpreted based on arrows object
    elif stats.maze_status == 'during' and event.key in arrow_keys:
        if event.key == pygame.K_UP:
            direction = arrows.north
        elif event.key == pygame.K_DOWN:
            direction = arrows.south
        elif event.key == pygame.K_LEFT:
            direction = arrows.west
        elif event.key == pygame.K_RIGHT:
            direction = arrows.east
            
        next_tile = Tile(player_tile.row, player_tile.col,
                         direction = direction)
        if maze.can_move_to_tile(sets, next_tile):
            player_tile.move(sets, direction)
            new_tile_color = maze.get_tile_color(player_tile)
            # take action based on next tile, such as update arrows
            call_tile_event(sets, maze, player_tile, arrows,
                            new_tile_color, stats, sb)

def call_tile_event(sets, maze, player_tile, arrows, tile_color,
                    stats, sb):
    """Implements event based on tile color"""
    # If tile is a rotate/reflect tile,
    # adjust arrows and rotate/reflect path tiles,
    # and adjust score.
    if tile_color == sets.rotate_cw_color:
        arrows.rotate_cw()
        for path_tile in maze.path_tiles:
            path_tile.rotate_cw(sets)
        player_tile.rotate_cw(sets)
        stats.score += sets.special_tile_bonus
    elif tile_color == sets.rotate_ccw_color:
        arrows.rotate_ccw()
        for path_tile in maze.path_tiles:
            path_tile.rotate_ccw(sets)
        player_tile.rotate_ccw(sets)
        stats.score += sets.special_tile_bonus
    elif tile_color == sets.reflect_x_color:
        arrows.reflect_x()
        for path_tile in maze.path_tiles:
            path_tile.reflect_x(sets)
        player_tile.reflect_x(sets)
        stats.score += sets.special_tile_bonus
    elif tile_color == sets.reflect_y_color:
        arrows.reflect_y()
        for path_tile in maze.path_tiles:
            path_tile.reflect_y(sets)
        player_tile.reflect_y(sets)
        stats.score += sets.special_tile_bonus
    sb.prep_score(sets, stats)
        
def player_solved_maze(sets, screen, maze, player_tile,
                       stats, play_button, sb, arrows):
    """
    When player solves maze, update sets/stats
    and prepare for next level
    """
    # Choose & display a random congratulatory message
    # Note pauses between message changes
    solved_msg = random.choice(sets.solved_msgs)
    sb.prep_message(sets, solved_msg)
    update_screen(sets, screen, maze, player_tile,
                  stats, play_button, sb, arrows)
    time.sleep(sets.solve_pause)
    
    # Status change placed after congratulatory message
    # because 'solved' status sets bonus timer to 0
    stats.maze_status = 'solved'
    
    # Timer bonus added to score
    stats.score += sb.bonus
    sb.prep_score(sets, stats)
    sb.prep_message(sets, 'TIME BONUS: ' + str(sb.bonus))
    update_screen(sets, screen, maze, player_tile,
                  stats, play_button, sb, arrows)
    time.sleep(sets.solve_pause)
    
    # Calculate/display difficulty bonus and add to score
    diff_bonus = len(maze.solve_tiles) * sets.diff_bonus_multiplier
    stats.score += diff_bonus
    sb.prep_score(sets, stats)
    sb.prep_message(sets, 'DIFFICULTY BONUS: ' + str(diff_bonus))
    update_screen(sets, screen, maze, player_tile,
                  stats, play_button, sb, arrows)
    time.sleep(sets.solve_pause)
    
    # Increment level
    stats.level += 1
    # Recalculate settingss based on changed settings
    sets.calculate(stats)
    # Change status so player can start next maze
    stats.maze_status = 'before'
