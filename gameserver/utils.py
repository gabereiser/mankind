from uuid import UUID
from passlib.context import CryptContext
from random import SystemRandom

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password):
    return pwd_context.hash(password)


_a = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789"


def gen_key(size: int) -> str:
    global _a
    r = SystemRandom()
    l = len(_a) - 1
    a = ""
    for _ in range(size):
        v = _a[r.randint(0, l)]
        a = f"{a}{v}"
    return a


def roll_dice(d20: str) -> int:
    (n, m) = d20.lower().split("d", 1)
    s = m
    if not m.isnumeric():
        if "+" in m:
            (s, m) = m.split("+")
            m = int(m)
        if "-" in m:
            (s, m) = m.split("-")
            m = -(int(m))
    r = SystemRandom()
    v = 0
    for _ in range(n):
        v += r.randint(1, int(s))
    v += m
    return v


def json_converter(o):
    if isinstance(o, UUID):
        return o.hex
