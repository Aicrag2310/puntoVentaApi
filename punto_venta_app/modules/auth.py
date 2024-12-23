import uuid
from datetime import datetime
from fastapi import APIRouter, Header, Depends
from jose import jwt
from jose.constants import ALGORITHMS
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from typing import List

from punto_venta_app import get_settings, AppGenericException
from punto_venta_app.database import get_db
from punto_venta_app.models.auth import AuthRequest
from punto_venta_app.orm import User


router = APIRouter()

pwd_context =  CryptContext(
    schemes=["bcrypt", "pbkdf2_sha256"],
    default="bcrypt",
)

@router.post('/api/auth')
def auth(request_data: AuthRequest,
         accept_language: str = Header(default='en'),
         db: Session = Depends(get_db)):
    
    config = get_settings()

    username = request_data.username
    password = request_data.password

    user = db.query(User).filter_by(username = username).first()

    if not user:
        raise AppGenericException(1, 'No se encontró ningún usuario', 404)
    
    if not pwd_context.verify(password, user.password):
        raise AppGenericException(2, 'Usuario o contraseña invalido', 404)
    
    now_seconds = int(datetime.now().timestamp())

    token = jwt.encode({
        'iat': now_seconds,
        'nbf': now_seconds,
        'jti': str(uuid.uuid4()),
        'identity': user.id,
        'fresh': False,
        'type': 'access'
    },config.secret, algorithm=ALGORITHMS.HS256)

    return {'token': token}
