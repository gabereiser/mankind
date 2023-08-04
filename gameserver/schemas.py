from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class ItemBase(BaseModel):
    name: str
    symbol: str
    description: str
    natural: bool
    size: float
    weight: float


class ItemCreate(ItemBase):
    pass


class ItemUpdate(ItemBase):
    pass


class Item(ItemBase):
    id: UUID

    class Config:
        orm_mode = True


class ShipBase(BaseModel):
    name: str
    ship_class: str
    hp: float  # hull-points
    ap: float  # armor-points
    sp: float  # shield-points
    fp: float  # fuel-points
    cs: float  # current-speed
    ws: float  # warp-speed
    x: float
    y: float
    z: float
    dx: float
    dy: float
    dz: float


class ShipCreate(ShipBase):
    pass


class ShipUpdate(ShipBase):
    pass


class Ship(ShipBase):
    id: UUID
    owner_id: UUID | None = None
    company_id: UUID | None = None
    location_id: UUID | None = None
    system_id: UUID
    max_hp: float
    max_ap: float
    max_sp: float
    max_ws: float
    max_cs: float
    cargo: dict[Item, int]
    maxcargo: int
    maxtonnage: int
    fittings: dict[str, list[Item]] = {}  # keys: 'high' 'mid' 'low'

    class Config:
        orm_mode = True


class StarSystemBase(BaseModel):
    name: str
    star_class: str


class StarSystemCreate(StarSystemBase):
    pass


class StarSystem(StarSystemBase):
    id: UUID
    x: float
    y: float
    z: float

    class Config:
        orm_mode = True


class CharacterBase(BaseModel):
    name: str
    created: datetime


class Character(CharacterBase):
    id: UUID
    account_id: UUID

    class Config:
        orm_mode = True


class AccountBase(BaseModel):
    username: str
    email: str
    created: datetime


class AccountUpdate(AccountBase):
    password: str | None = None


class AccountCreate(AccountBase):
    password: str


class AccountDelete(AccountBase):
    pass


class Account(AccountBase):
    id: UUID
    banned: bool
    banned_until: datetime
    characters: list[Character] = []

    class Config:
        orm_mode = True
