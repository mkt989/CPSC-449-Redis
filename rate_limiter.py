from fastapi import FastAPI, Depends, HTTPException
import redis.asyncio as redis

app = FastAPI()
redis_client = redis.Redis(host="localhost", port=6379, db=0)

async def rate_limiter(user_id: str):
    key = f"rate_limit:{user_id}"
    requests = await redis_client.incr(key)

    if requests == 1:
        await redis_client.expire(key, 60)  # Set expiry for the key to 60 seconds

    if requests > 5:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

@app.get("/rate-limited")
async def rate_limited_endpoint(user_id: str = "test_user", depends=Depends(rate_limiter)):
    return {"message": "Request successful"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)