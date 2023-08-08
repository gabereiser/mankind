from fastapi.staticfiles import StaticFiles
import uvicorn
from typing import Annotated
from fastapi import Depends, FastAPI, WebSocket, WebSocketDisconnect
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware
from schemas import Account
from network import server
from auth import get_current_active_user
import database
from routes import accounts, admin, public, universe, security
from items import *
import utils
import config as configuration

config = configuration.get_config()

app = FastAPI(title="Mankind API", version="0.1.0", debug=True)

app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=[f"{config.domain}", f"*.{config.domain}"]
)
app.include_router(security.router)
app.include_router(accounts.router)
app.include_router(universe.router)
app.include_router(public.router)
app.include_router(admin.router)


@app.get("/api/status", tags=["ops"])
async def root():
    return {"status": "ok"}


gameserver = server.ConnectionManager()


@app.websocket("/events")
async def websocket_endpoint(
    websocket: WebSocket,
    current_user: Annotated[Account, Depends(get_current_active_user)],
):
    client = await gameserver.connect(websocket, current_user)
    try:
        while True:
            await gameserver.handle(client)
    except WebSocketDisconnect:
        gameserver.disconnect(websocket)
        await gameserver.broadcast(f"Client #{client.id} left the chat")


@app.websocket("/rpc")
async def websocket_rpc(
    websocket: WebSocket,
    current_user: Annotated[Account, Depends(get_current_active_user)],
):
    socket: WebSocket = await websocket.accept("text")
    try:
        while True:
            request = socket.receive_json()
            socket.send_json(gameserver.rpc(current_user, request))
    except WebSocketDisconnect:
        pass


@app.on_event("startup")
async def startup():
    await database.bootstrap()


app.mount("/", StaticFiles(directory="public"), name="public")

if __name__ == "__main__":
    print(f"Server node: {utils.gen_key(64)}")
    uvicorn.run("service:app", host="0.0.0.0", port=8080)
