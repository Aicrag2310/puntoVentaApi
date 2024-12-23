from pydantic import BaseModel
from typing import Optional


class CategoriesFormRequestData(BaseModel):
    name: str
    description: str

class CategoriesUpdateFormRequestData(BaseModel):
    name: Optional[str]
    description: Optional[str]