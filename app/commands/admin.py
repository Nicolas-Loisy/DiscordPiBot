import sys
from discord.ext import commands
from decouple import config
import os
import git

def setup(bot):
    bot.add_command(restart)
    bot.add_command(update)
    bot.add_command(shutdown)
 
@commands.command()
async def restart(ctx):
    if str(config('MON_ID_UTILISATEUR'))  == str(ctx.author.id):
        await ctx.send("Redémarrage en cours...")

        print("argv was",sys.argv)
        print("sys.executable was", sys.executable)
        print("restart now")
        
        os.execv(sys.executable, ['python'] + sys.argv)
        # Arrêter l'exécution du code ici pour éviter les doublons de processus
        # return
        # sys.exit(1)
        # sys.exit()
    else:
        await ctx.send("Vous n'êtes pas autorisé à utiliser cette commande.")

@commands.command()
async def update(ctx):
    repo = git.Repo("./DiscordPiBot")  # Chemin vers le répertoire racine de votre programme

    try:
        repo.remotes.origin.pull(config('UPDATE_BRANCH'))
        await ctx.send("Mise à jour réussie. Redémarrer le bot pour lancer les modifications.")
 
    except git.GitCommandError as e:
        await ctx.send("Erreur lors de la mise à jour du programme.")
        print(e)

@commands.command()
async def shutdown(ctx):
    if str(config('MON_ID_UTILISATEUR'))  == str(ctx.author.id):
        await ctx.send("Arrêt en cours...")
        await ctx.bot.close()
    else:
        await ctx.send("Vous n'êtes pas autorisé à utiliser cette commande.")
