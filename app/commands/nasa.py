from discord.ext import commands
from decouple import config
import requests


def setup(bot):
    bot.add_command(asteroides)
    bot.add_command(terre)
    bot.add_command(terreAll)
    bot.add_command(apod)
    bot.add_command(mars)
    bot.add_command(nasa)

@commands.command()
async def asteroides(ctx):
    # Utilisation de l'API de la NASA pour obtenir des informations sur les astéroïdes
    api_key = config('NASA_API_KEY')

    url = f'https://api.nasa.gov/neo/rest/v1/feed?start_date=2023-09-27&end_date=2023-09-28&api_key={api_key}'
    response = requests.get(url)
    data = response.json()

    if 'element_count' in data:
        element_count = data['element_count']
        await ctx.send(f"Il y a {element_count} astéroïdes proches de la Terre dans cette période.")
    else:
        await ctx.send("Impossible de récupérer les informations sur les astéroïdes.")


@commands.command()
async def terre(ctx):
    # Utilisation de l'API de la NASA pour obtenir des images EPIC (Earth Polychromatic Imaging Camera)
    api_key = config('NASA_API_KEY')

    url = f'https://api.nasa.gov/EPIC/api/natural/images?api_key={api_key}'
    response = requests.get(url)
    data = response.json()

    if data:
        images = data
        if images:
            image_data = images[0]
            # Extraire les informations de date de l'image
            date = image_data['date'].split()[0]  # Format de la date : YYYY-MM-DD
            year, month, day = date.split('-')

            # Construire l'URL complète de l'image à partir du nom de fichier
            image_name = image_data['image']
            archive_url = f'https://epic.gsfc.nasa.gov/archive/natural/{year}/{month}/{day}/png/'
            image_url = archive_url + image_name + ".png"
            await ctx.send(f"Voici une image EPIC de la Terre :\n{image_url}")
        else:
            await ctx.send("Aucune image EPIC n'a été trouvée.")
    else:
        await ctx.send("Impossible de récupérer des images EPIC.")

@commands.command()
async def terreAll(ctx):
    # Utilisation de l'API de la NASA pour obtenir des images EPIC (Earth Polychromatic Imaging Camera)
    api_key = config('NASA_API_KEY')

    url = f'https://api.nasa.gov/EPIC/api/natural/images?api_key={api_key}'
    response = requests.get(url)
    data = response.json()

    if data:
        images = data
        if images:
            for image_data in images:
                # Extraire les informations de date de l'image
                date = image_data['date'].split()[0]  # Format de la date : YYYY-MM-DD
                year, month, day = date.split('-')

                # Construire l'URL complète de l'image à partir du nom de fichier
                image_name = image_data['image']
                archive_url = f'https://epic.gsfc.nasa.gov/archive/natural/{year}/{month}/{day}/png/'
                image_url = archive_url + image_name + ".png"
                await ctx.send(f"Voici une image EPIC de la Terre :\n{image_url}")
        else:
            await ctx.send("Aucune image EPIC n'a été trouvée.")
    else:
        await ctx.send("Impossible de récupérer des images EPIC.")

@commands.command()
async def apod(ctx):
    # Utilisation de l'API de la NASA pour obtenir l'Image astronomique du jour (APOD)
    api_key = config('NASA_API_KEY')

    url = f'https://api.nasa.gov/planetary/apod?api_key={api_key}'
    response = requests.get(url)
    data = response.json()

    if 'url' in data:
        image_url = data['url']
        title = data['title']
        explanation = data['explanation']
        await ctx.send(f"**{title}**\n{explanation}\n{image_url}")
    else:
        await ctx.send("Impossible de récupérer l'Image astronomique du jour.")

@commands.command()
async def mars(ctx):
    # Utilisation de l'API de la NASA pour obtenir des photos de Mars
    api_key = config('NASA_API_KEY')

    url = f'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=1000&api_key={api_key}'
    response = requests.get(url)
    data = response.json()

    if 'photos' in data:
        images = data['photos']
        
        image_data = images[0]
        date_photo = image_data['earth_date'] 
        image_url = image_data['img_src']
        await ctx.send(f"Voici des photos prises par le rover Curiosity sur Mars le {date_photo} :\n{image_url}")
    else:
        await ctx.send("Impossible de récupérer des photos de Mars.")

@commands.command()
async def nasa(ctx, search=""):
    if not search:
        await ctx.send("Veuillez spécifier une recherche pour les photos de la NASA.")
        return

    url = f'https://images-api.nasa.gov/search?q={search}'
    response = requests.get(url)
    data = response.json()

    if 'collection' in data:
        items = data['collection']['items']
        if items:
            image_url = items[0]['links'][0]['href']
            image_url = image_url.replace(" ", "%20")
            await ctx.send(f"Voici des photos archivées par la NASA :\n{image_url}")
        else:
            await ctx.send("Aucune image correspondant à votre recherche n'a été trouvée.")
    else:
        await ctx.send("Impossible de récupérer des photos de la NASA.")
