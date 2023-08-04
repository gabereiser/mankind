import re

COMMANDS = {}

def command(
    name: str,
    description: str,
    regex: str
):
    def boxed(func):
        COMMANDS[name] = {
            "name": name,
            "desc": description,
            "regex": regex,
            "func": func
		}
        return func
        # returning inner function

    return boxed

async def get_command(data: any) -> callable:
    for x in COMMANDS.values:
        p = re.compile(x.regex)
        if p.match(data.cmd):
            return x

@command(name="CMD", description="List of commands", regex="^(cmd)")
async def list_commands(client: any, data: any):
	for v in COMMANDS.values:
		client.send("{'name': {name}, 'desc': {desc} }")

@command(name="WHO", description="Who is online", regex="^(who)(.+)")
async def who(client: any, data: any):
    pass