import httpx
from rq import Queue
from rq.job import Job
from redis import Redis
from rq.registry import FailedJobRegistry
from quart import request

def leaderboard_post(value,callbackUrl):
    try:
        sending_request=httpx.post(callbackUrl,json=value)
        print(sending_request.status_code)
    except httpx.RequestError:
        return "Error Happened !!!",sending_request.status_code

#Creating worker function
def worker_func(user_name, final_result, guess, Url):
    value={'username':user_name, 'result':final_result, 'guesses':guess}
    redis_call=Redis()
    queue=Queue(connection=Redis())
    failedJobRegistry= FailedJobRegistry(queue=queue)
    r=queue.enqueue(leaderboard_post,value,Url)
    
