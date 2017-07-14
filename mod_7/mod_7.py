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


def apply_action(start, action):
    variables = []
    matches = dict()

    for x in action["action"]:
        if x.startswith("?"):
            variables.append(x[1:])

    for x in start:
        if x[0] == "place" and "from" in variables and "from" not in matches.keys():
            matches["from"] = x[1]
        elif x[0] == "place" and "to" in variables and "to" not in matches.keys():
            matches["to"] = x[1]
        elif x[0] == "place" and "seller" in variables:
            matches["seller"] = x[1]
        elif x[0] == "agent" and "purchaser" in variables:
            matches["purchaser"] = x[1]
        elif x[0] in variables:
            matches[x[0]] = x[1]

    for x in action["add"]:
        for ind, val in enumerate(x):
            if val.startswith("?"):
                variable_name = val[1:]
                if variable_name in matches.keys():
                    x[ind] = matches[variable_name]
        start.append(x)

    for x in action["delete"]:
        for ind, val in enumerate(x):
            if val.startswith("?"):
                variable_name = val[1:]
                if variable_name in matches.keys():
                    x[ind] = matches[variable_name]
        if x in start:
            start.remove(x)
    return start


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
            if key == "action":
                actions[a]["action"] = parse(actions[a]["action"])
            else:
                actions[a][key] = parse_list(actions[a][key])


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
