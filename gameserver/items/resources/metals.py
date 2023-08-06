from ..base.item import item, ItemBase


@item("Fe")
class Iron(ItemBase):
    name = "Iron"
    description = "Iron is a solid metal used in many applications and industries."
    symbol = "Fe"
    natural = True
    volume = 0.1
    weight = 1.2


@item("Cu")
class Copper(ItemBase):
    name = "Copper"
    description = "Copper is a solid metal used for electronics and heavy equipment."
    symbol = "Cu"
    natural = True
    volume = 0.1
    weight = 1.2


@item("Al")
class Aluminum(ItemBase):
    name = "Aluminium"
    description = (
        "Aluminium is a soft-solid metal used in ship and building construction."
    )
    symbol = "Al"
    natural = True
    volume = 0.1
    weight = 0.6


@item("Au")
class Gold(ItemBase):
    name = "Gold"
    description = "Gold is a soft-solid metal used in electronics and fine jewelry."
    symbol = "Al"
    natural = True
    volume = 0.1
    weight = 0.6


@item("Ti")
class Titanium(ItemBase):
    name = "Titanium"
    description = "Titanium is a hard metal used in structural projects and ship hulls."
    symbol = "Al"
    natural = True
    volume = 0.1
    weight = 0.6
