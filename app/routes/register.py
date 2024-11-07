# app/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from app.models.user_model import User
from app.utils.db import get_db
from passlib.hash import pbkdf2_sha256
import logging



router = APIRouter()



class Registration(BaseModel):
    First_name: str
    Last_name: str
    Phone_number: Optional[int]=None
    Username: str 
    Password: str
    Email: Optional[str]


def hash_password(password: str) -> str:
    return pbkdf2_sha256.hash(password)

@router.post("/register")
async def registration(registration: Registration, db: Session = Depends(get_db)):
    hashed_password = hash_password(registration.Password)
    user = User(
        first_name=registration.First_name,
        last_name=registration.Last_name,
        phone_number=registration.Phone_number,
        username=registration.Username,
        password=hashed_password,  
        email=registration.Email
    )
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except IntegrityError as e:
        db.rollback()
        # Log the error for debugging purposes
        logging.error("IntegrityError occurred:", exc_info=True)
        
        # Determine which unique field caused the error
        if 'username' in str(e.orig):
            raise HTTPException(status_code=400, detail="Username already exists")
        elif 'phone_number' in str(e.orig):
            raise HTTPException(status_code=400, detail="Phone number already exists")
        elif 'email' in str(e.orig):
            raise HTTPException(status_code=400, detail="Email already exists")
        else:
            raise HTTPException(status_code=400, detail="Integrity constraint failed")
    
    return {"message": "User registered successfully"}