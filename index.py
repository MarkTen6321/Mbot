import discord
from discord.ext import commands
import json

from spam import handleDiscordSpam

import time

from os import listdir, environ
from os.path import isfile, join

import traceback

description = "Meet Mbot the Fancy Bot!"

cogs_dir = "cogs"

from dotenv import load_dotenv
load_dotenv()

# Load token from either config.json or environment variables
config = json.load(open("./config.json", "r"))
config.update({ 'token': environ['token'] or config['token'] })


bot = commands.Bot(command_prefix="m!", description=description)

if __name__ == "__main__":
    for extension in [
        f.replace(".py", "") for f in listdir(cogs_dir) if isfile(join(cogs_dir, f))
    ]:
        try:
            bot.load_extension(cogs_dir + "." + extension)
        except (discord.ClientException, ModuleNotFoundError):
            print(f"Failed to load extension {extension}.")
            traceback.print_exc()


@bot.event
async def on_ready():
    print(
        "Logged in as: {0.name} \nID: {0.id} \nTimeStamp: {1}".format(
            bot.user, time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        )
    )


@bot.event
async def on_message(message):
    if (
        (not message.author == bot.user)
        and message.guild
        and config["guild_id"] == str(message.guild.id)
    ):
        await handleDiscordSpam(message)
    await bot.process_commands(message)


bot.run(config["token"])
