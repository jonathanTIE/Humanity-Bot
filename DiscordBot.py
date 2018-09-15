"""Discord bot :
https://boostlog.io/@anshulc95/how-to-host-a-discord-bot-on-heroku-for-free-5a9c230798a8b60096c43336
"""
import os
import ImageLogo
import asyncio
import discord
import logging
import re

TOKEN =  os.environ.get('TOKEN')#variable d'env .bashrc
logging.basicConfig(level=logging.INFO)

#link https://discordapp.com/oauth2/authorize?client_id=481506421670674461&scope=bot&permissions=101376
#Bot ID = 481506421670674461
CLIENT = discord.Client()
pattern_pic = r"!(HMT|hmt) .[^ ]* .[^ ]* .[^ ]*" #Format demandé : commande,couleur,background,pseudo
@CLIENT.event
async def on_message(message):
	Result = ''
	#Commande d'image :
	if re.match(pattern_pic, message.content):
		curArgs = re.match(pattern_pic, message.content).string.split(" ")
		if re.match(r"\(([0-9]{1,3},){2}[0-9]{1,3}\)",curArgs[1]): #check rgb code
			Result = ImageLogo.CreateLogo(curArgs[3], curArgs[1], curArgs[2], "rgbCode")
		else:
			Result = ImageLogo.CreateLogo(curArgs[3], curArgs[1], curArgs[2])
		if Result == "ImageToSend.jpg" :
			await CLIENT.send_file(message.channel, "ImageToSend.jpg")
		else:
			await CLIENT.send_message(message.channel,
		content=Result)
	#Commande d'aide :
	if re.match("!HMT help", message.content):
		await CLIENT.send_message(message.channel, 
		content=""" 
```Pour obtenir votre logo, merci d'utiliser la commande au format suivant : 
!HMT %CouleurDuPseudo %Background %VotrePseudo 
Avec la couleur du pseudo pouvant être R6, OW, CS, white ou un code rgb : '(255,255,255)' par exemple(sans les ')
Le background doit être obligatoiremement soit R6,OW,CS ou NEUTRE (la version moitié R6 moitié OW)
Le pseudo normalement pas de contrainte mais si un charactére spécial passe pas j'aurais certainement la flemme de le supporter ^^
Pour le code source : https://github.com/jonathanTIE/Humanity-Bot
Le bot est hébergé sur Heroku
Pour d'autres questions : essaiyez de joindre le staff(de préférance @jonathanTIE#4813)
		``` """) 
		
CLIENT.run(TOKEN)
