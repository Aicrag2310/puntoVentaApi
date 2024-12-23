from sqlalchemy.orm import Session
from punto_venta_app.orm import Category
from punto_venta_app.models.categoriesModel import CategoriesFormRequestData, CategoriesUpdateFormRequestData
import bcrypt
from punto_venta_app.models import AppGenericException
from datetime import datetime


def create_categories_from_request_data(db: Session, request_data: CategoriesFormRequestData) -> Category:

    register = Category()
    register.name = request_data.name or None
    register.description = request_data.description or None
    register.isActive = 1

    db.add(register)
    db.commit()
    
    return register

def update_categories_from_request_data(db: Session, request_data: CategoriesUpdateFormRequestData, category_id: int) -> Category:
    category = db.query(Category).filter(Category.id == category_id).first()

    if not category:
        raise AppGenericException(1, 'No se encontró ningúna categoria', 404)

    if request_data.name is not None:
        category.name = request_data.name 
    
    if request_data.description is not None:
        category.description = request_data.description
    
    category.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(category)
    return category