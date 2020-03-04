import Digraph as dg
from Digraph import node

def get_area_resulting_from_next_move(adjacency_list_mapping : dict, blocked_node : node, us_node : node, number: list, seen_set):
    if blocked_node not in adjacency_list_mapping or blocked_node in seen_set:
        return
    number[0] = number[0] + 1
    adj_nodes = adjacency_list_mapping.get(blocked_node)
    seen_set.add(blocked_node)
    for adj in adj_nodes:
        if adj[0] not in seen_set and us_node != adj[0]:
            get_area_resulting_from_next_move(adjacency_list_mapping, adj[0], us_node, number, seen_set)

def choose_food_target(parsed_data, us_length):
    digraph = parsed_data[0]
    food_nodes = parsed_data[1]
    player_node = parsed_data[2]
    index_map = parsed_data[3]

    tmp_node = None
    print("nodes: ",len(food_nodes))
    food_nodes = [food for food in food_nodes if dg.is_reachable(digraph, player_node, food, set()) == True]
    large_area_nodes = []
    small_area_nodes = []
    food_to_move_node_map = {}
    print("nodes: ",len(food_nodes))
    for food in food_nodes:
        tmp_food_node = food
        while tmp_food_node.previous != None:
            if tmp_food_node.previous == player_node:
                break
            else:
                tmp_food_node = tmp_food_node.previous
        if tmp_food_node != None:
            food_to_move_node_map[food] = tmp_food_node

    for food in food_to_move_node_map:
        number = [0]
        get_area_resulting_from_next_move(digraph, food_to_move_node_map[food], player_node, number, set())
        if number[0] <= us_length:
            small_area_nodes.append(food)
        else:
            large_area_nodes.append(food)

    large_area_nodes.sort(key = lambda node: node.distance)
    small_area_nodes.sort(key = lambda node: node.distance)
    #large_area_nodes.extend(small_area_nodes)

    if len(large_area_nodes) != 0:
        if large_area_nodes[0] in food_to_move_node_map:
            tmp_node = food_to_move_node_map[large_area_nodes[0]]

    return tmp_node