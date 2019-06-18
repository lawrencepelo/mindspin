class Tile():
    """Generate a tile"""    
    def __init__(self, row, col, direction = '0'):
        self.direction = direction
        if direction == 'N':
            self.row = row - 1
            self.col = col
        elif direction == 'S':
            self.row = row + 1
            self.col = col
        elif direction == 'E':
            self.row = row
            self.col = col + 1
        elif direction == 'W':
            self.row = row
            self.col = col - 1
        else:
            self.row = row
            self.col = col
            
    def get_row(self):
        return self.row
        
    def get_col(self):
        return self.col
