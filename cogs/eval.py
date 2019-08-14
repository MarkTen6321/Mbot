import discord
from discord.ext import commands
import ast
import json

config = json.load(open("./config.json", "r"))

# Credit : https://gist.github.com/nitros12/2c3c265813121492655bc95aa54da6b9


def add_returns(body):
    # Add return if last line is expression
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])  # Dunno what does this do TBH

    # Add return for if blocks and else blocks
    if isinstance(body[-1], ast.If):
        add_returns(body[-1].body)
        add_returns(body[-1].orelse)

    # Finally add returns for with blocks
    if isinstance(body[-1], ast.With):
        add_returns(body[-1].body)


async def is_owner(ctx):
    return str(ctx.author.id) in config["eval_allowed"]


class evilEval(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check(is_owner)
    async def evalCode(self, ctx, *, code):
        # Dont allow commands with Blocked Words
        blocked_words = [
            ".delete()",
            "os",
            "subprocess",
            "history()",
            "token",
            "kick",
            "ban",
        ]
        for blocked_word in blocked_words:
            if blocked_word in code:
                color = discord.Color.from_rgb(200, 0, 0)
                embed = discord.Embed(title="Blocked Keyword!", color=color)
                return await ctx.send(embed=embed)
        # Functions name around which we will wrap our code
        fn_name = "the_Evil_eval_function"
        # Removes the ```
        code = code.strip("` ")
        # Splits at newline characters and adds spaces
        # Then Joins them with new like chars again
        code = "\n".join(f"  {i}" for i in code.splitlines())
        # Wrap the whole code in an async Function
        body = f"async def {fn_name}():\n{code}"
        # Parsed into node so that add_returns can be used
        parsed = ast.parse(body)
        body = parsed.body[0].body
        add_returns(body)
        # Our codes Global environment
        env = {
            "bot": ctx.bot,
            "discord": discord,
            "commands": commands,
            "ctx": ctx,
            "__import__": __import__,
        }
        # We convert the node into a Function that can be called
        exec(compile(parsed, filename="<ast>", mode="exec"), env)
        stringify = lambda x: f"```{str(x)}```"
        # We use the same global var as of the function to run it
        # And wrap it in try-except block to catch the exceptions
        try:
            result = await eval(f"{fn_name}()", env)
        except Exception as err:
            color = discord.Color.from_rgb(200, 0, 0)
            embed = discord.Embed(
                title="Error:", description=stringify(err), color=color
            )
            await ctx.send(embed=embed)
        else:
            color = discord.Color.from_rgb(0, 200, 150)
            embed = discord.Embed(
                title="Result:", description=stringify(result), color=color
            )
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(evilEval(bot))
