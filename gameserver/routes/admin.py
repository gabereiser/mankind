from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
import auth
import schemas
import database

router = APIRouter(
    prefix="/api/v1/admin",
    tags=["admin"],
    dependencies=[Depends(auth.get_current_active_user)],
)


@router.get("/")
async def display_admin_dashboard(
    current_user: Annotated[schemas.Account, Depends(auth.get_current_active_user)]
):
    admin_user = database.get_account_by_username(
        next(database.session()), current_user.username
    )
    if admin_user.priv < 2:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Bearer"},
        )
    with open("admin/index.html", "r") as fp:
        html = fp.read()
        fp.close()
        return HTMLResponse(html)
