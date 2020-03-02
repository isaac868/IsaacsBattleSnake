from operator import attrgetter

class node:
    x: int
    y: int
    distance = 0.0
    previous = None

def generate_adjacency_list(width, height, food_coords : list, player_coords : list):
    return_map = {}
    tmp_map = {}
    food_node = None
    player_node = None
    for i in range(0, height):
        for j in range(0, width):
            tmp_node = node()
            tmp_node.x = j
            tmp_node.y = i
            
            if [j, i] == food_coords:
                food_node = tmp_node
            if [j, i] == player_coords:
                player_node = tmp_node

            adjacency_list = []
            return_map[tmp_node] = adjacency_list
            tmp_map[i*height + j] = tmp_node

    for i in range(0, height):
        for j in range(0, width):
            if j - 1 >= 0:
                return_map[tmp_map[j - 1 + i* height]].append([tmp_map[j + i * height], 1])
                return_map[tmp_map[j + i * height]].append([tmp_map[j - 1 + i* height], 1])
            if i - 1 >= 0:
                return_map[tmp_map[j + (i - 1) * height]].append([tmp_map[j + i * height], 1])
                return_map[tmp_map[j + i * height]].append([tmp_map[j + (i - 1) * height], 1])

    return [return_map, food_node, player_node]

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