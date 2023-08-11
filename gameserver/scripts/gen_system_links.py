import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import asyncio
import database as database
import models as models
import space.universe as universe

def main():
    db = next(database.session())
    s = db.query(models.StarSystem).all()
    print("Generating starlinks...")
    for x in range(len(s)):
        links = universe.generate_starlinks(db, x, s[x], s)
    for star in s:
        if len(star.gates) == 0:
            raise Exception(f"{star.name} has no links!")
            
if __name__ == "__main__":
    main()
    #loop = asyncio.get_event_loop()
    #loop.run_until_complete(main())