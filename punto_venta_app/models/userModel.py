from pydantic import BaseModel
from typing import Optional


class UserFormRequestData(BaseModel):
    username: Optional[str]
    email: Optional[str]
    phoneNumber: Optional[str]
    firstName: str
    lastName: Optional[str]
    password: Optional[str]
    role_id: Optional[int] = 1

class UserFormRequestEditData(BaseModel):
    username: Optional[str]
    email: Optional[str]
    phoneNumber: Optional[str]
    firstName: Optional[str]
    lastName: Optional[str]
    password: Optional[str]
    role_id: Optional[int] = 1