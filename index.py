import discord
from discord.ext import commands
import json

config = json.load(open('./config.json', 'r'))
from spam import handleDiscordSpam

import time

description = 'Meet Mbot the Fancy Bot!'

bot = commands.Bot(command_prefix='m!', description = description)

@bot.event
async def on_ready():
  print('Logged in as: {0.name} \nID: {0.id} \nTimeStamp: {1}'.format(bot.user, time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())))

@bot.event
async def on_message(message):
  # Discord Spam Module Only in my Guild :P
  if (not message.author == bot.user) and message.guild and config['guild_id'] == str(message.guild.id):
    await handleDiscordSpam(message)

  

bot.run(config['token'])