from sqlalchemy.orm import Session
from punto_venta_app.orm import User, Role
from punto_venta_app.models.userModel import UserFormRequestData
import bcrypt


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