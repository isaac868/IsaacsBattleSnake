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

