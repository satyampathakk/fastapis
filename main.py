# main.py

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import User, Message, SessionLocal,Messages
from typing import List
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

@app.post("/messages/send/", response_model=CreateUserMes)
def send_message(msg: CreateUserMes, db: Session = Depends(get_db)):
    sender = db.query(User).filter(User.username == msg.sender_username).first()
    if not sender:
        raise HTTPException(status_code=404, detail="Sender not found")

    recipient = db.query(User).filter(User.username == msg.recipient_username).first()
    if not recipient:
        raise HTTPException(status_code=404, detail="Recipient not found")

    new_msg = Messages(sender_username=msg.sender_username, recipient_username=msg.recipient_username, msg=msg.msg)
    db.add(new_msg)
    db.commit()
    db.refresh(new_msg)
    return new_msg

# Get messages between two users
@app.get("/messages/{sender_username}/{recipient_username}", response_model=List[CreateUserMes])
def get_messages_between(sender_username: str, recipient_username: str, db: Session = Depends(get_db)):
    messages = db.query(Messages).filter(
        (Messages.sender_username == sender_username) & 
        (Messages.recipient_username == recipient_username) |
        (Messages.sender_username == recipient_username) & 
        (Messages.recipient_username == sender_username)
    ).all()

    if not messages:
        raise HTTPException(status_code=404, detail="No messages found between these users")

    return messages


