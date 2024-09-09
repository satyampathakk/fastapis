# main.py

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import User, Message, SessionLocal
from pydantic import BaseModel
from typing import List
from datetime import datetime
from schema import *
app = FastAPI()

# Dependency: Get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a user
@app.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    new_user = User(username=user.username)
    db.add(new_user)
    db.commit()
    return {"username": new_user.username}

# Store a message
@app.post("/messages/", response_model=MessageResponse)
def create_message(msg: MessageCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == msg.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_msg = Message(username=msg.username, msg=msg.msg)
    db.add(new_msg)
    db.commit()
    db.refresh(new_msg)
    return new_msg

# Get all messages
@app.get("/messages/", response_model=List[MessageResponse])
def get_messages(db: Session = Depends(get_db)):
    messages = db.query(Message).all()
    return messages

# Get messages by username
@app.get("/users/{username}/messages", response_model=List[MessageResponse])
def get_user_messages(username: str, db: Session = Depends(get_db)):
    messages = db.query(Message).filter(Message.username == username).all()
    return messages
