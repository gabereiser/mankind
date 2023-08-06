from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class RpcMessage(Any):
    pass


class RpcRequest(RpcMessage):
    c: str
    d: RpcMessage

    def __init__(self, cmd: str, *args, **kwargs):
        self.c = cmd
        self.d = RpcMessage(*args, **kwargs)


class RpcResponse(RpcMessage):
    s: str
    t: datetime
    d: RpcMessage

    def __init__(self, cmd: str, timestamp: datetime, *args, **kwargs):
        self.s = cmd
        self.t = timestamp
        self.d = RpcMessage(*args, **kwargs)
