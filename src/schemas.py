from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class ContactModel(BaseModel):
    first_name: str = Field("first_name", min_length=3, max_length=100)
    second_name: str = Field("second_name", min_length=3, max_length=100)
    email: EmailStr
    phone_number: str = Field("phone_number", min_length=9, max_length=13)
    birthday: date
    additional_info: Optional[str] = 0


class RespondsContact(BaseModel):
    id: int = 1
    first_name: str
    second_name: str
    email: EmailStr
    phone_number: str
    birthday: date
    additional_info: Optional[str]

    class Config:
        orm_mode = True


class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    avatar: str = None

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    email: EmailStr