from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database.postgres import Base  

class User(Base):
    """User table for storing user details."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    preferences = relationship("UserPreferences", back_populates="user", cascade="all, delete-orphan")
    queries = relationship("QueryLogs", back_populates="user", cascade="all, delete-orphan")

class UserPreferences(Base):
    """Stores user preferences for personalized ranking."""
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    preferred_keywords = Column(JSON, nullable=True)

    user = relationship("User", back_populates="preferences")

class QueryLogs(Base):
    """Logs all user queries for personalized search history."""
    __tablename__ = "query_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    query = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

    user = relationship("User", back_populates="queries")