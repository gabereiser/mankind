from ..base.item import ItemBase, item


@item("H2O.D")
class Distilled_Water(ItemBase):
    name = "Distilled Water"
    description = "Distilled water is purified H2O without salt."
    symbol = "H2O.D"
    natural = True
    volume = 0.5
    weight = 1.0
