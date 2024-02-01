import discord
import os
import csv
from dotenv import load_dotenv

load_dotenv()
bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

@bot.slash_command()
async def archive(ctx):
    channel = ctx.channel
    
    async with ctx.typing():
        messages_data = []
        async for message in channel.history(limit=None):
            messages_data.append([message.author.name, message.content])

        # TODO the csv will be user_id,user_name,the date of the message , the amount of problems he did in that day 
        # idk what else but for now this will work
        filename = f"{channel.name}-archive.csv"
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Author", "Message"])
            writer.writerows(messages_data)

    await ctx.send(f"Channel archived. Check {filename}")
# TODO on message even for that channle that adds to the csv
# and if an edit happend it also edit the csv 
bot.run(os.getenv('TOKEN')) 
