import world
import sys
import random
from collections import deque

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

        self.visited = [] #list of globally visited nodes
        self.has_gold = False #does the player have gold?
        self.has_arrow = True #does the player have an arrow?
        self.score = 0

    def update_multi_move(self, node, finish): #after completing bfs, determine how many moves where made and update score
        while node is not finish:
            self.score -= 1
            node = node.previous

    def bfs(self, curr_node, finish): #bfs is used to go home with gold, or go to new undiscovered 'K' node
       #create queue, visited_nodes needs to be reset
       queue = deque([curr_node])
       visited_nodes = []

       while len(queue) > 0:
          node = queue.pop()
          if node in visited_nodes:
             continue

          visited_nodes.append(node)
          if node is finish:
              self.update_multi_move(node, curr_node)
              return self.node_location(node)

          for neighbor in node.neighbors:
             if neighbor not in visited_nodes and neighbor.value is 'K':
                neighbor.previous = node
                queue.appendleft(neighbor)
       return False


    def game_over(self): #check to see if current node is at a lethal spot or won
        if self.curr_node.pit: #if node is pit
            print('You fell in a pit!')
            self.score -= 1000
            return True
        elif self.curr_node.wumpus: #if node is wumpus
            print('You ran into the Wumpus!')
            self.score -= 1000
            return True
        elif self.has_gold and self.curr_node is self.maze[0][0]: #if node is at the start and has the gold
            print('You got out of the cave with the gold!')
            self.score += 1000
            return True
        return False

    def location(self): #return where curr_node is in maze in map form
        return self.map[self.curr_node.x][self.curr_node.y]

    def node_location(self, node): #return where curr_node is in map in maze form
        return self.maze[node.x][node.y]

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
        else: #no breeze, mark all adjacent nodes as not a pit
            location.breeze = False
            for neighbor in location.neighbors:
                neighbor.pit = False

        if node.stench: #if the node has a stench, mark all other nodes as a possible wumpus
            location.stench = True
            for neighbor in location.neighbors:
                if neighbor not in self.visited and neighbor.wumpus is not False:
                    neighbor.value = '?'
        else: #no stench, mark all adjacent nodes as not wumpus
            location.stench = False
            for neighbor in location.neighbors:
                neighbor.wumpus = False

    def determine_pit(self, node): #determine where pits are
        valid_nodes = 0
        invalid_node = ''
        for neighbor in node.neighbors: #if all breeze children are 'K' except one, thats the pit
            if neighbor.value is 'K':
                valid_nodes += 1
            elif neighbor.value is '?':
                invalid_node = neighbor

        if valid_nodes == len(node.neighbors)-1:
            if invalid_node is not '':
                invalid_node.pit = True
                invalid_node.value = 'P'

    def evaluate_world(self, map, maze): #evaluate current map to update nodes
        for row in map:
            for node in row:
                if node.pit is False and node.wumpus is False: #if a node if not a pit and wumpus, automatic 'K'
                    node.value = 'K'
                elif node.value is '?':
                    wumpus_count = 0
                    for neighbor in node.neighbors:
                        if neighbor.breeze is False and neighbor.stench is False: #if a '?' node has a normal node, then that '?' cannot be a hazard
                            node.pit = False
                            node.wumpus = False
                            node.value = 'K'
                            break

                        if neighbor.stench:
                            wumpus_count += 1

                    if wumpus_count >= 2: #if a '?' has atleast 2 stench children, that node is the wumpus
                        node.wumpus = True
                        node.value = 'W'
                    else:
                        node.wumpus = False

            for node in row:
                if node.breeze is True: #determine any pits with updated information
                    self.determine_pit(node)

    def guess_node(self, node): #guess a random '?' neighbor
        guess = node.neighbors[random.randint(0, len(node.neighbors)-1)]

        if guess.value is not '?': #if the guess is not a '?' node, do it again
            guess = self.guess_node(node)

        return guess

    def determine_move(self, node, location, map, maze): #check neighbors for a 'K' node that has not been visited, if all have, bfs to 'K' unvisited global node, else pick random '?'
        if self.has_gold: #have gold, go home
            return self.bfs(location, map[0][0])

        for neighbor in location.neighbors: #check local neighbors for a unvisited 'K'
            if neighbor.value is 'K' and neighbor not in self.visited:
                self.score -= 1
                return self.node_location(neighbor)

        for row in map: #check globally for 'K' nodes that have not been visited
            for element in row:
                if element.value is 'K' and element not in self.visited:
                    return self.bfs(location, element)

        #else, guess
        self.score -= 1
        return self.node_location(self.guess_node(location))

    def play(self): #play game
        self.map[0][0].value = 'K'

        while not self.game_over():
            node = self.location()
            self.evaluate_node(self.curr_node, node, self.map, self.maze)

            #printing current status of maze
            node.value = 'X'
            print('Determined Maze: \nhas_gold: {}'.format(self.has_gold))
            print('Conditions: breeze: {} stench: {}'.format(node.breeze, node.stench))
            self.m.print_maze()
            node.value = 'K'

            self.evaluate_world(self.map, self.maze)
            self.curr_node = self.determine_move(self.curr_node, node, self.map, self.maze)
        print('Game Over!\nScore: {}'.format(self.score))

if __name__ == '__main__':
    game = WumpusWorld(int(sys.argv[1]))
    game.play()
