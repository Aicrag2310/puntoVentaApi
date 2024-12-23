#from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from starlette import status

#from database.orm.Aplicadores import User
#from models import TokenData
from punto_venta_app.settings import get_settings


# functions for token handling

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


#async def make_user_from_token_data(token_data: TokenData) -> User:
 #   return User(id=int(token_data.sub), email=token_data.email)


async def get_token_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    settings = get_settings()
    try:
        payload = jwt.decode(token, settings.secret, algorithms=[jwt.ALGORITHMS.HS256])
        username: str = payload.get("identity")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    return payload
