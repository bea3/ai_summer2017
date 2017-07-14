from Queue import PriorityQueue
import collections
import pprint

test_world = [
    ['.', '*', '*', '*', '*', '*', '*'],
    ['.', '*', '*', '*', '*', '*', '*'],
    ['.', '*', '*', '*', '*', '*', '*'],
    ['.', '.', '.', '.', '.', '.', '.'],
    ['*', '*', '*', '*', '*', '*', '.'],
    ['*', '*', '*', '*', '*', '*', '.'],
    ['*', '*', '*', '*', '*', '*', '.'],
]

full_world = [
    ['.', '.', '.', '.', '.', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '.', '.', '.', '.', '.', '.', '.', '.',
     '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '*', '*', '*', '*', '*', '*', '*', '*', '*', '.', '.', 'x', 'x', 'x', 'x', 'x',
     'x', 'x', '.', '.'],
    ['.', '.', '.', '.', 'x', 'x', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', 'x', 'x', 'x', '#', '#', '#',
     'x', 'x', '#', '#'],
    ['.', '.', '.', '.', '#', 'x', 'x', 'x', '*', '*', '*', '*', '~', '~', '*', '*', '*', '*', '*', '.', '.', '#', '#',
     'x', 'x', '#', '.'],
    ['.', '.', '.', '#', '#', 'x', 'x', '*', '*', '.', '.', '~', '~', '~', '~', '*', '*', '*', '.', '.', '.', '#', 'x',
     'x', 'x', '#', '.'],
    ['.', '#', '#', '#', 'x', 'x', '#', '#', '.', '.', '.', '.', '~', '~', '~', '~', '~', '.', '.', '.', '.', '.', '#',
     'x', '#', '.', '.'],
    ['.', '#', '#', 'x', 'x', '#', '#', '.', '.', '.', '.', '#', 'x', 'x', 'x', '~', '~', '~', '.', '.', '.', '.', '.',
     '#', '.', '.', '.'],
    ['.', '.', '#', '#', '#', '#', '#', '.', '.', '.', '.', '.', '.', '#', 'x', 'x', 'x', '~', '~', '~', '.', '.', '#',
     '#', '#', '.', '.'],
    ['.', '.', '.', '#', '#', '#', '.', '.', '.', '.', '.', '.', '#', '#', 'x', 'x', '.', '~', '~', '.', '.', '#', '#',
     '#', '.', '.', '.'],
    ['.', '.', '.', '~', '~', '~', '.', '.', '#', '#', '#', 'x', 'x', 'x', 'x', '.', '.', '.', '~', '.', '#', '#', '#',
     '.', '.', '.', '.'],
    ['.', '.', '~', '~', '~', '~', '~', '.', '#', '#', 'x', 'x', 'x', '#', '.', '.', '.', '.', '.', '#', 'x', 'x', 'x',
     '#', '.', '.', '.'],
    ['.', '~', '~', '~', '~', '~', '.', '.', '#', 'x', 'x', '#', '.', '.', '.', '.', '~', '~', '.', '.', '#', 'x', 'x',
     '#', '.', '.', '.'],
    ['~', '~', '~', '~', '~', '.', '.', '#', '#', 'x', 'x', '#', '.', '~', '~', '~', '~', '.', '.', '.', '#', 'x', '#',
     '.', '.', '.', '.'],
    ['.', '~', '~', '~', '~', '.', '.', '#', '*', '*', '#', '.', '.', '.', '.', '~', '~', '~', '~', '.', '.', '#', '.',
     '.', '.', '.', '.'],
    ['.', '.', '.', '.', 'x', '.', '.', '*', '*', '*', '*', '#', '#', '#', '#', '.', '~', '~', '~', '.', '.', '#', 'x',
     '#', '.', '.', '.'],
    ['.', '.', '.', 'x', 'x', 'x', '*', '*', '*', '*', '*', '*', 'x', 'x', 'x', '#', '#', '.', '~', '.', '#', 'x', 'x',
     '#', '.', '.', '.'],
    ['.', '.', 'x', 'x', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', 'x', 'x', 'x', '.', '.', 'x', 'x', 'x', '.',
     '.', '.', '.', '.'],
    ['.', '.', '.', 'x', 'x', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', 'x', 'x', 'x', 'x', '.', '.', '.',
     '.', '.', '.', '.'],
    ['.', '.', '.', 'x', 'x', 'x', '*', '*', '*', '*', '*', '*', '*', '*', '.', '.', '.', '#', '#', '.', '.', '.', '.',
     '.', '.', '.', '.'],
    ['.', '.', '.', '.', 'x', 'x', 'x', '*', '*', '*', '*', '*', '*', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
     '~', '~', '~', '~'],
    ['.', '.', '#', '#', '#', '#', 'x', 'x', '*', '*', '*', '*', '*', '.', 'x', '.', '.', '.', '.', '.', '~', '~', '~',
     '~', '~', '~', '~'],
    ['.', '.', '.', '.', '#', '#', '#', 'x', 'x', 'x', '*', '*', 'x', 'x', '.', '.', '.', '.', '.', '.', '~', '~', '~',
     '~', '~', '~', '~'],
    ['.', '.', '.', '.', '.', '.', '#', '#', '#', 'x', 'x', 'x', 'x', '.', '.', '.', '.', '#', '#', '.', '.', '~', '~',
     '~', '~', '~', '~'],
    ['.', '#', '#', '.', '.', '#', '#', '#', '#', '#', '.', '.', '.', '.', '.', '#', '#', 'x', 'x', '#', '#', '.', '~',
     '~', '~', '~', '~'],
    ['#', 'x', '#', '#', '#', '#', '.', '.', '.', '.', '.', 'x', 'x', 'x', '#', '#', 'x', 'x', '.', 'x', 'x', '#', '#',
     '~', '~', '~', '~'],
    ['#', 'x', 'x', 'x', '#', '.', '.', '.', '.', '.', '#', '#', 'x', 'x', 'x', 'x', '#', '#', '#', '#', 'x', 'x', 'x',
     '~', '~', '~', '~'],
    ['#', '#', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#', '#', '#', '#', '#', '.', '.', '.', '.', '#', '#',
     '#', '.', '.', '.']]

cardinal_moves = [(0, -1), (1, 0), (0, 1), (-1, 0)]

costs = {'.': 1, '*': 3, '#': 5, '~': 7}


def get_successors(n, world, cost_so_far, moves, goal, costs):
    successors = dict()
    x = n[0]
    y = n[1]
    directions = dict()
    for direction in moves:
        new_x = direction[0] + x
        new_y = direction[1] + y
        if not new_x < 0 and not new_y < 0 and not new_y >= len(world) and not new_x >= len(world[0]) and world[new_y][
            new_x] != "x":
            successor = (new_x, new_y)
            successors[successor] = heuristic(successor, world, goal, costs) + cost_so_far[n]
            directions[successor] = direction
            cost_so_far[successor] = get_cost(world, successor, costs) + cost_so_far[n]
    return collections.OrderedDict(sorted(successors.items(), key=lambda t: t[1])), directions, cost_so_far


def get_cost(world, n, costs):
    x = n[0]
    y = n[1]
    type = world[y][x]
    if type == "." or type == "*" or type == "#" or type == "~":
        return costs[type]


def heuristic(n, world, goal, costs):
    return abs(n[1] - goal[1]) + abs(n[0] - goal[0]) + get_cost(world, n, costs)


def check_valid_move(current, step, moves):
    x = current[0]
    y = current[1]
    invalid_counter = 0

    for direction in moves:
        new_x = direction[0] + x
        new_y = direction[1] + y
        updated = (new_x, new_y)
        if updated != step:
            invalid_counter += 1

    if invalid_counter == len(moves):
        return False
    else:
        return True


def a_star_search(world, start, goal, costs, moves, heuristic):
    frontier = dict()
    cost_so_far = dict()
    cost_so_far[start] = 0
    total_score = cost_so_far[start] + heuristic(start, world, goal, costs)
    frontier[start] = total_score
    current_node = (frontier.items()[0], frontier.keys()[0])
    explored = []
    moves_made = []
    directions = dict()
    directions[start] = (0, 0)

    while len(frontier.keys()) > 0:
        frontier = collections.OrderedDict(sorted(frontier.items(), key=lambda t: t[1]))
        next_step = (frontier.items()[0], frontier.keys()[0])
        if len(frontier.keys()) > 1:
            while not check_valid_move(current_node[1], next_step[1], moves):
                frontier.pop(frontier.keys()[0])
                next_step = (frontier.items()[0], frontier.keys()[0])
        else:
            frontier.pop(frontier.keys()[0])
        current_node = next_step
        moves_made.append(directions.get(current_node[1]))

        if current_node[1] == goal:
            explored.append(goal)
            break

        successors, directions, cost_so_far = get_successors(current_node[1], world, cost_so_far, moves, goal, costs)

        for s in successors:
            successor_coords = (s[0], s[1])
            s_cost = cost_so_far[current_node[1]] + get_cost(world, current_node[1], costs)
            if successor_coords not in explored or s_cost < cost_so_far[successor_coords]:
                frontier[successor_coords] = successors[s]

        explored.append(current_node[1])
    return moves_made[1:]


def pretty_print_solution(world, path, start):
    path_world = world
    current = start
    while len(path) > 0:
        movement = path[0]
        path = path[1:]
        if movement[0] == 0 and movement[1] > 0:
            path_world[current[1]][current[0]] = "V"
        elif movement[0] == 0 and movement[1] < 0:
            path_world[current[1]][current[0]] = "^"
        elif movement[1] == 0 and movement[0] > 0:
            path_world[current[1]][current[0]] = ">"
        elif movement[1] == 0 and movement[0] < 0:
            path_world[current[1]][current[0]] = "<"
        current = (current[0] + movement[0], current[1] + movement[1])
    path_world[current[1]][current[0]] = "G"

    for i in range(len(path_world)):
        row = path_world[i]
        path_world[i] = ''.join(row)

    path_world = '\n'.join(path_world)

    print path_world


full_path = a_star_search(test_world, (0, 0), (6, 6), costs, cardinal_moves, heuristic)
print full_path
pretty_print_solution(test_world, full_path, (0, 0))

full_path = a_star_search(full_world, (0, 0), (26, 26), costs, cardinal_moves, heuristic)
print full_path
pretty_print_solution(full_world, full_path, (0, 0))
