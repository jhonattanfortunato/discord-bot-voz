@bot.event
async def on_voice_state_update(member, before, after):
    if member.bot:
        return

    texto = None
    canal_destino = None

    # Entrou em canal
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
        texto = f"{member.display_name} mudou de canal"

    else:
        return

    # 🔴 GARANTE que existe canal
    if canal_destino is None:
        return

    # 🔴 ESPERA o Discord atualizar o estado
    await asyncio.sleep(0.5)

    vc = canal_destino.guild.voice_client

    try:
        if vc is None:
            vc = await canal_destino.connect(timeout=10)
        elif vc.channel != canal_destino:
            await vc.move_to(canal_destino)

        tts = gTTS(text=texto, lang="pt-br")
        tts.save("voz.mp3")

        if vc.is_playing():
            vc.stop()

        vc.play(discord.FFmpegPCMAudio("voz.mp3"))

    except Exception as e:
        print("Erro ao entrar ou falar no canal:", e)