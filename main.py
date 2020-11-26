# -------------- Imports ------------- #
import Importer
import Loggy

import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
load_dotenv()

# ----------- Bot Variables ---------- #

TOKEN = (os.getenv('TOKEN'))
bot = commands.Bot(command_prefix="!RR")
bot.remove_command('help')

# ----------- Main Section ----------- #

@bot.event
async def on_ready():
    Loggy.Add("Discord: Bot Started","Discord")



@bot.command(name = "Rip")
async def Ripper(ctx,subreddit):
        Loggy.Add ("Ripping Image",ctx.author)
        await ctx.channel.send(Importer.Picture(subreddit))
    # @commands.cooldown(1, 10, commands.BucketType.user) 
# ------------------------------------ #
#                Secrets               #
# ------------------------------------ #

# ---------------- Gay --------------- #
@bot.command(name = "Gay")
async def Gay(ctx):
        Loggy.Add ("Secret - Gay",ctx.author)
        await ctx.channel.send("no u")

# --------------- Cute --------------- #

@bot.command(name = "Who's_The_Cutest_Of_Them_All?")
async def Cute(ctx):
        Loggy.Add ("Secret - Cute",ctx.author)
        await ctx.channel.send("https://i.imgur.com/SiKKBLU.jpg")

bot.run(TOKEN)