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
        self.map.generate_map() #set all agents to None
        self.map = self.map.maze

        self.visited = []
        self.has_gold = False
        self.score = 0

    def game_over(self): #check to see if current node is at a lethal spot or won
        if self.curr_node.pit or self.curr_node.wumpus: #if node is a pit or at wumpus
            return True
        elif self.has_gold and self.curr_node is self.maze[0][0]: #if node is at the start and has the gold
            return True
        return False

    def location(self): #return where curr_node is in maze in map form
        return self.map[self.curr_node.x][self.curr_node.y]

    def evaluate_node(self, node, location, map, maze): #evaluate current node
        self.visited.append(location)
        location.value = 'K'

        if node.gold: #if node is gold, take it
            self.has_gold = True

        if node.breeze: #if the node has a breeze, mark all other nodes as a possible pit
            location.breeze = True
            for neighbor in location.neighbors:
                if neighbor not in self.visited and neighbor.pit is not False:
                    neighbor.value = '?'
        else:
            location.breeze = False
            for neighbor in location.neighbors:
                neighbor.pit = False

        if node.stench:
            location.stench = True
            for neighbor in location.neighbors:
                if neighbor not in self.visited and neighbor.wumpus is not False:
                    neighbor.value = '?'
        else:
            location.breeze = False
            for neighbor in location.neighbors:
                neighbor.wumpus = False

    def evaluate_world(self, map, maze):
        for row in map:
            for node in row:
                if node.value is '?':
                    breeze_count = 0
                    wumpus_count = 0
                    for neighbor in node.neighbors
                        if neighbor.pit is False and neighbor.wumpus is False:
                            node.pit = False
                            node.wumpus = False
                            break
                        if neighbor.breeze:
                            breeze_count += 1
                        if neighbor.stench:
                            wumpus_count += 1

                        if breeze_count >= 2:
                            neighbor.pit = True
                        if wumpus_count >= 2:
                            neighbor.wumpus = True


    def determine_move(self):
        pass

    def play(self):
        while not self.game_over():
            node = self.location()
            self.evaluate_node(self.curr_node, self.location(), self.map, self.maze)
            self.evaluate_world(self.map, self.maze)
            self.curr_node = self.determine_move()
        print('Game Over!\nScore: {}'.format(self.score))

if __name__ == '__main__':
    game = WumpusWorld(int(sys.argv[1]))
