# This example requires the 'message_content' intent.

import discord
import os
import aiohttp
import io
import asyncio

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

    if message.content.startswith('$1cat'):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://cataas.com/cat') as resp:
                if resp.status != 200:
                    return await message.channel.send('Could not download file...')
                data = io.BytesIO(await resp.read())
                await message.channel.send(file=discord.File(data, 'cool_image.png'))

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$rango'):  # pyright: ignore[reportUnknownMemberType]
        await message.channel.send(file=discord.File('images/rango.jpg', 'rango.jpg'))

    if message.content.startswith('$cat generator'):
        x = 0
        while True:
            x+=1
            async with aiohttp.ClientSession() as session:
                    async with session.get('https://cataas.com/cat') as resp:
                        print(x)
                        if resp.status != 200:
                            return await message.channel.send('Could not download file...')
                        data = io.BytesIO(await resp.read())
                        await message.channel.send(file=discord.File(data, 'cool_image.png'))
            try:
                stop_msg = await client.wait_for(
                    'message', 
                    timeout=2.5,
                    check=lambda m: (
                            m.channel == message.channel and
                            m.author == message.author and
                            m.content.lower().strip() == "$cat stealer"
                        )
                )
                if stop_msg:
                    await message.channel.send("Stopping. 🛑")
                    break
            except asyncio.TimeoutError:
                await asyncio.sleep(.1)

ant_bot_key = os.getenv('ANT_BOT_V1')
client.run(ant_bot_key)  # pyright: ignore[reportArgumentType]
