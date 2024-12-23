from fastapi import APIRouter, Header, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from punto_venta_app import ValidationError
from punto_venta_app.database import get_db
from punto_venta_app.models.salesModel import SalesFormRequest
import punto_venta_app.processes.usersProcesses as processes
from punto_venta_app.orm import Sale, SaleDetail, Product
from punto_venta_app.models import AppGenericException
from punto_venta_app.security import get_token_user
from datetime import datetime


router = APIRouter()

@router.post("/api/sales")
def create_sale(
    request: SalesFormRequest,
    jwt_payload: dict = Depends(get_token_user),
    db: Session = Depends(get_db)
):
    userId = jwt_payload.get('identity')
    paymentMethod = ''
    if request.payment.paymentMethod == 0 or request.payment.paymentMethod == '0' :
        paymentMethod = 'Efectivo'

    try:
        new_sale = Sale(
            total=request.payment.total,
            payment_method=paymentMethod,
            user_id = userId
        )
        
        db.add(new_sale)
        db.commit()
        db.refresh(new_sale)
        for item in request.cart:
            unit_price = 0
            product = db.query(Product).filter(Product.id == item.id).first()
            if item.sale_type == 0:
                unit_price = product.retail_price
            if item.sale_type == 1:
                unit_price = product.wholesale_price
            sale_detail = SaleDetail(
                sale_id=new_sale.id,
                product_id=item.id,
                quantity=item.quantity,
                unit_price = unit_price,
                sale_type = item.sale_type,
                subtotal=item.total,
            )
            db.add(sale_detail)
        
        db.commit()
        
        return {"message": "Venta creada con éxito", "sale_id": new_sale.id}
    
    except Exception as e:
        print ('Error')
        print (e)
        db.rollback()
        raise AppGenericException(5, e, 404)
