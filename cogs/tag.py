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

    @commands.group(invoke_without_command = True)
    async def tag(self,ctx,*content):
        
        if ctx.invoked_subcommand is None:
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
            
    @tag.command()
    async def add(self,ctx,*content):
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
    @tag.command()
    async def edit(self,ctx,arg,*content):
       
        tag_title = db.document('discord_tags/{0}/tags/{1}'.format(ctx.guild.id,arg)).get()
        if tag_title.exists:
            tag_title.reference.update({'description': ' '.join(content)})
            color = discord.Color.from_rgb(0, 106, 212)
            embedTitle = 'Edited tag'
            description = arg
            embed = discord.Embed(color= color, description= description, title = embedTitle)
            await ctx.send(embed=embed)
        else:
            ctx.send('A tag with the name "{0}" does not exist, create a tag using `m!addtag [tag name] [value]'.format(arg))

    @tag.command()
    async def delete(self,ctx,arg):
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



async def handleTimeout(tag,ctx):
    db.collection(u'discord_tags').document(str(ctx.guild.id)).collection('tags').document(tag['title']).set(tag)
    color = discord.Color.from_rgb(6, 201, 6)
    embedTitle = 'Added new tag'
    description = tag['title']
    embed = discord.Embed(color= color, description= description, title = embedTitle)
    await ctx.send(embed=embed)
            
def setup(bot):
    bot.add_cog(tag(bot))

