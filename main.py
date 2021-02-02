import os,json,random,pathlib,atexit
import asyncio
import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from Python import Reddit as Rdt
from Python import Rule34 as R34

from dotenv import load_dotenv
load_dotenv()
#
JSON = json.load(open('Text/Text.json'))

#Iniate bot
bot     = commands.Bot(command_prefix=os.getenv("PREFIX"))
Servers = None
class Server():
    """
    A object representing a server's status and configurations
    """
    def __init__    (self,Limit=100,TextCleanup=True,PostCleanup=False,CleanupTime=30):
        self.RecentPosts= []
        self.Presets    = []
        self.Limit      = int(Limit)
        self.TextCleanup= bool(TextCleanup)
        self.PostCleanup= bool(PostCleanup)
        self.CleanupTime= int(CleanupTime)

# ------------------------------------ #
#           Useful Functions           #
# ------------------------------------ #
#Commands that are Shortcuts or Handlers

#Forms a message to be sent
def Form  (msg:str) -> str:
    return f"```{msg}```"
#Returns the serverclass from ctx
def SvCls (ctx) -> Server:
    return Servers[ctx.guild.id]

#Message cleanup
async def SendMessage(ctx,Msg:str,Type:int):
    Server = SvCls(ctx)
    Message = await ctx.channel.send(Msg)
    if Server.TextCleanup and Type == 0:
        await asyncio.sleep(Server.CleanupTime)
        await Message.delete()
    if Server.PostCleanup and Type == 1:
        await asyncio.sleep(Server.CleanupTime)
        await Message.delete()

Activity={
        "L":discord.ActivityType.listening,
        "W":discord.ActivityType.streaming,
        "P":discord.ActivityType.playing}
async def StatusUpdate():
    while True:
        Status = random.choice(JSON["Bot"]['Status'])
        Act,Name = Activity[Status[0]],Status[1]
        await bot.change_presence(activity=discord.Activity(type=Act, name=Name))
        await asyncio.sleep(60)

def LoadHandler():
    TmpServers = {}
    SaveFile = 'Text/State.json'
    if pathlib.Path(SaveFile).exists():
        #Get the dump from the designated save file
        print('Found State: Loading')
        with open(SaveFile) as File:
            Dump = json.load(File)
        for x in Dump:
            TmpServers[x] = Server(Dump[x]['Limit'],Dump[x]['TextCleanup'],Dump[x]['PostCleanup'],Dump[x]['CleanupTime'])
        global Servers
        Servers = TmpServers
    #If there is no existing State Dump (New Setup or Corruption)
    else:
        print('No State: Using Defaults')
        #Geneate a default state from defauls
        for Guild in bot.guilds:
            Servers[Guild.id] = Server()


@atexit.register
def ExitHandler():
    print('Bot Crashed OwO')
    if (Servers == None) or (Servers == {}):
        print('No State Loaded: Outta Here')
        return
    Dump = {}
    for x in Servers:
        Dump[x] = Servers[x].__dict__
    print(f"Saving State as:{Dump}")
    with open('Text/State.json','w') as File:
        json.dump(Dump,File)

# ------------------------------------ #
#             Bot Commands             #
# ------------------------------------ #

@bot.event
async def on_ready():
    LoadHandler()
    print("Bot Loaded UwU")
    Servers = await StatusUpdate()
async def on_guild_join(Guild):
    Servers[Guild.id] = Server()
async def on_guild_exit(Guild):
    del Servers[Guild.id]

@bot.command(name = 'r34', description = JSON['r34'][0], usage = JSON['r34'][1])
@commands.max_concurrency(1,per=BucketType.guild,wait=True)
@commands.is_nsfw()
async def r34(ctx):
    #Save message as the users command without the prefix and command
    Message = ctx.message.content[(len(bot.command_prefix)+4):]
    #Use the R34 api to get a post info
    Post = R34.Generate(ctx.guild.id,Message)
    if type(Post) == str:
        #String Error message becomes message
        Message = Post
    elif type(Post) == dict:
        #Append the post id to the recent posts
        (SvCls(ctx).RecentPosts[ctx.guild.id]).append(Post['@id'])
        #Format a message from that response
        Message = JSON['Rule34']['Post'].format(ctx.author,Post['@tags'],Post['@file_url'])
    await SendMessage(ctx,Message,1)

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

bot.run(os.getenv("TOKEN"))