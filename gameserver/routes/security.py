from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta

from auth import (
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
import database
from schemas import Token

router = APIRouter(prefix="/api/v1/auth")


@router.post("/token", response_model=Token, tags=["security"])
async def oauth2_login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await database.authenticate_user(
        next(database.session()), form_data.username, form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    response = JSONResponse(
        content={"access_token": access_token, "token_type": "bearer"}
    )
    exp = datetime.utcnow() + timedelta(days=30)
    response.set_cookie(key="_auth", value=access_token, expires=exp.ctime())
    return response
