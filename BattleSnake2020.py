import json
import os
import random
import numpy as np
import Digraph as dg
import bottle
from bottle import HTTPResponse


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
    print("MOVE:", json.dumps(data))


    player_coord = [data["you"]["body"][0]["x"],data["you"]["body"][0]["y"]] 

    return_data = dg.generate_adjacency_list(data["board"]["height"], data["board"]["width"], data["board"]["snakes"], data["you"]["body"][0], data["board"]["food"], player_coord)
    digraph = return_data[0]
    food_nodes = return_data[1]
    player_node = return_data[2]

    dg.dijkstra(digraph, player_node)
    
    tmp_node = None
    food_nodes.sort(key = lambda node: node.distance)
    for food in food_nodes:
        if dg.is_reachable(digraph, player_node, food) == True:
            tmp_node = food
    
    if tmp_node is not None:
        while tmp_node.previous != None:
            if tmp_node.previous == player_node:
                break
            else:
                tmp_node = tmp_node.previous

    # Choose a random direction to move in
    directions = ["up", "down", "left", "right"]

    move = "down"
    if tmp_node is not None:
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
