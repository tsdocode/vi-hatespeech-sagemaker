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
    await channel.send('Chú chó văn hoá is backkkkk :police_officer:')

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )


@client.event
async def on_message(message):
    CLASS_NAME = {
        'LABEL_1' : 'Ofensive',
        'LABEL_2' : 'Hate'
    }


    if message.author == client.user:
        return

    if message.content.startswith('.delete'):
        await message.channel.purge(limit=1000)
        return 

    text = message.content
    label = sentiment(text)
    if label in ['LABEL_1', 'LABEL_2']:
        mention = message.author.mention
        new_content = f"Negative from {mention}\nContent: {text}\nTYPE:{CLASS_NAME[label]}\nDeleted"
        await message.channel.send(new_content)
        await message.delete()
    else:
        await message.add_reaction("❤️")


client.run(TOKEN)
