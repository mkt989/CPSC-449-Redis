from fastapi import FastAPI, Depends, HTTPException
import redis.asyncio as redis

app = FastAPI()
redis_client = redis.Redis(host="localhost", port=6379, db=0)


@app.post("/track-visit")
async def track_visit(user_id: str):
    await redis_client.sadd("unique_visitors", user_id)
    unique_visitors_count = await redis_client.scard("unique_visitors")
    return {"unique_visitors": unique_visitors_count}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)