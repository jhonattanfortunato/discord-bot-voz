import discord
from discord.ext import commands
from gtts import gTTS
import asyncio
import os

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')

@bot.event
async def on_voice_state_update(member, before, after):
    if member.bot:
        return

    if before.channel is None and after.channel is not None:
        channel = after.channel
        texto = f"{member.display_name} entrou"

    elif before.channel is not None and after.channel is None:
        channel = before.channel
        texto = f"{member.display_name} saiu"

    else:
        return

    vc = channel.guild.voice_client
    if vc is None:
        vc = await channel.connect()
        await asyncio.sleep(1)

    tts = gTTS(text=texto, lang="pt-br", slow=False)
    tts.save("voz.mp3")

    if vc.is_playing():
        vc.stop()

    vc.play(discord.FFmpegPCMAudio("voz.mp3"))

bot.run(TOKEN)