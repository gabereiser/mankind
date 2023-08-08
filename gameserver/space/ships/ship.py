
SHIP_TYPES = {}

def ship(key: str):
    def boxed(klazz):
        if key in SHIP_TYPES:
            raise Exception(f"ship type #{key} already exists!")

        SHIP_TYPES[key] = klazz()
        print(f"ship type {key} has been added to the network.")
        return SHIP_TYPES[key]
        # returning inner function

    return boxed