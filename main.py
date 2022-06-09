import random

import discord
import requests
from discord.ext import commands

client = commands.Bot(command_prefix=">")

async def call_api(query):
    url = "https://api.urbandictionary.com/v0/define"

    querystring = {"term":query}

    response = requests.request("GET", url, params=querystring)

    return response.json()

@client.listen()
async def on_message(message):
    if type(message.channel) == discord.DMChannel and message.author.id != client.user.id:
        try: 
            ml = message.content.split(' ')
            word = random.choice(ml)
            data = await call_api(word)
            base = data['list'][random.randint(0, len(data['list']))]
            defenition = base["definition"]
            example = base["example"]
            for char in defenition:
                if char in '[]':
                    defenition = defenition.replace(char, '')
            for char in example:
                if char in '[]':
                    example = example.replace(char, '')
            final = f"\"{word}\" - `{defenition}`\nFor example: {example}"
            await message.channel.send(final)
        except IndexError:
            await message.channel.send("The selected word could not be found")


client.run("Your token here", bot=False)
