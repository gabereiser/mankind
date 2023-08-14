import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import asyncio
import database as database
import models as models
import space.universe as universe
import utils

def main():
    db = next(database.session())
    s = db.query(models.StarSystem).all()
    print("Generating starlinks...")
    for x in range(len(s)):
        links = universe.generate_starlinks(db, x, s[x], s)
    for star in s:
        links = utils.wait(database.get_gates_for_starsystem(db, star))
        if len(links) == 0:
            raise Exception(f"{star.name} <{star.id}> has no links")
        if len(links) == 1:
            # potential for two stars to link each other but no one else...
            # let's look at the other end.
            other_end = utils.wait(database.get_other_starsystem_from_gate(db, star, links[0]))
            other_end_links = utils.wait(database.get_gates_for_starsystem(db, other_end))
            if len(other_end_links) == 1 and (other_end_links[0] == links[0]):
                raise Exception(f"{star.name} and {other_end.name} link exclusively.")

            

            
if __name__ == "__main__":
    main()
    #loop = asyncio.get_event_loop()
    #loop.run_until_complete(main())