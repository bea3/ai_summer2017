import pprint
import copy
from unification import parse, unification


def parse_list(expressions_list):
    parsed = []
    for exp in expressions_list:
        parsed.append(parse(exp))
    return parsed


def found_goal(start, goal):
    goal_state = copy.deepcopy(goal)

    if len(start) < len(goal):
        return False

    for x in start:
        if x in goal_state:
            goal_state.remove(x)

    return len(goal_state) == 0


def generate_successor_states(start, actions):
    pass


def forward_planner(start_state, goal, actions, visited=None, debug=False):
    if found_goal(start_state, goal):
        return visited

    # parse all s-expressions
    start = parse_list(start_state)
    goal = parse_list(goal)
    for a in actions.keys():
        action = actions[a]
        for key in action.keys():
            if key == "conditions":
                actions[a]["conditions"] = parse_list(actions[a]["conditions"])
            elif key == "add":
                actions[a]["add"] = parse_list(actions[a]["add"])
            elif key == "delete":
                actions[a]["delete"] = parse_list(actions[a]["delete"])

    if visited is None:
        visited = [start]

    stack = []
    successor_states = generate_successor_states(start, actions)
    stack.insert(len(stack), successor_states[0])

    while len(stack) > 0:
        x = stack.pop(0)
        if x not in visited:
            visited.append(x)
            forward_planner(x, goal, actions, visited=visited, debug=debug)

    return []


start_state = [
    "(item Drill)",
    "(place Home)",
    "(place Store)",
    "(agent Me)",
    "(at Me Home)",
    "(at Drill Store)"
]

goal = [
    "(item Drill)",
    "(place Home)",
    "(place Store)",
    "(agent Me)",
    "(at Me Home)",
    "(at Drill Me)"
]

actions = {
    "drive": {
        "action": "(drive ?agent ?from ?to)",
        "conditions": [
            "(agent ?agent)",
            "(place ?from)",
            "(place ?to)",
            "(at ?agent ?from)"
        ],
        "add": [
            "(at ?agent ?to)"
        ],
        "delete": [
            "(at ?agent ?from)"
        ]
    },
    "buy": {
        "action": "(buy ?purchaser ?seller ?item)",
        "conditions": [
            "(item ?item)",
            "(place ?seller)",
            "(agent ?purchaser)",
            "(at ?item ?seller)",
            "(at ?purchaser ?seller)"
        ],
        "add": [
            "(at ?item ?purchaser)"
        ],
        "delete": [
            "(at ?item ?seller)"
        ]
    }
}

goal2 = [
    "(item Drill)",
    "(place Home)",
    "(place Store)",
    "(agent Me)",
    "(at Me Home)",
    "(at Drill Me)",
    "(agent Me)"
]

plan = forward_planner(start_state, goal, actions)
print plan
#
# plan_with_states = forward_planner( start_state, goal, actions, debug=True)
# print plan_with_states
