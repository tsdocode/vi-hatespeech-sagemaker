# bot.py
import os

import discord
from dotenv import load_dotenv
import random

from predict import predict


def sentiment(text):
    sen = predict(text)['label']
    return sen

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()



@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    
    channel = client.get_channel(962051038548983871)
    await channel.send('Hello World!')

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    text = message.content
    if sentiment(text) in ['LABEL_1', 'LABEL_2']:
        mention = message.author.mention
        new_content = f"Negative from {mention}\nContent: {text}\nDeleted"
        await message.channel.send(new_content)
        await message.delete()
    else:
        await message.add_reaction("❤️")


client.run(TOKEN)