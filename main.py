from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy.orm import Session

from . import crud, models, schemas,recommend_models
from .database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
from json import JSONDecodeError
import logging


models.Base.metadata.create_all(bind=engine)


app = FastAPI()

origins = ["http://localhost:3000", "http://172.24.103.119:3000"]
logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.UserResponse)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    logger.info("뭐가 문제지")
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_db_user = crud.create_user(db=db, user=user)

    return schemas.UserResponse(user=schemas.userSchema2Dto(new_db_user), token="")


@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return schemas.UserResponse(user=schemas.userSchema2Dto(db_user), token="")


@app.get("/programs/{user_id}", response_model=schemas.ProgramListResponseDto)
def getPrograms(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    programs = recommend_models.recommend(db_user)
    logger.info(programs)
    return schemas.ProgramListResponseDto(programs=programs)