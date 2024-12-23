from fastapi import APIRouter, Header, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from punto_venta_app import ValidationError
from punto_venta_app.database import get_db
from punto_venta_app.models.categoriesModel import CategoriesFormRequestData, CategoriesUpdateFormRequestData
import punto_venta_app.processes.categoriesProcesses as processes
from punto_venta_app.orm import Category
from punto_venta_app.models import AppGenericException

router = APIRouter()

@router.post('/api/categories')
def create_categories(request_data: CategoriesFormRequestData,
                    accept_languaje: str = Header(default='en'),
                    db: Session = Depends(get_db)):
    
    new_register = processes.create_categories_from_request_data(db, request_data)

    return {'message': 'Register created successfully ', 'id ': new_register.id}

@router.put('/api/categories/{category_id}')
def update_categories(request_data: CategoriesUpdateFormRequestData,
                category_id: int,
                accept_languaje: str = Header(default='en'),
                    db: Session = Depends(get_db)):
    
    update_user = processes.update_categories_from_request_data(db, request_data, category_id)
    return {'Message ': 'Producto actualizado correctamente'}

@router.delete('/api/categories/{category_id}')
def delete_categories(category_id: int,
                accept_languaje: str = Header(default='en'),
                    db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()

    if not category:
        raise AppGenericException(1, 'No se encontró ningúna categoria', 404)
    
    category.isActive = 0

    db.commit()
    db.refresh(category)

    return {'Message': 'Categoria eliminada correctamente'}

@router.get('/api/categories/autocomplete')
def category_autocomplete(accept_languaje: str = Header(default='en'),
                    db: Session = Depends(get_db)):
    
    category = db.query(Category).filter(Category.isActive == 1).all()

    if not category:
        raise AppGenericException(1, 'No se encontró ningúna categoria', 404)

    return {'data': category}