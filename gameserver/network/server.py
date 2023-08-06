from typing import List
from fastapi.websockets import WebSocket

from network.rpc import RpcRequest, RpcResponse
from .client import Client
from commands import commands
import schemas

__active_connections: List[Client] = []


class ConnectionManager:
    async def connect(self, websocket: WebSocket, user: any) -> Client:
        global __active_connections
        await websocket.accept()
        client = Client(websocket)
        client.user = user
        __active_connections.append(client)
        return client

    async def handle(self, client: Client):
        data = await client.recv()
        cmd = await commands.get_command(data)
        await cmd.func(client, data)

    def disconnect(self, websocket: WebSocket):
        global __active_connections
        [
            __active_connections.remove(x)
            for x in __active_connections
            if x.socket == websocket
        ]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: any):
        for connection in self.active_connections:
            await connection.send(message)

    async def rpc(
        self, current_user: schemas.Account, request: RpcRequest
    ) -> RpcResponse:
        pass
