from operator import attrgetter

class node:
    x: int
    y: int
    distance = 0.0
    previous = None

def generate_adjacency_list(width, height, snake_array: list, us_coord, food_coords : list, player_coords : list):
    return_map = {}
    snake_coords = set()
    food_coords_normalized = []
    food_nodes = []
    index_map = {}
    player_node = None

    for food in food_coords:
        food_coords_normalized.append(food["x"] + height * food["y"])

    for snake in snake_array:
        for coord in snake["body"]:
            if coord == us_coord:
                continue
            snake_coords.add(coord["y"] * height + coord["x"])
        head = [snake["body"][0]["x"], snake["body"][0]["y"]]
        if snake["body"][0] == us_coord:
            continue
        if head[0] - 1 >= 0:
            snake_coords.add(head[1] * height + head[0] - 1)
        if head[0] + 1 < width:
            snake_coords.add(head[1] * height + head[0] + 1)
        if head[1] - 1 >= 0:
            snake_coords.add((head[1] - 1) * height + head[0])
        if head[1] + 1 < height:
            snake_coords.add((head[1] + 1)* height + head[0])
    
    for i in range(0, height):
        for j in range(0, width):
            if i*height + j in snake_coords:
                continue

            tmp_node = node()
            tmp_node.x = j
            tmp_node.y = i
            
            if (i*height + j) in food_coords_normalized:
                food_nodes.append(tmp_node)
            if [j, i] == player_coords:
                player_node = tmp_node

            adjacency_list = []
            return_map[tmp_node] = adjacency_list
            index_map[i*height + j] = tmp_node
    
    for i in range(0, height):
        for j in range(0, width):
            if (j+ i* height) in index_map:
                if j - 1 >= 0 and (j - 1 + i* height) in index_map:
                    return_map[index_map[j - 1 + i* height]].append([index_map[j + i * height], 1])
                    return_map[index_map[j + i * height]].append([index_map[j - 1 + i* height], 1])
                if i - 1 >= 0 and (j + (i - 1) * height) in index_map:
                    return_map[index_map[j + (i - 1) * height]].append([index_map[j + i * height], 1])
                    return_map[index_map[j + i * height]].append([index_map[j + (i - 1) * height], 1])

    return [return_map, food_nodes, player_node, index_map]

def is_reachable(adjacency_list_mapping : dict, node1: node, node2: node, seen_set):
    if node1 == node2:
        return True
    if node1 not in adjacency_list_mapping or node1 in seen_set:
        return False
    adj_nodes = adjacency_list_mapping.get(node1)
    seen_set.add(node1)

    for adj in adj_nodes:
        if adj[0] == node2:
            return True
    
    tmp_bool = False
    for adj in adj_nodes:
        if adj[0] not in seen_set:
            tmp_bool = tmp_bool or is_reachable(adjacency_list_mapping, adj[0], node2, seen_set)
    return tmp_bool

def dijkstra(adjacency_list_mapping : dict, start_node : node):
    array = adjacency_list_mapping.copy()
    
    for i in array:
        i.distance = 1000
        i.previous = None

    start_node.distance = 0

    while len(array) != 0:
        u = min(array, key=attrgetter('distance'))
        adj_nodes = array.pop(u)

        for v in adj_nodes:
            if v[0] in array:
                tmp = u.distance + v[1]
                if tmp < v[0].distance:
                    v[0].distance = tmp
                    v[0].previous = u