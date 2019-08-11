import re
import asyncio
import discord
from firestore import db
from difflib import SequenceMatcher
import json
from discord.ext import commands


class tag(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Create a group for our sub commands
    @commands.group(invoke_without_command=True)
    async def tag(self, ctx, title: str, *content):
        content = ' '.join(content)
        if ctx.invoked_subcommand is None:

            tag_doc = db.document(
                'discord_tags/{0}/tags/{1}'.format(ctx.guild.id, title)).get()
            tag_field = tag_doc.to_dict()  # This is needed to fetch fields
            if tag_doc.exists:
                await ctx.send(tag_field['description'].replace('<br>', '\n'))
            else:
                color = discord.Color.from_rgb(237, 0, 0)
                description = 'That tag does not exist'
                embed = discord.Embed(color=color, description=description)
                await ctx.send(embed=embed)

    @tag.command()
    async def add(self, ctx, title: str, *content):
        content = ' '.join(content)

        tag_title = db.document(
            'discord_tags/{0}/tags/{1}'.format(ctx.guild.id, title)).get()
        if tag_title.exists:
            color = discord.Color.from_rgb(237, 0, 0)
            description = 'That tag already exists'
            embed = discord.Embed(color=color, description=description)
            await ctx.send(embed=embed)
        else:
            # Create a document with fields
            data = {
                u'title': title,
                u'description': content,
                u'author_id': ctx.author.id,
                u'author_name': ctx.author.name
            }
            await handleTimeout(data, ctx)

    @tag.command()
    async def edit(self, ctx, title: str, *content):
        content = ' '.join(content)
        tag_title = db.document(
            'discord_tags/{0}/tags/{1}'.format(ctx.guild.id, title)).get()
        if tag_title.exists:
            # update changes a specified field in a document
            tag_title.reference.update({'description': content})
            color = discord.Color.from_rgb(0, 106, 212)
            embedTitle = 'Edited tag'
            description = title
            embed = discord.Embed(
                color=color, description=description, title=embedTitle)
            await ctx.send(embed=embed)
        else:
            await ctx.send('A tag with the name "{0}" does not exist, create a tag using `m!addtag [tag name] [value]'.format(title))

    @tag.command()
    async def delete(self, ctx, title: str):

        tag_title = db.document(
            'discord_tags/{0}/tags/{1}'.format(ctx.guild.id, title)).get()

        if tag_title.exists:
            tag_title.reference.delete()  # You have to make it a reference to delete it
            color = discord.Color.from_rgb(227, 88, 2)
            embedTitle = 'Removed tag'
            description = title
            embed = discord.Embed(
                color=color, description=description, title=embedTitle)
            await ctx.send(embed=embed)
        else:
            await ctx.send('A tag with the name "{0}" does not exist'.format(title))


async def handleTimeout(tag, ctx):
    db.collection(u'discord_tags').document(str(ctx.guild.id)).collection(
        'tags').document(tag['title']).set(tag)
    color = discord.Color.from_rgb(6, 201, 6)
    embedTitle = 'Added new tag'
    description = tag['title']
    embed = discord.Embed(
        color=color, description=description, title=embedTitle)
    await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(tag(bot))
