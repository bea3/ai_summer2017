from IPython.core.display import *
from StringIO import StringIO
import random
import copy
import math
from collections import OrderedDict
import sys

"""
IMPORTANT NOTES:
- use value iteration and q-learning
- 70% desired direction, 30% (10% each) for undesired direction
- q_learning will return a policy: {(x1, y1): action1, (x2, y2): action2, ...}
- the best reward is related to the discount rate and the approximate number of actions you need to reach the goal
"""

costs = {'.': -1, '*': -3, '^': -5, '~': -7}
cardinal_moves = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def read_world(filename):
    with open(filename, 'r') as f:
        world_data = [x for x in f.readlines()]
    f.close()
    world = []
    for line in world_data:
        line = line.strip()
        if line == "": continue
        world.append([x for x in line])
    return world


def simulator(available_moves, desired_move):
    random_number = random.randint(1, 10)
    if random_number <= 7:
        return desired_move
    else:
        random_number = random.randint(1, 3)
        undesired_moves = copy.deepcopy(available_moves)
        undesired_moves.remove(desired_move)
        return undesired_moves[random_number - 1]


def get_cost(world, costs, state):
    x = state[0]
    y = state[1]
    feature = world[y][x]
    return costs[feature]


def has_enough_episodes(episodes):
    if len(episodes) == 0 or len(episodes) < 2:
        return False

    last_qs = episodes[-2]
    current_qs = episodes[-1]

    for x in current_qs.keys():
        current_q_direction = current_qs[x]
        last_q_direction = last_qs[x]
        q_keys = current_q_direction.keys()
        for key in q_keys:
            current_q_val = current_q_direction[key]
            last_q_val = last_q_direction[key]
            if math.fabs(current_q_val - last_q_val) > .01:
                return False

    return True


def initialize_q_states(world, goal, actions, reward):
    all_directions = dict()

    for action in actions:
        direction = dict()
        for i in range(len(world)):
            for j in range(len(world[i])):
                if (j, i) == goal:
                    direction[(j, i)] = reward
                else:
                    direction[(j, i)] = 0
        all_directions[action] = direction
    return all_directions


def pick_start(world, goal):
    random_y = random.randint(0, len(world) - 1)
    random_x = random.randint(0, len(world[0]) - 1)
    start_coords = (random_x, random_y)

    while start_coords == goal:
        random_y = random.randint(0, len(world) - 1)
        random_x = random.randint(0, len(world[0]) - 1)
        start_coords = (random_x, random_y)

    return start_coords


def pick_action(state, actions, episodes, visited, world):
    epsilon = 5
    random_num = random.randint(1, 10)

    if random_num >= epsilon or len(episodes) == 0:
        possible_actions = dict()
        for a in actions:
            next_state = (state[0] + a[0], state[1] + a[1])
            if next_state in visited.keys() and is_valid_move(state, a, world):
                possible_actions[a] = visited[next_state]
        possible_actions = OrderedDict(sorted(possible_actions.items(), key=lambda x: x[1]))

        try:
            return possible_actions.items()[0][0]
        except IndexError:
            return None

    else:
        possible_actions = dict()
        for a in actions:
            next_state = (state[0] + a[0], state[1] + a[1])
            direction_q = episodes[-1][a]
            if next_state in direction_q.keys():
                q_a = direction_q[next_state]
                possible_actions[a] = q_a
        possible_actions = OrderedDict(sorted(possible_actions.items(), key=lambda x: x[1], reverse=True))
        return possible_actions.items()[0][0]


def is_valid_move(state, action, world):
    next_state = (state[0] + action[0], state[1] + action[1])
    x = next_state[0]
    y = next_state[1]

    try:
        feature = world[y][x]
    except IndexError:
        return False

    if x >= len(world[0]) or x < 0:
        return False

    if y >= len(world) or y < 0:
        return False

    return feature != 'x'


def q_learning(world, costs, goal, reward, actions, gamma, alpha):
    episodes = []
    policy = dict()
    visited = dict()
    all_states = []
    for i in range(len(world)):
        for j in range(len(world[i])):
            policy[(j, i)] = None
            visited[(j, i)] = 0
            all_states.append((j, i))

    q = initialize_q_states(world, goal, actions, reward)
    while has_enough_episodes(episodes) == False:
        q = copy.deepcopy(q)

        state = pick_start(world, goal)
        visited[state] += 1
        while state != goal:
            desired_action = pick_action(state, actions, episodes, visited, world)
            while desired_action is not None and is_valid_move(state, desired_action, world) == False:
                desired_action = pick_action(state, actions, episodes, visited, world)
            if desired_action is None:
                state = goal
            else:
                action_taken = simulator(actions, desired_action)
                while is_valid_move(state, action_taken, world) == False:
                    action_taken = simulator(actions, desired_action)
                successor_state = (state[0] + action_taken[0], state[1] + action_taken[1])
                r = get_cost(world, costs, successor_state)
                all_possible_action_scores = []
                for a in actions:
                    successor_q_action = q[a]
                    all_possible_action_scores.append(successor_q_action[successor_state])
                max_next_a = max(all_possible_action_scores)
                q_action = q[desired_action]
                q_action[state] = (1 - alpha) + alpha * (r + gamma * max_next_a)
                state = successor_state

            visited[state] += 1

        episodes.append(q)
        print("Finished episode")

    print("Writing policy")
    for s in all_states:
        if s != goal:
            x = s[0]
            y = s[1]
            if world[y][x] == "x":
                policy[s] = "x"
            else:

                possible_directions = dict()
                for a in actions:
                    possible_directions[a] = episodes[-1][a][s]
                    possible_directions = OrderedDict(
                        sorted(possible_directions.items(), key=lambda x: x[1], reverse=True))
                highest_score = possible_directions.items()[0]

                score_x = highest_score[0][0]
                score_y = highest_score[0][1]

                if highest_score[1] == 0:
                    policy[s] = "?"
                elif highest_score[0] == (0, -1):
                    policy[s] = "^"
                elif highest_score[0] == (0, 1):
                    policy[s] = "v"
                elif highest_score[0] == (-1, 0):
                    policy[s] = "<"
                elif highest_score[0] == (1, 0):
                    policy[s] = ">"
        else:
            policy[s] = "G"
    return policy


def pretty_print_policy(rows, cols, policy):
    for c in range(cols):
        row_string = ""
        for r in range(rows):
            row_string += str(policy[(r, c)])
        print(row_string)


test_world = read_world("world.txt")
goal = (26, 26)
gamma = .9
alpha = .1
reward = 100

# print(test_world[22][4])

test_policy = q_learning(test_world, costs, goal, reward, cardinal_moves, gamma, alpha)
print(test_policy)
pretty_print_policy(len(test_world[0]), len(test_world), test_policy)

print "DONE"
