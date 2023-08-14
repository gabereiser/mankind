from typing import Dict
import logging
from dataclasses import dataclass

ITEMS: Dict[str, any] = {}

logger = logging.getLogger("uvicorn")


def item(key: str):
    def boxed(klazz):
        if len(key) >= 8:
            raise Exception(f"item {key} has a symbol that is too long!")
        if key in ITEMS:
            raise Exception(f"item {key} already exists!")

        ITEMS[key] = klazz()
        print(f"Commodity: {key} has been added to the network.")
        return ITEMS[key]
        # returning inner function

    return boxed


@dataclass
class ItemBase:
    name: str = ""
    desc: str = ""
    symbol: str = ""
    category: str = ""
    weight: float = 1.0
    volume: float = 1.0
    natural: bool = False
    count: int = 1

    def clone_one(self):
        v = self(**self.__dict__.copy())
        v.count = 1
        return v

    def clone(self):
        return self(**self.__dict__.copy())

    def get_one(self):
        if self.count >= 1:
            self.count -= 1
            return self.clone_one()
        else:
            raise Exception(
                f"not enough #{self.name} in the stack to take one. #{self.count}"
            )

    def add_one(self, item):
        if isinstance(item, self.__class__):
            self.count += 1
            item = None
        else:
            raise Exception(
                f"#{item.name} is not #{self.name}, unable to add to stack."
            )

    def destroy(self):
        self.count = 0
