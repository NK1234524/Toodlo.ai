from sqlalchemy import Integer, Column,Boolean, String, DateTime, ForeignKey
from .database import Base
from datetime import datetime , timezone

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer,primary_key=True,index=True)
    title = Column(String,nullable=False)
    description = Column(String , nullable=False)
    #completed = Column(Boolean,default=False)
    priority = Column(String,nullable=False)
    status = Column(String,nullable=False)
    created_at = Column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc))
    #notes = Column(String,nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"),nullable=False )
    due_Date = Column(DateTime(timezone=True),nullable=True)
    urgency = Column(String , nullable=False)

class User(Base):
    __tablename__ ="users"
    id = Column(Integer,primary_key=True,index=True)
    username = Column(String,nullable=False)
    Location = Column(String,nullable=False)
    email_id = Column(String,nullable=False)
    password_hash = Column(String, nullable=False)


class AI_Clarification_Pending(Base):
    __tablename__ = "Clarification_pending"
    id =Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer, ForeignKey("users.id"),nullable=False )
    original_req = Column(String,nullable=False)
    question = Column(String,nullable=False)

class DailyPlanning(Base):
    __tablename__ = "DailyPlanning"
    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey("users.id"),nullable=False)
    todo_id = Column(Integer,ForeignKey("todos.id"),nullable=False)
    plan_date = Column(DateTime(timezone=True),nullable=False)
    reason = Column(String ,nullable=False)   


