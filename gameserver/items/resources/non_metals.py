from ..base.item import item, ItemBase


@item("Na")
class Sodium(ItemBase):
    name = "Sodium"
    description = "Sodium is a resource found in saline liquids."
    symbol = "Na"
    natural = True
    volume = 0.1
    weight = 0.2


@item("Si")
class Silicone(ItemBase):
    name = "Silicone"
    description = "Silicone is used in electronics, medical devices, and ceramics."
    symbol = "Si"
    natural = True
    volume = 0.1
    weight = 0.2
