from fastapi import FastAPI
from enum import Enum
from pydantic import BaseModel
from fastapi import Query
from typing import Annotated

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
    title:str
    status:Status
    priority:Priority

# Root desitnation
@app.get("/")
def root():
    return {"message":"Welcome to the Todo list"}

users = []
# Create a user 
@app.post("/todo/createuser")
def CreateUser(user:UserDetails):
    users.append(user)
# To see the users
@app.get("/User") 
async def User_info():
    return users

todos = []
# Create a Todo 
@app.post("/todo/createtodo")
def CreateTodo(todo:TODO):
    todos.append(todo)


# To get todo through query. 
# Now here TODO is the object present here so title is used also 
# Here to make it case sensitive we used below code  
# Annotations are used to handle the query.
# Here we are using Query() method bcz here we need to validate the query.

@app.get("/todo")
def get_todo(q:Annotated[str | None, Query(min_length=2,max_length=50)]= None ):
    if q is None:
        return todos
    Filter_Todo = []
    for todo in todos:
        if (q.lower() in todo.title.lower() or 
            q.lower() in todo.status.lower() or
            q.lower() in todo.priority.lower()):
         
         Filter_Todo.append(todo)
    return Filter_Todo
    













