from sqlalchemy import Integer, Column,Boolean, String, DateTime
from .database import Base
from datetime import datetime , timezone

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer,primary_key=True,index=True)
    title = Column(String,nullable=False)
    description = Column(String , nullable=False)
    completed = Column(Boolean,default=False)
    priority = Column(String,nullable=False)
    status = Column(String,nullable=False)
    created_at = Column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc))
    notes = Column(String,nullable=True)

class User(Base):
    __tablename__ ="users"
    id = Column(Integer,primary_key=True,index=True)
    username = Column(String,nullable=False)
    Location = Column(String,nullable=False)
    email_id = Column(String,nullable=False)
    password_hash = Column(String, nullable=False)







