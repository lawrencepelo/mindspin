import sys
import pygame

def update_screen(settings, screen, maze):
    """Update images on the screen and flip to the new screen"""
    # Redraw the screen during each pass through the loop
    screen.fill(settings.bg_color)
    maze.draw(screen, settings) 
    pygame.display.flip()
    
def check_events(settings, screen):
    """Respond to keypresses and mouse events"""
    for event in pygame.event.get():
        # Close window if user clicks 'X' box
        if event.type == pygame.QUIT:
            sys.exit()
