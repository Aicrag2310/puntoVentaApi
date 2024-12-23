from fastapi import APIRouter, Header, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from punto_venta_app import ValidationError
from punto_venta_app.database import get_db
from punto_venta_app.models.userModel import UserFormRequestData, UserFormRequestEditData
import punto_venta_app.processes.usersProcesses as processes
from punto_venta_app.orm import User
from punto_venta_app.models import AppGenericException


router = APIRouter()

@router.post('/api/user')
def create_register(request_data: UserFormRequestData,
                    accept_languaje: str = Header(default='en'),
                    db: Session = Depends(get_db)):
    
    new_register = processes.create_user_from_request_data(db, request_data)

    return {'message': 'Register created successfully ', 'id ': new_register.id}

@router.put('/api/user/{user_id}')
def update_user(request_data: UserFormRequestEditData,
                user_id: int,
                accept_languaje: str = Header(default='en'),
                    db: Session = Depends(get_db)):
    
    update_user = processes.update_user_from_request_data(db, request_data, user_id)
    return {'Message ': 'Usuario actualizado correctamente'}

@router.delete('/api/user/{user_id}')
def delete_user(user_id: int,
                accept_languaje: str = Header(default='en'),
                    db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise AppGenericException(1, 'No se encontró ningún usuario', 404)
    
    user.isActive = 0

    db.commit()
    db.refresh(user)

    return {'Message': 'Usuario eliminado correctamente'}