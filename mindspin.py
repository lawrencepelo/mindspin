import pygame
import os
from maze import Maze
from tile import Tile
from settings import Settings
from arrows import Arrows
import game_functions as gf

def run_game():
    """Central function that controls the game"""
   
    pygame.init()    
    settings = Settings()
    
    # Locate pygame display on monitor
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (settings.screen_x,
                                                    settings.screen_y)
    
    # Create pygame display
    screen = pygame.display.set_mode(
        (settings.screen_width, settings.screen_height))
    pygame.display.set_caption('Mindspin')
    
    # Create random maze
    maze = Maze(screen, settings)
    
    # Create tile that player will move through maze
    player_tile = Tile(maze.start_tile.row, maze.start_tile.col,
                       screen, settings, settings.player_color)
                       
    # Create object that determines which direction player tile moves
    # when arrow keys are pressed
    arrows = Arrows(settings)
    
    # main gameplay loop
    while True:
        gf.check_events(settings, screen, maze, player_tile, arrows)
        gf.update_screen(settings, screen, maze, player_tile)    

run_game()
