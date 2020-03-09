from operator import attrgetter

class node:
    x: int
    y: int
    dims = []
    distance = 0.0
    previous = None

def is_diagonal_to(point1, point2):
    if [point1[0] - 1, point1[1] - 1] == point2:
        return True
    elif [point1[0] + 1, point1[1] - 1] == point2:
        return True
    elif [point1[0] + 1, point1[1] + 1] == point2:
        return True
    elif [point1[0] - 1, point1[1] + 1] == point2:
        return True
    else:
        return False

def generate_adjacency_list(width, height, snake_array: list, us_snake, food_coords : list, chase_tail : bool, ommit_nodes_near_head: bool):
    player_coords = [us_snake["body"][0]["x"],us_snake["body"][0]["y"]]
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
            if coord == us_snake["body"][0]:
                continue
            #if coord == snake["body"][len(snake["body"]) - 1]:
            #    continue
            snake_coords.add(coord["y"] * height + coord["x"])
        head = [snake["body"][0]["x"], snake["body"][0]["y"]]
        us_head = [us_snake["body"][0]["x"], us_snake["body"][0]["y"]]
        print("ttt", is_diagonal_to(head, us_head))
        if snake["body"][0] == us_snake["body"][0] or not ommit_nodes_near_head or (len(us_snake["body"]) > len(snake["body"]) and is_diagonal_to(head, us_head)):
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
            tmp_node.dims.append(width)
            tmp_node.dims.append(height)
            
            if (i*height + j) in food_coords_normalized:
                food_nodes.append(tmp_node)
            if [j, i] == player_coords:
                player_node = tmp_node

            adjacency_list = []
            return_map[tmp_node] = adjacency_list
            index_map[i*height + j] = tmp_node
    
    for node_index in index_map:
        target_node = index_map[node_index]
        node_left = index_map.get(target_node.x - 1 + target_node.y * height, None)
        node_up   = index_map.get(target_node.x + (target_node.y - 1) * height, None)
        
        if  node_left != None and target_node.x - 1 >= 0:
            connect_nodes(return_map, node_left, target_node, food_nodes, chase_tail)
        if  node_up != None and target_node.y - 1 >= 0:
            connect_nodes(return_map, node_up, target_node, food_nodes, chase_tail)

    return [return_map, food_nodes, player_node, index_map]

def connect_nodes(adjacency_list_mapping : dict, node1: node, node2: node, food_nodes, chase_tail: bool):
    cost = 1
    if not chase_tail and (node1 in food_nodes or node2 in food_nodes):
        cost = cost + 3
    #if not chase_tail and (node_is_on_edge(node1) or node_is_on_edge(node2)):
    #    cost = cost + 2
    adjacency_list_mapping[node1].append([node2, cost])
    adjacency_list_mapping[node2].append([node1, cost])

def node_is_on_edge(test_node):
    return test_node.x == 0 or test_node.x == (test_node.dims[0] - 1) or test_node.y == 0 or test_node.y == (test_node.dims[1] - 1)

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

def get_next_node_from_goal_node(goal_node: node, start_node: node):
    tmp_node = goal_node
    while tmp_node.previous != None:
        if tmp_node.previous == start_node:
            break
        else:
            tmp_node = tmp_node.previous
    if tmp_node != None:
        return tmp_node
    else:
        return None