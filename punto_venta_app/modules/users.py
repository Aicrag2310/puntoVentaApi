from fastapi import APIRouter, Header, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from punto_venta_app import ValidationError
from punto_venta_app.database import get_db
from punto_venta_app.models.userModel import UserFormRequestData
import punto_venta_app.processes.usersProcesses as processes

router = APIRouter()

@router.post('/api/user')
def create_register(request_data: UserFormRequestData,
                    accept_languaje: str = Header(default='en'),
                    db: Session = Depends(get_db)):
    
    new_register = processes.create_user_from_request_data(db, request_data)

    return {'message': 'Register created successfully ', 'id ': new_register.id}