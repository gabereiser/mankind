from sqlalchemy.orm import Session
from datetime import datetime
from uuid import UUID
import models, schemas
import utils
import storage


def bootstrap() -> None:
    models.Base.metadata.create_all(bind=storage.engine)
    db = storage.SessionLocal()
    count = db.query(models.Account).count()
    if count == 0:
        create_account(
            db,
            schemas.AccountCreate(
                username="user",
                password="password",
                email="admin@mankind.net",
                created=datetime.utcnow(),
            ),
        )


def session() -> Session:
    db = storage.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def authenticate_user(db: Session, username: str, password: str) -> models.Account:
    account = get_account_by_username(db, username)
    if not account:
        return False
    if not utils.verify_password(password, account.password):
        return False
    return account


def get_account(db: Session, account_id: UUID) -> models.Account:
    return db.query(models.Account).filter(models.Account.id == account_id).first()


def get_account_by_email(db: Session, email: str) -> models.Account:
    return db.query(models.Account).filter(models.Account.email == email).first()


def get_account_by_username(db: Session, username: str) -> models.Account:
    return db.query(models.Account).filter(models.Account.username == username).first()


def create_account(db: Session, account: schemas.AccountCreate) -> models.Account:
    hashed_password = utils.hash_password(account.password)
    db_account = models.Account(**account.model_dump())
    db_account.password = hashed_password
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account


def update_account(db: Session, account: schemas.AccountUpdate) -> models.Account:
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


def delete_account(db: Session, account: schemas.AccountDelete) -> None:
    db_account = (
        db.query(models.Account)
        .filter(models.Account.username == account.username)
        .first()
    )
    db_account.deleted = True
    db.add(db_account)
    db.commit()
    return


def create_character(db: Session, character: schemas.Character) -> models.Character:
    db_char = models.Character(**character.model_dump())
    db.add(db_char)
    db.commit()
    db.refresh(db_char)
    return db_char
