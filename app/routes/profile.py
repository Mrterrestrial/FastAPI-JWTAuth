from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.utils.db import get_db
from app.models.user_model import User
import jwt
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os

load_dotenv()  # Load once, at the beginning
secret_key = os.getenv('JWT_SECRET_KEY')
router = APIRouter()

def verify_jwt_token(token):
    algorithm = 'HS256'
    # Decode and verify the JWT token
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=403, detail="Invalid token")

@router.get('/me')
async def profile(request: Request, db: Session = Depends(get_db)):
    # Retrieve the token from cookies
    token = request.cookies.get('token')
    if not token:
        raise HTTPException(status_code=403, detail="Access Denied: No token provided")

    # Verify and decode the token
    payload = verify_jwt_token(token)
    
    # Fetch user from the database
    user = db.query(User).filter(User.id == payload["user_id"]).first()
    
    # If user is not found, raise an error
    if not user:
        raise HTTPException(status_code=403, detail="Access Denied: User not found")

    return user
