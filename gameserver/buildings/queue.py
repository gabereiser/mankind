from typing import List
from .recipe import Recipe


class ProductionQueue:
    current_recipe: Recipe
    backlog: List[Recipe]
