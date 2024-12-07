import redis
import asyncio
from fastapi import FastAPI, HTTPException


# Please note: This is meant for FastAPI and not Flask.
app = FastAPI()
redis_client = redis.Redis(host='localhost', port=6379, db=0)

@app.get("/check-redis-connection")
async def check_redis_connection():
    try:
        # Since Redis client is synchronous, use it in an async-friendly way
        is_connected = await  asyncio.get_running_loop().run_in_executor(None, redis_client.ping)
        if is_connected:
            return {"status": "Redis connection successful!"}
        else:
            raise HTTPException(status_code=500, detail="Redis connection failed.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error connecting to Redis: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
