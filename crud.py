from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(
        email=user.email,
        hashed_password=fake_hashed_password,
        name=user.name,
        gender=user.gender,
        height=user.height,
        weight=user.weight,
        birth_year=user.birth_year,
        job=user.job,
        area = user.area,
        has_children=user.has_children,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user