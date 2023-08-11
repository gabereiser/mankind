import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import asyncio
import database as database
import models as models
import space.universe as universe
import storage

def main():
    models.Base.metadata.create_all(bind=storage.engine)
    db = next(database.session())
    print("Generating universe...")
    stars = universe.generate_universe(db)
    for star in stars:
        gates = database.get_gates_for_starsystem(db, star)
        if len(gates) == 0:
            raise Exception(f"{star.name} has no links!")
            
if __name__ == "__main__":
    main()
    #loop = asyncio.get_event_loop()
    #loop.run_until_complete(main())