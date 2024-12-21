import redis.asyncio as redis
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI

app = FastAPI()
redis_client = redis.Redis(host="localhost", port=6379, db=0)

@asynccontextmanager
async def lifespan(app: FastAPI):
    pubsub = redis_client.pubsub()
    await pubsub.subscribe("notifications")  # Subscribe to 'notifications' channel

    async def listen_to_notifications():
        while True:
            message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
            if message:
                print("Received notification:", message["data"].decode("utf-8"))
            await asyncio.sleep(0.1)  # Avoid tight loop, add a short delay

    # Start listening in the background
    task = asyncio.create_task(listen_to_notifications())
    
    yield  # Start-up code

    # Clean up after shutdown
    await pubsub.unsubscribe("notifications")
    task.cancel()
    await task

app = FastAPI(lifespan=lifespan)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8010)
