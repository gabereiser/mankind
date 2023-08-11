from typing import List
from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    ForeignKeyConstraint,
    Integer,
    String,
    Uuid,
    Double,
    DateTime,
    JSON,
    Table,
    UniqueConstraint,
)
from sqlalchemy_mixins import AllFeaturesMixin
from sqlalchemy.orm import relationship, Mapped
from storage import Base

import uuid
import datetime


class Account(Base, AllFeaturesMixin):
    __tablename__ = "accounts"
    id = Column(Uuid, default=uuid.uuid4, primary_key=True, index=True)
    username = Column(String(32), unique=True, index=True)
    email = Column(String(64), unique=True, index=True)
    password = Column(String)
    created = Column(DateTime, default=datetime.datetime.utcnow)
    banned = Column(Boolean, default=False)
    banned_until = Column(DateTime, nullable=True, default=None)
    deleted = Column(Boolean, default=False)
    priv = Column(Integer, nullable=False, default=0)
    characters = relationship("Character", back_populates="account")


friendship_table = Table(
    "characters_friendslist",
    Base.metadata,
    Column("from_id", Uuid, ForeignKey("characters.id"), primary_key=True),
    Column("to_id", Uuid, ForeignKey("characters.id"), primary_key=True),
    UniqueConstraint("from_id", "to_id", name="unique_friendships"),
)


class Character(Base, AllFeaturesMixin):
    __tablename__ = "characters"
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    account_id = Column(Uuid, ForeignKey("accounts.id"))
    account = relationship("Account", back_populates="characters")
    created = Column(DateTime, default=datetime.datetime.utcnow)
    name = Column(String, unique=True)
    last_online = Column(DateTime, default=datetime.datetime.utcnow)
    ships = relationship("Ship", back_populates="owner")
    market_orders = relationship("MarketOrder")
    market_order_transactions = relationship("MarketOrderTransaction")
    ledger_id = Column(Uuid, ForeignKey("ledgers.id"), nullable=False)
    ledger = relationship("Ledger")
    current_location = Column(Uuid, nullable=False)
    friends_list = relationship(
        "Character",
        secondary=friendship_table,
        primaryjoin=id == friendship_table.c.from_id,
        secondaryjoin=id == friendship_table.c.to_id,
    )


class Company(Base, AllFeaturesMixin):
    __tablename__ = "companies"
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    name = Column(String(64), unique=True)
    ticker = Column(String(5), unique=True)
    created = Column(DateTime, default=datetime.datetime.utcnow)
    ledger_id = Column(Uuid, ForeignKey("ledgers.id"), nullable=False)
    ledger = relationship("Ledger")
    ships = relationship("Ship", back_populates="company")


class StarSystemGate(Base, AllFeaturesMixin):
    __tablename__ = "starsystem_links"
    __table_args__ = (
        ForeignKeyConstraint(["from_id", "to_id"], ["starsystems.id", "starsystems.id"]),
    )
    from_id = Column(Uuid, ForeignKey("starsystems.id"), primary_key=True, index=True, nullable=False)
    to_id = Column(Uuid, ForeignKey("starsystems.id"), primary_key=True, index=True, nullable=False)


class StarSystem(Base, AllFeaturesMixin):
    __tablename__ = "starsystems"
    id = Column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)
    x = Column(Double, nullable=False)
    y = Column(Double, nullable=False)
    z = Column(Double, nullable=False)
    classification = Column(String(2), name="class", nullable=False, default="O0")
    bodies: Mapped[List["OrbitalBody"]] = relationship("OrbitalBody", back_populates="starsystem")



#
# station_inventories = Table(
#    "station_inventories", Base.metadata,
#    Column("station_id", Uuid, ForeignKey("orbital_bodies.id"), nullable=False, primary_key=True),
#    Column("character_id", Uuid, ForeignKey("characters.id"), nullable=False, primary_key=True),
#    Column("inventory_id", Uuid, ForeignKey("inventories.id"), nullable=False, primary_key=True),
#    UniqueConstraint("colony_id", "character_id", name="unique_colony_inventories")
# )


class OrbitalBody(Base, AllFeaturesMixin):
    __tablename__ = "orbital_bodies"
    id = Column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
    starsystem_id = Column(Uuid, ForeignKey("starsystems.id"))
    starsystem = relationship("StarSystem", back_populates="bodies")
    name = Column(String, unique=True, nullable=False)
    otype = Column(Integer, name="type")  # 0=planet, 1=moon, 2=asteroid, 3=station
    stype = Column(
        Integer, name="sub_type"
    )  # depends on the otype, for planets: 0=rock, 1=lava, 2=desert, 3=temperate, 4=ice, 5=gas, 6=ocean
    axis = Column(Double, nullable=False)  # in AU
    eccentricity = Column(
        Double, nullable=False
    )  # in ratio 0:1 with 1 being hyperbolic
    inclination = Column(Double, nullable=False)  # in radians
    rings = Column(Integer, nullable=False, default=0)
    population = Column(Double, nullable=False, default=0)  # in millions
    pressure = Column(Double, nullable=False, default=0.0)  # in bar/psi
    temperature = Column(Double, nullable=False, default=-270.45)  # in celsius
    gravity = Column(
        Double, nullable=False, default=0.0
    )  # in m/s2 (earth is 9.807, jupiter is 24.97, pluto 0.62)
    fertility = Column(
        Double, nullable=False, default=0.0
    )  # in ratio 0:1 with 1 being lush and 0 being barren
    parent_id = Column(
        Uuid, ForeignKey("orbital_bodies.id"), nullable=True, default=None
    )
    colonies = relationship("Colony", back_populates="location")


OrbitalBody.parent = relationship(
    "OrbitalBody", back_populates="children", remote_side=OrbitalBody.id
)
OrbitalBody.children = relationship("OrbitalBody", back_populates="parent")


class Inventory(Base, AllFeaturesMixin):
    __tablename__ = "inventories"
    id = Column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
    items = Column(JSON, nullable=False, default="{}")


class Ship(Base, AllFeaturesMixin):
    __tablename__ = "ships"
    id = Column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String(64), unique=True, index=True)
    owner_id = Column(Uuid, ForeignKey("characters.id"), nullable=True, default=None)
    owner = relationship("Character", back_populates="ships")
    company_id = Column(Uuid, ForeignKey("companies.id"), nullable=True, default=None)
    company = relationship("Company", back_populates="ships")
    location_id = Column(Uuid)
    location_type = Column(
        String(1), nullable=False, default="C"
    )  # C=colony.id (landed), B=orbital_body.id (i.e. in orbit or landed), S=starsystem.id (i.e. not in orbit, but in the system)
    state = Column(
        String(1), nullable=False, default="L"
    )  # L=landed/landing, T=takeoff, E=enroute, W=warp, S=stationary, C=combat
    target_id = Column(Uuid, ForeignKey("ships.id"), nullable=True)
    created = Column(DateTime, default=datetime.datetime.utcnow)
    ship_class = Column("class", String, nullable=False)
    hp = Column(Double, nullable=False)
    max_hp = Column(Double, nullable=False)
    ap = Column(Double, nullable=False)
    max_ap = Column(Double, nullable=False)
    sp = Column(Double, nullable=False)
    max_sp = Column(Double, nullable=False)
    ep = Column(Double, nullable=False)
    max_ep = Column(Double, nullable=False)
    rr = Column(Double, nullable=False)
    max_rr = Column(Double, nullable=False)
    ws = Column(Double, nullable=False)
    max_ws = Column(Double, nullable=False)
    cs = Column(Double, nullable=False)
    max_cs = Column(Double, nullable=False)
    x = Column(Double, nullable=False)
    y = Column(Double, nullable=False)
    z = Column(Double, nullable=False)
    dx = Column(Double, nullable=False)
    dy = Column(Double, nullable=False)
    dz = Column(Double, nullable=False)
    max_cargo = Column(Double, nullable=False)
    max_tonnage = Column(Double, nullable=False)
    modules = Column(JSON, nullable=False, default="{}")
    inventory_id = Column(Uuid, ForeignKey("inventories.id"))
    inventory = relationship("Inventory")


class Colony(Base, AllFeaturesMixin):
    __tablename__ = "colonies"
    id = Column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
    location_id = Column(Uuid, ForeignKey("orbital_bodies.id"), nullable=False)
    owner_id = Column(Uuid, ForeignKey("characters.id"), nullable=True)
    company_id = Column(Uuid, ForeignKey("companies.id"), nullable=True)

    location = relationship("OrbitalBody")
    owner = relationship("Character")
    company = relationship("Company")

    name = Column(String, unique=True, index=True)
    population = Column(Integer)

    buildings = relationship("Building")
    inventory_id = Column(Uuid, ForeignKey("inventories.id"), nullable=False)
    inventory = relationship("Inventory")


class Building(Base, AllFeaturesMixin):
    __tablename__ = "buildings"
    id = Column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
    colony_id = Column(Uuid, ForeignKey("colonies.id"), nullable=False, index=True)
    colony = relationship("Colony", back_populates="buildings")
    name = Column(String, nullable=False)
    btype = Column(Integer, nullable=False, default=0)
    b_class = Column("class", String, nullable=False)

    jobs = relationship("BuildingJob")


class BuildingJob(Base, AllFeaturesMixin):
    __tablename__ = "buildings_jobs"
    id = Column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
    building_id = Column(Uuid, ForeignKey("buildings.id"), nullable=False)
    building = relationship("Building", back_populates="jobs")
    recipe_class = Column(String, nullable=False)
    install_date = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    completion_date = Column(DateTime, nullable=False)


class MarketOrder(Base, AllFeaturesMixin):
    __tablename__ = "market_orders"
    id = Column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
    location_id = Column(Uuid, nullable=False)
    issuer_id = Column(Uuid, ForeignKey("characters.id"), nullable=False)
    issuer = relationship("Character", back_populates="market_orders")
    created = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    closed = Column(DateTime, nullable=True, default=None)
    symbol = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    ask_bid = Column(Double, nullable=False)
    mtype = Column(Integer, nullable=False)  # 0=buy order, 1=sell order
    transactions = relationship("MarketOrderTransaction")


class MarketOrderTransaction(Base, AllFeaturesMixin):
    __tablename__ = "market_orders_transactions"
    id = Column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
    market_order_id = Column(Uuid, ForeignKey("market_orders.id"), nullable=False)
    market_order = relationship("MarketOrder", back_populates="transactions")
    date = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    character_id = Column(Uuid, ForeignKey("characters.id"), nullable=False)
    character = relationship("Character", back_populates="market_order_transactions")
    ttype = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)


class Ledger(Base, AllFeaturesMixin):
    __tablename__ = "ledgers"
    id = Column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
    transactions = relationship("LedgerTransaction", back_populates="ledger")


class LedgerTransaction(Base, AllFeaturesMixin):
    __tablename__ = "ledgers_transactions"
    date = Column(
        DateTime, default=datetime.datetime.utcnow(), primary_key=True, index=True
    )
    amount = Column(Double, nullable=False, default=0.0)
    desc = Column(String, nullable=False, default="")
    payer = Column(Uuid, nullable=False)
    payer_type = Column(
        String(1), nullable=False, default="P"
    )  # P=player, C=company, S=system
    ledger_id = Column(Uuid, ForeignKey("ledgers.id"), nullable=False)
    ledger = relationship("Ledger", back_populates="transactions")
