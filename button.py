import pygame.font

class Button():
    """
    This class creates an object to display a message
    telling player how to activate game between levels
    """
    def __init__(self, settings, screen):
        """ Initialize button attributes"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        
        # Set the dimensions and properties of the button
        self.width = settings.button_width
        self.height = settings.button_height
        self.button_color = settings.button_color
        self.text_color = settings.button_text_color
        self.font = pygame.font.SysFont(settings.button_font,
                                        settings.button_font_size)
        self.message = settings.button_message
        
        # Build the button's rect object and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        self.msg_image = self.font.render(self.message, True,
                                          self.text_color,
                                          self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
        
    def draw_button(self):
        """ Draw blank button and then draw message """
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
