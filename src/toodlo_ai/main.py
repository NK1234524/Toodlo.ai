from fastapi import FastAPI
from fastapi import Query
from typing import Annotated
from .Db.database import Base,engine
from .Db import models
from sqlalchemy.orm import Session
from fastapi import Depends
from .Db.database import get_db
from sqlalchemy import or_
from fastapi import HTTPException
from datetime import timedelta,date
from pwdlib import PasswordHash
from fastapi.security import OAuth2PasswordRequestForm
from .Auth.security_key import create_access_token,ACCESS_TOKEN_EXPIRE_MINUTES,get_current_user
from .AI.client import client
from .AI.deadline import calculate_due_date
from toodlo_ai.AI.Instruction.todo_creation_instruction import TODO_CREATION_INSTRUCTION
from toodlo_ai.AI.Instruction.Daily_Planning_instruction import DAILY_PLANNING_INSTRUCTION
from datetime import datetime, timedelta
from .Schemas.schema import(
    TODO,
    TODOResponse,    
    User_Registered,
    User_Registeration,    
    AI_Response_Model,
    AI_TODO_request,
    AI_TODO_Clarification_request,
    AI_Action,
    AI_Dailyplan
)


pwd_hash = PasswordHash.recommended()
Base.metadata.create_all(bind=engine)

app = FastAPI() 


#root
@app.get("/")
def root():
    return("Welcome to root page")


# Register a user : Register endpoint
@app.post("/Toodlo.ai/Register",response_model =User_Registeration)
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
async def Login(form_depends:Annotated[OAuth2PasswordRequestForm,  Depends()],
    db:Session = Depends(get_db)):

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
async def CreateTodo(todo:TODO,db:Session = Depends(get_db),
    current_user:models.User = Depends(get_current_user)):

    new_todo=models.Todo(
        title = todo.title,
        priority = todo.priority,
        status = todo.status,
        description=todo.description,
        #notes = todo.notes,
        user_id = current_user.id,
        due_Date = todo.due_Date
    )

    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)

    return new_todo

# Create Todo by AI gemini
@app.post("/Toodlo.ai/AI/CreateMyTodo")
async def AI_Create_Todo(request_model: AI_TODO_request, db:Session = Depends(get_db),
    current_user:models.User = Depends(get_current_user)):

    context = f"""
        Current date: {date.today()}
        User request: {request_model.content}
        """
    
    response = client.models.generate_content(
    model = "gemini-3.6-flash",
    
    contents = context,
    config = {
        "system_instruction":TODO_CREATION_INSTRUCTION,
        "response_mime_type":"application/json",
        "response_schema":AI_Response_Model
    }
)
    # print(response.parsed)
    if response.parsed.action == AI_Action.clarification_required:
        pending_clarification = models.AI_Clarification_Pending(
            user_id = current_user.id,
            original_req = request_model.content,
            question = response.parsed.question
        )
        
        db.add(pending_clarification)
        db.commit()
        return response.parsed
    if response.parsed.action ==AI_Action.ready:
        due_date = calculate_due_date(
            response.parsed.deadline_type,
            response.parsed.deadline_value
        )
        new_todo = models.Todo(
            title=response.parsed.todo.title,
            priority=response.parsed.todo.priority,
            status=response.parsed.todo.status,
            description=response.parsed.todo.description,
            #notes=response.parsed.todo.notes,
            user_id=current_user.id,
            due_Date= due_date,
            urgency = response.parsed.urgency
            )
        db.add(new_todo)
        db.commit()
        db.refresh(new_todo)
        return {
            "todo":new_todo,
            "breakdown":response.parsed.breakdown,
            "deadline_type":response.parsed.deadline_type,
            "deadline_value":response.parsed.deadline_value
        }
        


# Clarification of Todo
@app.post("/Toodlo.ai/AI/clarifyMyTodo")
async def AI_Todo_clarification(request_model : AI_TODO_Clarification_request,
    db:Session = Depends(get_db),current_user:models.User = Depends(get_current_user)):
    pending_Clarification = db.query(
        models.AI_Clarification_Pending
    ).filter(
        models.AI_Clarification_Pending.user_id == current_user.id
    ).first()

    if pending_Clarification is None :
        raise HTTPException (status_code= 404, detail= "No pending clarifiation found")
    context = f""" current date : {date.today()}
    Original request : {pending_Clarification.original_req}
    User clarification : {request_model.clarification}"""
    response = client.models.generate_content(
        model = "gemini-3.6-flash",
        contents = context,
        config = {
            "system_instruction":TODO_CREATION_INSTRUCTION,
            "response_mime_type":"application/json",
            "response_schema":AI_Response_Model
        }
    )
    if response.parsed.action ==AI_Action.ready:
        new_todo = models.Todo(
            title=response.parsed.todo.title,
            priority=response.parsed.todo.priority,
            status=response.parsed.todo.status,
            description=response.parsed.todo.description,
            #notes=response.parsed.todo.notes,
            user_id=current_user.id,
            due_Date=response.parsed.todo.due_Date
            )
        db.add(new_todo)
        db.commit()
        db.refresh(new_todo)
        return new_todo
    return response.parsed

# Daily planning of user from todo 
@app.post("/Toodlo.ai/AI/CreateDailyPlan")
async def Create_Daily_Plan(
    db:Session=Depends(get_db),
    current_user:models.User=Depends(get_current_user)
):
    todos = db.query(models.Todo).filter(
        models.Todo.user_id == current_user.id,
        models.Todo.status != "completed"
    ).all()
    context = f'''
    Current_Date :{date.today()}
    User's incomplete Todos :
    {
         [
            {
            "id" : todo.id,
            "title" : todo.title,
            "description" : todo.description,
            "priority" : todo.priority,
            "urgency" : todo.urgency,
            "due_Date" : todo.due_Date
            }
        for todo in todos
        ]
    }
    '''
    response = client.models.generate_content(
            model = "gemini-3.6-flash",
            contents = context,
            config = {
                "system_instruction":DAILY_PLANNING_INSTRUCTION,
                "response_mime_type":"application/json",
                "response_schema":AI_Dailyplan
            }
        )
    daily_plan = response.parsed
    if daily_plan is None :
        raise HTTPException(
            status_code=502,
            detail="AI failed to generate a valid daily plan"
        )
    valid_todo_id = {todo.id for todo in todos}
    for task in daily_plan.tasks:
        if task.todo_id not in valid_todo_id:
            raise HTTPException(
            status_code=502,
            detail = "AI returned the wrong todo ."
        )
    for task in daily_plan.tasks:
        # print("Saving Data:",task.todo_id)
        daily_plan_record = models.DailyPlanning(
            user_id = current_user.id,
            todo_id = task.todo_id,
            plan_date = datetime.now().astimezone().replace(
                hour =0, minute=0, second=0, microsecond=0
            ),
            reason = task.reason
        )
    
        db.add(daily_plan_record)
    # print("Pending:",len(db.new))
    # print("task_returned:",len(daily_plan.tasks))
    
    db.commit()
    # print("Commit Successful")
    return daily_plan

# Adaptive Replanning
@app.post("/Toolo.ai/AI/AdaptiveReplan")
async def Adaptive_Replan(
    db:Session = Depends(get_db),
    current_user:models.User = Depends(get_current_user)
):

    # This will help to remove the duplicate ones

    today = date.today()
    existing_plan = db.query(models.DailyPlanning).filter(
        models.DailyPlanning.user_id == current_user.id,
        models.DailyPlanning.plan_date >= datetime.combine(
            today,
            datetime.min.time()
        ).astimezone(),
        models.DailyPlanning.plan_date <datetime.combine(
            today + timedelta(days=1),
            datetime.min.time()
        ).astimezone()
    ).all()

    if existing_plan:
        tasks = []

    for plan in existing_plan:
        todo = db.query(models.Todo).filter(
            models.Todo.id == plan.todo_id,
            models.Todo.user_id == current_user.id
        ).first()

        if todo:
            tasks.append({
                "todo_id": todo.id,
                "title": todo.title,
                "status": todo.status,
                "priority": todo.priority,
                "due_date": todo.due_Date,
                "reason": plan.reason
            })

    

    
    yesterday = date.today() - timedelta(days =1)
    yesterday_plan = db.query(models.DailyPlanning).filter(
        models.DailyPlanning.user_id == current_user.id,
        models.DailyPlanning.plan_date >=datetime.combine(
            yesterday,
            datetime.min.time()
        )
    ).all()
    
    unfinished_task = []
    for plan in yesterday_plan:
            todo = db.query(models.Todo).filter(
                models.Todo.id == plan.todo_id,
                models.Todo.user_id == current_user.id,
                models.Todo.status !="completed"
            ).first()
            if todo:
                unfinished_task.append(todo)
   
    
    carried_forward_ids = {
    todo.id for todo in unfinished_task
    }

    additional_Task = db.query(models.Todo).filter(
        models.Todo.user_id == current_user.id,
        models.Todo.status !="completed",
        ~models.Todo.id.in_(carried_forward_ids)
    ).all()

    candidate_tasks = []

    for todo in unfinished_task:
        candidate_tasks.append({
            "id":todo.id,
            "titile":todo.title,
            "description":todo.description,
            "priority":todo.priority,
            "urgency":todo.urgency,
            "due_date":todo.due_Date,
            "is_Carry_forward":True
        })

    for todo in additional_Task:
        candidate_tasks.append({
            "id":todo.id,
            "titile":todo.title,
            "description":todo.description,
            "priority":todo.priority,
            "urgency":todo.urgency,
            "due_date":todo.due_Date,
            "is_Carry_forward":False
        })

    context = {
        "current date" : date.today().isoformat(),
        "candidate_tasks":candidate_tasks
    }
    response = client.models.generate_content(
        model = "gemini-3.6-flash",
        contents = str(context),
        config = {
            "system_instruction":DAILY_PLANNING_INSTRUCTION,
            "response_mime_type":"application/json",
            "response_schema":AI_Dailyplan
        }
    )
    daily_plan = response.parsed

    if daily_plan is None :
        raise HTTPException(
            status_code = 502,
            detail  = "AI failed to generate a valid daily plan"
        )

    valid_todo_ids = {todo["id"] for todo in candidate_tasks}
    returned_ids = [task.todo_id for task in daily_plan.tasks]
    
    # For removal of Duplicate data present in the Todo table :- 
    
    if len(returned_ids) != len(set(returned_ids)):
        raise HTTPException(
            status_code = "502",
            detail = "AI returned duplicated output"
        )

    if not set(returned_ids).issubset(valid_todo_ids):
        raise HTTPException(
            status_code = "502",
            detail = "AI returned an inelligible TODO ID"
        )
    # After adaptive replanning the data is inserted into the DB.
    today = date.today()
    for task in daily_plan.tasks:
        daily_plan_record = models.DailyPlanning(
            user_id = current_user.id,
            todo_id = task.todo_id,
            plan_date = datetime.combine(
                today,
                datetime.min.time()
            ).astimezone(),
            reason  = task.reason
        )
        db.add(daily_plan_record)
    db.commit()
    # return {
    #         "message": "Today's adaptive plan already exists",
    #         "tasks": tasks
    #     }
    return daily_plan   

   
    
# Get the Todos
@app.get("/Toodlo.ai/GetMyTodos",response_model=list[TODOResponse])
async def get_todo(q:Annotated[str | None, Query(min_length=2,max_length=50)]= None,
    db:Session=Depends(get_db),
    current_user : models.User= Depends(get_current_user)):

    if q is None:
        return db.query(models.Todo).filter(
            models.Todo.user_id == current_user.id
        ).all()

    return db.query(models.Todo).filter(
        models.Todo.user_id == current_user.id,
            or_(
                models.Todo.title.ilike(f"%{q}%"),
                models.Todo.status.ilike(f"%{q}%"),
                models.Todo.priority.ilike(f"%{q}%")                
            )
        ).all()
   





# Update Todo
@app.put("/Toodlo.ai/UpdateMyTodos/{id}",response_model=TODOResponse)
async def Update_Todo(id:int, todo:TODO, db:Session=Depends(get_db),
    current_user:models.User=Depends(get_current_user)): 
    existing_todo = db.query(models.Todo).filter(
        models.Todo.id == id,
        models.Todo.user_id == current_user.id
    ).first()

    if existing_todo is None:
        raise HTTPException(status_code=404,detail="Todo Not found")
    
    existing_todo.title = todo.title
    existing_todo.priority = todo.priority
    existing_todo.status = todo.status
    existing_todo.description = todo.description
    existing_todo.urgency = todo.urgency
    #existing_todo.notes = todo.notes

    db.commit()
    db.refresh(existing_todo)
    return existing_todo



    

# Delete Todo
@app.delete("/Toodlo.ai/DeleteMyTodo/{id}")
async def Delete_Todo(id:int,db:Session=Depends(get_db),
    current_user:models.User=Depends(get_current_user)):
    existing_todo = db.query(models.Todo).filter(
        models.Todo.id == id,
        models.Todo.user_id == current_user.id
    ).first()

    if existing_todo is None:
        raise HTTPException(status_code=404,detail="Todo not found")

    db.delete(existing_todo)
    db.commit()

    return {"Message": "The TODO is deleted successfully !!"}
    













