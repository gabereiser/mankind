import os
from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2AuthorizationCodeBearer
from jose import JWTError, jwt

import schemas
import database as db
import config as configuration

config = configuration.get_config()
SECRET_KEY = config.secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")
oauth2_client_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="/api/v1/auth/authorize",
    tokenUrl="/api/v1/auth/token",
    refreshUrl="/api/v1/auth/refresh",
)


async def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await db.get_account_by_username(
        next(db.session()), username=token_data.username
    )
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[schemas.Account, Depends(get_current_user)]
):
    if current_user.banned and (current_user.banned_until > datetime.utcnow()):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Banned")
    return current_user


async def get_current_super_user(
    current_user: Annotated[schemas.Account, Depends(get_current_active_user)]
):
    if current_user.priv < 1:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Insufficient permissions"
        )
    return current_user


async def get_current_admin_user(
    current_user: Annotated[schemas.Account, Depends(get_current_active_user)]
):
    if current_user.priv < 2:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Insufficient permissions"
        )
    return current_user


async def add_security_check(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Sec-Hash"] = request.client.host
    return response
