from quart import Quart
from quart_schema import QuartSchema
import redis
import random

app = Quart(__name__)
QuartSchema(app)

@app.route('/postgame', methods=['POST'])
async def postgame():
    r = redis.Redis(host='localhost',port=6379,db=0)
    # r.flushdb() #used to clear db

    for x in range(1, 20):
        game_status = random.choice(["won","lost"])
        guesses = random.randint(1, 6)
        score = (7-guesses)
        user = f"username{x}"
        if game_status == "lost":
            r.lpush(user,0) #push user and score as a list
            r.zadd("username",{user:0}) # will be used to traverse all users
        else:
            r.lpush(user,score)
            r.zadd("username",{user:score})

    json_result = {}
    #iterate all users and combine their individual scores and add it using zadd
    for key in r.zrange("username",0,-1):
        score_list = r.lrange(key,0,-1)
        avg_score = 0
        #loop through all scores for user, val is in bytes
        for val in score_list:
            avg_score += int(val) 
        #calc avg by total score / len of games
        avg_score = int(avg_score/r.llen(key))
        json_result[key.decode('utf-8')] = avg_score
        r.zadd("username",{key.decode('utf-8'): avg_score})
    return json_result

@app.route('/leaderboard')
async def leaderboard():
    r = redis.Redis(db=0)

    #get list of users and their scores
    scoreL = r.zrange("username",0,-1,withscores=True)
    result = {}
    for i in range(1,11):
        # print(scoreL[len(scoreL)-i][0].decode('utf-8') , int(scoreL[len(scoreL)-i][1]))
        #add top 10 from scoreL starting from end, since it is sorted in asc order
        result[scoreL[len(scoreL)-i][0].decode('utf-8')] = int(scoreL[len(scoreL)-i][1])
    
    return result

@app.errorhandler(409)
def conflict(e):
    return {"error": str(e)}, 409