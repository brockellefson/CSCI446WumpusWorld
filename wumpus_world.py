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
        self.m = world.Maze(size) #create maze of the same size to store logic of where to move
        self.m.generate_maze() #identify neighbors, set everything to '_'
        self.m.generate_map() #set all agents to None
        self.map = self.m.maze

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

    def node_location(self, node):
        return self.maze[node.x][node.y]

    def evaluate_node(self, node, location, map, maze): #evaluate current node
        self.visited.append(location)

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

    def determine_pit(self, node):
        valid_nodes = 0
        invalid_node = ''
        for neighbor in node.neighbors:
            if neighbor.value is 'K':
                valid_nodes += 1
            if neighbor.value is '?':
                invalid_node = neighbor

        if valid_nodes == len(node.neighbors)-1:
            invalid_node.pit = True
            invalid_node.value = 'P'

    def evaluate_world(self, map, maze):
        for row in map:
            for node in row:
                if node.pit is False and node.wumpus is False:
                    node.value = 'K'
                elif node.value is '?':
                    wumpus_count = 0
                    for neighbor in node.neighbors:
                        if neighbor.breeze is False and neighbor.stench is False:
                            node.pit = False
                            node.wumpus = False
                            node.value = 'K'
                            break

                        if neighbor.stench:
                            wumpus_count += 1

                        if wumpus_count >= 2:
                            node.wumpus = True
                            node.value = 'W'

            for node in row:
                if node.breeze is True:
                    self.determine_pit(node)

    def determine_move(self, location):
        for neighbor in location.neighbors:
            if neighbor.value is 'K':
                print('sup')
                return self.node_location(neighbor)

    def play(self):
        self.map[0][0].value = 'K'
        queue = [self.location()]


        while not self.game_over():
            node = self.location()
            self.evaluate_node(self.curr_node, self.location(), self.map, self.maze)
            self.evaluate_world(self.map, self.maze)
            self.curr_node = self.determine_move(node)
            print('Determined Maze:')
            #self.world.print_maze()
            self.m.print_maze()
        print('Game Over!\nScore: {}'.format(self.score))

if __name__ == '__main__':
    game = WumpusWorld(int(sys.argv[1]))
    game.play()
