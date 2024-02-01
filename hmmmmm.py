import discord
import os
import csv
from dotenv import load_dotenv
from funks import get_config,data_extractor



load_dotenv()
bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")


@bot.event
async def on_message(msg:discord.Message):
    if get_config()["auto_mode"] == True:
        # checks that the message in a channel the user wants to arhive 
        if msg.channel.id in list(get_config()["channels"]): 
            data:dict = data_extractor(msg.channel)
            return data 

    #TODO make this auto_mode thingy work
 
            

@bot.slash_command()
async def archive(ctx):
    channel = ctx.channel
    
    async with ctx.typing():
        messages_data = []
        async for message in channel.history(limit=None):
            message:discord.Message = message 
            data = data_extractor(str(message.content))
            print(data)
            if any(data):
                messages_data.append([message.author.id, message.content,str(message.created_at.isoformat()),data["streak"],data["days"],data["problems"],(data["today"])])
        # TODO 
        filename = f"{channel.name}-archive.csv"
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Author", "Message","Message date","streak","days","problems","practiced_day"]) 

            """
            [Author                           Message                                   Message Date                                      streak                    days                problems             practiced_day
            
            [the discord id of the author ||  the raw string content of the message ||  the date of the message in [YYYY-MM-DD] format || the streak of the user || days of the user ||  problems he solved ||  how many he solved in that day
            """

            writer.writerows(messages_data)

    await ctx.send(f"Channel archived. Check {filename}",ephemeral=True)
# TODO on message even for that channle that adds to the csv
# and if an edit happend it also edit the csv 
bot.run(os.getenv('TOKEN')) 


# a bit messy. iam going to eat, good luck.