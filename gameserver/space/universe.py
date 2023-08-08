from sqlalchemy.orm import Session
import math
import models
import random
import utils
import asyncio

classifications: list[str] = ["O", "B", "A", "F", "G", "K", "M", "L", "T"]

stotal: int = 0
ptotal: int = 0
mtotal: int = 0
atotal: int = 0


async def generate_universe(db: Session, seed: int) -> list[models.StarSystem]:
    print("Generating system names, please be patient, this can take up to 10 minutes.")
    sn: list = await utils.gen_system_names(15001)
    with open("./data/system_names.txt", "wt") as fp:
        for s in sn:
            fp.write(f"{s}\r\n")
            await asyncio.sleep(0.0001)
        fp.close()
    global stotal, ptotal, mtotal, atotal
    rand = random.Random(seed)
    s: list[models.StarSystem] = []
    print(f"Generating {len(sn)} stars, please be patient")
    for x in range(len(sn)):
        name = sn[x]
        star = await generate_starsystem(x, name)
        try:
            db.add(star)
            db.commit()
            db.refresh(star)
            stotal = stotal + 1
            s.append(star)
            # print(".", end="", flush=True)
        except Exception:
            # print("o", end="", flush=True)
            db.rollback()
            x -= 1
        await asyncio.sleep(0.0001)
    print("")
    print(
        "Stars: {}, Planets: {}, Moons: {}, Asteroid Fields: {}".format(
            stotal, ptotal, mtotal, atotal
        )
    )
    return s


async def generate_starsystem(seed: int, name: str) -> models.StarSystem:
    r = random.Random(seed)
    c = "{}{}".format(
        classifications[r.randint(0, len(classifications) - 1)], r.randint(0, 9)
    )
    x = r.uniform(-256, 256)
    y = r.uniform(-32, 32)
    z = r.uniform(-256, 256)
    s = models.StarSystem(name=name, classification=c, x=x, y=y, z=z, bodies=[])
    pcount = r.randint(0, 15)
    bodies = []
    for x in range(pcount):
        b = await generate_planet(r.randint(0, 999999999))
        b.starsystem = s
        bodies.append(b)
    bodies.sort(key=lambda x: x.axis)
    i = 0
    for b in bodies:
        i = i + 1
        b.name = f"{s.name} {intToRoman(i)}"
        if len(b.children) > 0:
            b.children.sort(key=lambda x: x.axis)
            ii = 0
            for m in b.children:
                ii = ii + 1
                m.name = f"{b.name} Moon {intToRoman(ii)}"

    achance = r.randint(0, 5)
    if achance >= 4:
        acount = r.randint(0, 15)
        for x in range(acount):
            a = await generate_asteroids(r.randint(0, 999999999))
            a.name = f"{s.name} Asteroid Field {intToRoman(x+1)}"
            a.starsystem = s
            bodies.append(a)
    s.bodies = bodies
    return s


async def generate_planet(seed: int) -> models.OrbitalBody:
    global ptotal
    r = random.Random(seed)
    axis = r.uniform(0.1, 60)
    ecc = r.uniform(0, 0.9)
    inc = math.radians(r.uniform(0, 90))
    t = r.randint(0, 6)  # 0=rock, 1=lava, 2=desert, 3=temperate, 4=ice, 5=gas, 6=ocean
    p = models.OrbitalBody(
        name="",
        otype=0,
        stype=t,
        axis=axis,
        eccentricity=ecc,
        inclination=inc,
        rings=0,
        population=0,
        pressure=0,
        gravity=0,
        temperature=0,
        fertility=0,
    )
    if t == 5:
        p.rings = r.randint(0, 3)
    if t == 3:
        if 1.2 > axis < 0.8:
            p.stype = 2
            p.population = r.randint(0, 1000)
            p.fertility = r.uniform(0.005, 0.01)
        else:
            p.population = r.randint(0, 1000000)
            p.fertility = r.uniform(0.5, 1.0)
    if t == 6:
        p.population = r.randint(0, 10000)
        p.fertility = r.uniform(0, 0.5)
    if t == 0:
        p.fertility = r.uniform(0, 0.1)
    p.children = []
    mcount = r.randint(0, 5)
    if mcount > 0:
        m = await generate_moon(r.randint(0, 999999999))
        m.parent = p
        p.children.append(m)
    ptotal = ptotal + 1
    return p


async def generate_moon(seed: int) -> models.OrbitalBody:
    global mtotal
    r = random.Random(seed)
    axis = r.uniform(0.1, 60)
    ecc = r.uniform(0, 0.9)
    inc = math.radians(r.uniform(0, 90))
    t = r.randint(0, 3)  # 0=rock, 1=lava, 2=temperate, 4=ice
    p = models.OrbitalBody(
        name="",
        otype=1,
        stype=t,
        axis=axis,
        eccentricity=ecc,
        inclination=inc,
        rings=0,
        population=0,
        pressure=0,
        gravity=0,
        temperature=0,
        fertility=0,
    )
    if t == 2:
        p.population = r.randint(0, 100000)
        p.fertility = r.uniform(0.5, 1.0)
    mtotal = mtotal + 1
    return p


async def generate_asteroids(seed: int) -> models.OrbitalBody:
    global atotal
    r = random.Random(seed)
    axis = r.uniform(0.1, 60)
    ecc = r.uniform(0, 0.9)
    inc = math.radians(r.uniform(0, 90))
    t = r.randint(0, 5)
    p = models.OrbitalBody(
        name="",
        otype=2,
        stype=t,
        axis=axis,
        eccentricity=ecc,
        inclination=inc,
        rings=0,
        population=0,
        pressure=0,
        gravity=0,
        temperature=0,
        fertility=0,
    )
    atotal = atotal + 1
    return p


def intToRoman(num):
    # Storing roman values of digits from 0-9
    # when placed at different places
    m = ["", "M", "MM", "MMM"]
    c = ["", "C", "CC", "CCC", "CD", "D", "DC", "DCC", "DCCC", "CM "]
    x = ["", "X", "XX", "XXX", "XL", "L", "LX", "LXX", "LXXX", "XC"]
    i = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"]

    # Converting to roman
    thousands = m[num // 1000]
    hundreds = c[(num % 1000) // 100]
    tens = x[(num % 100) // 10]
    ones = i[num % 10]

    ans = thousands + hundreds + tens + ones

    return ans
