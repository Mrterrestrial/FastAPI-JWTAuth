from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.utils.db import get_db
from app.models.user_model import User
from passlib.hash import pbkdf2_sha256
from pydantic import BaseModel
import jwt
from datetime import datetime, timedelta
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
import os

load_dotenv()
secret_key = os.getenv('JWT_SECRET_KEY')

class Login(BaseModel):
    Username: str 
    Password: str

def create_jwt_token(payload):
    algorithm = 'HS256'
    token = jwt.encode(payload, secret_key, algorithm=algorithm)
    return token

router = APIRouter()

@router.post('/login')
async def login(login: Login, db: Session = Depends(get_db)):
    # Find the user by username
    user = db.query(User).filter(User.username == login.Username).first()
    
    # If user is not found or password does not match
    if not user or not pbkdf2_sha256.verify(login.Password, user.password):
        raise HTTPException(status_code=404, detail="Username or Password is wrong")
    
    # Create JWT payload
    payload = {
        'user_id': user.id,
        'username': user.username,
        'role': 'normal_user',
        'exp': datetime.utcnow() + timedelta(minutes=15)
    }

    # Generate the JWT token
    token = create_jwt_token(payload)

    # Redirect the user to the profile page after login
    response = RedirectResponse(url="/me", status_code=302)
    response.set_cookie(key="token", value=token, httponly=True, secure=True)

    return response
