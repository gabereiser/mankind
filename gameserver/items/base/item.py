from typing import ClassVar
from uuid import UUID

from dataclasses import dataclass

ITEMS = {}


def item(
    id: int,
    name: str,
    description: str,
    symbol: str,
    natural: bool = False,
    volume: float = 1.0,
    weight: float = 1.0,
):
    def boxed(klazz):
        ITEMS[id] = klazz(
            oid=id,
            name=name,
            description=description,
            symbol=symbol,
            natural=natural,
            volume=volume,
            weight=weight,
        )
        return ITEMS[id]
        # returning inner function

    return boxed


@dataclass
class ItemBase:
    count: int = 1
