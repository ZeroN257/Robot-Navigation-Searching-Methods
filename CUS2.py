import sys
from queue import PriorityQueue

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
    print("Usage: python AS.py <input_file>")
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

def is_valid(x, y, grid):
    return 0 <= x < N and 0 <= y < M and grid[x][y] >= 0


def heuristic(node, goal_states):
    # A simple heuristic, such as the Manhattan distance
    x, y = node
    min_distance = float('inf')

    for goal_state in goal_states:
        gx, gy = goal_state
        distance = abs(gx - x) + abs(gy - y)
        if distance < min_distance:
            min_distance = distance

    return min_distance

# Define the get_neighbors function before ida_star
def get_neighbors(current_state, grid):
    x, y = current_state
    neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    valid_neighbors = [neighbor for neighbor in neighbors if is_valid(*neighbor, grid)]
    return valid_neighbors

# Define the search function before ida_star
def ida_star(initial_state, goal_states, grid):
    bound = heuristic(initial_state, goal_states)
    path, nodes_expanded = None, 0
    visited = set()  # Initialize an empty set to keep track of visited states

    while True:
        result, new_bound = search(initial_state, goal_states, grid, bound, visited)
        nodes_expanded += result[1]
        if result[0] == "FOUND":
            path = result[2]
            break
        if new_bound == float('inf'):
            break
        bound = new_bound

    return path, nodes_expanded

# Search function within IDA* with visited set
def search(current_state, goal_states, grid, bound, visited):
    nodes_expanded = 0
    f = heuristic(current_state, goal_states)

    if f > bound:
        return ("NOT_FOUND", f), f

    if current_state in goal_states:
        return ("FOUND", f, [current_state]), f

    minimum = float('inf')

    for neighbor in get_neighbors(current_state, grid):
        if neighbor not in visited:  # Check if the state has been visited
            visited.add(neighbor)  # Mark state as visited
            result, new_bound = search(neighbor, goal_states, grid, bound, visited)
            nodes_expanded += result[1]

            if result[0] == "FOUND":
                path = [current_state] + result[2]
                return ("FOUND", f, path), f

            if new_bound < minimum:
                minimum = new_bound

    return ("NOT_FOUND", minimum), minimum, nodes_expanded

# Perform Iterative Deepening A* Search
result, nodes_expanded = ida_star(initial_state, goal_states, grid)

if result is not None:
    print("IDA* Number of nodes:", nodes_expanded)
    if result[0] == "FOUND":
        movements = []
        for i in range(1, len(result[2])):
            prev_x, prev_y = result[2][i - 1]
            curr_x, curr_y = result[2][i]

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
else:
    print("No path found.")
