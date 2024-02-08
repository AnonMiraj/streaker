import discord
import os
from dotenv import load_dotenv
from funks import data_extractor
from database import add_record, create_tables_if_not_exist

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



create_tables_if_not_exist()
bot.load_extension('cogs.stats')
bot.run(os.getenv("TOKEN"))
