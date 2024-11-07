from fastapi import FastAPI
from pydantic import BaseModel
from config.database import Base, engine
from app.models.user_model import User 
from app.routes.index import router as index_router
from app.routes.register import router as register
from app.routes.profile import router as profile
from app.routes.login import router as login




def init_db():
    Base.metadata.create_all(bind=engine)


app = FastAPI()
app.include_router(index_router)
app.include_router(register)
app.include_router(profile)
app.include_router(login)




if __name__ == "__main__":
    import uvicorn
    init_db()
    print("Database tables created successfully!")
    uvicorn.run(app, host="127.0.0.1", port=8000)

