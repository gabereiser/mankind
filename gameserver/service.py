from fastapi.staticfiles import StaticFiles
import uvicorn
from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, WebSocket, WebSocketDisconnect, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse, JSONResponse
from schemas import Account, CharacterCreate, Token
from network import context, server
from auth import (
    create_access_token,
    get_current_active_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
import database

database.bootstrap()

app = FastAPI(title="Mankind API", version="0.1.0", debug=True)

@app.get("/")
async def index():
	with open("public/index.html", 'r') as fp:
		html = fp.read()
		fp.close()
		return HTMLResponse(html)
        
@app.get("/api/status")
async def root():
    return {"status": "ok"}


@app.post("/api/token", response_model=Token)
async def oauth2_login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = database.authenticate_user(next(database.session()), form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    response = JSONResponse(content={"access_token": access_token, "token_type": "bearer"})
    exp = (datetime.utcnow() + timedelta(days=30))
    response.set_cookie(key="_auth",
                        value=access_token,
                        expires=exp.ctime())
    return response


@app.get("/api/accounts/me/")
async def my_account_details(
    current_user: Annotated[Account, Depends(get_current_active_user)]
):
    return current_user


@app.get("/api/accounts/me/characters/")
async def list_characters(
    current_user: Annotated[Account, Depends(get_current_active_user)]
):
    account = database.get_account_by_username(next(database.session()), current_user.username)
    return account.characters

@app.get("/api/accounts/me/characters/create")
async def create_character(
    current_user: Annotated[Account, Depends(get_current_active_user)],
    create_char: CharacterCreate
):
    character = database.create_character(next(database.session()), create_character)
    return character


gameserver = server.ConnectionManager()
@app.websocket("/gameservice")
async def websocket_endpoint(websocket: WebSocket, current_user: Annotated[Account, Depends(get_current_active_user)]):
	client = await gameserver.connect(websocket, current_user)
	try:
		while True:
			await gameserver.handle(client)
	except WebSocketDisconnect:
		gameserver.disconnect(websocket)
		await gameserver.broadcast(f"Client #{client.id} left the chat")




app.mount("/", StaticFiles(directory="public"), name="public")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)