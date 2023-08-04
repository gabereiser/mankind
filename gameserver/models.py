from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Uuid,
    Double,
    DateTime,
    JSON,
)
from sqlalchemy.orm import relationship
from storage import Base

import uuid, datetime


class Account(Base):
    __tablename__ = "accounts"
    id = Column(Uuid, default=uuid.uuid4, primary_key=True, index=True)
    username = Column(String(32), unique=True, index=True)
    email = Column(String(64), unique=True, index=True)
    password = Column(String)
    created = Column(DateTime, default=datetime.datetime.utcnow)
    banned = Column(Boolean, default=False)
    banned_until = Column(DateTime, nullable=True, default=None)
    deleted = Column(Boolean, default=False)
    characters = relationship("Character", back_populates="account")


class Character(Base):
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


class Company(Base):
    __tablename__ = "companies"
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    name = Column(String(64), unique=True)
    ticker = Column(String(5), unique=True)
    created = Column(DateTime, default=datetime.datetime.utcnow)
    ships = relationship("Ship", back_populates="company")


class StarSystem(Base):
    __tablename__ = "starsystems"
    id = Column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)
    x = Column(Double, nullable=False)
    y = Column(Double, nullable=False)
    z = Column(Double, nullable=False)
    classification = Column(String(2), name="class", nullable=False, default="O0")
    bodies = relationship("OrbitalBody", back_populates="starsystem")
    ships_in_system = relationship("Ship", back_populates="starsystem")


class OrbitalBody(Base):
    __tablename__ = "orbital_bodies"
    id = Column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
    starsystem_id = Column(Uuid, ForeignKey("starsystems.id"))
    starsystem = relationship("StarSystem", back_populates="bodies")
    name = Column(String, unique=True, nullable=False)
    otype = Column(Integer, name="type")
    axis = Column(Double, nullable=False)
    eccentricity = Column(Double, nullable=False)
    inclination = Column(Double, nullable=False)
    rings = Column(Integer, default=0)
    population = Column(Integer, default=0)
    parent_id = Column(
        Uuid, ForeignKey("orbital_bodies.id"), nullable=True, default=None
    )
    ships_landed = relationship("Ship", back_populates="location")


OrbitalBody.parent = relationship(
    "OrbitalBody", back_populates="children", remote_side=OrbitalBody.id
)
OrbitalBody.children = relationship("OrbitalBody", back_populates="parent")


class Inventory(Base):
    __tablename__ = "inventories"
    id = Column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
    items = Column(JSON, nullable=False, default="{}")
    ship = relationship("Ship")


class Ship(Base):
    __tablename__ = "ships"
    id = Column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String(64), unique=True, index=True)
    owner_id = Column(Uuid, ForeignKey("characters.id"), nullable=True, default=None)
    owner = relationship("Character", back_populates="ships")
    company_id = Column(Uuid, ForeignKey("companies.id"), nullable=True, default=None)
    company = relationship("Company", back_populates="ships")
    location_id = Column(Uuid, ForeignKey("orbital_bodies.id"), nullable=True)
    location = relationship("OrbitalBody", back_populates="ships_landed")
    starsystem_id = Column(Uuid, ForeignKey("starsystems.id"), nullable=False)
    starsystem = relationship("StarSystem", back_populates="ships_in_system")
    created = Column(DateTime, default=datetime.datetime.utcnow)
    ship_class = Column(String)
    hp = Column(Double, nullable=False)
    max_hp = Column(Double, nullable=False)
    ap = Column(Double, nullable=False)
    max_ap = Column(Double, nullable=False)
    sp = Column(Double, nullable=False)
    max_sp = Column(Double, nullable=False)
    fp = Column(Double, nullable=False)
    max_fp = Column(Double, nullable=False)
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
    inventory = relationship("Inventory", back_populates="ship")


class Colony(Base):
    __tablename__ = "colonies"
    id = Column(Uuid, primary_key=True, index=True, default=uuid.uuid4)


class Building(Base):
    __tablename__ = "buildings"
    id = Column(Uuid, primary_key=True, index=True, default=uuid.uuid4)


class BuildingJob(Base):
    __tablename__ = "buildings_jobs"
    id = Column(Uuid, primary_key=True, index=True, default=uuid.uuid4)


class MarketOrder(Base):
    __tablename__ = "market_orders"
    id = Column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
    issuer_id = Column(Uuid, ForeignKey("characters.id"), nullable=False)
    issuer = relationship("Character", back_populates="market_orders")
    created = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)


class MarketOrderTransaction(Base):
    __tablename__ = "market_orders_transactions"
    id = Column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
    market_order_id = Column(Uuid, ForeignKey("market_orders.id"), nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    character_id = Column(Uuid, ForeignKey("characters.id"), nullable=False)
    character = relationship("Character", back_populates="market_order_transactions")


class Wallet(Base):
    __tablename__ = "wallets"
    id = Column(Uuid, primary_key=True, index=True, default=uuid.uuid4)
