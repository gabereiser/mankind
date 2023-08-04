from items.base.interfaces import Refineable
from ..base.item import ItemBase, item, ITEMS


@item(
    id=0,
    name="Helium",
    description="Helium is a gas found in some atmosphers of planets and moons.",
    symbol="He",
    natural=True,
    volume=0.1,
    weight=0.01,
)
class Helium(ItemBase):
    pass


@item(
    id=1,
    name="Oxygen",
    description="Oxygen is a gas found in some atmospheres of planets and moons.",
    symbol="O",
    natural=True,
    volume=0.1,
    weight=0.05,
)
class Oxygen(ItemBase):
    pass


@item(
    id=2,
    name="Pyrite",
    description="Pyrite is an iron-rich mineral found on some planets and moons.",
    symbol="Fe.01",
    natural=True,
    volume=1,
    weight=1.75,
)
class Pyrite(ItemBase, Refineable):
    def refine() -> list[ItemBase]:
        iron = ITEMS.get(100)
        iron.count = 150
        ret = list()
        ret.append(iron)
        return ret


@item(
    id=3,
    name="Malachite",
    description="Malachite is an copper-rich mineral found on some planets and moons.",
    symbol="Cu.01",
    natural=True,
    volume=1,
    weight=2.05,
)
class Malachite(ItemBase, Refineable):
    def refine() -> list[ItemBase]:
        copper = ITEMS.get(101)
        copper.count = 50
        ret = list()
        ret.append(copper)
        return ret


@item(
    id=4,
    name="Rock Salt",
    description="Rock Salt is an sodium-rich mineral found on some planets and moons.",
    symbol="Na.01",
    natural=True,
    volume=1,
    weight=1.05,
)
class Malachite(ItemBase, Refineable):
    def refine() -> list[ItemBase]:
        sodium = ITEMS.get(200)
        sodium.count = 15
        ret = list()
        ret.append(sodium)
        return ret
