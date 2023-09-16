from discord.ext import commands
import discord
import random
from decouple import config
import requests


def setup(bot):
    bot.add_command(ping)
    bot.add_command(saluer)
    bot.add_command(effacer)
    bot.add_command(sondage)
    bot.add_command(de)
    bot.add_command(meteo)

@commands.command()
async def ping(ctx):
    latency = round(ctx.bot.latency * 1000)  # Ping en millisecondes
    await ctx.send(f'Pong ! Latence : {latency} ms')

@commands.command()
async def saluer(ctx):
    await ctx.send(f'Salut {ctx.author.mention} ! Je suis un bot Discord.')

@commands.command()
async def effacer(ctx, nombre: int):
    await ctx.channel.purge(limit=nombre+1)
    await ctx.send(f'Effacé {nombre} messages.')

@commands.command()
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

@commands.command()
async def de(ctx, faces: int = 6):
    if faces < 2:
        await ctx.send("Le dé doit avoir au moins 2 faces.")
        return

    resultat = random.randint(1, faces)
    await ctx.send(f"Lancé de dé : {resultat}")

@commands.command()
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
