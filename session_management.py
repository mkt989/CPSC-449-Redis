import uuid
from fastapi import FastAPI, HTTPException
import redis.asyncio as redis

app = FastAPI()
redis_client = redis.Redis(host="localhost", port=6379, db=0)

@app.post("/login")
async def login(user_id: str):
    session_token = str(uuid.uuid4())
    await redis_client.setex(f"session:{session_token}", 1800, user_id)  # Expires in 30 minutes
    return {"session_token": session_token}

@app.get("/validate-session/{session_token}")
async def validate_session(session_token: str):
    user_id = await redis_client.get(f"session:{session_token}")
    if user_id:
        return {"status": "Session valid", "user_id": user_id.decode("utf-8")}
    else:
        raise HTTPException(status_code=401, detail="Invalid session token")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)