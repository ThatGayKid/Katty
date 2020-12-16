# -------------- Imports ------------- #
#Python Imports
import time
import os
#Pip Imports
import discord
from discord.ext import commands
from discord.ext.commands import Bot, has_permissions, CheckFailure
from discord.ext.commands.cooldowns import BucketType
import asyncio

#Locally Stored Imports
import Loggy
import Importer
Loggy.Create("Katty")

from dotenv import load_dotenv
load_dotenv()

# ----------- Bot Variables ---------- #
TOKEN = os.getenv("TOKEN")
bot = commands.Bot(command_prefix=os.getenv("PREFIX"))
BCN = os.getenv("BCN")#Bot Cooldown Normal
BCR = os.getenv("BCR")#Bot Cooldown Reddit

def Form(msg):
    # lines = (msg.split('\n'))
    # for x in range(len(lines)):
    #     lines[x] = f"|  {lines[x]}"
    # msg = "\n".join(lines)
    # return f"```____________________\n{msg}\n________```"
    return f"```\n{msg}\n```"
# ------------------------------------ #
#                  Bot                 #
# ------------------------------------ #

# ----------- Main Section ----------- #
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name=(str(bot.command_prefix+"Help"))))
    Loggy.Add("Discord,Bot Activated","Discord")

# --------------- Help --------------- #
bot.remove_command('help')
@bot.command(name = "Help")
@commands.cooldown(1,BCN,BucketType.default)
async def Help(ctx):
    Loggy.Add ("Command, Help",ctx.author)
    msg = (f"\
User Commands:\n\
    Help:\n\
        Prints this menu.\n\
        Usage - {bot.command_prefix}Help\n\
    Gen:\n\
        Generates Images based on options from Gen Help\n\
        Usage - {bot.command_prefix}Gen\n\
    Add:\n\
        Adds new Gen Options (W.I.P.)\n\
        Usage - {bot.command_prefix}Add\n\
    \n\
Admin Only: \n\
    Prefix:\n\
        Changes the bot's prefix\n\
        Usage - {bot.command_prefix}Prefix *PREFIX*\n\
    Limit:\n\
        Changes amount of preloaded images\n\
        Usage - {bot.command_prefix}Limit *LIMIT*")
    await ctx.channel.send(Form(msg))

# ------------- Generate ------------- #
@bot.command(name = "Gen")
@commands.cooldown(1,BCR,BucketType.default)
async def Gen(ctx):
    message = ctx.message.content[(len(bot.command_prefix))+4:]
    
    if message == "Help":
        msg=Form((Importer.Help()))
    
    elif len(message) == 0:
        msg=Form((Importer.Help()))
        
    else:
        msg=(Importer.GeneratePost(message))

    log = "Command,Generate - "+message
    Loggy.Add(log,ctx)
    await ctx.channel.send(msg)


# ------------ Add Entries ----------- #
@bot.command(name = "Add")
@commands.cooldown(1,BCN,BucketType.default)
async def AddPost(ctx):
    Loggy.Add("Command,Add Started",ctx)
    Input = ["","",[]]

# ---------- Option Handler ---------- #
    async def Option(Reaction,botmessage):
        React=str(Reaction[0])
        User=str(Reaction[1])
        await botmessage.clear_reactions()
        Loggy.Add(f"Command,Add Option {React}",ctx)

        if React == "💬":
            await botmessage.edit(content=Form( "Please enter a name for this entry:" ))
            Input[0] = (await bot.wait_for('message', check=lambda message: message.author == ctx.author)).content
            return 
        
        elif React == '📄':
            await botmessage.edit(content=Form( "Write a Description for your entry:" ))
            Input[1] = (await bot.wait_for('message', check=lambda message: message.author == ctx.author)).content
            return 

        elif React == '📌':
            Subs = []
            while True:
                await botmessage.edit(content=Form( 'Now Add a SubReddit to get posts from:\nExample: "memes" or "r/pics"' ))
                Sub = (await bot.wait_for('message', check=lambda message: message.author == ctx.author)).content.lower()
                
                #Remove Formatting
                if Sub[:2] == "r/":
                    Sub = Sub[2:]
                    
                #Check if it's valid
                if Importer.Check(Sub) != True:
                    msg="Subreddit is invalid so it has not added. "
                elif Sub in Subs:
                    msg="Subreddit has already been added. "
                else:
                    msg = ""
                    Subs.append(Sub)
                
                if len(Subs) == 0:
                    msg += "Please Enter a Subreddit."
                elif len(Subs) == 1:
                    msg += "Is this your final Subreddit?"
                else:
                    msg += "Are these your final Subreddits?"
                    
                await botmessage.edit(content=(Form(msg+f"\nCurrent: {Subs}")))
                
                if len(Subs) > 0:
                    for emoji in ['➕','✅']:
                        await botmessage.add_reaction(emoji)
                    await asyncio.sleep(0.5)

                    Awn = await bot.wait_for('reaction_add')
                    await botmessage.clear_reactions()
                    if str(Awn[0]) == "✅":
                        Input[2] = Subs
                        break
            return
        
        elif React == '✅':
            #Check if all the entries are full
            for x in Input:
                if len(x) == 0:
                    await botmessage.edit(content=(Form("Error: Missing an Entry!")))
                    await asyncio.sleep(3)
                    return
                
            msg = \
            f"\nName: {Input[0]}\
              \nDescription:{Input[1]}\
              \nSubreddits: {Input[2]}\
            \n\nAre you happy with this?:"
            
            await botmessage.edit(content=(Form(msg)))
            for emoji in ['❌','✅']:
                await botmessage.add_reaction(emoji)
            await asyncio.sleep(0.3)
            
            while True:
                Awn = await bot.wait_for('reaction_add')
                await botmessage.clear_reactions()
                Reaction = str(Awn[0])
                if Reaction =="✅":
                    return "SUBMIT"


    botmessage = await ctx.channel.send('Loading...')
    while True:
        await botmessage.edit(content=(Form("Loading...")))
        await botmessage.clear_reactions()
        
        for emoji in ['💬','📄','📌','✅']:
            await botmessage.add_reaction(emoji)
        await asyncio.sleep(0.2)
        
        await botmessage.edit(content=(Form(\
        f"Please select an option:\
        \n💬 - Name: {Input[0]}\
        \n📄 - Description: {Input[1]}\
        \n📌 - Subreddits: {Input[2]}\
        \n✅ - Submit")))

        Awn = await bot.wait_for('reaction_add')
        if await Option(Awn,botmessage) == "SUBMIT":
            break

    Importer.Add(Input[0],Input[1],Input[2],ctx.author)
    Loggy.Add(f"Command,Add - {Input[0]} - {Input[1]} - {Input[2]} - {str(ctx.author)}",ctx)
    await botmessage.edit(content=(Form(f"{Input[0]} was Successfully Added")))

@bot.command(name = "Del")
@commands.cooldown(1,BCN,BucketType.default)
async def RemovePost(ctx):
    await ctx.channel.send('WIP')

@bot.command(name = "Edit")
@commands.cooldown(1,BCN,BucketType.default)
async def RemovePost(ctx):
    await ctx.channel.send('WIP')
# ------------------------------------ #
#----------------Admin-----------------#
# ------------------------------------ #

# --------------- Limit -------------- #
@bot.command(name = "Limit")
@commands.has_permissions(ban_members=True, kick_members=True) 
async def Limit(ctx, Limit):
    Importer.Limit = Limit
    Loggy.Add (f"Admin, Limit - {Limit}",ctx)
    msg = (f"Limit changed to "+Importer.Limit)
    await ctx.send(Form(msg))

# -------------- Prefix -------------- #
@bot.command(name = "Prefix")
@commands.has_permissions(ban_members=True, kick_members=True) 
async def setprefix(ctx,*,prefix):
    bot.command_prefix = prefix
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=(bot.command_prefix+"Help")))
    Loggy.Add ("Admin,Prefix - "+prefix,ctx)
    msg = (f"Prefix changed to ``{prefix}``")
    await ctx.send(Form(msg))
    #Changes help message to fit prefix
    

# ------------------------------------ #
#                Secrets               #
# ------------------------------------ #

# ---------------- Gay --------------- #
@bot.command(name = "Gay")
@commands.cooldown(1,BCN,BucketType.default)
async def Gay(ctx):
    Loggy.Add ("Secret,Gay",ctx)
    botmessage = await ctx.channel.send(Form("no u"+ctx.user))

# --------------- Cute --------------- #
#If your reading this, you have free access to this hidden command. If you want dick around with it.
@bot.command(name = "SexyBoy")
@commands.cooldown(1,BCN,BucketType.default)
async def Cute(ctx):
    Loggy.Add ("Secret,Cute",ctx)
    await ctx.channel.send("https://imgur.com/a/zBWGUuB")
                   
bot.run(TOKEN)