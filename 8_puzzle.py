
#%%

#function for command string
import numpy as np 
import sys 

class Puzzle:
    def __init__(self,tiles = None):
        self.tiles = tiles if tiles else [[0,1,2],[3,4,5],[6,7,8]]
        self.blank =  (0,0)
        
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
        if set(arr) != set([0,1,2,3,4,5,6,7,8]):
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
        self.setState([0,1,2,3,4,5,6,7,8])
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
            if tuple(map(tuple,current)) == ((0,1,2),(3,4,5),(6,7,8)):
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
                    
                
            
            
            


def cmd(commandString,puzzle):
        commands = {
            "setState": lambda *args: puzzle.setState(args),
            "printState": lambda: Puzzle.printState(puzzle.tiles), 
            "move":lambda *args: puzzle.move(args[0]), 
            "scrambleState": lambda *args: puzzle.scrambleState(args[0]), 
            "solveBFS": lambda: puzzle.solveBFS(),
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
                    commands[command](*args)  # Pass args if they exist
                else:
                    commands[command]()
            else:
                print(f"Error: Invalid Command:")
        except Exception as e:
            print("Error processing command")

def validlines(line):
    validstarts = ["setState", "printState", "move", "scrambleState","setseed","solveBFS","#","/",""]
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

