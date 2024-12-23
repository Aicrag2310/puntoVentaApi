from pydantic import BaseModel, Field
from typing import List, Optional

# Modelo para cada artículo del carrito
class CartItem(BaseModel):
    id: int
    quantity: int
    total: float
    sale_type: int

# Modelo para el pago
class Payment(BaseModel):
    paymentMethod: str
    total: float
    payments: List[Optional[float]] = []

# Modelo principal para la solicitud de venta
class SalesFormRequest(BaseModel):
    cart: List[CartItem]
    payment: Payment
