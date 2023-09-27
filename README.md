# DiscordPiBot

Projet DiscordPiBot
Développeurs : Nicolas Loisy
Projet : Bot/Robot Discord
Titre : DiscordPiBot
DiscordPiBot : [ Python ]

DiscordPiBot est un bot Discord codé en Python qui offre une variété de fonctionnalités pour animer et administrer votre serveur Discord. Vous pouvez ajouter ce bot à votre serveur pour faciliter la gestion et l'animation de votre communauté.

## Installation

Pour utiliser DiscordPiBot, suivez ces étapes d'installation :

1. **Cloner le dépôt Git**

   Tout d'abord, assurez-vous d'avoir [Git](https://git-scm.com/) installé sur votre système. Ensuite, exécutez la commande suivante dans votre terminal pour cloner le dépôt DiscordPiBot :

   ```bash
   git clone https://github.com/Nicolas-Loisy/DiscordPiBot.git
   cd DiscordPiBot
   ```

2. **Installer les dépendances**

   Vous devez installer plusieurs dépendances Python pour faire fonctionner DiscordPiBot. Exécutez les commandes suivantes dans votre terminal :

   ```bash
   py -3 -m pip install -U discord.py==2.0.0
   py -3 -m pip install -U python-decouple
   py -3 -m pip install -U requests
   py -3 -m pip install -U ffmpeg-python
   py -3 -m pip install -U ffmpeg  # (Note : Cette dépendance peut ne pas être requise pour certaines fonctionnalités)
   py -3 -m pip install -U gitpython
   ```

3. **Configurer le fichier .env**

   Avant de pouvoir exécuter le bot, vous devez configurer votre token Discord. Créez un fichier `.env` à la racine du répertoire DiscordPiBot et ajoutez-y votre token Discord de la manière suivante :

   ```
   DISCORD_TOKEN=VotreTokenDiscord
   MON_ID_UTILISATEUR=VotreIDUtilisateur
   ```

   Assurez-vous également de remplacer `VotreTokenDiscord` par le token de votre bot Discord et `VotreIDUtilisateur` par votre ID d'utilisateur Discord.

4. **Exécuter le bot**

   Une fois que tout est configuré, vous pouvez exécuter le bot en utilisant la commande suivante :
```bash
   py -3 .\main.py
```
Ou
```bash
   python3 DiscordPiBot.py
```

   Le bot se connectera à votre serveur Discord et sera prêt à répondre à vos commandes.

## Commandes

DiscordPiBot offre plusieurs commandes pour administrer et animer votre serveur Discord. Voici quelques-unes des commandes disponibles :


## Commandes

### Commandes Administration

DiscordPiBot offre plusieurs commandes pour administrer et animer votre serveur Discord. Voici la liste des commandes disponibles :

- `!restart`: Redémarre le bot Discord. Seul l'utilisateur dont l'ID correspond à `MON_ID_UTILISATEUR` peut utiliser cette commande. Cette commande est utile pour appliquer les mises à jour du bot.

- `!update`: Met à jour le bot Discord depuis le dépôt Git. Cette commande est disponible pour tous les utilisateurs. Elle permet de synchroniser le bot avec la dernière version du code source.

- `!shutdown`: Arrête complètement le bot Discord. Seul l'utilisateur dont l'ID correspond à `MON_ID_UTILISATEUR` peut utiliser cette commande. Cette commande permet de fermer le bot de manière propre.

### Commandes Utilitaires

DiscordPiBot propose également des commandes utilitaires pour ajouter de la diversité à votre serveur Discord :

- `!ping`: Affiche la latence du bot en millisecondes. Utile pour vérifier la réactivité du bot.

- `!saluer`: Le bot vous salue en mentionnant votre nom d'utilisateur Discord.

- `!effacer [nombre]`: Supprime un certain nombre de messages dans le canal actuel, y compris la commande elle-même.

- `!sondage [question] [options...]`: Crée un sondage avec une question et plusieurs options. Les membres du serveur peuvent voter en réagissant aux options proposées.

- `!de [faces]`: Lance un dé virtuel avec un nombre spécifié de faces (par défaut : 6) et affiche le résultat.

- `!meteo [ville]`: Affiche les informations météorologiques pour une ville donnée (par défaut : Paris). Cette commande nécessite une clé d'API OpenWeatherMap dans la variable d'environnement `OPENWEATHERMAP_API_KEY`.

### Commandes Multimédia et divers

DiscordPiBot offre également des commandes pour ajouter de l'amusement et de la créativité à votre serveur Discord :

- `!chien`: Affiche une image aléatoire d'un chien pour égayer votre serveur.

- `!chat`: Affiche une image aléatoire d'un chat, car qui n'aime pas les chats ?

- `!savephoto`: Permet d'enregistrer une image envoyée en tant que pièce jointe. Utile pour conserver des souvenirs visuels sur votre serveur.

- `!listphotos`: Affiche la liste des images enregistrées sur le serveur.

- `!showrandomphoto`: Affiche de manière aléatoire l'une des images enregistrées. 

- `!savesound [nom]`: Enregistre un fichier audio en tant que son personnalisé sous le nom spécifié. Utilisez cette commande en joignant un fichier audio au message. (Exemple : `!savesound mon_son`)

- `!playsound [nom]`: Joue un son personnalisé enregistré précédemment dans un salon vocal. Assurez-vous d'être connecté à un salon vocal pour utiliser cette commande. (Exemple : `!playsound mon_son`)

- `!listtracks`: Affiche la liste des sons personnalisés disponibles pour la lecture.

<!-- Ajoutez d'autres commandes et leurs descriptions ici si nécessaire -->

N'hésitez pas à personnaliser davantage ces descriptions en fonction de vos besoins ou à ajouter d'autres commandes au besoin.


## Auteur

DiscordPiBot a été créé par [Nicolas Loisy](https://github.com/Nicolas-Loisy).

## Contributions

Les contributions à ce projet sont les bienvenues. Si vous souhaitez améliorer DiscordPiBot ou ajouter de nouvelles fonctionnalités, n'hésitez pas à soumettre des pull requests.

Amusez-vous bien avec DiscordPiBot ! Si vous avez des questions ou des problèmes, n'hésitez pas à [contacter l'auteur](https://github.com/Nicolas-Loisy).