from dotenv import load_dotenv
import os
import jwt
from datetime import datetime,timedelta,timezone
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from fastapi import Depends
from ..Db.database import get_db
from sqlalchemy.orm import Session
from ..Db import models
from fastapi import HTTPException
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES =30

# OAuthBearer Scheme
# From this endpoint Client gets their Bearer <token>

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="Toodlo.ai/login"
)

# Created the access token here : token for the access is created
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta is not None:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)


    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM)
    return encoded_jwt

# Get the current user after the TOKEN verification : Token sended by Frontend
def get_current_user( token:Annotated[str, Depends(oauth2_scheme)],db:Session = Depends(get_db)):
    try:
     payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )
    except jwt.InvalidTokenError:
     raise HTTPException(status_code=401 , detail="Invalid request")

    if "sub" not in payload:
       raise HTTPException(status_code=401,detail="Invalid Token")
     
    user_id = int(payload["sub"])

    user = db.query(models.User).filter(
        models.User.id == user_id
    ).first()

    if user is None :
        raise HTTPException(status_code = 401 , detail="User not found")

    return user



