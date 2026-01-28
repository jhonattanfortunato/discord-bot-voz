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
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"🤖 Bot conectado como {bot.user}")

@bot.event
async def on_voice_state_update(member, before, after):
    if member.bot:
        return

    texto = None
    canal_destino = None

    # Entrou no canal
    if before.channel is None and after.channel is not None:
        canal_destino = after.channel
        texto = f"{member.display_name} entrou"

    # Saiu do canal
    elif before.channel is not None and after.channel is None:
        canal_destino = before.channel
        texto = f"{member.display_name} saiu"

    # Mudou de canal
    elif before.channel and after.channel and before.channel != after.channel:
        canal_destino = after.channel
        texto = f"{member.display_name} mudou"

    else:
        return

    await asyncio.sleep(0.5)

    vc = canal_destino.guild.voice_client

    try:
        if vc is None:
            vc = await canal_destino.connect()
        elif vc.channel != canal_destino:
            await vc.move_to(canal_destino)

        tts = gTTS(text=texto, lang="pt-br")
        tts.save("voz.mp3")

        if vc.is_playing():
            vc.stop()

        vc.play(discord.FFmpegPCMAudio("voz.mp3"))

    except Exception as e:
        print("❌ Erro no bot de voz:", e)

bot.run(TOKEN)
