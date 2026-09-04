from fastapi import FastAPI
from enum import Enum
from pydantic import BaseModel,Field
from fastapi import Query
from typing import Annotated
from .Db.database import Base,engine
from .Db import models
from sqlalchemy.orm import Session
from fastapi import Depends
from .Db.database import get_db

Base.metadata.create_all(bind=engine)

app = FastAPI() 

class UserDetails(BaseModel):
    User:str
    

class Priority(str,Enum):
    low = "low"
    medium = 'medium'
    high = 'high'

class Status(str,Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"

class TODO(BaseModel):
    title:str=Field(min_length=3,max_length=100)
    status:Status
    priority:Priority
    description:str

# Temporary page 
@app.get("/")
def root():
    return{"Welocme"}
# Login page desitnation
@app.get("/Toodlo.ai/login")
def login():
    return {"message":"Welcome Login page"}

# Login page credentials submission
@app.post("/Toodlo.ai/login")
def login(username:str,password:str):
    return {"message":"Login Successful"}

users = []

# Register to toodolio.ai 
@app.post("/Toodlo.ai/register")
def Register(user:UserDetails):
    users.append(user)

# Dashboard page

# Home page
@app.get("/Toodlo.ai/Home")
def Home():
    return{"Message":"Welcome to the Toodlo.ai home page"}

todos = []

# Create a Todo 
@app.post("/Toodlo.ai/Home/Todo")
def CreateTodo(todo:TODO,db:Session = Depends(get_db)):
    new_todo=models.Todo(
        title = todo.title,
        priority = todo.priority,
        status = todo.status,
        description=todo.description
    )

    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)

    return new_todo

# Get the Todos
@app.get("/Toodlo.ai/Home/Todo")
async def get_todo(q:Annotated[str | None, Query(min_length=2,max_length=50)]= None ):
    if q is None:
        return todos
    Filter_Todo = []
    for todo in todos:
        if (q.lower() in todo.title.lower() or 
            q.lower() in todo.status.lower() or
            q.lower() in todo.priority.lower()):
         
         Filter_Todo.append(todo)
    return Filter_Todo

# Update Todo
@app.put("/Toodlo.ai/Home/Todo/{id}")
async def Update_Todo(id:int, todo:TODO): 
    todos[id]=todo
    

# Delete Todo
@app.delete("/Toodlo.ai/Home/Todo/{id}")
async def Delete_Todo(id:int):
    todos.pop(id)
   













