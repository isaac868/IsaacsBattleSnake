from Digraph import node

def get_area_resulting_from_next_move(adjacency_list_mapping : dict, blocked_node : node, number: list):
    if blocked_node not in adjacency_list_mapping:
        return
    number[0] = number[0] + 1
    adj_nodes = adjacency_list_mapping.pop(blocked_node)
    for adj in adj_nodes:
        get_area_resulting_from_next_move(adjacency_list_mapping, adj[0], number)

