import discord
from discord.ext import commands
import asyncio
import os
import pyttsx3

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# 🔊 Controle global
bot_ativo = True

# 🎙️ Configuração da voz
engine = pyttsx3.init()
engine.setProperty("rate", 165)  # velocidade da fala
engine.setProperty("volume", 1.0)

def falar(texto):
    engine.save_to_file(texto, "voz.wav")
    engine.runAndWait()

@bot.event
async def on_ready():
    print(f"🤖 Bot online como {bot.user}")

# 🧩 COMANDOS
@bot.command()
@commands.has_permissions(administrator=True)
async def ligar(ctx):
    global bot_ativo
    bot_ativo = True
    await ctx.send("🔊 Bot de voz **LIGADO**")

@bot.command()
@commands.has_permissions(administrator=True)
async def desligar(ctx):
    global bot_ativo
    bot_ativo = False
    if ctx.guild.voice_client:
        await ctx.guild.voice_client.disconnect()
    await ctx.send("🔇 Bot de voz **DESLIGADO**")

@bot.event
async def on_voice_state_update(member, before, after):
    if member.bot or not bot_ativo:
        return

    texto = None
    canal_destino = None

    # Entrou
    if before.channel is None and after.channel is not None:
        canal_destino = after.channel
        texto = f"{member.display_name} entrou no canal"

    # Saiu
    elif before.channel is not None and after.channel is None:
        canal_destino = before.channel
        texto = f"{member.display_name} saiu do canal"

    # Mudou
    elif before.channel and after.channel and before.channel != after.channel:
        canal_destino = after.channel
        texto = f"{member.display_name} mudou de canal"

    else:
        return

    await asyncio.sleep(0.5)

    vc = canal_destino.guild.voice_client

    try:
        if vc is None:
            vc = await canal_destino.connect()
        elif vc.channel != canal_destino:
            await vc.move_to(canal_destino)

        falar(texto)

        if vc.is_playing():
            vc.stop()

        vc.play(discord.FFmpegPCMAudio("voz.wav"))

    except Exception as e:
        print("❌ Erro no bot:", e)

bot.run(TOKEN)
