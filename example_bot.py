# This example requires the 'message_content' intent.

import discord
import os
import aiohttp
import io

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$cat'):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://cataas.com/cat') as resp:
                if resp.status != 200:
                    return await message.channel.send('Could not download file...')
                data = io.BytesIO(await resp.read())
                await message.channel.send(file=discord.File(data, 'cool_image.png'))

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

ant_bot_key = os.getenv('ANT_BOT_V1')
print(ant_bot_key)
client.run(ant_bot_key)
