import re
import asyncio
import discord 
from firestore import db 
from difflib import SequenceMatcher
import json
from discord.ext import commands

class addtag(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    @commands.command()
    async def addtag(self,ctx,*content):
        args = content
        
        tag_title = db.document('discord_tags/{0}/tags/{1}'.format(ctx.guild.id,args[0])).get()
        if tag_title.exists:
            color = discord.Color.from_rgb(237, 0, 0)
            description = 'That tag already exists'
            embed = discord.Embed(color= color, description= description)
            await ctx.send(embed=embed)
        else:
            data = {
                u'title': args[0],
                u'description': ' '.join(args[1:len(args)]),
                u'author_id': ctx.author.id,
                u'author_name': ctx.author.name
    }
            await handleTimeout(data,ctx)

async def handleTimeout(tag,ctx):
    db.collection(u'discord_tags').document(str(ctx.guild.id)).collection('tags').document(tag['title']).set(tag)
    color = discord.Color.from_rgb(6, 201, 6)
    embedTitle = 'Added new tag'
    description = tag['title']
    embed = discord.Embed(color= color, description= description, title = embedTitle)
    await ctx.send(embed=embed)
def setup(bot):
    bot.add_cog(addtag(bot))