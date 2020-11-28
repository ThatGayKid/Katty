# -------------- Imports ------------- #
import discord
from discord.ext import commands
from discord.ext.commands import Bot, has_permissions, CheckFailure
from discord.ext.commands.cooldowns import BucketType

import Importer
import Loggy
Loggy.Create("Katty")

import time
import os
from dotenv import load_dotenv
load_dotenv()

# ----------- Bot Variables ---------- #
TOKEN = os.getenv("TOKEN")
bot = commands.Bot(command_prefix="K!")

HHelp = ("```\
Help - Displays this menu\n\
Gen  - Input\n\
Admin\n\
  - Input\n\
Gen  - Input\n\
```")

BCN = 1#Bot Cooldown Normal
BCR = 2#Bot Cooldown Reddit

# ------------------------------------ #
#                  Bot                         #
# ------------------------------------ #

# ----------- Main Section ----------- #
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=(bot.command_prefix+"Help")))
    Loggy.Add("Discord,Bot Activated","Discord")

# --------------- Help --------------- #
bot.remove_command('help')
@bot.command(name = "Help")
@commands.is_nsfw()
@commands.cooldown(1,BCN,BucketType.default)
async def Help(ctx):
    Loggy.Add ("Command, Help",ctx.author)
    msg = (HHelp)
    await ctx.channel.send(msg)

# --------------- Catty -------------- #
@bot.command(name = "Gen")
@commands.is_nsfw()
@commands.cooldown(1,BCR,BucketType.default)
async def Catty(ctx,Input):
    Loggy.Add ("Command,Catty",ctx.author)
    await ctx.channel.send(Importer.Picture(Input))

# ------------------------------------ #
#                 Admin                #
# ------------------------------------ #

@bot.command(name = "Reload")
@commands.is_owner()
async def Reload(ctx):
    import Importer
    import Loggy
    Loggy.Create("Katty")
    Loggy.Add ("Command,Reload",ctx.author)
    load_dotenv()

@bot.command(name = "Prefix")
@commands.has_permissions(ban_members=True, kick_members=True) 
async def setprefix(ctx, prefix):
    bot.command_prefix = prefix
    await ctx.send(f"Prefix changed to ``{prefix}``")
    Loggy.Add (f"Command,Prefix - ``{prefix}``",ctx.author)
    #Changes help message to fit prefix
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=(bot.command_prefix+"Help")))
# ------------------------------------ #
#                Secrets               #
# ------------------------------------ #

# ---------------- Gay --------------- #
@bot.command(name = "Gay")
@commands.is_nsfw()
@commands.cooldown(1,BCN,BucketType.default)
async def Gay(ctx):
    Loggy.Add ("Secret,Gay",ctx.author)
    await ctx.channel.send("no u")

# --------------- Cute --------------- #
#If your reading this, you have free access to this hidden command. If you want dick around with it.
@bot.command(name = "SexyBoy")
@commands.is_nsfw()
@commands.cooldown(1,BCN,BucketType.default)
async def Cute(ctx):
    Loggy.Add ("Secret,Cute",ctx.author)
    await ctx.channel.send("https://imgur.com/a/zBWGUuB")

bot.run(TOKEN)