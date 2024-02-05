import discord
import os
from dotenv import load_dotenv
from funks import data_extractor, checkisinstance
from database import add_record, create_tables_if_not_exist, Stats
import datetime

load_dotenv()
bot = discord.Bot()


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")


# @bot.event
# async def on_message(msg: discord.Message):
#     if get_config()["auto_mode"] == True:
#         # checks that the message in a channel the user wants to arhive
#         if msg.channel.id in list(get_config()["channels"]):
#             data: dict = data_extractor(msg.channel)
#             return data

# TODO make this auto_mode thingy work


@bot.slash_command()
async def archive(ctx):
    channel = ctx.channel

    async with ctx.typing():
        messages_data = []
        async for message in channel.history(limit=None):
            message: discord.Message = message
            data = data_extractor(str(message.content))
            print(data)
            if data.get("streak") is not None:
                messages_data.append(
                    [
                        str(message.author.id),
                        message.author.name,
                        message.created_at.strftime("%Y-%m-%d"),
                        message.content,
                        data["streak"],
                        data["today"],
                    ]
                )

        for record in messages_data:
            print(record)
            add_record(record)

        """
            [discord_id                       discord_name                             message                                   message date                                      streak                    days                problems             practiced_day

            [the discord id of the author ||  the discord name of the author        ||  the raw string content of the message ||  the date of the message in [YYYY-MM-DD] format || the streak of the user || days of the user ||  problems he solved ||  how many he solved in that day
            """
    await ctx.send("Channel archived. Check database")


# TODO on message event for that channle that adds to the csv
# and if an edit happend it also edit the csv


@bot.slash_command()
async def stats(ctx: discord.ApplicationContext):
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


create_tables_if_not_exist()
bot.run(os.getenv("TOKEN"))
