from items.base.interfaces import Refineable
from ..base.item import ItemBase, item, ITEMS
import random


@item("N")
class Nitrogen(ItemBase):
    name = "Nitrogen"
    description = "Nitrogen is a gas found in some atmospheres of planets and moons."
    symbol = "N"
    natural = True
    volume = 0.08
    weight = 0.05


@item("H")
class Hydrogen(ItemBase):
    name = "Hydrogen"
    description = "Hydrogen is a gas found in some atmospheres of planets and moons."
    symbol = "H"
    natural = True
    volume = 0.1
    weight = 0.09


@item("He")
class Helium(ItemBase):
    name = "Helium"
    description = "Helium is a gas found in some atmospheres of planets and moons."
    symbol = "He"
    natural = True
    volume = 0.1
    weight = 0.01


@item("O")
class Oxygen(ItemBase):
    name = "Oxygen"
    description = "Oxygen is a gas found in some atmospheres of planets and moons."
    symbol = "O"
    natural = True
    volume = 0.1
    weight = 0.05


@item("H2O")
class Water(ItemBase):
    name = "Drinking Water"
    description = "Drinking Water is a liquid found on some planets and moons. It may contain NaCL."
    symbol = "H2O"
    natural = True
    volume = 0.5
    weight = 1.0


@item("NaCL")
class Salt(ItemBase, Refineable):
    name = "Salt"
    description = "Salt is commonly found on Temperate and Rock planets and moons in sea water and within rocks as rock salt. It can also be distilled from H2O in a distillery."
    symbol = "NaCL"
    natural = True
    volume = 0.2
    weight = 0.01


@item("Fe.Ore")
class IronOre(ItemBase, Refineable):
    name = "Iron Ore"
    description = "Iron Ore is found on some planets and moons."
    symbol = "Fe.Ore"
    natural = True
    volume = 1
    weight = 1.75


@item("SiO2")
class Silica(ItemBase, Refineable):
    name = "Silica"
    description = "Silica is found on some planets and moons."
    symbol = "SiO2"
    natural = True
    volume = 1
    weight = 0.9


@item("Cu.Ore")
class CopperOre(ItemBase, Refineable):
    name = "Copper Ore"
    description = "Copper Ore is found on some planets and moons."
    symbol = "Cu.Ore"
    natural = True
    volume = 1
    weight = 2.05


@item("Al.Ore")
class AluminumOre(ItemBase, Refineable):
    name = "Aluminum Ore"
    description = "Aluminum Ore is found on some planets and moons."
    symbol = "Al.Ore"
    natural = True
    volume = 1
    weight = 1.05


@item("Au.Ore")
class GoldOre(ItemBase, Refineable):
    name = "Gold Ore"
    description = "Gold Ore is found on some planets and moons."
    symbol = "Au.Ore"
    natural = True
    volume = 0.5
    weight = 1.05


@item("Ti.Ore")
class TitaniumOre(ItemBase, Refineable):
    name = "Titanium Ore"
    description = "Titanium Ore is found on some planets and moons."
    symbol = "Ti.Ore"
    natural = True
    volume = 1
    weight = 1.9


@item("U.Ore")
class UraniumOre(ItemBase, Refineable):
    name = "Uranium Ore"
    description = "Uranium Ore is found on some planets and moons."
    symbol = "U.Ore"
    natural = True
    volume = 1
    weight = 1.4


@item("Corn")
class Corn(ItemBase, Refineable):
    name = "Corn"
    description = "Corn has become one of the few crops left after the blight of 2351. Genetically engineered to survive and grow in mid-high atmospheric pressures and temperatures."
    symbol = "Corn"
    natural = True
    volume = 0.8
    weight = 0.4


@item("Wheat")
class Corn(ItemBase, Refineable):
    name = "Wheat"
    description = "Wheat has become one of the few crops left after the blight of 2351. Genetically engineered to survive and grow in low-mid atmospheric pressures and temperatures."
    symbol = "Wheat"
    natural = True
    volume = 0.8
    weight = 0.4
