#Python Included Imports
import random
from array import *

#Pip included Imports
from progress.spinner import PieSpinner
import praw

from dotenv import load_dotenv
import os
load_dotenv()


# ------------------------------------ #
#             Dictionaries             #
# ------------------------------------ #



#Bot Variables
AutoCorrectStatus = False
Limit = 10
Presets = {}
# ------------------------------------ #
#               Functions              #
# ------------------------------------ #

def Help(Message):
    msg = "```Options:"
    #Prints Name then Discrption for each entry
    for Option in Presets:
        msg += f"\n    {Presets[Option]['Name']} :"
        msg += f"\n        {Presets[Option]['Description']}"
    #Appeneds Discord Formatting To the End
    msg+='```'
    return msg

def Add(InName,InDescription,InSubReddits):
    Presets [str(InName)]={
         "Name"         : InName,
         "Description"  : InDescription,
         "SubReddits"   : InSubReddits,
         "Posts"        : iter(['End'])
         }

def GeneratePost(Input):
    #Combine these 2 later
    if Input not in Presets:
        return\
(f"{Input} isn't a valid option :frowning:\n\
Try using Gen Help")

    Result = next(Presets[Input]['Posts'])

    if Result == "End":
        PreprocessPosts(Input)
#Return the result
    return Result


def PreprocessPosts(Input):
    reddit = praw.Reddit(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        user_agent=os.getenv("USER_AGENT")
    )
    TMP = ""
    TMPPosts = []
    spinner = PieSpinner("Generating Posts for "+Input+" ")
    #Generate the posts form the sub
    #Appends subreddit to a string
    for Sub in Presets[Input]["SubReddits"]:
        if TMP == Presets[Input]["SubReddits"][-1]:
            TMP = TMP + (Sub)
        else:
            TMP = TMP + (Sub+"+")
            spinner.next()
        Import = reddit.subreddit(TMP).hot(limit=(Limit*1.25))
    del TMP
    #Take each posts and dispose of the non image posts
    for Post in Import:
        spinner.next()
        if Post.url[-4:-3] == ".":
            TMPPosts.append(Post.url)
    random.shuffle(TMPPosts)
    
    Result = (TMPPosts[:Limit])
    Result.append('End')
    Presets[Input]["Posts"] = iter(Result)
    spinner.finish()


Add("Anime Titty Comittee","Shows you a member of the ATE(Anime Titty Committee).",['AnimeGirls','AverageAnimeTiddies'])
Add("Pets At Home","Shows you the cutest Kitty Catty you've ever seen.",['animecatgirls','Nekomimi'])

#Create post lists
for Entry in Presets:
    PreprocessPosts(Entry)

