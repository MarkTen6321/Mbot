import re
import asyncio
import discord 
from firestore import db 
from difflib import SequenceMatcher
import json
from discord.ext import commands

class tag(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def tag(self,ctx,*content):
        args = content
        
        tag_doc = db.document('discord_tags/{0}/tags/{1}'.format(ctx.guild.id,args[0])).get()
        tag_field = tag_doc.to_dict()
        if tag_doc.exists:
            await ctx.send(tag_field['description'].replace('<br>','\n'))
        else:
            color = discord.Color.from_rgb(237, 0, 0)
            description = 'That tag does not exist'
            embed = discord.Embed(color= color, description= description)
            await ctx.send(embed=embed)
            
def setup(bot):
    bot.add_cog(tag(bot))

