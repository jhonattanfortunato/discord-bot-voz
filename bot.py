@bot.event
async def on_voice_state_update(member, before, after):
    if member.bot:
        return

    texto = None
    canal_destino = None

    # Entrou em um canal
    if before.channel is None and after.channel is not None:
        canal_destino = after.channel
        texto = f"{member.display_name} entrou no canal"

    # Saiu do canal
    elif before.channel is not None and after.channel is None:
        canal_destino = before.channel
        texto = f"{member.display_name} saiu do canal"

    # Mudou de canal
    elif before.channel is not None and after.channel is not None and before.channel != after.channel:
        canal_destino = after.channel
        texto = f"{member.display_name} mudou de canal"

    else:
        return

    vc = canal_destino.guild.voice_client

    # Se o bot já estiver conectado em outro canal, move ele
    if vc and vc.is_connected():
        if vc.channel != canal_destino:
            await vc.move_to(canal_destino)
    else:
        vc = await canal_destino.connect()
        await asyncio.sleep(1)

    tts = gTTS(text=texto, lang="pt-br", slow=False)
    tts.save("voz.mp3")

    if vc.is_playing():
        vc.stop()

    vc.play(discord.FFmpegPCMAudio("voz.mp3"))
