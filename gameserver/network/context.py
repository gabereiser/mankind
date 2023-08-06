from fastapi.websockets import WebSocket
from .client import Client


class Context:
    client: Client

    def __init__(self, socket: WebSocket) -> None:
        self.client = Client(socket)

    async def run() -> None:
        pass

    async def send(self, data: any) -> None:
        await self.client.send(data)

    async def recv(self) -> any:
        await self.client.recv()
