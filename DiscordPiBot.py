## Installation via terminal Python
# py -3 -m pip install -U discord.py==2.0.0
# py -3 -m pip install -U python-decouple
# py -3 -m pip install -U requests
# py -3 -m pip install -U ffmpeg-python
# py -3 -m pip install -U ffmpeg #KO

import sys
import discord
from discord.ext import commands
from discord.utils import get
from decouple import config
import random
import requests
import os
import asyncio

# import ffmpeg
from pydub import AudioSegment
from pydub.playback import play

# Vérifie si le dossier 'photos' existe, sinon le crée
if not os.path.exists('photos'):
    os.makedirs('photos')

# Vérifie si le dossier 'sounds' existe, sinon le crée
if not os.path.exists('sounds'):
    os.makedirs('sounds')

token = config('DISCORD_TOKEN') # Ajouter cette variable dans le fichier .env
if token is None:
    print("La variable d'environnement DISCORD_TOKEN n'est pas définie dans le fichier .env.")
    sys.exit(1)  # Arrête le programme avec un code d'erreur non nul

intents = discord.Intents.all()
client = discord.Client(intents=intents)

bot = commands.Bot(command_prefix='!', intents=intents)

# Liste pour stocker les photos enregistrées
saved_photos = []

@bot.event
async def on_ready():
    print(f'Connecté en tant que {bot.user.name}')

@bot.command()
async def saluer(ctx):
    await ctx.send(f'Salut {ctx.author.mention} ! Je suis un bot Discord.')

@bot.command()
async def effacer(ctx, nombre: int):
    await ctx.channel.purge(limit=nombre+1)
    await ctx.send(f'Effacé {nombre} messages.')

@bot.command()
async def sondage(ctx, question, *options):
    if len(options) < 2:
        await ctx.send("Veuillez fournir au moins deux options pour le sondage.")
        return

    formatted_options = [f"{index+1}. {option}" for index, option in enumerate(options)]
    options_text = "\n".join(formatted_options)

    embed = discord.Embed(title="Sondage", description=question, color=discord.Color.blue())
    embed.add_field(name="Options", value=options_text, inline=False)
    embed.set_footer(text=f"Sondage créé par {ctx.author.name}")

    message = await ctx.send(embed=embed)

    for index in range(len(options)):
        await message.add_reaction(chr(0x31 + index))  # Unicode pour les réactions de 1 à 9

@bot.command()
async def de(ctx, faces: int = 6):
    if faces < 2:
        await ctx.send("Le dé doit avoir au moins 2 faces.")
        return

    resultat = random.randint(1, faces)
    await ctx.send(f"Lancé de dé : {resultat}")

@bot.command()
async def chien(ctx):
    response = requests.get('https://dog.ceo/api/breeds/image/random')
    if response.status_code == 200:
        data = response.json()
        image_url = data['message']
        embed = discord.Embed(title="Chien", color=discord.Color.green())
        embed.set_image(url=image_url)
        await ctx.send(embed=embed)
    else:
        await ctx.send("Impossible de récupérer une image de chien.")

@bot.command()
async def chat(ctx):
    try:
        response = requests.get('https://api.thecatapi.com/v1/images/search')
        data = response.json()
        image_url = data[0]['url']
        embed = discord.Embed(title="Image de chat aléatoire", color=discord.Color.dark_gold())
        embed.set_image(url=image_url)
        await ctx.send(embed=embed)
    except requests.exceptions.RequestException:
        await ctx.send("Impossible de récupérer une image de chat.")

@bot.command()
async def meteo(ctx, ville=None):
    if ville is None:
        await ctx.send("Veuillez spécifier une ville.")
        ville = "Paris"

    # Récupérer la clé d'API de la variable d'environnement
    api_key = config('OPENWEATHERMAP_API_KEY')

    url = f'http://api.openweathermap.org/data/2.5/weather?q={ville}&appid={api_key}&units=metric'
    response = requests.get(url)
    data = response.json()

    if data['cod'] == 200:
        city = data['name']
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        sunshine = "Oui" if 'sun' in data['weather'][0]['icon'] else "Non"

        temperature = round(temperature)  # Arrondir la température à l'entier le plus proche

        await ctx.send(f"**Météo à {city}**\nTempérature : {temperature}°C\nHumidité : {humidity}%\nEnsoleillement : {sunshine}")
    else:
        await ctx.send("Impossible de récupérer les informations météorologiques pour cette ville.")


@bot.command()
async def savephoto(ctx):
    # Vérifie si un fichier image est attaché au message
    if len(ctx.message.attachments) > 0:
        attachment = ctx.message.attachments[0]
        if attachment.content_type.startswith('image/'):
            # Télécharge et enregistre l'image dans un dossier local
            await attachment.save(f'photos/{attachment.filename}')
            saved_photos.append(attachment.filename)
            await ctx.send(f"La photo a été enregistrée avec succès.")
        else:
            await ctx.send("Veuillez envoyer une image valide.")
    else:
        await ctx.send("Veuillez envoyer une image en tant que pièce jointe.")

@bot.command()
async def showrandomphoto(ctx):
    if len(saved_photos) > 0:
        # Sélectionne aléatoirement une photo parmi celles enregistrées
        random_photo = random.choice(saved_photos)
        # Charge l'image depuis le dossier local
        with open(f'photos/{random_photo}', 'rb') as file:
            # Crée un objet File à partir de l'image
            photo = discord.File(file)
            # Envoie l'image dans le canal Discord
            await ctx.send(file=photo)
    else:
        await ctx.send("Aucune photo enregistrée.")


@bot.command()
async def savesound(ctx, name: str):
    # Vérifie si l'utilisateur a joint un fichier audio
    if len(ctx.message.attachments) == 0:
        await ctx.send("Veuillez joindre un fichier audio.")
        return

    attachment = ctx.message.attachments[0]

    # Vérifie si le fichier est au format mp3 ou wav
    if not attachment.filename.endswith('.mp3') and not attachment.filename.endswith('.wav'):
        await ctx.send("Veuillez envoyer un fichier audio au format .mp3 ou .wav.")
        return

    # Enregistre le fichier avec le nom spécifié
    await attachment.save(f'sounds/{name}{attachment.filename[-4:]}')
    await ctx.send(f"Le son a été enregistré sous le nom {name}{attachment.filename[-4:]}.")

@bot.command()
async def playsound(ctx, name):
    voice_state = ctx.author.voice

    if voice_state is None or voice_state.channel is None:
        await ctx.send("Vous devez être connecté à un salon vocal pour utiliser cette commande.")
        return

    voice_channel = voice_state.channel
    voice_client = ctx.voice_client

    if voice_client is not None and voice_client.is_connected():
        if voice_client.channel == voice_channel:
            print("Le bot est déjà connecté à votre salon vocal.")

            if voice_client.is_playing():
                await ctx.send("Le bot est déjà en train de jouer un son.")
                print("Le bot est déjà en train de jouer un son.")
                return
        else:
            await voice_client.disconnect()
            await voice_channel.connect(self_mute = False)
    else:
        await voice_channel.connect(self_mute = False)

    audio_source = discord.FFmpegPCMAudio(f'sounds/{name}.mp3')
    voice_client = ctx.voice_client
    voice_client.play(audio_source)

    await ctx.send(f"Joue le son : {name}")


# Lister les fichiers audio

# Automatiser le pull / update du code + restart du programme => voir histo GPT

# Generer / Uploader aleat rec Glados

# Controler GPIO PI

@bot.command()
async def logout(ctx):
    await bot.close()

@bot.command()
async def restart(ctx):
    if str(config('MON_ID_UTILISATEUR'))  == str(ctx.author.id):
        await ctx.send("Redémarrage en cours...")

        python = sys.executable
        os.execl(python, python, *sys.argv)

        # Arrêter l'exécution du code ici pour éviter les doublons de processus
        return

    else:
        await ctx.send("Vous n'êtes pas autorisé à utiliser cette commande.")


# Lancement du bot
bot.run(token)
