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
    
    # Initialize settings and stats
    settings = Settings()
    stats = GameStats()
    
    # main gameplay loop
    while True:    
        # Locate pygame display on monitor
        os.environ['SDL_VIDEO_WINDOW_POS']="%d,%d" % (settings.screen_x,
                                                      settings.screen_y)
    
        # Maze size can change with each level, so pygame display,
        # scoreboard, and play button must be reconfigured
        # before each level
        screen = pygame.display.set_mode(
            (settings.screen_width, settings.screen_height))
        pygame.display.set_caption('Mindspin')    
        sb = Scoreboard(settings, screen, stats)
        play_button = Button(settings, screen)
        
        # Create random maze
        maze = Maze(screen, settings)
        
        # Create tile that player will move through maze
        player_tile = Tile(maze.start_tile.row, maze.start_tile.col,
                           screen, settings, settings.player_color)
                       
        # Create object that determines which direction player tile 
        # moves when arrow keys are pressed
        arrows = Arrows(settings)
        
        # Loop continually checks for player keypresses
        # and redraws screen until player solves maze or quits
        while not player_tile.same_location_as(maze.end_tile):
            gf.check_events(settings, screen, maze, player_tile,
                            arrows, stats, play_button)
            gf.update_screen(settings, screen, maze, player_tile,
                             stats, play_button, sb)
                             
        # Updates score and prepares for next level
        gf.player_solved_maze(settings, stats, sb)

run_game()
