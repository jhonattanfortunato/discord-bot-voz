@bot.event
async def on_voice_state_update(member, before, after):
    if member.bot:
        return

    texto = None
    channel = None

    # Entrou em um canal
    if before.channel is None and after.channel is not None:
        channel = after.channel
        texto = f"{member.display_name} entrou"

    # Saiu de um canal
    elif before.channel is not None and after.channel is None:
        channel = before.channel
        texto = f"{member.display_name} saiu"

    # Mudou de canal
    elif before.channel != after.channel:
        channel = after.channel
        texto = f"{member.display_name} mudou de canal"

    if texto is None or channel is None:
        return

    vc = channel.guild.voice_client
    if vc is None or not vc.is_connected():
        vc = await channel.connect()
        await asyncio.sleep(1)

    tts = gTTS(text=texto, lang="pt-br")
    tts.save("voz.mp3")

    if vc.is_playing():
        vc.stop()

    vc.play(discord.FFmpegPCMAudio("voz.mp3"))
