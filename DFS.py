from collections import deque
import sys

# Function to read grid data from a text file
def read_grid_data(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()

    # Extract N and M dimensions
    N, M = map(int, lines[0].strip('[]\n').split(','))

    # Extract initial state
    initial_state = tuple(map(int, lines[1].strip('()\n').split(',')))

    # Extract goal states
    goal_lines = lines[2].strip('()\n').split('|')
    goal_states = [tuple(map(int, state.strip('() ').split(','))) for state in goal_lines if state.strip() != '']

    # Extract wall locations
    wall_lines = lines[3:]
    walls = []

    for wall in wall_lines:
        cleaned_wall = wall.strip('()\n').split(',')
        cleaned_wall = [int(value) for value in cleaned_wall if value.strip() != '']
        if cleaned_wall:
            walls.append(tuple(cleaned_wall))

    return N, M, initial_state, goal_states, walls

if len(sys.argv) != 2:
    print("Usage: python script_name.py <input_file>")
    sys.exit(1)
    
# Provide the path to your text file
file_name = sys.argv[1]  # Replace with the actual file path

# Read the grid data from the file
N, M, initial_state, goal_states, walls = read_grid_data(file_name)

# Initialize the grid
grid = [[0] * M for _ in range(N)]

# Update grid size based on problem specification
for x, y, w, h in walls:
    N = max(N, x + w)
    M = max(M, y + h)

grid = [[0] * M for _ in range(N)]

# Mark walls on the grid
for x, y, w, h in walls:
    for i in range(x, x + w):
        for j in range(y, y + h):
            grid[i][j] = -1

# Mark goal cells on the grid
for x, y in goal_states:
    grid[x][y] = 1

# Mark the initial state on the grid
initial_x, initial_y = initial_state
grid[initial_x][initial_y] = 0  # Assuming the initial state is represented as 0

def is_valid(x, y):
    return 0 <= x < N and 0 <= y < M and grid[x][y] >= 0

# Depth-First Search (DFS) for Robot Navigation

def depth_first_search(initial_state, goal_states, grid):
    def dfs(current_state, path):
        nonlocal nodes_expanded  # Declare nodes_expanded as nonlocal

        if current_state in goal_states:
            return path + [current_state]

        x, y = current_state
        visited.add(current_state)
        nodes_expanded += 1  # Increment the node expanded count

        for neighbor in neighbors(x, y, grid):
            if neighbor not in visited:
                result = dfs(neighbor, path + [current_state])
                if result:
                    return result

    visited = set()
    nodes_expanded = 0  # Initialize a counter for nodes expanded
    return dfs(initial_state, []), nodes_expanded  # Return the result and nodes_expanded

def neighbors(x, y, grid):
    N, M = len(grid), len(grid[0])
    candidates = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    return [(nx, ny) for nx, ny in candidates if 0 <= nx < N and 0 <= ny < M and grid[nx][ny] >= 0]

# Perform DFS
result, nodes_expanded = depth_first_search(initial_state, goal_states, grid)

if result is not None:
    print("DFS_Number of nodes:", nodes_expanded)
else:
    print("No path found.")

if result:
    movements = []
    for i in range(1, len(result)):
        prev_x, prev_y = result[i - 1]
        curr_x, curr_y = result[i]

        if prev_y < curr_y:
            movements.append("down")
        elif prev_y > curr_y:
            movements.append("up")
        elif prev_x < curr_x:
            movements.append("right")
        elif prev_x > curr_x:
            movements.append("left")

    print("; ".join(movements))
else:
    print("No path found.")
