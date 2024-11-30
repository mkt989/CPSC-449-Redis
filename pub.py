import redis
import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


# Please note: This is meant for FastAPI and not Flask.
app = FastAPI()
redis_client = redis.Redis(host='localhost', port=6379, db=0)
class Message(BaseModel):
    message: str

@app.post("/send-notification")
async def send_notification(data: Message):
    redis_client.publish("notifications", data.message)
    return {"status": "Notification sent"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)