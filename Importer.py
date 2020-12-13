#Python Included Imports
import random
from array import *
import os
#Pip included Imports
from progress.spinner import PieSpinner

from dotenv import load_dotenv
load_dotenv()

import praw
reddit = praw.Reddit(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    user_agent=os.getenv("USER_AGENT")
)
    


# ------------------------------------ #
#             Dictionaries             #
# ------------------------------------ #



#Bot Variables
AutoCorrectStatus = int((os.getenv("CORRECTIONS")))
Limit = int(os.getenv("LIMIT"))
Presets = {}
# ------------------------------------ #
#               Functions              #
# ------------------------------------ #

def Help():
    msg = "Options:"
    #Prints Name then Discrption for each entry
    for Option in Presets:
        msg += f"\n\n  {Presets[Option]['Name']}"
        msg += f"      {Presets[Option]['Description']}"
        msg += "\n   SubReddits:"
        for Subreddits in Presets[Option]['SubReddits']:
            msg += f"\n     {Subreddits}"
    #Appeneds Discord Formatting To the End
    return msg

def Add(InName,InDescription,InSubReddits,InAuthor):
    Presets [str(InName)]={
         "Name"         : InName,
         "Description"  : InDescription,
         "SubReddits"   : InSubReddits,
         "Author"       : InAuthor,
         "Posts"        : iter(['End']),
         "Tags"         : "NONE" #Not Implimented Yet
         }

def Edit(OName,InType,InText):
    Presets[str(OName)][InType] = InText

def Delete(UName,Preset):
    if Presets[Preset]['Author'] == UName:
        del Presets[Preset]
        return f"{Preset} deleted successfully."
    else:
        return f"{Preset} has not been deleted, you are not the author"

def Check(SubReddit):
    TMP = []
    try:
        for x in reddit.subreddit(SubReddit).top(limit=(1)):
            TMP.append(x)
            return True
    except: 
        return False

def GeneratePost(Input):
    #Combine these 2 later
    for Entry in Presets:
        if Input in Entry:
            Input = Entry

    if Input not in Presets:
        return\
(f"{Input} isn't a valid option :frowning:\n\
Try using Gen Help")

    Result = next(Presets[Input]['Posts'])

    if Result == "End":
        PreprocessPosts(Input)
        Result = next(Presets[Input]['Posts'])

#Return the result

    return Result


def PreprocessPosts(Input):
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
