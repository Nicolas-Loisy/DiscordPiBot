## Installation via terminal Python
# py -3 -m pip install -U discord.py==2.0.0
# py -3 -m pip install -U python-decouple

import sys
import discord
from discord.ext import commands
from decouple import config

token = config('DISCORD_TOKEN') # Ajouter cette variable dans le fichier .env
if token is None:
    print("La variable d'environnement DISCORD_TOKEN n'est pas définie dans le fichier .env.")
    sys.exit(1)  # Arrête le programme avec un code d'erreur non nul

intents = discord.Intents.all()
client = discord.Client(intents=intents)

bot = commands.Bot(command_prefix='!', intents=intents)

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


# Generer / Uploader aleat rec Glados

# Controler GPIO PI


bot.run(token)
