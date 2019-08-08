import pygame.font
from pygame.sprite import Group
import datetime

class Scoreboard():
    """A class to place text on the screen"""
    
    def __init__(self, settings, screen, stats):
        """Initialize scorekeeping attributes"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        
        # Font settings for scoring information
        self.text_color = settings.sb_font_color
        self.font = pygame.font.SysFont(settings.sb_font, 
                                        settings.sb_font_size)
        #print(self.font.get_ascent())
                                        
        self.bonus = None
        
    def prep_bonus(self, settings, stats):
        """Turn the score into a rendered image"""
        if stats.maze_status == 'before':
            self.bonus = settings.bonus_start       
        elif stats.maze_status == 'during':
            # Calculate time elapsed since maze activated
            time_delta = datetime.datetime.now() - stats.start_time
            time_secs = time_delta.total_seconds()
            # If time limit has expired, game is over
            if time_secs >= settings.time_limit:
                stats.maze_status = 'failed'
                self.prep_message(settings, 'GAME OVER!')
                self.bonus = 0
            else:
                # If time limit hasn't expired, 
                # calcuate current timer bonus
                bonus_real = (settings.bonus_coeff * time_secs ** 2 +
                              settings.bonus_start)
                self.bonus = int(round(bonus_real, 0))
        elif stats.maze_status in ['solved', 'failed']:
            self.bonus = 0

        # Format and render bonus
        bonus_str = "{:,}".format(self.bonus)
        self.bonus_image = self.font.render('Bonus: ' + bonus_str,
                                            True,
                                            self.text_color,
                                            settings.bg_color)
                                          
        # Display the bonus at the top left of the screen
        self.bonus_rect = self.bonus_image.get_rect()
        self.bonus_rect.left = (self.screen_rect.left + 
                                settings.border_x)
        self.bonus_rect.top = settings.border_y
        
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
        self.score_rect.top = settings.border_y
        
    def prep_level(self, settings, stats):
        """Turn the score into a rendered image"""
        level_str = "{:,}".format(stats.level)
        self.level_image = self.font.render('Level: ' + level_str,
                                            True,
                                            self.text_color,
                                            settings.bg_color)
                                            
        # Display the level at the top right of the screen
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = (self.screen_rect.right - 
                                 settings.border_x)
        self.level_rect.top = settings.border_y
        
    def prep_message(self, settings, msg):
        """Turn the message into a rendered image"""
        self.message_image = self.font.render(msg,
                                              True,
                                              self.text_color,
                                              settings.bg_color)
                                            
        # Display the level at the bottom center of the screen
        self.message_rect = self.message_image.get_rect()
        self.message_rect.centerx = self.screen_rect.centerx
        self.message_rect.top = (settings.screen_height -
                                 settings.border_y -
                                 settings.sb_font_size)
                                 
    def prep_compass(self, settings, maze, arrows):
        """ Create images of the compass directions """
        # Create and locate image of direction above maze
        self.compass_up_image = self.font.render(arrows.get_key('U'),
                                                  True,
                                                  self.text_color,
                                                  settings.bg_color)
        self.compass_up_rect = self.compass_up_image.get_rect()
        self.compass_up_rect.centerx = maze.wall_rect.centerx
        self.compass_up_rect.top = (maze.wall_rect.top -
                                    settings.sb_font_size - 
                                    settings.border_y)
                                     
        # Create and locate image of direction below maze
        self.compass_down_image = self.font.render(arrows.get_key('D'),
                                                  True,
                                                  self.text_color,
                                                  settings.bg_color)
        self.compass_down_rect = self.compass_down_image.get_rect()
        self.compass_down_rect.centerx = maze.wall_rect.centerx
        self.compass_down_rect.bottom = (maze.wall_rect.bottom +
                                         settings.sb_font_size +
                                         settings.border_y)
                                        
        # Create and locate image of direction to right of maze
        self.compass_right_image = self.font.render(arrows.get_key('R'),
                                                  True,
                                                  self.text_color,
                                                  settings.bg_color)
        self.compass_right_rect = self.compass_right_image.get_rect()
        self.compass_right_rect.centery = maze.wall_rect.centery
        self.compass_right_rect.right = (maze.wall_rect.right +
                                         settings.sb_font_size +
                                         settings.border_x)
                                        
        # Create and locate image of direction to left of maze
        self.compass_left_image = self.font.render(arrows.get_key('L'),
                                                  True,
                                                  self.text_color,
                                                  settings.bg_color)
        self.compass_left_rect = self.compass_left_image.get_rect()
        self.compass_left_rect.centery = maze.wall_rect.centery
        self.compass_left_rect.right = (maze.wall_rect.left -
                                        settings.sb_font_size -
                                        settings.border_x)

    def draw_scoreboard(self):
        """Draw scoreboard elements to the screen"""
        self.screen.blit(self.bonus_image, self.bonus_rect)
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.screen.blit(self.message_image, self.message_rect)
        self.screen.blit(self.compass_up_image, self.compass_up_rect)
        self.screen.blit(self.compass_down_image, self.compass_down_rect)
        self.screen.blit(self.compass_right_image, self.compass_right_rect)
        self.screen.blit(self.compass_left_image, self.compass_left_rect)
