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

# Guarda se o bot está ativo por servidor
bot_ativo = {}

@bot.event
async def on_ready():
    print(f"🤖 Bot conectado como {bot.user}")

# 🔊 Ligar bot
@bot.command()
@commands.has_permissions(administrator=True)
async def ligar(ctx):
    bot_ativo[ctx.guild.id] = True
    await ctx.send("🔊 Bot de voz **ligado**")

# 🔇 Desligar bot
@bot.command()
@commands.has_permissions(administrator=True)
async def desligar(ctx):
    bot_ativo[ctx.guild.id] = False
    vc = ctx.guild.voice_client
    if vc and vc.is_connected():
        await vc.disconnect()
    await ctx.send("🔇 Bot de voz **desligado**")

@bot.event
async def on_voice_state_update(member, before, after):
    if member.bot:
        return

    if not bot_ativo.get(member.guild.id, False):
        return

    guild = member.guild
    afk_channel = guild.afk_channel

    texto = None
    canal_destino = None

    # Entrou no canal
    if before.channel is None and after.channel is not None:
        if after.channel == afk_channel:
            return
        canal_destino = after.channel
        texto = f"{member.display_name} entrou"

    # Saiu do canal
    elif before.channel is not None and after.channel is None:
        if before.channel == afk_channel:
            return
        canal_destino = before.channel
        texto = f"{member.display_name} saiu"

    # Mudou de canal
    elif before.channel and after.channel and before.channel != after.channel:

        # Foi movido para AFK
        if after.channel == afk_channel:
            canal_destino = before.channel
            texto = f"{member.display_name} foi movido para o AFK"

        # Mudança normal
        elif before.channel != afk_channel:
            canal_destino = after.channel
            texto = f"{member.display_name} mudou"

        else:
            return
    else:
        return

    await asyncio.sleep(0.5)

    try:
        vc = await canal_destino.connect()

        tts = gTTS(text=texto, lang="pt-br")
        tts.save("voz.mp3")

        vc.play(discord.FFmpegPCMAudio("voz.mp3"))

        # ⏳ Espera terminar de falar
        while vc.is_playing():
            await asyncio.sleep(0.2)

        # 🔌 Desconecta após falar
        await vc.disconnect()

    except Exception as e:
        print("❌ Erro no bot de voz:", e)

bot.run(TOKEN)