from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(
        hashed_password=fake_hashed_password,
        email=user.email,
        name=user.name,
        gender=user.gender,
        height=user.height,
        weight=user.weight,
        birth_year=user.birth_year,
        job=user.job,
        has_children=user.has_children,
        phone_country_code=user.phone_country_code,
        phone_local_number=user.phone_local_number,
        area_level_1=user.area_level_1,
        area_level_2=user.area_level_2,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
