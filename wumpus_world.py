import world
import sys

class WumpusWorld:
    def __init__(self, size):
        self.maze = world.Maze(size)
        self.maze.print_maze()




if __name__ == '__main__':
    game = WumpusWorld(int(sys.argv[1]))
