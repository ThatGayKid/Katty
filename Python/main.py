import os,json,asyncio,discord,random
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import Reddit as Rdt
import Rule34 as R34

from dotenv import load_dotenv
load_dotenv()
#
JSON = json.load(open('Text/Text.json'))

#Iniate bot
bot     = commands.Bot(command_prefix=os.getenv("PREFIX"))
#Shortcut Commaands
Servers = {}

class Server():
    """
    A object representing a server's status and configurations
    """
    def __init__    (self,Guild):
        self.Presets    = []
        self.Limit      = 100
        self.TextCleanup= True
        self.PostCleanup= False
        self.CleanupTime= 30

    def PresetDef   (self):
        with json.load(open('Defaults.json')) as Def:
            for Preset in Def:
                self.Presets.append(Preset(Preset['Name'],Preset['Desc'],Preset['SubR'],'Default'))

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

async def Setup(Guild):
    print(f'|Guild Setup|ID:{Guild.id}|Name:{Guild.name}|')
    Servers[Guild.id] = Server(Guild)

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


# ------------------------------------ #
#             Bot Commands             #
# ------------------------------------ #

@bot.event
async def on_ready():
    for Guild in (bot.guilds):
        await Setup(Guild)
    await StatusUpdate()
async def on_guild_join(Guild):
    await Setup(Guild)

@bot.command(name = 'r34', description = JSON['r34'][0], usage = JSON['r34'][1])
@commands.max_concurrency(1,per=BucketType.guild,wait=True)
@commands.is_nsfw()
async def r34(ctx):
    #Save message as the users command without the prefix and command
    Message = ctx.message.content[(len(bot.command_prefix)+4):]
    #Use the R34 api to get a post info
    Post = R34.Generate(ctx.guild.id,Message)
    #Generate a message from the post's date
    Message = JSON['Rule34']['Post'].format(ctx.author,Post['@tags'],Post['@file_url'])
    #Send that message with the post setting on the message handler
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