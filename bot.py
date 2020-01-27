import os
import discord
import json
from dotenv import load_dotenv
load_dotenv()
from discord.ext import commands
TOKEN = os.getenv('TOKEN_REALBOT')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()
bot = commands.Bot(command_prefix='R! ')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='Kurisutina')
async def secretMessage(ctx):
  res = '''This is a real secret message, It's so cool!, '''+ str(ctx.author) + ' youuuuuuu SONUVABITCH!'
  await ctx.send(res)

bot.run(TOKEN)