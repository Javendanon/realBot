
import os
import discord
import json
from dotenv import load_dotenv
load_dotenv()
from discord.ext import commands
from discord import guild, channel
import urllib 
import requests

# Cargando datos del bot
TOKEN = os.getenv('TOKEN_REALBOT')
GUILD = os.getenv('DISCORD_GUILD')
# inicializando el bot
client = discord.Client()
bot = commands.Bot(command_prefix='R! ')

async def WriteFile (path,data):
    with open(path, 'w') as f: 
        json.dump(data, f, ensure_ascii=False) 

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='Kurisutina')
async def secretMessage(ctx):
  res = '''This is a real secret message, It's so cool!, '''+ str(ctx.author) + ' youuuuuuu SONUVABITCH!'
  await ctx.send(res)

@bot.command(name='listCarrete')
async def listCarrete(ctx):
    res = 'La lista de carretes es la siguiente: \n'
    with open('./data/data.json') as f:
        data = json.load(f)
    for carrete in data['carretes']:
        res+= str(carrete['id']) + '. ' + carrete['fecha'] + ' ' + carrete['desc'] + ' en ' + carrete['ubicacion'] + '\n'
    await ctx.send(res)

@bot.command(name='addCarrete')
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

@bot.command(name='delCarrete')
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

@bot.command(name='cambiaFoto')
async def cambiaFoto(ctx, link, rut):
    URI = 'https://sgu.utem.cl/pgai/perfil_foto.php'
    f = open('temp_photo.jpg', 'wb')
    f.write(urllib.request.urlopen(link).read())
    f.close()
    photo = open('temp_photo.jpg','rb').read()
    data = {
        'rut' : rut,
        't_usu' : 1
    }
    files = {'foto_perfil':('temp_photo.jpg', open('temp_photo.jpg', 'rb'), "multipart/form-data")}
    req = requests.post(URI,files=files,data=data)
    response = 'y el servidor responde......' + req.text
    await ctx.send(response)
    
@bot.command(name = 'malla')
async def getMalla(ctx):
    # emoji = discord.utils.get(guild.emojis,name='Kappucha')
    # emoji = discord.utils.get(guild.emojis, name='LUL')
    # print (emoji)
    uri = 'https://cdn.discordapp.com/attachments/604360454227099648/604360478470307850/Malla.png'
    # emoji = 
    with open('malla.png','rb') as malla:
        await ctx.send(file = discord.File(malla, 'malla.png'))
        # await message.add_reaction(emoji)
bot.run(TOKEN)  