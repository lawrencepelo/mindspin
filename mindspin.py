import pygame
import os
from maze import Maze
from tile import Tile
from settings import Settings
from arrows import Arrows
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
import game_functions as gf
import datetime
import time

def run_game():
    """Central function that controls the game"""
   
    pygame.init()
    pygame.mouse.set_visible(False)
    
    # Initialize sets and stats
    stats = GameStats()    
    sets = Settings(stats)
    
    # main gameplay loop
    while True:    
        # Locate pygame display on monitor
        os.environ['SDL_VIDEO_WINDOW_POS']="%d,%d" % (sets.screen_x,
                                                      sets.screen_y)
    
        # Maze size can change with each level, so pygame display,
        # scoreboard, and play button must be reconfigured
        # before each level
        screen = pygame.display.set_mode(
            (sets.screen_width, sets.screen_height))
        pygame.display.set_caption('Mindspin')    
        sb = Scoreboard(sets, screen, stats)
        sb.prep_score(sets, stats)
        sb.prep_level(sets, stats)
        sb.prep_message(sets, 'MESSAGE')
        play_button = Button(sets, screen, stats)
        
        # Create random maze
        maze = Maze(screen, sets)
        
        # Create tile that player will move through maze
        player_tile = Tile(maze.get_start_tile(sets).row,
                           maze.get_start_tile(sets).col,
                           screen, sets, sets.player_color)
                       
        # Create object that determines which direction player tile 
        # moves when arrow keys are pressed
        arrows = Arrows(sets)
        
        # Clear excess keypresses from event queue
        pygame.event.clear()
        
        # Loop continually checks for player keypresses
        # and redraws screen until player solves maze or quits
        while not player_tile.same_location_as(maze.get_end_tile(sets)):
            gf.check_events(sets, screen, maze, player_tile,
                            arrows, stats, play_button, sb)
            gf.update_screen(sets, screen, maze, player_tile,
                             stats, play_button, sb, arrows)
                             
        # Updates score and prepares for next level
        gf.player_solved_maze(sets, screen, maze, player_tile,
                              stats, play_button, sb, arrows)

run_game()
