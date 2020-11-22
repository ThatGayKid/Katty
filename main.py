# -------------- Imports ------------- #
import discord
from discord.ext import commands
from discord.ext.commands import Bot, has_permissions, CheckFailure
import Importer
import Loggy

import os
from dotenv import load_dotenv
load_dotenv()

# ----------- Bot Variables ---------- #

TOKEN = (os.getenv('TOKEN'))
bot = commands.Bot(command_prefix="!Katty ")
bot.remove_command('help')

# ----------- Main Section ----------- #

@bot.event
async def on_ready():
    Loggy.Add("Discord: Bot Started","Discord")


# ----------- Help Command ----------- #
HHelp = ("```\
Help   - Displays this menu\n\
Catty  - Shows you a Cute Cat Girl\n\
Kitty  - Shows you a Cute Cat\n\
Pussy  - Shows you a Cute Anime Girl\n\
```")
    
@bot.command(name = "Help")
async def Help(ctx):
        Loggy.Add ("Command - Help: Starting",ctx.author)
        msg = (HHelp)
        await ctx.channel.send(msg)
        return

# ------------------------------------ #
#             Main Commands            #
# ------------------------------------ #

# --------------- Catty -------------- #
@bot.command(name = "Catty")
async def Catty(ctx):
        Loggy.Add ("Command - Catty: Starting",ctx.author)
        await ctx.channel.send(Importer.Picture(0))
        return

# --------------- Kitty -------------- #
@bot.command(name = "Kitty")
async def Kitty(ctx):
        Loggy.Add ("Command - Kitty: Starting",ctx.author)
        await ctx.channel.send(Importer.Picture(1))
        return

# --------------- Pussy -------------- #
@bot.command(name = "Pussy")
async def Pussy(ctx):
        Loggy.Add ("Command - Pussy: Starting",ctx.author)
        await ctx.channel.send(Importer.Picture(2))
        return

# ------------------------------------ #
#                Secrets               #
# ------------------------------------ #

# ---------------- Gay --------------- #
@bot.command(name = "Gay")
async def Gay(ctx):
        Loggy.Add ("Secret - Gay",ctx.author)
        await ctx.channel.send("no u")
        return

# --------------- Cute --------------- #

@bot.command(name = "Who's_The_Cutest_Of_Them_All?")
async def Cute(ctx):
        Loggy.Add ("Secret - Cute",ctx.author)
        await ctx.channel.send("https://i.imgur.com/SiKKBLU.jpg")
        return

bot.run(TOKEN)