from typing import Annotated
from fastapi import APIRouter, Depends
import auth
import schemas
import database

router = APIRouter(
    prefix="/api/v1/account",
    tags=["account"],
    dependencies=[Depends(auth.get_current_active_user)],
)


@router.get("/me")
async def get_my_account(
    current_user: Annotated[schemas.Account, Depends(auth.get_current_active_user)]
):
    return current_user


@router.get("/me/characters")
async def list_characters(
    current_user: Annotated[schemas.Account, Depends(auth.get_current_active_user)]
):
    account = await database.get_account_by_username(
        next(database.session()), current_user.username
    )
    return account.characters


@router.post("/me/characters/create")
async def create_character(
    current_user: Annotated[schemas.Account, Depends(auth.get_current_active_user)],
    create_char: schemas.CharacterCreate,
):
    character = await database.create_character(
        next(database.session()), current_user, create_char
    )
    return character
