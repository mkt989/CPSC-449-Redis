from fastapi import FastAPI, Depends, HTTPException
import redis.asyncio as redis

app = FastAPI()
redis_client = redis.Redis(host="localhost", port=6379, db=0)



@app.post("/add-score")
async def add_score(user_id: str, score: int):
    await redis_client.zadd("leaderboard", {user_id: score})
    return {"message": "Score added"}

@app.get("/leaderboard")
async def get_leaderboard():
    top_scores = await redis_client.zrevrange("leaderboard", 0, 9, withscores=True)
    return {"leaderboard": [(user.decode("utf-8"), score) for user, score in top_scores]}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)