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
from sqlalchemy import or_
from fastapi import HTTPException
from datetime import datetime ,timedelta
from pwdlib import PasswordHash
from fastapi.security import OAuth2PasswordRequestForm
from .Auth.security_key import create_access_token,ACCESS_TOKEN_EXPIRE_MINUTES


pwd_hash = PasswordHash.recommended()
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

# Todo Pydantic BaseModel
class TODO(BaseModel):
    title:str=Field(min_length=3,max_length=100)
    status:Status
    priority:Priority
    description:str

class TODOResponse(BaseModel):
    id : int
    title : str
    description : str
    completed : bool
    priority : Priority
    status  : Status
    created_at : datetime
    notes : str | None

# User registered Pydantic BaseModel
class User_Registered(BaseModel):
    username : str
    Location : str
    email_id : str
    password : str = Field(min_length=8,max_length=8)

# User login pydantic BaseModel
class User_Login(BaseModel):
    identifier: str
    password : str

#root
@app.get("/")
def root():
    return("Welcome to root page")


# Register a user : Register endpoint
@app.post("/Toodlo.ai/Register")
async def Register(user:User_Registered,db:Session = Depends(get_db)):
    hashed_password = pwd_hash.hash(user.password)
    new_user = models.User(
        username = user.username,
        Location = user.Location,
        email_id = user.email_id,
        password_hash = hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Login of user : Login endpoint
@app.post("/Toodlo.ai/login")
async def Login(form_depends:Annotated[OAuth2PasswordRequestForm,  Depends()],db:Session = Depends(get_db)):
    verify_user  = db.query(models.User).filter(
        or_(
            models.User.email_id == form_depends.username,
            models.User.username == form_depends.username
        )        
    ).first()
    if verify_user is None:
        raise HTTPException(status_code=404,detail="User is not found")

    if not pwd_hash.verify(form_depends.password , verify_user.password_hash):
        raise HTTPException(status_code = 401 , detail="Incorrect password")

    access_token = create_access_token(
        data ={"sub":str(verify_user.id)},
        expires_delta =timedelta(
            minutes = ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    return{
        "access_token":access_token,
        "token_type":"bearer"
    }



# Create a Todo 
@app.post("/Toodlo.ai/CreateMyTodo",response_model=TODOResponse)
async def CreateTodo(todo:TODO,db:Session = Depends(get_db)):
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
@app.get("/Toodlo.ai/GetMyTodos",response_model=list[TODOResponse])
async def get_todo(q:Annotated[str | None, Query(min_length=2,max_length=50)]= None,db:Session=Depends(get_db) ):
    if q is None:
        return db.query(models.Todo).all()

    return db.query(models.Todo).filter(
            or_(
                models.Todo.title.ilike(f"%{q}%"),
                models.Todo.status.ilike(f"%{q}%"),
                models.Todo.priority.ilike(f"%{q}%"),
            )
        ).all()
   





# Update Todo
@app.put("/Toodlo.ai/UpdateMyTodos/{id}",response_model=TODOResponse)
async def Update_Todo(id:int, todo:TODO, db:Session=Depends(get_db)): 
    existing_todo = db.query(models.Todo).filter(
        models.Todo.id == id
    ).first()

    if existing_todo is None:
        raise HTTPException(status_code=404,detail="Todo Not found")
    
    existing_todo.title = todo.title
    existing_todo.priority = todo.priority
    existing_todo.status = todo.status
    existing_todo.description = todo.description

    db.commit()
    db.refresh(existing_todo)
    return existing_todo



    

# Delete Todo
@app.delete("/Toodlo.ai/DeleteMyTodo/{id}")
async def Delete_Todo(id:int,db:Session=Depends(get_db)):
    existing_todo = db.query(models.Todo).filter(
        models.Todo.id == id
    ).first()

    if existing_todo is None:
        raise HTTPException(status_code=404,detail="Todo not found")

    db.delete(existing_todo)
    db.commit()

    return {"Message: The TODO is deleted successfully !!"}
    













