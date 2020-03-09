import json
import os
import random
import numpy as np
import Digraph as dg
import SnakeFunctions as sf
import bottle
from bottle import HTTPResponse
from random import choice

previous_tail_coord = []

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

    timer = sf.ElapsedTime("time")

    data = bottle.request.json
    print("MOVE:", data["turn"])

    height = data["board"]["height"]
    width = data["board"]["width"]
    global previous_tail_coord
    description_string = ""

    chase_tail = data["you"]["health"] <= 85

    player_coord = [data["you"]["body"][0]["x"],data["you"]["body"][0]["y"]] 


    return_data = dg.generate_adjacency_list(height, width, data["board"]["snakes"], data["you"], data["board"]["food"], False, True)
    digraph = return_data[0]
    food_nodes = return_data[1]
    player_node = return_data[2]
    index_map = return_data[3]

    dg.dijkstra(digraph, player_node)
    tmp_node = None

    if chase_tail or len(data["you"]["body"]) <= 4 or True:
        tmp_node = sf.choose_food_target(return_data, len(data["you"]["body"]))
        description_string = "food"
    else:
        if previous_tail_coord[0] in index_map:
            tail_node = dg.get_next_node_from_goal_node(index_map[previous_tail_coord[0]], player_node)
            tmp_node = tail_node 
            description_string = "avoiding food"

    # Choose a random direction to move in
    directions = ["up", "down", "left", "right"]

    move = "down"
    if tmp_node is None:
        max = 0
        if len(digraph[player_node]) == 0:
            return_data = dg.generate_adjacency_list(height, width, data["board"]["snakes"], data["you"], data["board"]["food"], False, False)
            digraph = return_data[0]
            food_nodes = return_data[1]
            player_node = return_data[2]
            index_map = return_data[3]

            dg.dijkstra(digraph, player_node)
        for adj_node in digraph[player_node]:
            number = [0]
            sf.get_area_resulting_from_next_move(digraph, adj_node[0], player_node, number, set())
            if number[0] >= max:
                tmp_node = adj_node[0]
                max = number[0]
                description_string = "max area"

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

    tmp_tail_coords = data["you"]["body"][len(data["you"]["body"]) - 1]
    previous_tail_coord = [tmp_tail_coords["x"] + tmp_tail_coords["y"] * height]

    # Shouts are messages sent to all the other snakes in the game.
    # Shouts are not displayed on the game board.
    shout = "I am a python snake!"

    print("Direction: ", move, "move type: ", description_string)
    timer.EndTiming()
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
