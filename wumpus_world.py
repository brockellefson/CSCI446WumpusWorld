import world
import sys

class WumpusWorld:
    def __init__(self, size):
        self.world = world.Maze(size)
        self.world.generate_maze()
        self.world.generate_hazards()
        self.maze = self.world.maze

        self.world.print_maze()

        self.curr_node = self.maze[0][0] #always start at 0,0
        self.map = world.Maze(size) #create maze of the same size to store logic of where to move
        self.map.generate_maze() #identify neighbors, set everything to '_'
        self.map = self.map.maze

        self.has_gold = False
        self.score = 0

    def game_over(self): #check to see if current node is at a lethal spot or won
        if self.curr_node.pit or self.curr_node.wumpus: #if node is a pit or at wumpus
            return True
        elif self.curr_node.has_gold and self.curr_node is self.maze[0][0]: #if node is at the start and has the gold
            return True
        return False

    def location(self): #return where curr_node is in maze in map form
        return self.map[self.curr_node.x][self.curr_node.y]

    def eval_node(self): #evaluate node
        if self.curr_node.breeze: #if node has a breeze
            self.location.breeze = True
            for neighbor in self.location.neighbor:
                if not neighbor.visited and neighbor.pit is None: #if the neighbor has not been visited, possible pit
                    neighbor.value = '?'
        else:
            self.location.breeze = False

        if self.curr_node.stench: #if node has a stench
            self.location.stench = True
            for neighbor in self.location.neighbor:
                if not neighbor.visited and neighbor.pit is None and self.world.wumpus_alive: #if the neighbor has not been visited, not a pit, and wumpus is alive
                    neighbor.value = '?'
        else:
            self.location.stench = False

    def eval_map(self): #evaluate map
        for row in self.map:
            for node in row:
                if node.value is '?': #if node is possibly a hazard, check it
                    for neighbor in node.neighbors: #if a neighbor does not have a breeze or a stench, this node is legal
                        if not neighbor.stench or not neighbor.breeze:
                            node.value = 'K'
                            node.valid = True



if __name__ == '__main__':
    game = WumpusWorld(int(sys.argv[1]))
