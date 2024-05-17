from queue import PriorityQueue
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

def is_valid(x, y, grid):
    return 0 <= x < N and 0 <= y < M and grid[x][y] >= 0

def heuristic(node, goal_states):
    # Manhattan distance heuristic
    x, y = node
    min_distance = float('inf')

    for goal_state in goal_states:
        gx, gy = goal_state
        distance = abs(gx - x) + abs(gy - y)
        if distance < min_distance:
            min_distance = distance

    return min_distance
#Search_Fuction
def greedy_best_first_search(initial_state, goal_states, grid):
    open_set = PriorityQueue()
    open_set.put((heuristic(initial_state, goal_states), initial_state))
    came_from = {}
    explored = set()
    nodes_expanded = 0  # Initialize the counter for expanded nodes      
    
    while not open_set.empty():
        _, current_state = open_set.get()
        nodes_expanded += 1  # Increment the node count

        if current_state in goal_states:
            path = reconstruct_path(came_from, initial_state, current_state)
            return path, nodes_expanded

        explored.add(current_state)

        for neighbor in get_neighbors(current_state, grid):
            if neighbor not in explored and neighbor not in came_from:
                came_from[neighbor] = current_state
                open_set.put((heuristic(neighbor, goal_states), neighbor))
                nodes_expanded += 1

    return None, nodes_expanded

def get_neighbors(current_state, grid):
    x, y = current_state
    neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    valid_neighbors = [neighbor for neighbor in neighbors if is_valid(*neighbor, grid)]
    return valid_neighbors


def reconstruct_path(came_from, initial_state, current_state):
    if current_state == initial_state:
        return [current_state]
    elif current_state not in came_from:
        return None  # Return None when a valid path cannot be reconstructed
    else:
        path = reconstruct_path(came_from, initial_state, came_from[current_state])
        path.append(current_state)
        return path


# Perform A* search
result, nodes_expanded = greedy_best_first_search(initial_state, goal_states, grid)

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
