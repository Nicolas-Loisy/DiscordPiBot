from discord.ext import commands
import discord
import os
import requests
import random

# import ffmpeg
from pydub import AudioSegment
from pydub.playback import play


SOUND_PATH = "data/sounds"
IMG_PATH = "data/photos"


# Vérifie si le dossier 'photos' existe, sinon le crée
if not os.path.exists(IMG_PATH):
    os.makedirs(IMG_PATH)

# Vérifie si le dossier 'sounds' existe, sinon le crée
if not os.path.exists(SOUND_PATH):
    os.makedirs(SOUND_PATH)

def setup(bot):
    bot.add_command(chien)
    bot.add_command(chat)
    bot.add_command(savephoto)
    bot.add_command(listphotos)
    bot.add_command(showrandomphoto)
    bot.add_command(savesound)
    bot.add_command(playsound)
    bot.add_command(listtracks)
    

# Liste pour stocker les photos enregistrées
saved_photos = []

@commands.command()
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

@commands.command()
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

@commands.command()
async def savephoto(ctx):
    # Vérifie si un fichier image est attaché au message
    if len(ctx.message.attachments) > 0:
        attachment = ctx.message.attachments[0]
        if attachment.content_type.startswith('image/'):
            # Télécharge et enregistre l'image dans un dossier local
            await attachment.save(f'{IMG_PATH}/{attachment.filename}')
            saved_photos.append(attachment.filename)
            await ctx.send(f"La photo a été enregistrée avec succès.")
        else:
            await ctx.send("Veuillez envoyer une image valide.")
    else:
        await ctx.send("Veuillez envoyer une image en tant que pièce jointe.")

@commands.command()
async def listphotos(ctx):
    if saved_photos:
        photo_list = "\n".join(saved_photos)
        await ctx.send(f"Images enregistrées :\n{photo_list}")
    else:
        await ctx.send("Aucune image enregistrée n'a été trouvée.")

@commands.command()
async def showrandomphoto(ctx):
    if len(saved_photos) > 0:
        # Sélectionne aléatoirement une photo parmi celles enregistrées
        random_photo = random.choice(saved_photos)
        # Charge l'image depuis le dossier local
        with open(f'{IMG_PATH}/{random_photo}', 'rb') as file:
            # Crée un objet File à partir de l'image
            photo = discord.File(file)
            # Envoie l'image dans le canal Discord
            await ctx.send(file=photo)
    else:
        await ctx.send("Aucune photo enregistrée.")


@commands.command()
async def savesound(ctx, name: str):
    # Vérifie si l'utilisateur a joint un fichier audio
    if len(ctx.message.attachments) == 0:
        await ctx.send("Veuillez joindre un fichier audio en utilisant la commande `!savesound <nom>`.")
        return

    attachment = ctx.message.attachments[0]

    # Vérifie si le fichier est au format mp3 ou wav
    if not attachment.filename.endswith('.mp3') and not attachment.filename.endswith('.wav'):
        await ctx.send("Veuillez envoyer un fichier audio au format .mp3 ou .wav.")
        return

    # Enregistre le fichier avec le nom spécifié
    await attachment.save(f'{SOUND_PATH}/{name}{attachment.filename[-4:]}')
    await ctx.send(f"Le son a été enregistré sous le nom {name}{attachment.filename[-4:]}.")

    # Exemple d'utilisation : !savesound nom_du_son

@commands.command()
async def playsound(ctx, name):
    voice_state = ctx.author.voice

    if voice_state is None or voice_state.channel is None:
        await ctx.send("Vous devez être connecté à un salon vocal pour utiliser cette commande.")
        return

    voice_channel = voice_state.channel
    voice_client = ctx.voice_client

    if voice_client is not None:
        if voice_client.channel != voice_channel:
            await voice_client.move_to(voice_channel)
    else:
        await voice_channel.connect(self_mute=False)

    file_path = '{SOUND_PATH}/{name}.mp3'
    if not os.path.exists(file_path):
        await ctx.send(f"Le fichier audio '{name}' n'existe pas.")
        return

    audio_source = discord.FFmpegPCMAudio(file_path)
    voice_client = ctx.voice_client
    voice_client.play(audio_source)

    await ctx.send(f"Joue le son : {name}")


@commands.command()
async def listtracks(ctx):
    sound_dir = '{SOUND_PATH}/'  # Répertoire où sont stockés les fichiers audio

    # Vérifie si le répertoire existe
    if not os.path.exists(sound_dir):
        await ctx.send("Aucun répertoire de sons trouvé.")
        return

    # Liste les fichiers audio dans le répertoire
    sound_files = [f.split('.')[0] for f in os.listdir(sound_dir) if f.endswith('.mp3')]

    if not sound_files:
        await ctx.send("Aucun fichier audio trouvé dans le répertoire.")
    else:
        await ctx.send("Liste des pistes disponibles : \n" + "\n".join(sound_files))
