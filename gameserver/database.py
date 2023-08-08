from typing import Dict, List
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from datetime import datetime
from uuid import UUID
import os
import json
import models
import schemas
import utils
import storage
import jobs
from space import universe


async def bootstrap() -> None:
    models.Base.metadata.create_all(bind=storage.engine)
    jobs.start_background_jobs()
    db = storage.SessionLocal()
    count = db.query(models.Account).count()
    if count == 0:
        await create_account(
            db,
            schemas.AccountCreate(
                username="user",
                password="password",
                email="admin@mankind.net",
                created=datetime.utcnow(),
            ),
        )
    count = db.query(models.StarSystem).count()
    if count == 0:
        stars = universe.generate_universe(db, 42)
        db.add_all(stars)
        db.commit()
    if not os.path.exists("data/universe.json"):
        print("generating json world data")
        with open("data/universe.json", "w") as fp:
            sstars = db.query(models.StarSystem).all()
            stars = [x.to_dict(nested=True) for x in sstars]
            json.dump(
                stars,
                fp,
                sort_keys=True,
                default=utils.json_converter,
            )
            fp.flush()
            fp.close()


def __get_bodies_dict_list(db: Session, parent: UUID | None, star: UUID) -> List[Dict]:
    ret: List[Dict] = []
    for body in (
        db.query(models.OrbitalBody)
        .filter(
            models.OrbitalBody.parent_id == parent,
            models.OrbitalBody.starsystem_id == star,
        )
        .all()
    ):
        d = body.__dict__
        if len(body.children) > 0:
            d["children"] = __get_bodies_dict_list(db, body.id, star.id)
        ret.append(d)
        return ret


def session() -> Session:
    db = storage.SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def authenticate_user(
    db: Session, username: str, password: str
) -> models.Account:
    account = await get_account_by_username(db, username)
    if not account:
        return False
    if not utils.verify_password(password, account.password):
        return False
    return account


async def get_account(db: Session, account_id: UUID) -> models.Account:
    return db.query(models.Account).filter(models.Account.id == account_id).first()


async def get_account_by_email(db: Session, email: str) -> models.Account:
    return db.query(models.Account).filter(models.Account.email == email).first()


async def get_account_by_username(db: Session, username: str) -> models.Account:
    return db.query(models.Account).filter(models.Account.username == username).first()


async def create_account(db: Session, account: schemas.AccountCreate) -> models.Account:
    hashed_password = utils.hash_password(account.password)
    db_account = models.Account(**account.model_dump())
    db_account.password = hashed_password
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account


async def update_account(db: Session, account: schemas.AccountUpdate) -> models.Account:
    db_account = (
        db.query(models.Account)
        .filter(models.Account.username == account.username)
        .first()
    )
    db_account.email = account.email
    if account.password is not None:
        db_account.password = utils.hash_password(account.password)
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account


async def delete_account(db: Session, account: schemas.Account) -> None:
    db_account = (
        db.query(models.Account)
        .filter(models.Account.username == account.username)
        .first()
    )
    db_account.deleted = True
    db.add(db_account)
    db.commit()
    return


async def create_character(
    db: Session, current_user: schemas.Account, character: schemas.Character
) -> models.Character:
    ledger = models.Ledger()
    db.add(ledger)
    db_char = models.Character(**character.model_dump())
    db_char.ledger = ledger
    db_char.account_id = current_user.id
    db_char.current_location = (
        db.query(models.OrbitalBody)
        .filter(and_(models.OrbitalBody.otype == 0, models.OrbitalBody.stype == 3))
        .first()
    )
    db.add(db_char)
    db.commit()
    db.refresh(db_char)
    return db_char


async def get_starsystems(
    db: Session, page: int = 0, limit: int = 50
) -> list[models.StarSystem]:
    return db.query(models.StarSystem).offset(page).limit(limit).all()


async def get_starsystem(db: Session, id: UUID) -> models.StarSystem:
    return db.query(models.StarSystem).filter(models.StarSystem.id == id).first()


async def get_ships_in_system(db: Session, id: UUID) -> List[models.Ship]:
    return (
        db.query(models.Ship)
        .filter(models.Ship.location_type == "S", models.Ship.location_id == id)
        .all()
    )


async def get_ships_in_orbit(db: Session, id: UUID) -> List[models.Ship]:
    return (
        db.query(models.Ship)
        .filter(models.Ship.location_type == "B", models.Ship.location_id == id)
        .all()
    )


async def get_ships_in_colony(db: Session, id: UUID) -> List[models.Ship]:
    return (
        db.query(models.Ship)
        .filter(models.Ship.location_type == "C", models.Ship.location_id == id)
        .all()
    )


async def get_ships_owned_by(db: Session, id: UUID) -> List[models.Ship]:
    return (
        db.query(models.Ship)
        .filter(or_(models.Ship.owner_id == id, models.Ship.company_id == id))
        .all()
    )


async def get_ship_in_command_by_player(
    db: Session, player: models.Character
) -> models.Ship:
    return db.query(models.Ship).filter(models.Ship.owner_id == player.id).first()
