import os
import redis
import time

# Connect to Redis with the same settings as the API
r = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"), 
    port=6379, 
    decode_responses=True
)

def process_redis_jobs():
    print("Worker is live and watching 'job_queue'...")
    while True:
        # blpop waits for a job to appear in 'job_queue'
        # The '0' means it waits forever until a job arrives
        job = r.blpop("job_queue", timeout=0) 
        
        if job:
            # job is a tuple: (list_name, data)
            job_id = job[1]
            print(f"Starting work on job: {job_id}")
            
            # Simulate processing time (2 seconds)
            time.sleep(2) 
            
            # Update the status in the hash map so the dashboard sees it
            r.hset(f"job:{job_id}", "status", "completed")
            print(f"Finished job: {job_id}")

if __name__ == "__main__":
    process_redis_jobs()