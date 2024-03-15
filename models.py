import enum
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from sqlalchemy import Integer, Enum

from .database import Base

class Gender(enum.Enum):
    F = "F"
    M = "M"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    name = Column(String)
    gender = Column(Enum(Gender))
    height = Column(Float)
    weight = Column(Float)
    birth_year = Column(Integer)
    job = Column(String)
    has_children = Column(Boolean)
    phone_country_code= Column(String)
    phone_local_number= Column(String)
    area_level_1= Column(String)
    area_level_2= Column(String)
