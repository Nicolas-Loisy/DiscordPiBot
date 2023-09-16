#!/usr/bin/env python3

## Installation via terminal Python
# py -3 -m pip install -U discord.py==2.0.0
# py -3 -m pip install -U python-decouple
# py -3 -m pip install -U requests
# py -3 -m pip install -U ffmpeg-python
# py -3 -m pip install -U ffmpeg #KO
# py -3 -m pip install -U gitpython

import sys
import discord
from discord.ext import commands
from discord.utils import get
from decouple import config

from commands import admin
from commands import tools
from commands import picturesAndSounds


# Ajouter cette variable dans le fichier .env
token = config('DISCORD_TOKEN') 
if token is None:
    print("La variable d'environnement DISCORD_TOKEN n'est pas définie dans le fichier .env.")
    sys.exit(1)  # Arrête le programme avec un code d'erreur non nul

intents = discord.Intents.all()
client = discord.Client(intents=intents)

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Connecté en tant que {bot.user.name}')

@commands.command()
async def logout(ctx):
    if str(config('MON_ID_UTILISATEUR'))  == str(ctx.author.id):
        await bot.close()
    else:
        await ctx.send("Vous n'êtes pas autorisé à utiliser cette commande.")



# Ajoutez vos commandes au bot
bot.add_command(logout)
admin.setup(bot)
tools.setup(bot)
picturesAndSounds.setup(bot)


# Lancement du bot
bot.run(token)
