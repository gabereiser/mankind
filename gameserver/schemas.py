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
        from_attributes = True


class Inventory(BaseModel):
    id: UUID
    items: list[Item] = []


class ShipBase(BaseModel):
    name: str


class ShipCreate(ShipBase):
    pass


class ShipUpdate(ShipBase):
    ds: float  # desired-speed
    dx: float
    dy: float
    dz: float
    pass


class ShipPosition(ShipBase):
    id: UUID
    owner_id: UUID | None = None
    company_id: UUID | None = None
    x: float
    y: float
    z: float
    cs: float
    ds: float  # desired-speed
    dx: float
    dy: float
    dz: float


class Ship(ShipBase):
    id: UUID
    owner_id: UUID | None = None
    company_id: UUID | None = None
    location_id: UUID | None = None
    system_id: UUID
    ship_class: str
    hp: float  # hull-points
    ap: float  # armor-points
    sp: float  # shield-points
    ep: float  # energy-points
    rr: float  # recharge rate
    cs: float  # current-speed

    ws: float  # warp-speed
    ds: float  # desired-speed
    dx: float  # -,
    dy: float  # -|- The forward-normalized (lookat) vector
    dz: float  # -'
    x: float  # -,
    y: float  # -|- The position vector
    z: float  # -'
    max_hp: float
    max_ap: float
    max_sp: float
    max_ep: float
    max_rr: float
    max_ws: float
    max_cs: float
    inventory: Inventory
    maxcargo: int
    maxtonnage: int
    modules: dict[str, list[Item]] = {}  # keys: 'high' 'mid' 'low'

    class Config:
        from_attributes = True


class StarSystemBase(BaseModel):
    name: str
    classification: str


class StarSystem(StarSystemBase):
    id: UUID
    x: float
    y: float
    z: float

    class Config:
        from_attributes = True


class OrbitalBody(BaseModel):
    id: UUID
    system_id: UUID
    parent_id: UUID | None = None
    name: str
    otype: int
    stype: int
    axis: float
    eccentricity: float
    inclination: float
    rings: int
    population: int
    pressure: float
    temperature: float
    gravity: float
    fertility: float

    class Config:
        from_attributes = True


OrbitalBody.children: list[OrbitalBody] = []


class LedgerTransactionBase(BaseModel):
    amount: float
    desc: str


class LedgerTransactionCreate(LedgerTransactionBase):
    payer: UUID | None = None
    payer_type: str = "S"


class LedgerTransaction(LedgerTransactionBase):
    date: datetime
    payer: UUID | None = None
    payer_type: str = "S"
    ledger: UUID

    class Config:
        from_attributes = True


class LedgerBase(BaseModel):
    pass


class Ledger(LedgerBase):
    id: UUID
    transactions: list[LedgerTransaction] = []

    class Config:
        from_attributes = True

class CandleStick(BaseModel):
    symbol: str
    timestamp: datetime
    open_v: float
    close_v: float
    high_v: float
    low_v: float
    volume: int

class CharacterBase(BaseModel):
    name: str


class CharacterCreate(CharacterBase):
    pass


class Character(CharacterBase):
    id: UUID
    created: datetime
    account_id: str
    last_online: str
    ships: list = []
    market_orders: list = []
    market_order_transactions: list = []
    ledger: Ledger

    class Config:
        from_attributes = True


class AccountBase(BaseModel):
    username: str
    email: str


class AccountUpdate(AccountBase):
    password: str | None = None


class AccountCreate(AccountBase):
    password: str


class Account(AccountBase):
    id: UUID
    created: datetime
    banned: bool = False
    banned_until: datetime | None = None

    class Config:
        from_attributes = True
