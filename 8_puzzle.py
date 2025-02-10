
import numpy as np 
import sys 
import heapq

class Puzzle:
    def __init__(self,tiles = None):
        self.tiles = tiles if tiles else [[1,2,3],[4,5,6],[7,8,0]]
        if tiles is None:
            self.blank =  (0,0)
        else:
            self.blank = self.find_blank()
        
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
    
    def validmove(self,direction):
        i,j = self.find_blank()
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
        i,j = self.find_blank()
        #move up 
        if direction =="up":
            if i>0:
                rem = self.tiles[i-1][j]
                self.tiles[i-1][j] = 0 
                self.tiles[i][j] = rem
            else:
                raise ValueError("Error: Invalid Move")
        
        #move down 
        elif direction == "down":
            if i<2:
                rem = self.tiles[i+1][j]
                self.tiles[i+1][j] = 0
                self.tiles[i][j] = rem 
        
        #move left
        elif direction == "left":
            if j>0:
                rem = self.tiles[i][j-1]
                self.tiles[i][j-1] = 0 
                self.tiles[i][j] = rem 
            else: 
                raise ValueError("Error: Invalid Move")
        
        #move right 
        else:
            if j<2: 
                rem = self.tiles[i][j+1]
                self.tiles[i][j+1] = 0
                self.tiles[i][j] = rem
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
        
    def solveBFS(self,maxnodes=1000):
        #quque for BFS
        queue = []
        #visited states
        visited = set()
        #parent dictionary to store the parent and the action from the parent that led to the current state 
        parent = {}
        nodes_count = 0 
        
        queue.append(self.tiles)
        visited.add(tuple(map(tuple, self.tiles)))
        parent[tuple(map(tuple, self.tiles))] = (None, None)
        nodes_count+=1
        
        while queue:
            current = queue.pop(0)
            if tuple(map(tuple,current)) == ((1,2,3),(4,5,6),(7,8,0)):
                path = []
                while current != self.tiles:
                    state, action = parent[current]
                    path.append(action)
                    current = state
                print(" > ".join(str(x) for x in path[::-1]))
                break
            current_puz = Puzzle(current)
            i,j = current_puz.find_blank()     
                        
            if current_puz.validmove("left"):
                temp = [list(row[:]) for row in current]
                temp[i][j] = temp[i][j-1]
                temp[i][j-1] = 0
                temp_tuple = tuple(map(tuple, temp))

                if temp_tuple not in visited:
                    if nodes_count >= maxnodes:
                        print(f"Error: maxnodes limit ({maxnodes}) reached")
                        return None
                    queue.append(temp_tuple)
                    visited.add(temp_tuple)
                    parent[temp_tuple] = (current, "left")
                    nodes_count+=1  
                    

                
            if current_puz.validmove("right"):
                temp = [list(row[:]) for row in current]
                temp[i][j] = temp[i][j+1]
                temp[i][j+1] = 0
                temp_tuple = tuple(map(tuple, temp))

                if temp_tuple not in visited:
                    if nodes_count >= maxnodes:
                        print(f"Error: maxnodes limit ({maxnodes}) reached")
                        return None
                    queue.append(temp_tuple)
                    visited.add(temp_tuple)
                    parent[temp_tuple] = (current, "right")
                    nodes_count+=1
            
                
            if current_puz.validmove("up"):
                temp = [list(row[:]) for row in current]
                temp[i][j] = temp[i-1][j]
                temp[i-1][j] = 0
                temp_tuple = tuple(map(tuple, temp))

                if temp_tuple not in visited:
                    if nodes_count >= maxnodes:
                        print(f"Error: maxnodes limit ({maxnodes}) reached")
                        return None
                    queue.append(temp_tuple)
                    visited.add(temp_tuple)
                    parent[temp_tuple] = (current, "up")
                    nodes_count+=1

                    
            if current_puz.validmove("down"):
                temp = [list(row[:]) for row in current]
                temp[i][j] = temp[i+1][j]
                temp[i+1][j] = 0
                temp_tuple = tuple(map(tuple, temp))
                if temp_tuple not in visited:
                    if nodes_count >= maxnodes:
                        print(f"Error: maxnodes limit ({maxnodes}) reached")
                        return None
                    queue.append(temp_tuple)
                    visited.add(temp_tuple)
                    parent[temp_tuple] = (current, "down")
                    nodes_count+=1
                    
    def solveDFS(self, maxnodes=1000, maxdepth=31):
        visited = set()
        stack = [(tuple(map(tuple, self.tiles)), [])]
        nodes_explored = 0

        while stack and nodes_explored < maxnodes:
            state, path = stack.pop()
            nodes_explored += 1

            if state == ((1,2,3),(4,5,6),(7,8,0)):
                print(f"Nodes created during search: {nodes_explored}")
                print(f"Solution length:", len(path))
                print("Move sequence:")
                if path:
                    for move in path:
                        print(f"move {move}")
                else:
                    print("No move needed")
                return path
            

            if len(path) >= maxdepth:
                continue

            if state not in visited:
                visited.add(state)
                for direction in ["up", "down", "left", "right"]:
                    new_state = self.apply_move(state, direction)
                    if new_state and new_state not in visited:
                        stack.append((new_state, path + [direction]))

        print(f"Error: {'maxnodes' if nodes_explored >= maxnodes else 'maxdepth'} limit reached")
        return None

    def apply_move(self, state, direction):
        i, j = next((i, j) for i, row in enumerate(state) for j, val in enumerate(row) if val == 0)
        new_state = [list(row) for row in state]
        
        if direction == "up" and i > 0:
            new_state[i][j], new_state[i-1][j] = new_state[i-1][j], new_state[i][j]
        elif direction == "down" and i < 2:
            new_state[i][j], new_state[i+1][j] = new_state[i+1][j], new_state[i][j]
        elif direction == "left" and j > 0:
            new_state[i][j], new_state[i][j-1] = new_state[i][j-1], new_state[i][j]
        elif direction == "right" and j < 2:
            new_state[i][j], new_state[i][j+1] = new_state[i][j+1], new_state[i][j]
        else:
            return None
        
        return tuple(map(tuple, new_state))
    
    def h1_func(self):
        """
        Counts the number of misplaced items 

        Args:
            self: the tile 

        Returns:
            int: number of displaced items 
        """
        countdisp = 0 
        given = self.tiles 
        true = [[1,2,3],[4,5,6],[7,8,0]]
        for i in range(len(given)):
            for j in range(len(given[0])):
                if given[i][j] != true [i][j]:
                    countdisp+=1 
        return countdisp  
    
    def h2_func(self):
        """
        Counts the sum of Manhatan distances for a given state 

        Args:
            self: the tile

        Returns:
            int: sum of manhattan distances
        """
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
        
        
        
    
    def solveAstar(self, maxnodes=1000):
        print("we are here")
        """1. Initialize:
        - Open list (priority queue), containing the starting node with f = g + h.
        - Closed list (set), which will keep track of visited nodes.

        2. While open list is not empty:
        a. Pop the node with the lowest f value from the open list. This is the current node.
        
        b. If the current node is the goal:
            - Reconstruct the path from the goal to the start (using parent pointers), and return it as the solution.

        c. Add the current node to the closed list (mark it as visited).

        d. For each neighbor of the current node:
            - If the neighbor is in the closed list, skip it (already visited).
            
            - Calculate the tentative g score for the neighbor (g = g_current + cost to neighbor).
            
            - If the neighbor is not in the open list or the tentative g score is lower than the previous g score:
                - Set the parent of the neighbor to the current node.
                - Calculate the f score of the neighbor (f = g + h).
                - If the neighbor is not in the open list, add it to the open list.

        3. If open list is empty and no solution has been found, return failure (no path exists)."""
        
        open_list = []
        # Set of visited states
        closed_set = set()
        # Dictionary to keep track of g_scores
        g_scores = {}
        # Dictionary to store parent states for path reconstruction
        parents = {}
    
        curt= tuple(map(tuple,self.tiles))
        npuzzel = Puzzle(curt)
        h1 = npuzzel.h1_func()
        
                    
    
    
    
        




def cmd(commandString,puzzle):
    commands = {
        "setState": lambda *args: puzzle.setState(args),
        "printState": lambda: Puzzle.printState(puzzle.tiles), 
        "move":lambda *args: puzzle.move(args[0]), 
        "scrambleState": lambda *args: puzzle.scrambleState(args[0]), 
        "solveBFS": lambda: puzzle.solveBFS(),
        "solveDFS": lambda: puzzle.solveDFS(),
        "setseed": lambda *args: puzzle.setseed(args[0]),
        "solveAstar": lambda: puzzle.solveAstar()
    }
    parts = commandString.split()
    command  = parts[0]
    if len(parts)>1:
        args = parts[1:]
    else:
        args = []
    try: 
        if command in commands: 
            if args:
                commands[command](*args)  
            else:
                commands[command]()
        else:
            print(f"Error: Invalid Command:")
    except Exception as e:
        print("Error processing command")

def validlines(line):
    validstarts = ["setState", "printState", "move", "scrambleState","setseed","solveBFS","solveDFS","solveAstar","#","/",""]
    for prefix in validstarts:
        if line.startswith(prefix):
            return True
    return False

def cmdfile(filename,puzzle):
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            #to print the empty lines 
            if not line:
                print()
            else: 
                if validlines(line):
                    print(line)
                    if line.startswith("#") or line.startswith("/"):
                        continue 
                    else: 
                        cmd(line, puzzle)
                else: 
                    print("Error: invalid command: text of line that caused the issue")
                
if __name__ == "__main__":
    puzzle = Puzzle()
    if len(sys.argv) < 2:
        print("No input file specified")
        sys.exit(1)
    filename = sys.argv[1]
    print("Processing commands from file:", filename)
    
    try: 
        cmdfile(filename, puzzle)
    except:
        print("Error: Not specified yet")

