from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

COLOR = {
"R6":(4,129,5),
"OW":(0,0,0),
"CS":(255,255,255),
"WHITE":(255,255,255)
}
BACKGROUND_FILE = {
"R6":"Logo_pseudo_r6",
"OW":"Logo_pseudo_ow",
"CS":"Logo_pseudo_csgo",
"NEUTRE":"Logo_pseudo"
}
def CreateLogo(IOName, IOColor, IOBackground, TypeIOColor="str"):
	IMG_NAME = ""
	rgb = [0,0,0]
	if IOColor.upper() in COLOR:
		rgb = COLOR[IOColor.upper()]
	elif TypeIOColor=="rgbCode":
		IOColor = IOColor.split(",")
		rgb[0], rgb[1], rgb[2] = int(IOColor[0][1:]), int(IOColor[1]), int(IOColor[2][:-1])#remove les parenthéses
		rgb = tuple(rgb)
	else:
		return "Couleur entrée incorrecte : ne mettez pas d'espace n'importe où, seulement entre les couleurs, les pseudos et les noms du background"
	if IOBackground.upper() in BACKGROUND_FILE:
		IMG_NAME = BACKGROUND_FILE[IOBackground.upper()]
	else:
		return "Background entrée incorrect : ne mettez pas d'espace n'importe où, seulement entre les couleurs, les pseudos et les noms du background"
	
	img = Image.open(IMG_NAME + ".jpg")
	draw = ImageDraw.Draw(img)
	curSize = 350 
	# font = ImageFont.truetype(<font-file>, <font-size>)
	font = ImageFont.truetype("Ordinary.ttf",size=curSize) #Ordinary.ttf ou arial.ttf
	fontSize = font.getsize(IOName)
	if len(IOName) <= 4:
		position = (250, 400)
	else:
		while(fontSize[0] >= 750):
			curSize -= 10
			font = ImageFont.truetype("Ordinary.ttf",size=curSize)
			fontSize = font.getsize(IOName)
		position = (250, 400 + (200-fontSize[1])/2)
	# draw.text((x, y),"Sample Text",(r,g,b))
	draw.text(position,IOName,rgb,font) #,font=font
	img.save("ImageToSend.jpg")
	return "ImageToSend.jpg"