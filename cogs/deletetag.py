import re
import asyncio
import discord 
from firestore import db 
from difflib import SequenceMatcher
import json
from discord.ext import commands

class deletetag(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command()
    async def deletetag(self,ctx,arg):
        tag_title = db.document('discord_tags/{0}/tags/{1}'.format(ctx.guild.id,arg)).get()
        
        if tag_title.exists:
            tag_title.reference.delete()
            color = discord.Color.from_rgb(227, 88, 2)
            embedTitle = 'Removed tag'
            description = arg
            embed = discord.Embed(color= color, description= description, title = embedTitle)
            await ctx.send(embed=embed)
        else:
            await ctx.send('A tag with the name "{0}" does not exist'.format(arg))
def setup(bot):
    bot.add_cog(deletetag(bot))