
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
LIST_NOTIF_CHANNEL = [x for x in os.environ.get('LIST_CHECKING_CHANNEL').split("|")]
CHANNEL_FOR_NOTIF = os.environ.get('NOTIFICATION_CHANNEL')
DICT_SERVER_CHANNEL = {} #Format : {server:[[ChannelsToCheck], Channel_For_Notif]}

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
	if re.match("!(HMT|hmt) help", message.content):
		await CLIENT.send_message(message.channel, 
		content="""
```Pour obtenir votre logo, merci d'utiliser la commande au format suivant : 
!HMT %CouleurDuPseudo %Background %VotrePseudo 
Avec la couleur du pseudo pouvant être R6, OW, CS, white ou un code rgb : '(255,255,255)' par exemple(sans les ')
Le background doit être obligatoiremement soit R6,OW,CS ou NEUTRE (la version moitié R6 moitié OW)
Le pseudo normalement pas de contrainte mais si un charactére spécial passe pas j'aurais certainement la flemme de le supporter ^^
Pour le code source : https://github.com/jonathanTIE/Humanity-Bot (svp le regardez pas)
Le bot est hébergé sur Heroku
Pour d'autres questions : essaiyez de joindre le staff(de préférance @jonathanTIE#4813)
		``` """) 
@CLIENT.event		
async def on_ready():
	global CHANNEL_FOR_NOTIF,LIST_NOTIF_CHANNEL,DICT_SERVER_CHANNEL
	curCheck = []
	curForNotif = None
	for server in CLIENT.servers:
		for x in server.channels:
			if str(x) == CHANNEL_FOR_NOTIF:
				curForNotif = x
			else:
				for y in LIST_NOTIF_CHANNEL:
					if str(y) == str(x):
						curCheck.append(x)		
		DICT_SERVER_CHANNEL[server] = [curCheck,curForNotif]
	CLIENT.loop.create_task(infinite_check())
				
@CLIENT.event
async def infinite_check():
	CurVoiceMembers = []
	global DICT_SERVER_CHANNEL
	print(DICT_SERVER_CHANNEL)
	while True:
		for server in DICT_SERVER_CHANNEL:
			ChannelForNotification = DICT_SERVER_CHANNEL[server][1]
			for ChannelToCheck in DICT_SERVER_CHANNEL[server][0]:
				voiceMembers = ChannelToCheck.voice_members
				if  voiceMembers and CurVoiceMembers != voiceMembers:
					await CLIENT.send_message(ChannelForNotification,
					content=":alerte: Quelqu'un s'est connecté sur le channel {0}! {1} est/sont présent(s) ! :alerte:".format(
					ChannelToCheck.name, str([x.name for x in ChannelToCheck.voice_members])))
					CurVoiceMembers = voiceMembers
				elif not voiceMembers:
					CurVoiceMembers = []
				else:
					pass
		await asyncio.sleep(1)
		
CLIENT.run(TOKEN)
