from fastapi.websockets import WebSocket
from .client import Client
from commands import commands

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[Client] = []

    async def connect(self, websocket: WebSocket, user: any) -> Client:
        await websocket.accept()
        client = Client(websocket)
        client.user = user
        self.active_connections.append(client)
        return client
        
    async def handle(self, client: Client):
        data = await client.recv()
        cmd = await commands.get_command(data)
        await cmd.func(client, data)

    def disconnect(self, websocket: WebSocket):
        [self.active_connections.remove(x) for x in self.active_connections if x.socket == websocket]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: any):
        for connection in self.active_connections:
            await connection.send(message)
            
