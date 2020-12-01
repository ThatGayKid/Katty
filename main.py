# -------------- Imports ------------- #
#Python Imports
import time
import os
#Pip Imports
import discord
from discord.ext import commands
from discord.ext.commands import Bot, has_permissions, CheckFailure
from discord.ext.commands.cooldowns import BucketType

#Locally Stored Imports
import Importer
import Loggy
Loggy.Create("Katty")

from dotenv import load_dotenv
load_dotenv()

# ----------- Bot Variables ---------- #
TOKEN = os.getenv("TOKEN")
bot = commands.Bot(command_prefix=os.getenv("PREFIX"))
MSGPrefix = ">>> "
BCN = 0#Bot Cooldown Normal
BCR = 0#Bot Cooldown Reddit

# ------------------------------------ #
#                  Bot                 #
# ------------------------------------ #

# ----------- Main Section ----------- #
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=(str(bot.command_prefix+"Help"))))
    Loggy.Add("Discord,Bot Activated","Discord")

# --------------- Help --------------- #
bot.remove_command('help')
@bot.command(name = "Help")
@commands.is_nsfw()
@commands.cooldown(1,BCN,BucketType.default)
async def Help(ctx):
    Loggy.Add ("Command, Help",ctx.author)
    msg = ("\
    User Commands:\n\
    Help:\n\
        Prints this menu.\n\
        Usage - "+bot.command_prefix+"Help\n\
    Gen:\n\
        Generates Images based on Input.\n\
        Usage - "+bot.command_prefix+"Gen\n\
    Add:\n\
        Adds new options for Gen NOT AVALIABLE YET\n\
        Usage - "+bot.command_prefix+"Add\n\
    \n\
    Admin Only: \n\
    Prefix:\n\
        Changes the bot prefix.\n\
        Usage - "+bot.command_prefix+"Prefix *PREFIX*\n\
    Limit:\n\
        Changes amount of preloaded images.\n\
        Usage - "+bot.command_prefix+"Limit *LIMIT*\n")
    await ctx.channel.send("```"+msg+"```")

# ------------- Generate ------------- #
@bot.command(name = "Gen")
@commands.is_nsfw()
@commands.cooldown(1,BCR,BucketType.default)
async def Gen(ctx,*,message):
    log = "Command,Generate - "+message
    
    if message == "Help" or "":
        msg=(Importer.Help(message))
    else:
        msg=(Importer.GeneratePost(message))

    log = "Command,Generate - "+message
    Loggy.Add(log,ctx.author)
    await ctx.channel.send(msg)
# ------------ Re-generate ------------ #
# @Gen.error
# async def Gen.error(ctx, error):
#     log = ("Crash,Generate - "+commands.CommandInvokeError)
#     msg = "OOPSIE WOOPSIE!! Uwu We made a fucky wucky!! A wittle fucko boingo! The code monkeys at our headquaters are working VEWY HARD to fix this!"
#     Loggy.Add(err,ctx.author)
#     await ctx.channel.send(msg)

# ------------ Add Entries ----------- #
@bot.command(name = "Add")
@commands.is_nsfw()
@commands.cooldown(1,BCR,BucketType.default)
async def AddPost(ctx):
    msg = ">>>Not Avaliable"
    await ctx.channel.send(msg)
    
# ------------------------------------ #
#----------------Admin-----------------#
# ------------------------------------ #

# --------------- Limit -------------- #
@bot.command(name = "Limit")
@commands.has_permissions(ban_members=True, kick_members=True) 
async def Limit(ctx, Limit):
    Importer.Limit = Limit
    Loggy.Add (f"Admin, Limit - {Limit}",ctx.author)
    msg = (f"Limit changed to "+Importer.Limit)
    await ctx.send(MSGPrefix+msg)

# -------------- Prefix -------------- #
@bot.command(name = "Prefix")
@commands.has_permissions(ban_members=True, kick_members=True) 
async def setprefix(ctx,*,prefix):
    bot.command_prefix = prefix
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=(bot.command_prefix+"Help")))
    Loggy.Add ("Admin,Prefix - "+prefix,ctx.author)
    msg = (f"Prefix changed to ``{prefix}``")
    await ctx.send(MSGPrefix+msg)
    #Changes help message to fit prefix
    

# -------------- Reload -------------- #
@bot.command(name = "Reload")
@commands.is_owner()
async def Reload(ctx):
    
    import Importer
    import Loggy
    Loggy.Create("Katty")
    Loggy.Add ("Admin,Reload",ctx.author)
    load_dotenv()    
    TOKEN = os.getenv("TOKEN")
    bot.command_prefix = os.getenv("PREFIX")
    msg = ("Reloaded Bot ;)")
    await ctx.send(MSGPrefix+msg)
# ------------------------------------ #
#                Secrets               #
# ------------------------------------ #

# ---------------- Gay --------------- #
@bot.command(name = "Gay")
@commands.is_nsfw()
@commands.cooldown(1,BCN,BucketType.default)
async def Gay(ctx):
    await bot.add_reaction(bot,"\U0001F534")
    Loggy.Add ("Secret,Gay",ctx.author)
    await ctx.channel.send(MSGPrefix+"no u")

# --------------- Cute --------------- #
#If your reading this, you have free access to this hidden command. If you want dick around with it.
@bot.command(name = "SexyBoy")
@commands.is_nsfw()
@commands.cooldown(1,BCN,BucketType.default)
async def Cute(ctx):
    Loggy.Add ("Secret,Cute",ctx.author)
    await ctx.channel.send("https://imgur.com/a/zBWGUuB")
                   
bot.run(TOKEN)