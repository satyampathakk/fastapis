# models.py
from sqlalchemy import Column, String, Text, DateTime,Integer
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

# Define Message model with a foreign key to `username`
class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    msg = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Create database tables
Base.metadata.create_all(bind=engine)
