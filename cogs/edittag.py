import re
import asyncio
import discord 
from firestore import db 
from difflib import SequenceMatcher
import json
from discord.ext import commands

class edittag(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    @commands.command()
    async def edittag(self,ctx,arg,*content):
       
        tag_title = db.document('discord_tags/{0}/tags/{1}'.format(ctx.guild.id,arg)).get()
        if tag_title.exists:
            tag_title.reference.update({'description': ' '.join(content)})
            color = discord.Color.from_rgb(6, 201, 6)
            embedTitle = 'Edited tag'
            description = arg
            embed = discord.Embed(color= color, description= description, title = embedTitle)
            await ctx.send(embed=embed)
        else:
            ctx.send('A tag with the name "{0}" does not exist, create a tag using `m!addtag [tag name] [value]'.format(arg))
def setup(bot):
    bot.add_cog(edittag(bot))