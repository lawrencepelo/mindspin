from maze import Maze
from settings import Settings

settings = Settings()

maze = Maze(settings.rows, settings.cols,
            settings.start_side, settings.end_side)
maze.display()
