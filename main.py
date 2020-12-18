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
#Asyncio Delay Tyes
FailDelay    = 5  #Delay for a command failing
TimeoutDelay = 60 #Delay for a command to timeout
DeleteDelay  = 10 #Delay for deleting a message
EmojiDelay  = 0.3 #Delay for reacting to emoji
def Form(msg):
    return f"```{msg}```"
# ------------------------------------ #
#                  Bot                 #
# ------------------------------------ #

# ----------- Main Section ----------- #
@bot.event
async def Ready():
    Loggy.Add ("Bot,Started","Discord")
    await bot.change_presence(activity=discord.Game(name=(str("Try: "+bot.command_prefix+"Help"))))

# --------------- Help --------------- #
#How long the help message should stay up before deleting
HelpRemain = 30
bot.remove_command('help')
@bot.command(name = "Help")
@commands.cooldown(1,HelpRemain,BucketType.default)
async def Help(ctx):
    Loggy.Add ("Help,Start",ctx)
    msg = (f"\
User Commands:\n\
  Help:\n\
    Prints this menu.\n\
    Usage - {bot.command_prefix}Help\n\
  Gen:\n\
    Generates Images based on options from Gen Help\n\
    Usage - {bot.command_prefix}Gen\n\
  Add:\n\
    Adds new Gen Options\n\
    Usage - {bot.command_prefix}Add\n\
    \n\
  Del:\n\
    Delete a  Gen Options (W.I.P.)\n\
    Usage - {bot.command_prefix}Add\n\
    \n\
  Edit:\n\
    Edit a Gen Options (W.I.P.)\n\
    Usage - {bot.command_prefix}Add\n\
    \n\
Owner Only: \n\
  Prefix:\n\
    Changes the bot's prefix\n\
    Usage - {bot.command_prefix}Prefix *PREFIX*\n\
  Limit:\n\
    Changes amount of preloaded images\n\
    Usage - {bot.command_prefix}Limit *LIMIT*\
")
    botmessage = await ctx.channel.send(Form(msg))
    Loggy.Add ("Help,Displayed",ctx)
    await asyncio.sleep(HelpRemain)
    await botmessage.delete()
    Loggy.Add ("Help,Deleted",ctx)
    Loggy.Add ("Help,End",ctx)

# ------------- Generate ------------- #
@bot.command(name = "Gen")
@commands.max_concurrency(1,per=BucketType.default,wait=True)
async def Gen(ctx):
    Loggy.Add(f"Generate,Start",ctx)
    message = ctx.message.content[(len(bot.command_prefix))+4:]
    
    if message == "Help" or len(message) == 0:
        msg=Form((Importer.Help()))
        Loggy.Add(f"Generate,Help",ctx)

    else:
        msg=(Importer.GeneratePost(message))
        Loggy.Add(f"Generate,Image - {message}",ctx)

    Loggy.Add(f"Generate,End",ctx)
    await ctx.channel.send(msg)
    

# ------------ Add Entries ----------- #
@bot.command(name = "Add")
@commands.max_concurrency(1,per=BucketType.default,wait=False)
@commands.guild_only()
async def Add(ctx):
    Loggy.Add("Add,Start",ctx)
    Input = ["","",[]]
# ---------- Option Handler ---------- #
    async def Option(Reaction,botmessage):
        React=str(Reaction[0])
        User=str(Reaction[1])
        await botmessage.clear_reactions()
        Loggy.Add(f"Add,Option {Reaction[0]}",ctx)

        if React == "💬":
            await botmessage.edit(content=Form( "How about you give it a catchy name:" ))
            try:
                Input[0] = (await bot.wait_for('message', timeout=60 , check=lambda message: message.author == ctx.author)).content
                Loggy.Add(f"Add,Name - {Input[0]}",ctx)
            except asyncio.TimeoutError:
                Loggy.Add(f"Add,Name Timeout",ctx)
                await botmessage.edit(content=Form( "Ah,I Timed Out." ))
                await asyncio.sleep(TimeoutDelay)
            return 
        
        elif React == '📄':
            await botmessage.edit(content=Form( "Type out a nice description for me:" ))
            try:
                Input[1] = (await bot.wait_for('message', timeout=60 , check=lambda message: message.author == ctx.author)).content
                Loggy.Add(f"Add,Description - {Input[1]}",ctx)
            except asyncio.TimeoutError:
                Loggy.Add(f"Add,Description Timeout",ctx)
                await botmessage.edit(content=Form( "Ah,I Timed Out." ))
                await asyncio.sleep(TimeoutDelay)
            return 

        elif React == '📌':
            Subs = []
            while True:
                await botmessage.edit(content=Form( 'Now you can type out a Subreddit\nHere are some examples: "memes","r/pics"' ))
                try:
                    Sub = (await bot.wait_for('message', timeout=60 , check=lambda message: message.author == ctx.author)).content.lower()
                    Loggy.Add(f"Add,SubReddit - {Sub}",ctx)
                except asyncio.TimeoutError:
                    Loggy.Add(f"Add,SubReddit Text Timeout",ctx)
                    await botmessage.edit(content=Form( "Ah,I Timed Out." ))
                    await asyncio.sleep(TimeoutDelay)
                    break
                
                #Remove Formatting
                if Sub[:2] == "r/":
                    Sub = Sub[2:]
                    
                #Check if it's valid
                if Importer.Check(Sub) != True:
                    msg="Thay Subreddit was Invalid so I didn't add it."
                    Loggy.Add(f"Add,SubReddit Invalid - {Sub}",ctx)
                elif Sub in Subs:
                    msg="Dude! You already have that Subreddit."
                    Loggy.Add(f"Add,SubReddit Repeat - {Sub}",ctx)
                else:
                    msg = ""
                    Subs.append(Sub)
                    Loggy.Add(f"Add,SubReddit Added {Sub}",ctx)
                
                if len(Subs) > 0:
                    msg += "Is this gonna be it?"
                    
                await botmessage.edit(content=(Form(msg+f"\nCurrent ones: {Subs}")))
                
                for emoji in ['➕','✅']:
                    await botmessage.add_reaction(emoji)
                await asyncio.sleep(EmojiDelay)
                try:
                    Awn = await bot.wait_for('reaction_add', timeout=60)
                except asyncio.TimeoutError:
                    Loggy.Add(f"Add,SubReddit Accept Timeout",ctx)
                    await botmessage.edit(content=Form( "Ah,I Timed Out." ))
                    await asyncio.sleep(TimeoutDelay)
                    break
                
                await botmessage.clear_reactions()
                if str(Awn[0]) == "✅":
                    Input[2] = Subs
                    Loggy.Add(f"Add,SubReddits Added - {Input[2]}",ctx)
                    break
            return
        
        elif React == '✅':
            #Check if all the entries are full
            for x in Input:
                if len(x) == 0:
                    Loggy.Add(f"Add,Submit Missing Entry",ctx)
                    await botmessage.edit(content=(Form("Oops an Error, You're Missing an Entry.")))
                    await asyncio.sleep(FailDelay)
                    return
                
            msg = \
            f"\nName:        {Input[0]}\
              \nDescription: {Input[1]}\
              \nSubreddits:  {Input[2]}\
            \n\nIs this okay with you?"
            
            await botmessage.edit(content=(Form(msg)))
            for emoji in ['❌','✅']:
                await botmessage.add_reaction(emoji)
            await asyncio.sleep(EmojiDelay)
            
            while True:
                try:
                    Awn = await bot.wait_for('reaction_add', timeout=60)
                except asyncio.TimeoutError:
                    Loggy.Add(f"Add,Submit Timeout",ctx)
                    await botmessage.edit(content=Form( "Ah,I Timed Out." ))
                    await asyncio.sleep(TimeoutDelay)
                    break
                await botmessage.clear_reactions()
                Reaction = str(Awn[0])
                if Reaction =="✅":
                    Loggy.Add(f"Add,Submit Success",ctx)
                    return "SUBMIT"
                else:
                    Loggy.Add(f"Add,Submit Failed",ctx)


    botmessage = await ctx.channel.send("I'm Just Loading...")
    while True:
        await botmessage.edit(content=(Form("I'm Just Loading...")))
        await botmessage.clear_reactions()
        
        for emoji in ['💬','📄','📌','✅']:
            await botmessage.add_reaction(emoji)
        await asyncio.sleep(EmojiDelay)
        
        await botmessage.edit(content=(Form(\
        f"Could you select an option?\
        \n💬 - Name:        {Input[0]}\
        \n📄 - Description: {Input[1]}\
        \n📌 - Subreddits:  {Input[2]}\
        \n✅ - Submit")))
        try:
            Awn = await bot.wait_for('reaction_add', timeout=60)
        except asyncio.TimeoutError:
            await botmessage.clear_reactions()
            await botmessage.edit(content=Form( "Ah,I Timed Out." ))
            await asyncio.sleep(DeleteDelay)
            await botmessage.delete()
            break
        ConfirmTest = await Option(Awn,botmessage)
        if ConfirmTest  == True:
            break

    if ConfirmTest  == True:
        Importer.Add(Input[0],Input[1],Input[2],ctx.author)
        Loggy.Add(f"Add, New Entry - {Input[0]},{Input[1]},{Input[2]},{str(ctx.author)}",ctx)
        await botmessage.edit(content=(Form(f"I successfully added {Input[0]} 🌝")))
        await asyncio.sleep(DeleteDelay)
        await botmessage.delete()
        
    Loggy.Add(f"Add,End",ctx)

@bot.command(name = "Del")
@commands.max_concurrency(1,per=BucketType.default,wait=False)
async def Del(ctx):
    Loggy.Add(f"Del,Start",ctx)
    botmessage = await ctx.channel.send('WIP')
    await asyncio.sleep(DeleteDelay)
    botmessage.delete()
    Loggy.Add(f"Del,End",ctx)

@bot.command(name = "Edit")
@commands.max_concurrency(1,per=BucketType.default,wait=False)
async def Edit(ctx):
    Loggy.Add(f"Edit,Start",ctx)
    botmessage = await ctx.channel.send('WIP')
    await asyncio.sleep(DeleteDelay)
    botmessage.delete()
    Loggy.Add(f"Edit,End",ctx)
# ------------------------------------ #
#----------------Admin-----------------#
# ------------------------------------ #

# --------------- Limit -------------- #
@bot.command(name = "Limit")
@commands.max_concurrency(1,per=BucketType.default,wait=False)
@commands.is_owner()
async def Limit(ctx):
    Loggy.Add(f"Limit,Start",ctx)
    message = ctx.message.content[(len(bot.command_prefix))+5:]
    if len(message) == 0:
        msg=f"I currently pick from the top {Importer.Limit} posts"
        Loggy.Add(f"Limit,Display",ctx)
    else:
        try:
            Importer.Limit = int(message)
            msg=f"✅: I pick from the top {Importer.Limit} posts now."
            Loggy.Add(f"Limit, Changed -{message}",ctx)
        except:
            msg=f"❌: Dude, that's incorrect usage! Come on, read the docs."
            Loggy.Add(f"Limit,Error -{message}",ctx)
            
    await ctx.channel.send(Form(msg))
    Loggy.Add(f"Limit,End",ctx)
    
# -------------- Prefix -------------- #
@bot.command(name = "Prefix")
@commands.max_concurrency(1,per=BucketType.default,wait=False)
@commands.is_owner()
async def Prefix(ctx):
    Loggy.Add(f"Prefix,Start",ctx)
    message = ctx.message.content[(len(bot.command_prefix))+7:]
    if len(message) == 0:
        msg=f"You can call me with {bot.command_prefix}."
        Loggy.Add(f"Prefix,Display",ctx)
    else:
        try:
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=(bot.command_prefix+"Help")))
            msg=f"✅: You can now call me with {bot.command_prefix}."
            Loggy.Add(f"Prefix, Changed -{message}",ctx)
        except:
            msg=f"❌: Dude, that's incorrect usage! Come on, read the docs."
            Loggy.Add(f"Prefix,Error -{message}",ctx)
            
    await ctx.channel.send(Form(msg))
    Loggy.Add(f"Prefix,End",ctx)
    

# ------------------------------------ #
#                Secrets               #
# ------------------------------------ #

# ---------------- Gay --------------- #
@bot.command(name = "Gay")
async def Gay(ctx):
    Loggy.Add ("Gay,No U",ctx)
    botmessage = await ctx.channel.send(Form("no u"+ctx.user))

# --------------- Cute --------------- #
#If your reading this, you have free access to this hidden command. If you want dick around with it.
@bot.command(name = "SexyBoy")
async def Cute(ctx):
    Loggy.Add ("Cute,Generated",ctx)
    await ctx.channel.send("https://imgur.com/a/zBWGUuB")
                   
bot.run(TOKEN)