import pprint
import copy
from unification import parse, unification, unify


def found_goal(state, goal):
    goal_state = copy.deepcopy(goal)

    if len(state) < len(goal):
        return False

    for x in state:
        if x in goal_state:
            goal_state.remove(x)

    return len(goal_state) == 0


def apply_action(action_exp, sub_list):
    for item in sub_list:
        action_exp = action_exp.replace(item, sub_list[item])
    return action_exp


def get_unifications(state, partial_action, precondition):
    for rule in state:
        sub_list = unify(rule, precondition)
        if sub_list != False:
            partial_action = apply_action(partial_action, sub_list)
    return partial_action


def generate_successor_states(state, actions):
    results = []
    for action_key in actions:
        preconditions = actions[action_key]["conditions"]
        results = []
        partial_action = actions[action_key]["action"]
        for precond in preconditions:
            partial_action = get_unifications(state, partial_action, precond)
        results.append(partial_action)

    return results


def forward_planner(start_state, goal, actions, visited=None, debug=False):
    if found_goal(start_state, goal):
        return visited

    if visited is None:
        visited = [start_state]

    stack = []
    successor_states = generate_successor_states(start_state, actions)

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

plan = forward_planner(start_state, goal, actions)
print plan

#
# plan_with_states = forward_planner( start_state, goal, actions, debug=True)
# print plan_with_states
