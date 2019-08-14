import discord
from discord.ext import commands
import json
from urllib.request import urlopen
import codecs
import re


class mdn(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def mdn(self, ctx, *args):
        # add search terms together with + for url use
        search_term = "+".join(args)

        if not args:
            await ctx.send("You need to enter a search term")
            return
        # initiate a reader
        reader = codecs.getreader("utf-8")
        # fetch the url
        json_url = urlopen(
            "https://developer.mozilla.org/en-US/search.json?q={0}&topic=js".format(
                search_term
            ),
            data=None,
            timeout=6,
        )
        # Get the data from the url
        data = json.load(reader(json_url))

        # Construct the embed
        color = discord.Color.from_rgb(19, 143, 194)
        # get the page title
        title = removehtml(data["documents"][0]["title"])
        # excerpt is the short description for a page
        description = removehtml(data["documents"][0]["excerpt"])
        url = data["documents"][0]["url"]
        embed = discord.Embed(
            title=title, color=color, description=description, url=url
        )
        embed.set_author(
            name="MDN",
            icon_url="https://www.stickpng.com/assets/images/58480eb3cef1014c0b5e492a.png",
        )
        await ctx.send(embed=embed)


# This function removes html tags like <tag>something</tag> -> something


def removehtml(raw_html):
    cleanr = re.compile("<.*?>")
    cleantext = re.sub(cleanr, "", raw_html)
    return cleantext


def setup(bot):
    bot.add_cog(mdn(bot))
