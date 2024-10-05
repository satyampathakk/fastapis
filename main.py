# main.py
import os
from sqlalchemy import desc
from fastapi import FastAPI, Depends, HTTPException,Request
from sqlalchemy.orm import Session
from models import User, Message, SessionLocal,Messages,UserDetails
from typing import List
from schema import *
from sqlalchemy.sql.expression import func
import psutil
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a user
@app.get('/')
def home():
    return {"message": "Hello, World!"}
@app.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    new_user = User(username=user.username)
    db.add(new_user)
    db.commit()
    return {"username": new_user.username}

@app.post("/details/{username}", response_model=CreateDetails)  
def create_user_details(username: str, details: CreateDetails, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == username).first()
    if not db_user:
        return HTTPException(status_code=404, detail="User not found")
    existing_details = db.query(UserDetails).filter(UserDetails.username == username).first()
    if existing_details:

        existing_details.public_key = details.public_key  # Replace with the new value
        db.commit()
        print("hello")
        return existing_details

    new_details = UserDetails(username=username, public_key=details.public_key)  # Unpack CreateDetails data
    db.add(new_details)
    db.commit()
    return new_details

@app.get("/users/{username}/details")
def get_user_details(username: str, db: Session = Depends(get_db)):
    db_user_details = db.query(UserDetails).filter(UserDetails.username == username).first()
    if not db_user_details:
        raise HTTPException(status_code=404, detail="User details not found")

    return db_user_details

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
    messages = db.query(Message).order_by(Message.timestamp.desc()).limit(15).all()
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
    ).order_by(Messages.timestamp.desc()).limit(3).all()

    if not messages:
        raise HTTPException(status_code=404, detail="No messages found between these users")
    return messages


@app.get("/system-usage")
def get_system_usage():
    cpu_usage_percent = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    total_memory = memory_info.total / (1024 * 1024)  # Total Memory in MB
    free_memory = memory_info.free / (1024 * 1024)    # Free Memory in MB
    used_memory = memory_info.used / (1024 * 1024)    # Used Memory in MB
    memory_usage_percent = memory_info.percent        # Memory usage percentage

    return {
        "cpu_usage_percent": cpu_usage_percent,
        "total_memory": total_memory,
        "free_memory": free_memory,
        "used_memory": used_memory,
        "memory_usage_percent": memory_usage_percent
    }



