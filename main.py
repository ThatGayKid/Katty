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
@commands.is_nsfw()
@commands.cooldown(1,BCN,BucketType.default)
async def Help(ctx):
    Loggy.Add ("Command, Help",ctx.author)
    msg = (f"\
    User Commands:\n\
    Help:\n\
        Prints this menu.\n\
        Usage - {bot.command_prefix}Help\n\
    Gen:\n\
        Generates Images based on Input.\n\
        Usage - {bot.command_prefix}Gen\n\
    Add:\n\
        Adds new options for Gen NOT AVALIABLE YET\n\
        Usage - {bot.command_prefix}Add\n\
    \n\
    Admin Only: \n\
    Prefix:\n\
        Changes the bot prefix.\n\
        Usage - {bot.command_prefix}Prefix *PREFIX*\n\
    Limit:\n\
        Changes amount of preloaded images.\n\
        Usage - {bot.command_prefix}Limit *LIMIT*")
    await ctx.channel.send(Form(msg))

# ------------ Add Entries ----------- #
@bot.command(name = "Add")
@commands.is_nsfw()
@commands.cooldown(1,BCR,BucketType.default)
async def AddPost(ctx):
    Loggy.Add("Command,Add Started",ctx)
    Input = ["","",[],""]

# ---------- Option Handler ---------- #
    async def Option(Reaction,BotMessage):
        
        await BotMessage.remove_reaction(Reaction[0],Reaction[1])
        Loggy.Add(f"Command,Add {Reaction[0]}",Reaction[1])
        
        if Reaction[0] == '💬':
            await BotMessage.remove_reaction(Reaction[0],Reaction[1])
            Loggy.Add("AddPost, Option 💬 Started",ctx)
            
            Mes = "Please enter a name for this entry:"
            await BotMessage.edit(content=Form( Mes ))
            
            Input[0] = (await bot.wait_for('message', check=lambda message: message.author == ctx.author)).content
            return 
        
        elif Reaction[0] == '📄':
            await BotMessage.remove_reaction(Reaction[0],Reaction[1])
            Loggy.Add("AddPost, Option 📄 Started",ctx)
            
            Mes = "Write a Description for your entry:"
            await BotMessage.edit(content=Form( Mes ))
            
            Input[1] = "\n"+(await bot.wait_for('message', check=lambda message: message.author == ctx.author)).content
            return 
        
        elif Reaction[0] == '📌':
            await BotMessage.remove_reaction(Reaction[0],Reaction[1])
            
            UserIn = []
            Loggy.Add("AddPost, Option 📌 Started",ctx)
            
            while True:
                Mes = "Now Add a SubReddit to get posts from:"
                await BotMessage.edit(content=Form( Mes ))
                UserIn.append((await bot.wait_for('message', check=lambda message: message.author == ctx.author)).content)
                Mes = \
                f"Would you like to add another?\
                \nCurrent: {UserIn}"
                await BotMessage.edit(content=(Form(Mes)))
                
                EmojisAdd = ['✅','❌']
                #Clear Emojis
                BotMessage.clear_reactions()
                #Add
                for emoji in EmojisAdd:
                    await BotMessage.add_reaction(emoji)
                EmojisAdd = ['✅','❌']
                await asyncio.sleep(0.2)
                
                Awn = await bot.wait_for('reaction_add')
                Reaction = str(Awn[0])
                if Reaction == "❌":
                    Input[2] = UserIn
                    break
            
        
        elif Reaction[0] == '✅':
            Loggy.Add("AddPost, Option ✅ Started",ctx)
            #CHECK SYSTEM HERE
            print(ctx.author)
            msg = \
            f"   {Input[0]}\
            \n   {Input[1]}\
            \n   SubReddits:"
            for Sub in Input[2]:
                \
            msg += f"\n    {Sub}"

            msg += "\n\nAre you happy with this?(Y/N): "
            botmessage = await ctx.channel.send(Form(msg))
            
            for emoji in ['✅','❌']:
                await botmessage.add_reaction(emoji)
            await asyncio.sleep(1)

            while True:
                Awn = await bot.wait_for('reaction_add')
                Reaction = str(Awn[0])
                if Reaction =="✅":
                    return "SUBMIT"
                elif Reaction =="❌":
                    return

# ----------- Main Program ----------- #
    botmessage = await ctx.channel.send('Loading...')
    Emojis = ['💬','📄','📌','✅']
    for emoji in Emojis:
        await botmessage.add_reaction(emoji)
    await asyncio.sleep(0.2)

    while True:
        await botmessage.edit(content=(Form(\
        f"Please select an option:\
        \n💬 - Name: {Input[0]}\
        \n📄 - Description:{Input[1]}\
        \n📌 - Subreddits: {Input[2]}\
        \n✅ - Submit")))

        Awn = await bot.wait_for('reaction_add')
        if await Option(Awn,botmessage) == "SUBMIT":
            break

    Importer.Add(Input[0],Input[1],Input[2],ctx.author)
    log = (f"Command,Add - {Input[0]} - {Input[1]} - {Input[2]}")
    msg=f"Your Entry : {Input[0]} was Added Successfully"
    Loggy.Add(log,ctx)
    await ctx.channel.send(Form(msg))

# ------------- Generate ------------- #
@bot.command(name = "Gen")
@commands.is_nsfw()
@commands.cooldown(1,BCR,BucketType.default)
async def Gen(ctx):
    message = ctx.message.content[(len(bot.command_prefix))+3:]
    if message == "Help":
        msg=Form((Importer.Help()))
    
    elif len(message) == 0:
        msg=Form((Importer.Help()))
        
    else:
        msg=(Importer.GeneratePost(message))

    log = "Command,Generate - "+message
    Loggy.Add(log,ctx)
    await ctx.channel.send(msg)


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