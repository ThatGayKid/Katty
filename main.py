import atexit
import pickle
import asyncio
from os import getenv
from pathlib import Path
from sys import getsizeof
from json import load as jsonload
from random import choice as randomchoice

import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

from Python import Reddit as Rdt
from Python import Rule34 as R34

from dotenv import load_dotenv
load_dotenv()
#
JSON = jsonload(open('Text/Text.json'))

#Iniate bot
bot     = commands.Bot(command_prefix=getenv("PREFIX"))
Servers = None
class Server():
    """A object representing a server's status and configurations"""
    def __init__    (self):
        self.TextCleanup = True
        self.PostCleanup = False
        self.CleanupTime = 30

# ------------------------------------ #
#           Useful Functions           #
# ------------------------------------ #
#Commands that are Shortcuts or Handlers

#Returns the serverclass from ctx
def Sv (ctx) -> Server:
    return Servers[ctx.guild.id]

#Message cleanup
async def SendMessage(ctx,Msg):
    Server = Sv(ctx)
    #If the message is a string         (Error Message)
    if type(Msg) == str:
        Message = await ctx.send(f"```{Msg}```")
    #If the message is an discord embed (Post and Embed)
    if type(Msg) == discord.embeds.Embed:
        Message = await ctx.send(embed=Msg)

    if ((type(Msg) == str)                  and (Server.TextCleanup)) or\
       ((type(Msg) == discord.embeds.Embed) and (Server.PostCleanup)):
        await asyncio.sleep(Server.CleanupTime)
        await Message.delete()

Activity={
        "L":discord.ActivityType.listening,
        "W":discord.ActivityType.streaming,
        "P":discord.ActivityType.playing}

def LoadHandler():
    global Servers
    #If there is a saved state
    if Path('Text/State.pickle').exists():
        #Get the dump from the designated save file
        print('Found State: Loading')
        with open('Text/State.pickle','rb') as File:
            Servers = pickle.load(File)
    #If there is no existing State Dump (New Setup or Corruption)
    else:
        #Geneate a default state from defauls
        print('No State: Using Defaults')
        Servers = {}
        for Guild in bot.guilds:
            Servers[Guild.id] = Server()


@atexit.register
def ExitHandler():
    print('Bot Closing OwO')
    #If state is empty or invalid
    if (Servers == None) or (Servers == {}):
        print('No State Loaded: Not Saving')
    #If state is valid, save to pickle
    else:
        print(f"State Found: Saving State")
        with open('Text/State.pickle','wb') as File:
            pickle.dump(Servers,File)

async def StatusUpdate():
    while True:
        Status = randomchoice(JSON["Bot"]['Status'])
        Act,Name = Activity[Status[0]],Status[1]
        await bot.change_presence(activity=discord.Activity(type=Act, name=Name))
        await asyncio.sleep(60*5)

# ------------------------------------ #
#             Bot Commands             #
# ------------------------------------ #

@bot.event
async def on_ready():
    LoadHandler()
    print("Bot Loaded UwU")
    #await StatusUpdate()

async def on_guild_join(Guild):
    Servers[Guild.id] = Server()
    print(f'Added to server {Guild.id}')

@bot.command(name = 'r34', description = JSON['r34'][0], usage = JSON['r34'][1])
@commands.cooldown(3,1,type=BucketType.member)
@commands.is_nsfw()
async def r34(ctx):
    #Save message as the users command without the prefix and command
    Input = ctx.message.content[(len(bot.command_prefix)+4):]
    #Use the R34 api to get a post info
    Post = R34.Generate(ctx.guild.id,Input)
    if type(Post) == str:
        #String Error message becomes message
        Message = Post
    else:
        #Format a message from that response
        Title   = JSON['Rule34']['PostTitle'].format(author = str(ctx.author))
        Desc    = JSON['Rule34']['PostTags'].format(tags = Post['@tags'])
        Message = discord.Embed(title = Title,description=Desc,url=f"https://rule34.xxx/index.php?page=post&s=view&id={Post['@id']}")
        Message.set_image(url=Post['@sample_url'])

    await SendMessage(ctx,Message)

@bot.command(name="em")
async def embed(ctx):
    URL = "https://media.discordapp.net/attachments/415136979626360842/809829207886528512/rs6z0ff7yht51.png"
    Message = discord.Embed(title = "Test Scenario")
    Message.set_image(url=URL)
    Message.set_author(name=str(ctx.author))
    await ctx.send(embed=Message)

# @bot.command(name = 'rd', description = JSON['rd'][0], usage = JSON['rd'][1])
# @commands.max_concurrency(1,per=BucketType.guild,wait=True)
# async def r(ctx,SubReddit,*a):
#     Message = ''
#     await SendMessage(ctx,Message,1)

# @bot.command(name = 'Limit', description=JSON['Limit'][0],  usage = JSON['Limit'][1])
# @commands.is_owner()
# async def Limit(ctx,*Message):
#     try:
#         if len(Message) == 0:
#             msg=JSON['Limit']['Def'].format(SvClass(ctx).Limit)
#         else:
#             try:
#                 SvClass(ctx).Limit = int(Message)
#                 msg=JSON['Limit']['Change'].format(SvClass(ctx).Limit)
#             except ValueError:
#                 msg=JSON['Limit']['Fail']
#     except commands.errors.NotOwner:
#         msg = JSON['Bot']['Owner']
#         SendMessage(ctx,Form(msg),0)

@bot.command(name = "RollOver",hidden = True)
@commands.is_owner()
async def death(ctx):
    exit()

@bot.command(name = "Size",hidden = True)
@commands.is_owner()
async def Size(ctx):
    print(getsizeof(Sv(ctx)))

bot.run(getenv("TOKEN"))