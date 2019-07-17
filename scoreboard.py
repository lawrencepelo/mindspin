import pygame.font
from pygame.sprite import Group
import datetime

class Scoreboard():
    """A class to report scoring info"""
    
    def __init__(self, settings, screen, stats):
        """Initialize scorekeeping attributes"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        
        # Font settings for scoring informations
        self.text_color = settings.sb_font_color
        self.font = pygame.font.SysFont(settings.sb_font, 
                                        settings.sb_font_size)
        self.bonus = None
        
    def prep_bonus(self, settings, stats):
        """Turn the score into a rendered image"""
        # Calculate time elapsed since maze activated
        time_delta = datetime.datetime.now() - stats.start_time
        time_secs = time_delta.total_seconds()
        
        # If time limit has expired, game is over
        if time_secs >= settings.time_limit:
            stats.game_over = True
            self.game_active = False
            self.bonus = 0
        # If time limit hasn't expired, calcuate current timer bonus
        else:        
            bonus_real = (settings.bonus_coeff * time_secs ** 2 +
                          settings.bonus_start)
            self.bonus = int(round(bonus_real, 0))
            
        bonus_str = "{:,}".format(self.bonus)
        self.bonus_image = self.font.render('Bonus: ' + bonus_str,
                                            True,
                                            self.text_color,
                                            settings.bg_color)
                                            
        # Display the bonus at the top left of the screen
        self.bonus_rect = self.bonus_image.get_rect()
        self.bonus_rect.left = self.screen_rect.left + 20
        self.bonus_rect.top = 20
        
    def prep_score(self, settings, stats):
        """Turn the score into a rendered image"""
        score_str = "{:,}".format(stats.score)
        self.score_image = self.font.render('Score: ' + score_str,
                                            True,
                                            self.text_color,
                                            settings.bg_color)
                                            
        # Display the score at the top center of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.centerx = self.screen_rect.centerx
        self.score_rect.top = 20
        
    def prep_level(self, settings, stats):
        """Turn the score into a rendered image"""
        level_str = "{:,}".format(stats.level)
        self.level_image = self.font.render('Level: ' + level_str,
                                            True,
                                            self.text_color,
                                            settings.bg_color)
                                            
        # Display the level at the top right of the screen
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.screen_rect.right - 20
        self.level_rect.top = 20

    def draw_scoreboard(self):
        """Draw scoreboard elements to the screen"""
        self.screen.blit(self.bonus_image, self.bonus_rect)
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.level_image, self.level_rect)

