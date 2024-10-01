# models.py
from sqlalchemy import Column, String, Text, DateTime,Integer,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime

# Define the SQLite database
SQLALCHEMY_DATABASE_URL = "sqlite:///./chat.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Define User model with `username` as primary key
class User(Base):
    __tablename__ = "users"
    username = Column(String, primary_key=True, index=True, unique=True)

class UserDetails(Base):
    __tablename__ = "user_details"
    username = Column(String, ForeignKey('users.username'), primary_key=True, index=True, unique=True)
    public_key = Column(Text)

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    msg = Column(Text)
    timestamp = Column(DateTime, default=datetime.now)

class Messages(Base):
    __tablename__ = "message"

    id = Column(Integer, primary_key=True, index=True)
    sender_username = Column(String, index=True)
    recipient_username = Column(String, index=True)  # Added recipient field
    msg = Column(Text)
    timestamp = Column(DateTime, default=datetime.now)

# Create database tables
Base.metadata.create_all(bind=engine)