from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    name: str
    gender: str
    height: float
    weight: float
    job: str


class UserSchemaBase(UserBase):
    has_children: bool
    phone_country_code: str
    phone_local_number: str
    area_level_1: str
    area_level_2: str
    birth_year: int


class UserDtoBase(UserBase):
    hasChildren: bool
    phoneCountryCode: str
    phoneLocalNumber: str
    area: list[str]
    birthYear: int


class UserCreate(UserSchemaBase):
    password: str


class UserSchema(UserSchemaBase):
    id: int

    class Config:
        from_attributes = True


class UserDto(UserDtoBase):
    id: int


def userSchema2Dto(user=UserSchema):
    return UserDto(
        id=user.id,
        email=user.email,
        name=user.name,
        gender=user.gender,
        height=user.height,
        weight=user.weight,
        job=user.job,
        hasChildren=user.has_children,
        phoneCountryCode=user.phone_country_code,
        phoneLocalNumber=user.phone_local_number,
        area=[user.area_level_1, user.area_level_2],
        birthYear=user.birth_year,
    )

class UserResponse(BaseModel):
    user: UserDto
    token: str
