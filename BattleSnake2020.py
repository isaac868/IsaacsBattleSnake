import json
import os
import random
import numpy as np
import Digraph as dg
import SnakeFunctions as sf
import bottle
from bottle import HTTPResponse
from random import choice


@bottle.route("/")
def index():
    return "Your Battlesnake is alive!"


@bottle.post("/ping")
def ping():
    """
    Used by the Battlesnake Engine to make sure your snake is still working.
    """
    return HTTPResponse(status=200)


@bottle.post("/start")
def start():
    """
    Called every time a new Battlesnake game starts and your snake is in it.
    Your response will control how your snake is displayed on the board.
    """
    data = bottle.request.json
    print("START:", json.dumps(data))

    response = {"color": "#00FF00", "headType": "regular", "tailType": "regular"}
    return HTTPResponse(
        status=200,
        headers={"Content-Type": "application/json"},
        body=json.dumps(response),
    )


@bottle.post("/move")
def move():
    """
    Called when the Battlesnake Engine needs to know your next move.
    The data parameter will contain information about the board.
    Your response must include your move of up, down, left, or right.
    """
    data = bottle.request.json
    print("MOVE:", data["turn"])


    player_coord = [data["you"]["body"][0]["x"],data["you"]["body"][0]["y"]] 

    return_data = dg.generate_adjacency_list(data["board"]["height"], data["board"]["width"], data["board"]["snakes"], data["you"]["body"][0], data["board"]["food"], player_coord)
    digraph = return_data[0]
    food_nodes = return_data[1]
    player_node = return_data[2]
    index_map = return_data[3]

    dg.dijkstra(digraph, player_node)
    
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
        sf.get_area_resulting_from_next_move(digraph, food_to_move_node_map[food], player_node, number, set())
        if number[0] <= len(data["you"]["body"]):
            small_area_nodes.append(food)
        else:
            large_area_nodes.append(food)

    large_area_nodes.sort(key = lambda node: node.distance)
    small_area_nodes.sort(key = lambda node: node.distance)
    #large_area_nodes.extend(small_area_nodes)

    if len(large_area_nodes) != 0:
        if large_area_nodes[0] in food_to_move_node_map:
            tmp_node = food_to_move_node_map[large_area_nodes[0]]

    # Choose a random direction to move in
    directions = ["up", "down", "left", "right"]

    move = "down"
    if tmp_node is None:
        max = 0
        for adj_node in digraph[player_node]:
            number = [0]
            sf.get_area_resulting_from_next_move(digraph, adj_node[0], player_node, number, set())
            if number[0] >= max:
                tmp_node = adj_node[0]
                max = number[0]

    if tmp_node.x < player_coord[0]:
        move = "left"
    elif tmp_node.x > player_coord[0]:
        move = "right"
    elif tmp_node.y < player_coord[1]:
        move = "up"
    elif tmp_node.y > player_coord[1]:
        move = "down"
    else:
        move = "down"

    # Shouts are messages sent to all the other snakes in the game.
    # Shouts are not displayed on the game board.
    shout = "I am a python snake!"

    print("Direction: ", move)
    response = {"move": move, "shout": shout}
    return HTTPResponse(
        status=200,
        headers={"Content-Type": "application/json"},
        body=json.dumps(response),
    )


@bottle.post("/end")
def end():
    """
    Called every time a game with your snake in it ends.
    """
    data = bottle.request.json
    print("END:", json.dumps(data))
    return HTTPResponse(status=200)


def main():
    bottle.run(
        application,
        host=os.getenv("IP", "0.0.0.0"),
        port=os.getenv("PORT", "8080"),
        debug=os.getenv("DEBUG", True),
    )


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == "__main__":
    main()
