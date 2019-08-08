class Arrows():
    """
    A class to contain and edit movement directions
    associated with arrow keys.
    """
    def __init__(self, sets):
        self.north = sets.initial_arrow_north
        self.south = sets.initial_arrow_south
        self.west = sets.initial_arrow_west
        self.east = sets.initial_arrow_east
        
    def rotate_cw(self):
        """Adjust arrow keys sets after maze
           rotates clockwise"""
        temp = self.north
        self.north = self.east
        self.east = self.south
        self.south = self.west
        self.west = temp

    def rotate_ccw(self):
        """Adjust arrow keys sets after maze
           rotates counter-clockwise"""
        temp = self.west
        self.west = self.south   
        self.south = self.east   
        self.east = self.north               
        self.north = temp
        
    def reflect_x(self):
        """Adjust arrow keys sets after maze
           reflects around x-axis"""
        temp = self.north
        self.north = self.south
        self.south = temp
        
    def reflect_y(self):
        """Adjust arrow keys sets after maze
           reflects around y-axis"""
        temp = self.east
        self.east = self.west
        self.west = temp
        
    def get_key(self, direction):
        """Returns the arrow key ('N','S','W','E') associated
           with the given direction ('U','D','L','R')"""
        if self.north == direction:
            return 'N'
        elif self.south == direction:
            return 'S'
        elif self.west == direction:
            return 'W'
        elif self.east == direction:
            return 'E'
        else:
            return None
        
