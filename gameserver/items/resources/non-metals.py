from ..base.item import item, ItemBase


@item(
    id=200,
    name="Sodium",
    description="Sodium is a resource found in saline liquids.",
    symbol="Na",
    natural=True,
    volume=0.1,
    weight=0.2,
)
class Sodium(ItemBase):
    pass
