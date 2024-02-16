import discord
import os
from dotenv import load_dotenv
from funks import data_extractor
from database import add_trainee, add_record

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

allowed_users = [445594139506245635, 1202346286330683432, 1201245946265219092]


@bot.slash_command()
async def archive(ctx):
    if ctx.author.id not in allowed_users:
        await ctx.send("Sorry, you are not allowed to use this command.", delete_after=25)
        return

    channel = ctx.channel

    api_key = os.getenv("API")

    async with ctx.typing():
        messages_data = []
        async for message in channel.history(limit=None):
            message: discord.Message = message
            data = data_extractor(str(message.content).upper())
            if data.get("streak") is not None:
                record_data = {
                    "discord_id": str(message.author.id),
                    "post_date": message.created_at.isoformat(),
                    "message": message.content,
                    "streak": data["streak"],
                    "today_problems": data["today"],
                }
                messages_data.append(record_data)
                if data["streak"] == 0:
                    trainee_data = {
                        "discord_id": str(message.author.id),
                        "discord_pfp": str(message.author.display_avatar.url),
                        "discord_name": message.author.name
                    }
                    add_trainee(trainee_data, api_key)

        for record in reversed(messages_data):
            add_record(record, api_key)

    await ctx.send("Channel archived. Check database")

# bot.load_extension('cogs.stats')
bot.run(os.getenv("TOKEN"))
