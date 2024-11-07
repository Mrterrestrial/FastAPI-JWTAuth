from fastapi import APIRouter, Depends

router = APIRouter()

@router.get("/")
def read_root():
    return {"message": "Welcome to Secure API with OAuth2 & JWT"}