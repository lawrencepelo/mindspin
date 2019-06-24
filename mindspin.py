import pygame
import time
from maze import Maze
from settings import Settings
import game_functions as gf

def run_game():
    """Central function that controls the game"""
    pygame.init()
    
    settings = Settings()
    
    screen = pygame.display.set_mode(
        (settings.screen_width, settings.screen_height))
    pygame.display.set_caption('Mindspin')
    
    # Create random maze
    maze = Maze(settings)
    
    while True:
        gf.check_events(settings, screen)
        gf.update_screen(settings, screen, maze)    
time.sleep(10)
run_game()
