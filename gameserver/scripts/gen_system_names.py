import sys

sys.path.append("..")

import gameserver.utils as utils
import asyncio


async def gen_system_names():
    print("Generating system names, please be patient, this can take up to 10 minutes.")
    sn = await utils.gen_system_names(15000)
    with open("./data/system_names.txt", "wt") as fp:
        for s in sn:
            fp.write(f"{s}\r\n")
            await asyncio.sleep(0.0001)
        fp.close()


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(gen_system_names())


if __name__ == "__main__":
    main()
