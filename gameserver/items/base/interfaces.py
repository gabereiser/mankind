from items.base.item import ItemBase


class Refineable:
    def refine() -> list[ItemBase]:
        return list()


class Fittable:
    def fit() -> None:
        pass
