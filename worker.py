from redis import Redis
from rq import Queue, Worker

redis = Redis()
queue = Queue('queue_name')

# Start a worker with a custom name
worker = Worker([queue], connection=redis, name='foo')
print("worker: " + str(worker))
print("worker name: " + str(worker.name))
print("worker queues: " + str(worker.queues))
print("worker count: " + str(worker.count))
