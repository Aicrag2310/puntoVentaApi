from sqlalchemy.orm import Session
from punto_venta_app.orm import User, Role
from punto_venta_app.models.userModel import UserFormRequestData, UserFormRequestEditData
import bcrypt
from punto_venta_app.models import AppGenericException
from datetime import datetime


def create_user_from_request_data(db: Session, request_data: UserFormRequestData) -> User:
    role: Role = db.get(Role, request_data.role_id)

    salt = bcrypt.gensalt()
    byte_pswd = request_data.password.encode('utf-8')

    register = User()
    register.username = request_data.username or None
    register.email = request_data.email or None
    register.phone_number = request_data.phoneNumber or None
    register.firstname = request_data.firstName
    register.lastName = request_data.lastName
    register.password = bcrypt.hashpw(byte_pswd, salt)
    register.isActive = 1

    register.roles.append(role)

    db.add(register)
    db.commit()
    
    return register

def update_user_from_request_data(db: Session, request_data: UserFormRequestEditData, user_id: int) -> User:
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise AppGenericException(1, 'No se encontró ningún usuario', 404)

    if request_data.username is not None:
        user.username = request_data.username 
    
    if request_data.email is not None:
        user.email = request_data.email
    if request_data.phoneNumber is not None:
        user.phone_number = request_data.phoneNumber
    if request_data.firstName is not None:
        user.firstname = request_data.firstName
    if request_data.lastName is not None:
        user.lastName = request_data.lastName
    if request_data.password is not None:
        salt = bcrypt.gensalt()
        user.password = bcrypt.hashpw(request_data.password.encode('utf-8'), salt)

    if request_data.role_id is not None:
        role = db.get(Role, request_data.role_id)
        if not role:
            raise AppGenericException(2, 'No se encontró ningún rol', 404)
        user.roles.clear()
        user.roles.append(role)
    
    user.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(user)
    return user