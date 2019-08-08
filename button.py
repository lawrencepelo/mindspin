import pygame.font

class Button():
    """
    This class creates an object to display a message
    telling player how to activate game between levels
    """
    def __init__(self, sets, screen, stats):
        """ Initialize button attributes"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        
        # Set the dimensions and properties of the button
        self.width = sets.button_width
        self.height = sets.button_height
        self.button_color = sets.button_color
        self.text_color = sets.button_text_color
        self.font = pygame.font.SysFont(sets.button_font,
                                        sets.button_font_size)
        self.message = sets.button_message
        
        # Build the button's rect object and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        self.msg_image = self.font.render(
            self.message + str(stats.level),
            True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
        
    def draw_button(self):
        """ Draw blank button and then draw message """
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
