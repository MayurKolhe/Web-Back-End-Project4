import socket
import httpx
from quart import Quart, request
from quart_schema import QuartSchema
import redis
import math
import json
import time

app = Quart(__name__)
QuartSchema(app)

redis_client = redis.Redis(host='localhost', port=6379, db=0, charset='utf-8', decode_responses=True)

response = None
while response is None:
    try:
        game_URL = socket.getfqdn("127.0.0.1:5100")
        response = httpx.post('http://'+game_URL+'/webhook', json={'callbackUrl': 'http://127.0.0.1:5400/leaderboard/post', 'client': 'leaderboard'})
    except httpx.RequestError:
        time.sleep(5)

@app.route("/leaderboard/post", methods=["POST"])
async def postScore():
    user_details = await request.get_json()
    print(user_details)
    try:
        user_name = user_details["user_name"]
        guesses = user_details["guesses"]
        win = user_details["win"]
    except TypeError:
        return {"msg":"Error: data improperly formed"}, 400

    game_score =  (7 - guesses)

    # NOTE: INCRBY creates the key if it doesn't exist:
    # https://database.guide/redis-incrby-command-explained/
    t_score = int(redis_client.hincrby(user_name, "total_score", game_score))
    t_games = int(redis_client.hincrby(user_name, "no_of_games", 1))

    average = int(t_score / t_games)
    redis_client.zadd("leaderboard", {user_name: float(average)})
    return "success", 200



@app.route("/leaderboard", methods=["GET"])
async def get_leaderboard():
    """
    
    """
    top_users = redis_client.zrevrange("leaderboard", 0, 9)

    return {"leaders":top_users}, 200
