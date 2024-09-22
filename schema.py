# main.py

from models import User, Message, SessionLocal
from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    username: str

class MessageCreate(BaseModel):
    username: str  
    msg: str

class MessageResponse(BaseModel):
    id: int
    username: str
    msg: str
    timestamp: datetime

    class Config:
        from_attributes = True
class CreateUserMes(BaseModel):
    sender_username:str
    recipient_username:str
    msg: str
    
class CreateDetails(BaseModel):
    public_key:str