from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
from json import JSONDecodeError
import logging
from .ml_model.models import recom_forest_hiking, calc_effect, recom_exp_healing


# ,recom_exp_healing

import random
import pandas as pd

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


@app.get("/programs", response_model=schemas.ProgramListResponseDto)
def getPrograms(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    exp_healing_programs = recom_exp_healing.run(
        db_user.birth_year, db_user.gender, db_user.job, db_user.has_children
    )

    forest_hiking = recom_forest_hiking.run()

    res_dtos: list[schemas.ProgramMini] = []
    res_programs = pd.concat([forest_hiking, exp_healing_programs])

    for __idx__, row in res_programs.iterrows():
        res_dtos.append(
            schemas.ProgramMini(
                id=row["id"],
                name=row["name"],
                rate=3,
                category=row["category"],
                place=row["place"],
            )
        )

    random.shuffle(res_dtos)
    return schemas.ProgramListResponseDto(programs=res_dtos)


@app.get("/program", response_model=schemas.ProgramDetailResponseDto)
def getPrograms(user_id: int, program_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    program, effect = calc_effect.run(
        program_id, db_user.height, db_user.birth_year, db_user.gender, db_user.weight
    )
    print("-=-=-=-=-=-=-=-=")
    print(program)
    print("-=-=-=-=-=-=-=-=")

    print(effect)

    programDetail = schemas.ProgramDetail(
        id=program_id,
        name= program["name"],
        rate=3,
        category=program.category,
        place=program.place,
        healthResult=effect,
        duration=program.duration,
        maxPeople=program["max_people"],
        fee=program.fee,
        distance=program.distance,
        address=program.address,
    )

    print(programDetail)

    return schemas.ProgramDetailResponseDto(program=programDetail)
