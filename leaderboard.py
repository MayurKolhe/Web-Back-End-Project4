import httpx
from quart import Quart, request
from quart_schema import QuartSchema
import redis

app = Quart(__name__)
QuartSchema(app)

redis_client = redis.Redis(host='localhost', port=6379, db=0, charset='utf-8', decode_responses=True)

try:
    response = httpx.post('http://127.0.0.1:5100/webhookUrl', json={'Url': "http://127.0.0.1:5400/leaderboard/post", 'client_name': 'leaderboard'})
except httpx.RequestError as e:   
    print("Request Error : ",e)

@app.route("/leaderboard/post", methods=["POST"])
async def postScore():
    user_details = await request.get_json()
    print(user_details)
    try:
        user_name = user_details["username"]
        guesses = user_details["guesses"]
        win = user_details["result"]
    except TypeError:
        return {"msg":"Error: data improperly formed"}, 400

    game_score =  (6 - guesses)
        
    t_score = int(redis_client.hincrby(user_name, "total_score", game_score))
    t_games = int(redis_client.hincrby(user_name, "no_of_games", 1))

    average = int(t_score / t_games)
    redis_client.zadd("leaderboard", {user_name: float(average)})
    return "success", 200



@app.route("/leaderboard", methods=["GET"])
async def get_leaderboard():
    """
    
    """        
    top_users = redis_client.zrevrange("leaderboard", 0, 9, withscores=True)
    answer="Top 10 leaders are: \n\n"
    for i in top_users:
        i=str(i)
        answer=answer + i[1:-1] + "\n"
        
    return answer
    
