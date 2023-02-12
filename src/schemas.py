from datetime import date
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
