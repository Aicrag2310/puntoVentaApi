from fastapi import APIRouter, Header, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from punto_venta_app import ValidationError
from punto_venta_app.database import get_db
from punto_venta_app.models.productModel import ProductFormRequestData, ProductUpdateFormRequestData
import punto_venta_app.processes.productProcesses as processes
from punto_venta_app.orm import Product
from punto_venta_app.models import AppGenericException
from sqlalchemy import func

router = APIRouter()

@router.post('/api/product')
def create_product(request_data: ProductFormRequestData,
                    accept_languaje: str = Header(default='en'),
                    db: Session = Depends(get_db)):
    
    new_register = processes.create_product_from_request_data(db, request_data)

    return {'message': 'Register created successfully ', 'id ': new_register.id}


@router.get('/api/product/autocomplete')
def get_product_autocomplete(db: Session = Depends(get_db)):
    
    products = db.query(Product).filter(Product.isActive == 1).all()

    data = [
        processes.make_products_table_item_from_register(product)
        for product in products
    ]

    return data

@router.put('/api/product/{product_id}')
def update_product(request_data: ProductUpdateFormRequestData,
                product_id: int,
                accept_languaje: str = Header(default='en'),
                    db: Session = Depends(get_db)):
    update_user = processes.update_product_from_request_data(db, request_data, product_id)
    return {'Message ': 'Producto actualizado correctamente'}

@router.delete('/api/product/{product_id}')
def delete_product(product_id: int,
                accept_languaje: str = Header(default='en'),
                    db: Session = Depends(get_db)):
    user = db.query(Product).filter(Product.id == product_id).first()

    if not user:
        raise AppGenericException(1, 'No se encontró ningún producto', 404)
    
    user.isActive = 0

    db.commit()
    db.refresh(user)

    return {'Message': 'Producto eliminado correctamente'}

@router.get('/api/product/table/data')
def get_product_table(limit: Optional[int] = Query(default=10),
                      query: str = '',
                                   offset: Optional[int] = Query(default=0),
                           db: Session = Depends(get_db)):
    
    products = processes.create_items_for_table(db, limit, offset, query)

    data = [
        processes.make_products_table_item_from_register(product)
        for product in products
    ]

    return data

@router.get('/api/product/table/count')
def get_product_table(query: str = '',
                      db: Session = Depends(get_db)):
    search_query = query
    query = db.query(func.count(Product.id))
    query = query.filter(Product.isActive == 1)

    '''if search_query:
        # Split the search query into individual words
        search_words = search_query.split()

        # Create many list of statements for each word in the search query
        name_stmts = []
        model_stmts = []
        description_stmts = []
        barcode_stmts = []
        for word in search_words:
            name_stmts.append(Product.name.like(f'%{word}%'))
            model_stmts.append(Product.model.like(f'%{word}%'))
            description_stmts.append(Product.description.like(f'%{word}%'))
            barcode_stmts.append(Product.barcode.like(f'%{word}%'))

        # Combine the `like` statements using the `or_` operator on each query field
        query = query.where(or_(
            and_(*name_stmts),
            and_(*model_stmts),
            and_(*description_stmts),
            and_(*barcode_stmts),
        ))'''

    if search_query != '':
        palabras = search_query.split(' ')
        filters = [
            Product.name.op('REGEXP')(rf'(?i)(?=.*{palabra}).*') |
            Product.description.op('REGEXP')(rf'(?i)(?=.*{palabra}).*')             
            for palabra in palabras
        ]
        query = query.filter(*filters)

    count = query.scalar()
    return {'count': count}

@router.get('/api/product/{product_id}')
def get_product_by_id(product_id: int,
                      accept_languaje: str = Header(default='en'),
                    db: Session = Depends(get_db)):
    
    product = db.query(Product).filter(Product.id == product_id, Product.isActive == 1).first()
    
    if not product:
        raise AppGenericException(2, 'No se encontró ningún producto', 404)
    
    data = [processes.make_products_table_item_from_register(product)]
    
    return data
