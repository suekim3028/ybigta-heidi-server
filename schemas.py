from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    name: str
    gender: str
    height: float
    weight: float
    birth_year: int
    job: str
    area: str
    has_children: bool



class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        from_attributes = True
