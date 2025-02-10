#%%
import heapq

class Puzzle:
    def __init__(self, tiles, parent=None, move=None, g=0):
        self.tiles = tiles  # 2D tuple representing puzzle state
        self.parent = parent  # Parent node (for path reconstruction)
        self.move = move  # Move taken to reach this state
        self.g = g  # Cost from start to current state
        self.h = self.h1_func()  # Heuristic value
        self.f = self.g + self.h  # A* score (f = g + h)

    def h1_func(self):
        """Heuristic: Counts misplaced tiles."""
        goal_state = ((1, 2, 3), (4, 5, 6), (7, 8, 0))  # Goal state for 8-puzzle
        misplaced = sum(
            1 for i in range(3) for j in range(3) if self.tiles[i][j] != goal_state[i][j] and self.tiles[i][j] != 0
        )
        return misplaced

    def get_blank_position(self):
        """Finds the position (i, j) of the empty tile (0)."""
        for i in range(3):
            for j in range(3):
                if self.tiles[i][j] == 0:
                    return i, j
        return None

    def get_neighbors(self):
        """Generates valid moves from the current state."""
        neighbors = []
        x, y = self.get_blank_position()
        moves = {'Up': (-1, 0), 'Down': (1, 0), 'Left': (0, -1), 'Right': (0, 1)}

        for move, (dx, dy) in moves.items():
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < 3 and 0 <= new_y < 3:  # Check if the move is within bounds
                new_tiles = [list(row) for row in self.tiles]  # Convert tuple to mutable list
                new_tiles[x][y], new_tiles[new_x][new_y] = new_tiles[new_x][new_y], new_tiles[x][y]  # Swap tiles
                neighbors.append(Puzzle(tuple(map(tuple, new_tiles)), parent=self, move=move, g=self.g + 1))

        return neighbors

    def reconstruct_path(self):
        """Reconstructs the path from the goal to the start."""
        path = []
        current = self
        while current.parent:
            path.append(current.move)
            current = current.parent
        return path[::-1]  # Reverse to get path from start to goal

    def __lt__(self, other):
        """Compares two puzzle states based on f-score for priority queue."""
        return self.f < other.f

def a_star_solver(start_state):
    """Solves the puzzle using A* search."""
    open_list = []  # Priority queue (min-heap)
    closed_set = set()  # Set of visited states

    start_puzzle = Puzzle(start_state)
    heapq.heappush(open_list, start_puzzle)

    while open_list:
        current = heapq.heappop(open_list)  # Pop node with lowest f-score

        if current.h == 0:  # Goal reached (h = 0 means no misplaced tiles)
            return current.reconstruct_path()

        closed_set.add(current.tiles)  # Mark current node as visited

        for neighbor in current.get_neighbors():
            if neighbor.tiles in closed_set:  # Skip already visited states
                continue

            # Check if this path to the neighbor is better
            heapq.heappush(open_list, neighbor)

    return None  # No solution found

# Example usage:
initial_state = ((1,2,3), (4, 6,5), (7, 8, 0))
solution = a_star_solver(initial_state)

if solution:
    print("Solution found:", solution)
else:
    print("No solution exists.")

# %%
