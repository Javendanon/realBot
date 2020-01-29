import os
import discord
import json
from dotenv import load_dotenv
load_dotenv()
from discord.ext import commands
from discord import guild, channel
import urllib 
import requests
import random
import asyncio
from gtts import gTTS

# Cargando datos del bot
TOKEN = os.getenv('TOKEN_REALBOT')
URI_CAMBIARFOTO = os.getenv('URI_CAMBIARFOTO')
TLD = os.getenv(TLD_GTTS)

bot = commands.Bot(command_prefix='R! ')

async def WriteFile (path,data):
    with open(path, 'w') as f: 
        json.dump(data, f, ensure_ascii=False) 

def getGtts(members):
    targetMember = random.randint(0,len(members)-1)
    # phrase = getApiMsg
    phrase = [
        'Tontito',
        'Jolaperra',
        'Bastardo culiao',
        'Bacallo conchetumare',
        'Chupa el pico',
        'Maldito hijo de la bastarda',
        'Chupa ano maldito conchetumare',
        'Maricon',
        'Puto',
        'Peruano',
        'Chupa la que cuelga',
        'Tu mamá es homvre',
        'Hijo de la come moco',
        'Tu mamá es maraca i era',
        'Maricon culiao',
        'Sangano conchetumare',
        'Enfermo culio',
        'Enfermo conchetumare',
        'Prestai el poto gratis',
        'Deconstruido de mierda',
        'Igualito a Paty Maldonado facho de mierda',
        'Ojala te hubieran llevado a ti a juan fernandez en vez de felipito',
        'Tan ahueonao que fijo votaste por piñera',
        'Cuckeao culiao',
        'mamahuevo',
        'mamon',
        'burgués puto',
        'Aliade deconstruide y la puta que te parió'
    ]
    tts = members[targetMember] + phrase[random.randint(0,len(phrase)-1)]
    gtts = gTTS(tts, lang='es-us',tld=TLD)
    with open('message.mp3','wb') as file:
        gtts.write_to_fp(file)
    
def getInterval(a,b):
    return random.randint(a,b)

def getMembers (selectedId):
    membersArray = []
    members = bot.get_channel(selectedId).members
    for member in members:
        member_pulent = str(member).split('#')
        membersArray.append(member_pulent[0])
    return membersArray

def getAvailableChannels():
    voiceChannels = {}
    availableChannels = {}
    for server in bot.guilds: #Llena un dict con los nombres y el id de cada canal de voz
        for channel in server.voice_channels:
            voiceChannels[channel.name] = channel.id
    for name,idChannel in voiceChannels.items():
        actualChannel = bot.get_channel(idChannel)
        if (len(actualChannel.members)>0):
            availableChannels[actualChannel.name] = actualChannel.id
    print(availableChannels)
    return availableChannels

async def DoTheThing():
    availableChannels = getAvailableChannels()
    if (len(availableChannels)==0):
        return 
    ## if there is not available channel FALTA ESTO 
    selectChannel = random.randint(0,len(availableChannels)-1)
    selectedChannelName = list(availableChannels.keys())[selectChannel]
    selectedChannelId = list(availableChannels.values())[selectChannel]
    members = getMembers(selectedChannelId)
    
    # get TTS
    getGtts(members)
    #play TTS in vc 
    channel = bot.get_channel(selectedChannelId)
    vc = await channel.connect()
    vc.play(discord.FFmpegPCMAudio('message.mp3'))
    while (vc.is_playing()):
        pass
    dis = await vc.disconnect()


async def PuteoFunction():
    # 30 y 1800 segundos
    interval = getInterval(0,5)
    while (True):
        await DoTheThing()
        await asyncio.sleep(interval)
        interval = getInterval(0,5)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    bot.loop.create_task(PuteoFunction())

@bot.command(name='Kurisutina')
async def secretMessage(ctx):
  res = '''This is a real secret message, It's so cool!, '''+ str(ctx.author) + ' youuuuuuu SONUVABITCH!'
  await ctx.send(res)

@bot.command(name='listCarrete',help='Lista los carretes que hay pendientes')
async def listCarrete(ctx):
    res = 'La lista de carretes es la siguiente: \n'
    with open('./data/data.json') as f:
        data = json.load(f)
    for carrete in data['carretes']:
        res+= str(carrete['id']) + '. ' + carrete['fecha'] + ' ' + carrete['desc'] + ' en ' + carrete['ubicacion'] + '\n'
    await ctx.send(res)

@bot.command(name='addCarrete',help='Agrega un nuevo carrete a la lista')
async def addCarrete(ctx, newFecha, newDesc, newUbicacion):
    with open('./data/data.json') as f:
        data = json.load(f)
    newId = len(data['carretes'])+1
    data['carretes'].append({
        "id": newId,
        "ubicacion": newUbicacion,
        "desc": newDesc,
        "fecha": newFecha
    })
    await WriteFile('./data/data.json',data)
    res = 'Carrete añadido mi washo'
    await ctx.send(res)

@bot.command(name='delCarrete',help='Borra un carrete de la lista')
async def deleteCarrete(ctx, id):
    with open('./data/data.json') as f:
        data = json.load(f)
    for carrete in data['carretes']:
        if (carrete['id']==str(id-1)):
            carrete['id'].pop(id-1)
    await WriteFile('./data/data.json',data)
    res = 'Carrete d e l e t e a d o, F my friend.'
    await ctx.send(res)
# @bot.command(name='modCarrete')
# async def modifyCarrete(ctx,id):

@bot.command(name='cambiaFoto',help='Averigualo washin, el rut va sin digito verificador: 12345678')
async def cambiaFoto(ctx, link_foto, rut_victima):
    f = open('temp_photo.jpg', 'wb')
    f.write(urllib.request.urlopen(link_foto).read())
    f.close()
    photo = open('temp_photo.jpg','rb').read()
    data = {
        'rut' : rut,
        't_usu' : 1
    }
    files = {'foto_perfil':('temp_photo.jpg', open('temp_photo.jpg', 'rb'), "multipart/form-data")}
    req = requests.post(URI_CAMBIARFOTO,files=files,data=data)
    response = 'y el servidor responde......' + req.text
    await ctx.send(response)
    
@bot.command(name = 'malla',help='Muestra la malla de la carrera')
async def getMalla(ctx):
    # emoji = discord.utils.get(guild.emojis,name='Kappucha')
    # emoji = discord.utils.get(guild.emojis, name='LUL')
    # print (emoji)
    # emoji = 
    with open('malla.png','rb') as malla:
        await ctx.send(file = discord.File(malla, 'malla.png'))
        # await message.add_reaction(emoji)


bot.run(TOKEN)