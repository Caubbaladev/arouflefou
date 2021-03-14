import discord
from discord.ext import commands, tasks
from random import choice
import os
import tracemalloc
import youtube_dl
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix='!')
players = {}

status = ['Coca bien frais', 'Vos daronnes', 'PALALALA', 'Miami','Moula','Chicha Lounge']

@client.event
async def on_ready():
    tracemalloc.start()
    bot = client.user
    change_status.start()
    print(f"Connecté en tant que {bot}")

@client.command(name='ping', help='Indice de latence')
async def ping(ctx):
    await ctx.send(f"PALALA Latence: {round(client.latency * 1000)} ms")

@client.command()
async def joue(ctx, url : str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music to end or use the 'stop' command")
        return

    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
    await voiceChannel.connect()
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))


@client.command()
async def quitte(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")


@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")


@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()

@tasks.loop(seconds=20)
async def change_status():
    await client.change_presence(activity=discord.Game(choice(status)))

@client.event
async def on_message(message):
    bot = client.user
    if message.author == bot:
        return

    if "!clip" in message.content.lower():
        await message.channel.send(
            "https://www.youtube.com/watch?v=y1If9gVjLcs")
        await message.channel.send("bientot disque d'or chakal")
    greet = ("bjr", "BJR", "Bjr", "bonjour", "BONJOUR", "Bonjour", "slt",
             "Slt", "Salut", "salut", "SALUT", "wsh", "wesh", "WESH", "Wesh",
             "Wsh", "Hello", "HELLO", "HI", "Hi", "hello", "hi")
    if message.content.startswith(greet):
        await message.channel.send(
            "wsh les rageux c'est arouf le plus beau des rebeux")
        await message.channel.send("Commandes : spam Arouf(pote) !clip math !joue lien*")

    if message.content.startswith("spam"):
        await message.channel.send("quelle phrase bg ?")
        a = await client.wait_for('message')
        await message.channel.send("combien de fois bg ?")
        nb = await client.wait_for('message')
        nb = nb.content
        for i in range(int(nb)):
            await message.channel.send(a.content)
    if "sale" in message.content.lower():
        await message.channel.send(
            "https://media.tenor.com/images/1ff714f19eba6002e5a3dd5fdedad024/tenor.gif"
        )

    if message.content.startswith("Arouf"):
        await message.channel.send("Ouais?")
        pot = await client.wait_for("message")
        pot = pot.content
        if pot == "pote":
            await message.channel.send("ok")
            b = await client.wait_for("message")
            b = b.content
            if len(b) > 0:
                await message.channel.send("je suis d'accord")
        elif pot != "pote":
            await message.channel.send("sale pute")
    beau = ("t beau", "T beau", "T Beau", "T BEAU", "TU ES BEAU", "Tu es beau",
            "Le plus beau", "LE PLUS BEAU", "Lpb", "LPB", "TU ES BEAU",
            "tu es beau", "le plus beau", "lbp", "je t'aime", "jtm",
            "Je t'aime", "JTM", "JE T'AIME", "T'es beau", "T'ES BEAU",
            "Magnifique", "MAGNIFIQUE", "Je taime", "JE TAIME", "Je T'aime",
            "Je Taime", "t'es beau", "magnifique", "je taime", "je t aime")
    if message.content.startswith(beau):
        await message.channel.send("https://i.imgur.com/QI17fpm.gif")
    if message.content.startswith("math"):
        await message.channel.send("Tu veux que je fasse tes exos pd?")
        calc = await client.wait_for("message")
        calc = calc.content
        calc = calc.lower()
        if calc == "oe" or calc == "oui" or calc == "ouais" or calc == "oue" or calc == "ouai" or calc == "ui":
            await message.channel.send("(+) (-) (div) (*)")
            calc_form = await client.wait_for("message")
            calc_form = calc_form.content
            if calc_form == "+":
                await message.channel.send("Le premier chiffre")
                p1_plus = await client.wait_for("message")
                p1_plus = p1_plus.content
                await message.channel.send("Le deuxième chiffre")
                p2_plus = await client.wait_for("message")
                p2_plus = p2_plus.content
                await message.channel.send(f"{p1_plus} + {p2_plus}")
                p3_plus = int(p1_plus) + int(p2_plus)
                await message.channel.send(f"Le résultat est {p3_plus} ")
            if calc_form == "-":
                await message.channel.send("Le premier chiffre")
                p1_minus = await client.wait_for("message")
                p1_minus = p1_minus.content
                await message.channel.send("Le deuxième chiffre")
                p2_minus = await client.wait_for("message")
                p2_minus = p2_minus.content
                await message.channel.send(f"{p1_minus} - {p2_minus}")
                p3_minus = int(p1_minus) - int(p2_minus)
                await message.channel.send(f"Le résultat est {p3_minus}")
            if calc_form == "div":
                await message.channel.send("Le premier chiffre")
                p1_divide = await client.wait_for("message")
                p1_divide = p1_divide.content
                await message.channel.send("Le deuxième chiffre")
                p2_divide = await client.wait_for("message")
                p2_divide = p2_divide.content
                await message.channel.send(f"{p1_divide} / {p2_divide}")
                p3_divide = int(p1_divide) / int(p2_divide)
                await message.channel.send(f"Le résultat est {p3_divide}")
            if calc_form == "*":
                await message.channel.send("Le premier chiffre")
                p1_times = await client.wait_for("message")
                p1_times = p1_times.content
                await message.channel.send("Le deuxième chiffre")
                p2_times = await client.wait_for("message")
                p2_times = p2_times.content
                await message.channel.send(f"{p1_times} * {p2_times}")
                p3_times = int(p1_times) * int(p2_times)
                await message.channel.send(f"Le résultat est {p3_times}")
            await message.channel.send("Dis merci maintenant")
            merci = await client.wait_for("message")
            merci = merci.content
            merci = merci.lower()
            if len(merci) > 0:
                if merci == "mrc" or merci == "merci" or merci == "thx" or merci == "thanks" or merci == "bien vu" or merci == "bv":
                    await message.channel.send("C'est bien, je préfère.")
                else:
                    await message.channel.send("Suce ma queue")
    await client.process_commands(message)

keep_alive()
token = os.environ.get("DISCORD_BOT_SECRET")
client.run(os.getenv('TOKEN'))