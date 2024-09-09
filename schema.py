# main.py

from models import User, Message, SessionLocal
from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    username: str

class MessageCreate(BaseModel):
    username: str  # Changed to reference `username` instead of `user_id`
    msg: str

class MessageResponse(BaseModel):
    id: int
    username: str
    msg: str
    timestamp: datetime

    class Config:
        from_attributes = True
