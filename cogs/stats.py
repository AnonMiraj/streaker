import discord
from discord.ext import commands
from database import Stats
from tabulate import tabulate
from funks import checkisinstance


class stats(commands.Cog):  # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(
        self, bot
    ):  # this is a special method that is called when the cog is loaded
        self.bot = bot

    @discord.slash_command()
    async def top(self, ctx: discord.ApplicationContext):


        async with ctx.typing():
            # Header for the table
            headers = ["RANK", "MEMVER", "PROBLEMS", "STREAK"]
            stat10 = tabulate(Stats.top_ten(), headers=headers, tablefmt="double_grid")

            embed = discord.Embed(
            title=f"leader boards",
            color=discord.Colour.blurple(),
            description=f"```{stat10}```",
            )

        await ctx.send(embed=embed)

    @discord.slash_command()
    async def stats(self, ctx: discord.ApplicationContext):
        # Defer the response while fetching data to not timeout
        await ctx.defer()

        # Create an embed to display stats
        embed = discord.Embed(
            title=f"Streaker {ctx.guild.name} stats", color=discord.Colour.blurple()
        )

        # Fetch and add data for the top streaker
        top_streaker = Stats.highest_streaker()
        embed = checkisinstance(
            embed=embed,
            title="Top Streaker",
            value_title="streaks",
            obj=top_streaker,
            objx=tuple,
        )

        embed.add_field(name="-", value="", inline=False)

        # Fetch and add data for the highest current streaker
        highest_current_streaker = Stats.highest_current_streaker()
        embed = checkisinstance(
            embed=embed,
            title="Top current Streaker",
            value_title="streaks",
            obj=highest_current_streaker,
            objx=tuple,
        )

        embed.add_field(name="-", value="", inline=False)

        # Fetch and add data for the highest problems solver
        highest_problems_solver = Stats.highest_problems_solver()
        embed = checkisinstance(
            embed=embed,
            title="most problems sovled",
            value_title="problems solved",
            obj=highest_problems_solver,
            objx=tuple,
        )

        # Set a footer with a competition invitation URL
        embed.set_footer(text="compete with us on https://streaker.com (example url)")

        # Send the embed as a response
        await ctx.followup.send(embed=embed)


def setup(bot):  # this is called by Pycord to setup the cog
    bot.add_cog(stats(bot))  # add the cog to the bot
