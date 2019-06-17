import itertools
import random

def get_next_tile(tile, direction):
    if direction == 'N':
        return [tile[0] - 1, tile[1]]
    elif direction == 'S':
        return [tile[0] + 1, tile[1]]
    elif direction == 'E':
        return [tile[0], tile[1] - 1]
    elif direction =='W':
        return [tile[0], tile[1] + 1]
        
def can_move_to_tile(tile):
    if tile[0] < 0 or tile[0] >= rows:
        return False
    elif tile[1] < 0 or tile[1] >= cols:
        return False
        
    used_tiles = 0
    for direction in ['N', 'S', 'E', 'W']:
        next_tile = get_next_tile(tile, direction)
        if next_tile[0] >= 0 and next_tile[0] < rows and next_tile[1] >= 0 and next_tile[1] < cols:
            if maze[next_tile[0]][next_tile[1]] == 1:
                used_tiles += 1
            
    return used_tiles == 1
        
def extend_maze_path(tile):
    dir_shuffle = random.sample(['N', 'S', 'E', 'W'], 4)
    
    for direction in dir_shuffle:
        next_tile = get_next_tile(tile, direction)
        if can_move_to_tile(next_tile):
            maze[next_tile[0]][next_tile[1]] = 1
            extend_maze_path(next_tile)
    
rows = 20
cols = 50

first_row = list(itertools.repeat(0, cols))
maze = []
for _ in range(0, rows):
    maze.append(first_row.copy())

maze[rows // 2][cols // 2] = 1

extend_maze_path([rows // 2, cols // 2])

for i in range(0, rows):
    print(maze[i])
