from ..base.item import item, ItemBase


@item(
    id=100,
    name="Iron",
    description="Iron is a solid metal refined from Pyrite.",
    symbol="Fe",
    natural=True,
    volume=0.1,
    weight=1.2,
)
class Iron(ItemBase):
    pass


@item(
    id=101,
    name="Copper",
    description="Copper is a solid metal refined from Malachite.",
    symbol="Cu",
    natural=True,
    volume=0.1,
    weight=1.2,
)
class Copper(ItemBase):
    pass


@item(
    id=102,
    name="Aluminium",
    description="Aluminium is a soft-solid metal refined from Kamacite.",
    symbol="Al",
    natural=True,
    volume=0.1,
    weight=0.6,
)
class Aluminum(ItemBase):
    pass
