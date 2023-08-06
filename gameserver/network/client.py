from fastapi.websockets import WebSocket


class Client:
    socket: WebSocket

    def __init__(self, socket: WebSocket) -> None:
        self.socket = socket

    async def send(self, data: any) -> None:
        return await self.socket.send_json(data)

    async def recv(self) -> any:
        return await self.socket.receive_json()
