import sys
import os.path
from typing import List
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import asyncio
from sqlalchemy.orm import Session
import database as database
import models as models
import space.universe as universe
import utils

def validate(db: Session, star: models.StarSystem, stars: List[models.StarSystem]) -> bool:
    gates = utils.wait(database.get_gates_for_starsystem(db, star))
    if len(gates) == 0:
        raise Exception(f"{star.name} has no links!")
    if len(gates) == 1:
        # potential for two stars to link each other but no one else...
        # let's look at the other end.
        other_end = utils.wait(database.get_other_starsystem_from_gate(db, star, gates[0]))
        other_end_links = utils.wait(database.get_gates_for_starsystem(db, other_end))
        if len(other_end_links) == 1 and (other_end_links[0] == gates[0]):
            print(f"{star.name} exclusively links to {other_end.name}, attempting to rectify")
            links = universe.generate_starlinks(db, hash(utils.gen_key(1, 8)), other_end, stars)
            if len(links) <= 1:
                return validate(db, star, stars)
            else:
                return True
            
def main():
    db = next(database.session())
    s = db.query(models.StarSystem).all()
    print("Validating starlinks...")
    for star in s:
        validate(db, star, s)
            
if __name__ == "__main__":
    main()
    #loop = asyncio.get_event_loop()
    #loop.run_until_complete(main())