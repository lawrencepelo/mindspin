class Arrows():
    """
    A class to contain and edit movement directions
    associated with arrow keys.
    """
    def __init__(self, settings):
        self.up = settings.initial_arrow_up
        self.down = settings.initial_arrow_down
        self.left = settings.initial_arrow_left
        self.right = settings.initial_arrow_right
        
    def rotate_cw(self):
        temp = self.up
        self.up = self.left
        self.left = self.down
        self.down = self.right
        self.right = temp

    def rotate_ccw(self):
        temp = self.up
        self.up = self.right
        self.right = self.down
        self.down = self.left
        self.left = temp
        
    def reflect_x(self):
        temp = self.up
        self.up = self.down
        self.down = temp
        
    def reflect_y(self):
        temp = self.right
        self.right = self.left
        self.left = temp
