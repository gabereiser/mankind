from typing import List
from items.base.item import ItemBase


class Recipe:
    inputs: List[ItemBase] = []
    outputs: List[ItemBase] = []
