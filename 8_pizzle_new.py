#%%
import numpy as np 
import sys 
import heapq

class Puzzle:
    def __init__(self,tiles = None):
        self.tiles = tiles if tiles else [[1,2,3],[4,5,6],[7,8,0]]
        self.goal_state = [[1,2,3],[4,5,6],[7,8,0]]
        if tiles is None:
            self.blank =  (0,0)
        else:
            self.blank = self.find_blank()
    
    def is_goal(self):
        return self.tiles == self.goal_state
    
    def copy(self):
        return Puzzle([row[:] for row in self.tiles])
    
    def __eq__(self, other):
        return self.tiles == other.tiles
    
    def __hash__(self):
        return hash(str(self.tiles))

    def find_blank(self):
        for i in range(len(self.tiles)):
            for j in range(len(self.tiles[i])):
                if self.tiles[i][j] == 0:
                    return (i, j)
    
    @staticmethod    
    def printState(tiles):
        for row in tiles:
            print(" ".join(str(x) if x!=0 else " " for x in row))
        print("---------------")
        return ""

    def setState(self,args):
        arr = list(map(int,args))
        if len(arr)!=9: 
            raise ValueError("Error: Invalid Input Puzzle State")
        if set(arr) != set([1,2,3,4,5,6,7,8,0]):
            raise ValueError("Error: Invalid Input Puzzle State")
        self.tiles = np.array(arr).reshape(3,3).tolist()
        return ""
    
    def __lt__(self, other):
        return self.h2_func() < other.h2_func()
    
    def validmove(self,direction):
        i,j = self.blank
        if direction == "up" and i > 0:
            return True
        if direction == "down" and i < 2:
            return True
        if direction == "left" and j > 0:
            return True
        if direction == "right" and j < 2:
            return True
        return False

    def move(self,direction):
        i,j = self.blank
        #move up 
        if direction =="up":
            if i>0:
                rem = self.tiles[i-1][j]
                self.tiles[i-1][j] = 0 
                self.tiles[i][j] = rem
                self.blank = (i-1, j)

            else:
                raise ValueError("Error: Invalid Move")
        
        #move down 
        elif direction == "down":
            if i<2:
                rem = self.tiles[i+1][j]
                self.tiles[i+1][j] = 0
                self.tiles[i][j] = rem 
                self.blank = (i+1, j)

        
        #move left
        elif direction == "left":
            if j>0:
                rem = self.tiles[i][j-1]
                self.tiles[i][j-1] = 0 
                self.tiles[i][j] = rem 
                self.blank = (i, j-1)

            else: 
                raise ValueError("Error: Invalid Move")
        
        #move right 
        else:
            if j<2: 
                rem = self.tiles[i][j+1]
                self.tiles[i][j+1] = 0
                self.tiles[i][j] = rem
                self.blank = (i, j+1)
            else: 
                raise ValueError("Error: Invalid Move")
                    
        
    def getvalidmovedir(self):
        valid = False
        while valid == False:
            move = np.random.choice(["up", "down", "left", "right"])
            valid = self.validmove(move)
        return move
        
    def scrambleState(self,n):
        n = int(n)
        if n<0:
            raise ValueError("Error: Invalid Input. Number of moves must be positive")
        self.setState([1,2,3,4,5,6,7,8,0])
        nmoves = 0 
        curmove = self.getvalidmovedir()
        print("Initial State:")
        Puzzle.printState(self.tiles)
        while nmoves<n:
            self.move(curmove)
            nmoves += 1
            curmove = self.getvalidmovedir()
            Puzzle.printState(self.tiles)
        
    def setseed(self,seed):
        seed = int(seed)  
        np.random.seed(seed) 
        
    def h2_func(self):
        correctord = [2, 2,0, 0,0, 1,0, 2,1, 0,1, 1,1, 2,2, 0,2, 1]
        value_to_coords = dict()
        tiles = self.tiles
        for i, row in enumerate(tiles):
            for j, val in enumerate(row):
                if val is None:
                    value_to_coords.setdefault(0, set()).add((i, j))
                else:
                    value_to_coords.setdefault(val, set()).add((i, j))
        value_to_coords = dict(sorted(value_to_coords.items()))
        flattened = [num for coords_set in value_to_coords.values() for coord in coords_set for num in coord]
        m_dist = sum([abs(flattened[x] - correctord[x]) for x in range(len(flattened))])
        return m_dist
    
    def generate_successors(self):
        successors = []
        for direction in ["up", "down", "left", "right"]:
            if self.validmove(direction):
                new_puzzle = self.copy()
                new_puzzle.move(direction)
                successors.append((new_puzzle, direction))
        return successors
    
    def a_star_search(self):
        frontier = []
        heapq.heappush(frontier, (self.h2_func(), self))
        visited = set()

        while frontier:
            _, current = heapq.heappop(frontier)
            if current.is_goal():
                return current  # Found solution

            visited.add(current)

            for successor, _ in current.generate_successors():
                if successor not in visited:
                    heapq.heappush(frontier, (successor.h2_func(), successor))

def test_a_star():
    # Create a solvable puzzle state
    initial_state = [[1, 2, 3], 
                    [4, 0, 6], 
                    [7, 5, 8]]  # A simple state that requires movement
    
    puzzle = Puzzle(initial_state)
    
    print("Initial State:")
    Puzzle.printState(puzzle.tiles)

    # Run A* search
    solution = puzzle.a_star_search()
    
    if solution:
        print("Solution Found:")
        Puzzle.printState(solution.tiles)
    else:
        print("No solution found.")

# Run the test
test_a_star()       


# %%
