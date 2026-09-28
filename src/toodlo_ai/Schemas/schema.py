from enum import Enum
from pydantic import BaseModel,Field
from datetime import datetime ,timedelta
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
    #notes:str | None=None
    due_Date:datetime | None =None
    urgency:str | None=None

class TODOResponse(BaseModel):
    id : int
    title : str
    description : str
    #completed : bool
    priority : Priority
    status  : Status
    created_at : datetime
    #notes : str | None
    due_Date : datetime | None =None

# User registered Pydantic BaseModel
class User_Registered(BaseModel):
    username : str
    Location : str
    email_id : str
    password : str = Field(min_length=8,max_length=8)

# User registration pydantic response BaseModel
class User_Registeration(BaseModel):
    id : int
    username :str
    Location :str
    email_id :str

# User login pydantic response BaseModel
class User_Login(BaseModel):
    identifier: str
    password : str

# AI action
class AI_Action(str,Enum):
    ready ="ready"
    clarification_required = "clarification_required"

# Deadline_Type
class DeadlineType(str,Enum):
    explicit = "explicit"
    relative = "relative"
    suggested = "suggested"


# AI TodoList model for Daily planning
class AI_Todo_list(BaseModel):
    todo_id:int
    reason:str

    
# AI Daily planning model 
class AI_Dailyplan(BaseModel):
    tasks : list[AI_Todo_list]



# AI RESPONSE model
class AI_Response_Model(BaseModel):
    action : AI_Action
    todo:TODO | None = None
    question : str | None = None
    breakdown : str | None = None
    urgency : str | None = None
    deadline_type : DeadlineType | None = None
    deadline_value : str | None = None

# AI request model to the Frontend
class AI_TODO_request(BaseModel):
    content :str

# AI request model for clarification
class AI_TODO_Clarification_request(BaseModel):
    clarification : str | None=None

# AI response for subtasks
class AI_TODO_Subtasks(BaseModel):
    subtask1:str 
    subtask2:str 
    subtask3:str
    subtask4:str
    subtask5:str

# AI urgency 
class AI_Urgency(str, Enum):
    very_urgent = "very_urgent"
    less_urgent = "less_urgent"
    can_take_more_time = "can_take_more_time"



