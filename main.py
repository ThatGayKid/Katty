# -------------- Imports ------------- #
import discord
from discord.ext import commands
from discord.ext.commands import Bot, has_permissions, CheckFailure
from discord.ext.commands.cooldowns import BucketType
import Importer

import Loggy
Loggy.Create("Katty")

import os
from dotenv import load_dotenv
load_dotenv()

# ----------- Bot Variables ---------- #
TOKEN = os.getenv("TOKEN")
bot = commands.Bot(command_prefix="!K ")

HHelp = ("```\
Help   - Displays this menu\n\
Catty  - Shows you a Cute Cat Girl\n\
Kitty  - Shows you a Cute Anime Girl\n\
```")

BCN = 5#Bot Cooldown Normal
BCR = 2#Bot Cooldown Reddit

# ------------------------------------ #
#                  Bot                         #
# ------------------------------------ #

# ----------- Main Section ----------- #
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="you ;)")) 
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

@bot.command(name = "Prefix")
@commands.has_permissions(ban_members=True, kick_members=True) 
async def setprefix(ctx, prefix):
    bot.command_prefix = prefix
    await ctx.send(f"Prefix changed to ``{prefix}``")

# --------------- Catty -------------- #
@bot.command(name = "Catty")
@commands.is_nsfw()
@commands.cooldown(1,BCR,BucketType.default)
async def Catty(ctx):
    Loggy.Add ("Command,Catty",ctx.author)
    await ctx.channel.send(Importer.Picture(0))

# --------------- Kitty -------------- #
@bot.command(name = "Kitty")
@commands.is_nsfw()
@commands.cooldown(1,BCR,BucketType.default)
async def Kitty(ctx):
    Loggy.Add ("Command,Kitty",ctx.author)
    await ctx.channel.send(Importer.Picture(1))

# ---------------- Gay --------------- #
@bot.command(name = "Gay")
@commands.is_nsfw()
@commands.cooldown(1,BCN,BucketType.default)
async def Gay(ctx):
    Loggy.Add ("Secret,Gay",ctx.author)
    await ctx.channel.send("no u")

# --------------- Cute --------------- #
@bot.command(name = "Cutey Pie")
@commands.is_nsfw()
@commands.cooldown(1,BCN,BucketType.default)
async def Cute(ctx):
    Loggy.Add ("Secret,Cute",ctx.author)
    await ctx.channel.send("https://i.imgur.com/SiKKBLU.jpg")

bot.run(TOKEN)