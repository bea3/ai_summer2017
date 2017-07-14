from __future__ import division

import matplotlib.pyplot as plt
import networkx as nx
import pprint
import copy
from collections import OrderedDict

connecticut = {
    "nodes": ["Fairfield", "Litchfield", "New Haven", "Hartford", "Middlesex", "Tolland", "New London", "Windham"],
    "edges": [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (2, 4), (3, 4), (3, 5), (3, 6), (4, 6), (5, 6), (5, 7), (6, 7)],
    "coordinates": [(46, 52), (65, 142), (104, 77), (123, 142), (147, 85), (162, 140), (197, 94), (217, 146)]}

europe = {
    "nodes": ["Iceland", "Ireland", "United Kingdom", "Portugal", "Spain",
              "France", "Belgium", "Netherlands", "Luxembourg", "Germany",
              "Denmark", "Norway", "Sweden", "Finland", "Estonia",
              "Latvia", "Lithuania", "Poland", "Czech Republic", "Austria",
              "Liechtenstein", "Switzerland", "Italy", "Malta", "Greece",
              "Albania", "Macedonia", "Kosovo", "Montenegro", "Bosnia Herzegovina",
              "Serbia", "Croatia", "Slovenia", "Hungary", "Slovakia",
              "Belarus", "Ukraine", "Moldova", "Romania", "Bulgaria",
              "Cyprus", "Turkey", "Georgia", "Armenia", "Azerbaijan",
              "Russia"],
    "edges": [(0, 1), (0, 2), (1, 2), (2, 5), (2, 6), (2, 7), (2, 11), (3, 4),
              (4, 5), (4, 22), (5, 6), (5, 8), (5, 9), (5, 21), (5, 22), (6, 7),
              (6, 8), (6, 9), (7, 9), (8, 9), (9, 10), (9, 12), (9, 17), (9, 18),
              (9, 19), (9, 21), (10, 11), (10, 12), (10, 17), (11, 12), (11, 13), (11, 45),
              (12, 13), (12, 14), (12, 15), (12, 17), (13, 14), (13, 45), (14, 15),
              (14, 45), (15, 16), (15, 35), (15, 45), (16, 17), (16, 35), (17, 18),
              (17, 34), (17, 35), (17, 36), (18, 19), (18, 34), (19, 20), (19, 21),
              (19, 22), (19, 32), (19, 33), (19, 34), (20, 21), (21, 22), (22, 23),
              (22, 24), (22, 25), (22, 28), (22, 29), (22, 31), (22, 32), (24, 25),
              (24, 26), (24, 39), (24, 40), (24, 41), (25, 26), (25, 27), (25, 28),
              (26, 27), (26, 30), (26, 39), (27, 28), (27, 30), (28, 29), (28, 30),
              (29, 30), (29, 31), (30, 31), (30, 33), (30, 38), (30, 39), (31, 32),
              (31, 33), (32, 33), (33, 34), (33, 36), (33, 38), (34, 36), (35, 36),
              (35, 45), (36, 37), (36, 38), (36, 45), (37, 38), (38, 39), (39, 41),
              (40, 41), (41, 42), (41, 43), (41, 44), (42, 43), (42, 44), (42, 45),
              (43, 44), (44, 45)],
    "coordinates": [(18, 147), (48, 83), (64, 90), (47, 28), (63, 34),
                    (78, 55), (82, 74), (84, 80), (82, 69), (100, 78),
                    (94, 97), (110, 162), (116, 144), (143, 149), (140, 111),
                    (137, 102), (136, 95), (122, 78), (110, 67), (112, 60),
                    (98, 59), (93, 55), (102, 35), (108, 14), (130, 22),
                    (125, 32), (128, 37), (127, 40), (122, 42), (118, 47),
                    (127, 48), (116, 53), (111, 54), (122, 57), (124, 65),
                    (146, 87), (158, 65), (148, 57), (138, 54), (137, 41),
                    (160, 13), (168, 29), (189, 39), (194, 32), (202, 33),
                    (191, 118)]}


def draw_map(planar_map, size, color_assignments=None):
    def as_dictionary(a_list):
        dct = {}
        for i, e in enumerate(a_list):
            dct[i] = e
        return dct

    G = nx.Graph()

    labels = as_dictionary(planar_map["nodes"])
    pos = as_dictionary(planar_map["coordinates"])

    # create a List of Nodes as indices to match the "edges" entry.
    nodes = [n for n in range(0, len(planar_map["nodes"]))]

    if color_assignments:
        colors = [c for n, c in color_assignments]
    else:
        colors = ['red' for c in range(0, len(planar_map["nodes"]))]

    G.add_nodes_from(nodes)
    G.add_edges_from(planar_map["edges"])

    # plt.figure(figsize=size, dpi=600)
    plt.figure()

    nx.draw(G, node_color=colors, with_labels=True, labels=labels, pos=pos)
    plt.show()


# draw_map(connecticut, (5, 4),
#          [("Fairfield", "red"), ("Litchfield", "blue"), ("New Haven", "red"), ("Hartford", "blue"),
#           ("Middlesex", "red"), ("Tolland", "blue"), ("New London", "red"), ("Windham", "blue")])


def create_graph(map):
    graph = {}
    for x in range(len(map["nodes"])):
        node = map["nodes"][x]
        graph[node] = get_neighbors(map, x)
    return graph


def create_subgraph(original_graph, to_visit):
    subgraph = {}
    for x in to_visit:
        subgraph[x] = original_graph[x]
    return subgraph


def create_colors_dict(map, colors):
    graph = {}
    for x in map["nodes"]:
        colors = copy.deepcopy(colors)
        graph[x] = colors
    return graph


def get_neighbors(map, node_index):
    neighbors = []
    for edge in map["edges"]:
        if edge[0] == node_index:
            to_neighbor = edge[1]
            neighbors.append(map["nodes"][to_neighbor])
        elif edge[1] == node_index:
            from_neighbor = edge[0]
            neighbors.append(map["nodes"][from_neighbor])
    return neighbors


def get_next_variable_degree_heuristic(graph, to_visit):
    new_graph = create_subgraph(graph, to_visit)
    ordered_places = sorted(new_graph, key=lambda k: len(new_graph[k]), reverse=True)
    next_place = ordered_places[0]
    for p in new_graph:
        if len(new_graph[p]) == len(new_graph[next_place]):
            next_place = min(next_place, p)
    return next_place


def get_least_constraining_value(colors_dict, graph, node, i):
    node_colors = colors_dict[node]
    num_similarities = dict()

    for color in node_colors:
        score = 0
        for neighbor in graph[node]:
            neighbor_colors = colors_dict[neighbor]
            if color in neighbor_colors:
                score += 1
        num_similarities[color] = score

    num_similarities = OrderedDict(sorted(num_similarities.items(), key=lambda v: v))

    ordered_colors = num_similarities.keys()
    return ordered_colors[i]


def assign_color(colors_dict, graph, node, i):
    new_colors_dict = copy.deepcopy(colors_dict)

    node_colors = new_colors_dict[node]

    if isinstance(node_colors, str) or i > len(node_colors) - 1:
        pprint.pprint("BACKTRACKING: " + node)
        return colors_dict

    marked_color = get_least_constraining_value(colors_dict, graph, node, i)
    new_colors_dict[node] = marked_color

    for x in graph[node]:
        if node == "Norway" and x == "Denmark":
            return colors_dict

        if new_colors_dict[x] == marked_color:
            return assign_color(colors_dict, graph, node, i + 1)
        elif x != node and len(new_colors_dict[x]) > 0 and marked_color in new_colors_dict[x] and len(
                new_colors_dict[x]) == 1:
            return assign_color(colors_dict, graph, node, i + 1)
        elif x != node and len(new_colors_dict[x]) > 0 and marked_color in new_colors_dict[x]:
            node_colors = new_colors_dict[x]
            node_colors.remove(marked_color)
    return new_colors_dict


def pop_from_list(list, node):
    while node in list:
        list.remove(node)
    return list


def backtrack(history):
    pass


def color_map(planar_map, colors, trace=False):
    visited = []
    to_visit = []
    graph = create_graph(planar_map)
    colors_dict = create_colors_dict(planar_map, colors)
    states = []
    i = 0

    start_node = get_next_variable_degree_heuristic(graph, graph.keys())
    to_visit.append(start_node)

    while len(to_visit) > 0:
        vertex = get_next_variable_degree_heuristic(graph, to_visit)
        old_colors_dict = copy.deepcopy(colors_dict)
        colors_dict = assign_color(colors_dict, graph, vertex, i)

        while colors_dict == old_colors_dict:
            if len(states) == 0:
                vertex = get_next_variable_degree_heuristic(graph, graph.keys())
                to_visit.append(start_node)
                colors_dict = create_colors_dict(planar_map, colors)
                colors_dict = assign_color(colors_dict, graph, vertex, i + 1)
            else:
                previous_state = states[-1]
                del states[-1]
                vertex = previous_state["vertex"]
                colors_dict = previous_state["colors_dict"]
                visited = previous_state["visited"]
                to_visit = previous_state["to_visit"]
                child = previous_state["child"] + 1
                colors_dict = assign_color(colors_dict, graph, vertex, child)
                if vertex == "Norway":
                    pprint.pprint(previous_state)

        state = {}
        state["colors_dict"] = colors_dict
        state["to_visit"] = to_visit
        state["visited"] = visited
        state["vertex"] = vertex
        state["child"] = i
        states.append(state)

        to_visit = pop_from_list(to_visit, vertex)
        if vertex not in visited:
            visited.append(vertex)
            for neighbor in graph[vertex]:
                if neighbor not in visited and neighbor not in to_visit:
                    to_visit.insert(0, neighbor)
    print("VISITED")
    print(visited)

    color_array = []
    for x in map["nodes"]:
        color = colors_dict[x]
        if isinstance(colors_dict[x], list):
            color = colors_dict[x][0]
        color_array.append((x, color))
    print("COLORS")
    pprint.pprint(color_array)

    return color_array


map = europe

connecticut_colors = color_map(map, ["red", "blue", "green", "yellow"], trace=True)

edges = map["edges"]
nodes = map["nodes"]
colors = connecticut_colors
COLOR = 1

draw_map(map, (5, 4), connecticut_colors)

for start, end in edges:
    try:
        assert colors[start][COLOR] != colors[end][COLOR]
    except AssertionError:
        print "%s and %s are adjacent but have the same color." % (nodes[start], nodes[end])
