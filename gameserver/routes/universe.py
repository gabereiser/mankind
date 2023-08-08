from typing import Annotated
from fastapi import APIRouter, Depends
from uuid import UUID
import auth
import database
import schemas

router = APIRouter(
    prefix="/api/v1/universe",
    tags=["universe"],
    dependencies=[Depends(auth.get_current_active_user)],
)


@router.get("/starsystems")
async def list_starsystems(
    current_user: Annotated[schemas.Account, Depends(auth.get_current_active_user)],
    page: int = 0,
    limit: int = 50,
):
    return await database.get_starsystems(next(database.session()), page, limit)


@router.get("/starsystems/{id}")
async def get_starsystem(
    current_user: Annotated[schemas.Account, Depends(auth.get_current_active_user)],
    id: UUID,
):
    return await database.get_starsystem(next(database.session()), id)


@router.get("/starsystems/{id}/ships")
async def get_ships_in_system(id: UUID):
    return await database.get_ships_in_system(next(database.session()), id)
