import discord
import asyncio
import os # default module

from dotenv import load_dotenv
load_dotenv()



class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user}')
        print('------')



intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(str(os.getenv("TOKEN")))
