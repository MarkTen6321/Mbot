import discord
from discord.ext import commands
import json
from urllib.request import urlopen
import codecs
import re


class djs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def djs(self, ctx, *args):
        # set Default embed color
        title = None
        color = discord.Color.from_rgb(33, 150, 244)
        # Allow for the method/property/event to be split by # or .
        if "#" in args[0]:
            search = args[0].split("#")
        elif "." in args[0]:
            search = args[0].split(".")
        else:
            await ctx.send(
                "Please use command like this `[prefix]djs <Class>#<search>`"
            )
        # initiate reader
        reader = codecs.getreader("utf-8")
        # get raw "api" of djs docs
        json_url = urlopen(
            "https://raw.githubusercontent.com/discordjs/discord.js/docs/stable.json",
            data=None,
            timeout=6,
        )
        # Get it in json format
        data = json.load(reader(json_url))
        # Find the Class the user has inputted
        objectClass = list(
            filter(lambda x: x["name"].lower() == search[0].lower(), data["classes"])
        )
        # This is kindof cheaty but since Client is the only Class with events I did it like this
        if objectClass[0]["name"] == "Client":

            # if the user inputted an event find which event it was and initiate the embed
            if findEvent(objectClass, search) != []:

                classEvent = findEvent(objectClass, search)
                title = "{0}#{1}".format(objectClass[0]["name"], classEvent[0]["name"])
                description = classEvent[0]["description"]
                url = "https://discord.js.org/#/docs/main/stable/class/{0}?scrollTo={1}".format(
                    objectClass[0]["name"], classEvent[0]["name"]
                )
                embed = discord.Embed(
                    title=title, color=color, description=description, url=url
                )

        # if the user inputted a property find which event it was and initiate the embed
        if findProperty(objectClass, search) != []:

            classProperty = findProperty(objectClass, search)
            title = "{0}#{1}".format(objectClass[0]["name"], classProperty[0]["name"])
            description = classProperty[0]["description"]
            url = "https://discord.js.org/#/docs/main/stable/class/{0}?scrollTo={1}".format(
                objectClass[0]["name"], classProperty[0]["name"]
            )
            embed = discord.Embed(
                title=title, color=color, description=description, url=url
            )
            embed.add_field(
                name="type", value=classProperty[0]["type"][0][0][0], inline=False
            )

        # if the user inputted a method find which event it was and initiate the embed
        elif findMethod(objectClass, search) != []:

            classMethod = findMethod(objectClass, search)

            title = "{0}#{1}".format(objectClass[0]["name"], classMethod[0]["name"])
            description = classMethod[0]["description"]
            url = "https://discord.js.org/#/docs/main/stable/class/{0}?scrollTo={1}".format(
                objectClass[0]["name"], classMethod[0]["name"]
            )
            embed = discord.Embed(
                title=title, color=color, description=description, url=url
            )
            if not "examples" in classMethod[0]:
                if not "returns" in classMethod[0]:
                    pass
                else:
                    embed.add_field(
                        name="Returns",
                        value=classMethod[0]["returns"][0][0][0],
                        inline=False,
                    )
            else:
                if not "returns" in classMethod[0]:
                    embed.add_field(
                        name="Example",
                        value=classMethod[0]["examples"][0].replace("//", "```js\n")
                        + "```",
                        inline=False,
                    )
                else:
                    embed.add_field(
                        name="Example",
                        value=classMethod[0]["examples"][0].replace("//", "```js\n")
                        + "```",
                        inline=False,
                    )
                    embed.add_field(
                        name="Returns",
                        value=classMethod[0]["returns"][0][0][0],
                        inline=False,
                    )

        # if all else fails
        elif title is None:
            title = "No results"
            description = "What you were looking for probably does not exist"
            color = discord.Color.from_rgb(191, 38, 0)
            embed = discord.Embed(title=title, color=color, description=description)
        embed.set_author(
            name="Discord.js", icon_url="https://discord.js.org/static/logo-square.png"
        )
        await ctx.send(embed=embed)


# Make functions to find different Class options


def findProperty(objClass, searcher):

    m = list(
        filter(lambda y: y["name"].lower() == searcher[1].lower(), objClass[0]["props"])
    )
    return m


def findMethod(objClass, searcher):

    m = list(
        filter(
            lambda y: y["name"].lower() == searcher[1].lower(), objClass[0]["methods"]
        )
    )
    return m


def findEvent(objClass, searcher):

    m = list(
        filter(
            lambda y: y["name"].lower() == searcher[1].lower(), objClass[0]["events"]
        )
    )
    return m


def setup(bot):
    bot.add_cog(djs(bot))
