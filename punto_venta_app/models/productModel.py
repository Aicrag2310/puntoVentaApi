from pydantic import BaseModel
from typing import Optional


class ProductFormRequestData(BaseModel):
    name: str
    description: str
    purchase_price: float
    retail_price: float
    wholesale_price: float
    stock: int
    min_stock: int
    isActive: Optional[int] = 1
    category: int

class ProductUpdateFormRequestData(BaseModel):
    name: Optional[str]
    description: Optional[str]
    purchase_price: Optional[float]
    retail_price: Optional[float]
    wholesale_price: Optional[float]
    stock: Optional[int]
    min_stock: Optional[int]
    category: Optional[int]

class ProductTableItem(BaseModel):
    id: int
    name: str
    description: str
    retail_price: float
    wholesale_price: float
    purchase_price: float
    stock: int
    min_stock: int
    max_stock: int
    categoryId: int
    category: str
