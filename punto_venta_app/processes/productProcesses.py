from sqlalchemy.orm import Session
from punto_venta_app.orm import Product
from punto_venta_app.models.productModel import ProductFormRequestData, ProductUpdateFormRequestData, ProductTableItem
import bcrypt
from punto_venta_app.models import AppGenericException
from datetime import datetime
from typing import Optional
from sqlalchemy import func

def create_product_from_request_data(db: Session, request_data: ProductFormRequestData) -> Product:

    register = Product()
    register.name = request_data.name or None
    register.description = request_data.description or None
    register.purchase_price = request_data.purchase_price or None
    register.retail_price = request_data.retail_price
    register.wholesale_price = request_data.wholesale_price
    register.min_stock = request_data.min_stock
    register.stock = request_data.stock
    register.isActive = 1
    register.category_id = request_data.category


    db.add(register)
    db.commit()
    
    return register

def update_product_from_request_data(db: Session, request_data: ProductUpdateFormRequestData, product_id: int) -> Product:
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise AppGenericException(1, 'No se encontró ningún producto', 404)

    if request_data.name is not None:
        product.name = request_data.name 
    
    if request_data.description is not None:
        product.description = request_data.description

    if request_data.purchase_price is not None:
        product.purchase_price = float(request_data.purchase_price)

    if request_data.retail_price is not None:
        product.retail_price = float(request_data.retail_price)

    if request_data.wholesale_price is not None:
        product.wholesale_price = float(request_data.wholesale_price)
    
    if request_data.stock is not None:
        product.stock = request_data.stock

    if request_data.min_stock is not None:
        product.min_stock = request_data.min_stock

    if request_data.category is not None:
        product.category_id = request_data.category
    
    product.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(product)
    return product


def create_items_for_table(db: Session, limit: Optional[int], offset: Optional[int], search_query=None):

    query = db.query(Product).filter(Product.isActive == 1)

    if search_query != '':
        palabras = search_query.split(' ')
        filters = [
            Product.name.op('REGEXP')(rf'(?i)(?=.*{palabra}).*') |
            Product.description.op('REGEXP')(rf'(?i)(?=.*{palabra}).*')
            for palabra in palabras
        ]
        query = query.filter(*filters)
    
    query = query.order_by(func.length(Product.id))
    query = query.limit(limit).offset(offset)

    return query.all()

def make_products_table_item_from_register(product: Product) -> ProductTableItem:
    return ProductTableItem(**{
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'retail_price': product.retail_price,
        'wholesale_price': product.wholesale_price,
        'purchase_price': product.purchase_price,
        'stock': product.stock,
        'min_stock': product.min_stock,
        'max_stock': product.max_stock,
        'categoryId': product.category_id,
        'category': product.category.name,
    })