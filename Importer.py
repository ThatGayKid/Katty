import random
from array import *

import praw
from progress.bar import Bar

from dotenv import load_dotenv
import os
load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    user_agent=os.getenv("USER_AGENT")
)


# ------------------------------------ #
#             Dictionaries             #
# ------------------------------------ #

# ------------ Conversion ------------ #
lstConvDicts = [
    {
    #r/AnimeGirls
    #Note: alternative with s on end
    "kitty"        : "AnimeGirls",
    "anime"        : "AnimeGirls",
    "egirl"        : "AnimeGirls",
    "animegirl"    : "AnimeGirls"
    },
    {
    "katty"         : "CatGirls",
    "catty"         : "CatGirls",
    "animecatgirl" : "CatGirls",
    "catgirl"      : "CatGirls"
    }
    ]

# ------------ Subreddits ------------ #
DictSubs = {
    "AnimeGirls" : ['AnimeGirls','AverageAnimeTiddies'],
    "CatGirls"   : ['animecatgirls','Nekomimi']
}

# ------------------------------------ #
#               Functions              #
# ------------------------------------ #

#Creates a dictonary of posts

Posts = {
    "AnimeGirls": [],
    "CatGirls" : []
}
def GeneratePosts(Input):
    bar = Bar(('Importing Image - '+Input), fill='#', max=101)
    bar.next()
    TMPPosts = []
    
    #While there are less thann 100 posts stored
    while len(Posts[Input]) <= 100 :
        #For all the subreddits for the input
        for x in range(len(DictSubs[Input])):
            #Define the sub
            Sub = DictSubs[Input][x]
            #Generate the posts form the sub
            Import = reddit.subreddit(Sub).hot(limit=300)
            #Take each posts and dispose of the non
            for Post in Import:
                if Post.url[-4:-3] == ".":
                    TMPPosts.append(Post.url)
            bar.next(50)
        random.shuffle(TMPPosts)
        #Trim Posts to 200
        Posts[Input] = TMPPosts[100:]
        bar.finish()
        

def Picture(Input):
# ---------- Sanatise input ---------- #
    #Lowercase it
    Input = Input.lower()
    #Replace Spaces
    Spaces = [" ","-","_"]
    TMP = ""
    #For the length of Space Characters
    for Chr in Input:
        #If a non-space character
        if Chr not in Spaces:
            #Append It
            TMP = TMP + Chr
    Input = TMP

    #Remove "s" at the end of the string
    if Input[-1] == "s":
        Input = Input[:-1]


# -------- Auto-Corrects Term -------- #
#Run through theconversion dictionary
    for Dicts in lstConvDicts:
        #If the term is in a dictionary
        if Input in Dicts:
            #Return the name of the entry
            #e.g. (is Anime_Girls in the AnimeGirls entry) yes so AnimeGirls is returned
            Input = (Dicts[Input])


    for Types in range(len(DictSubs)):
        if len(Posts[Input]) < 1:
            GeneratePosts(Input)
    
            
    Response = Posts[Input][0]
    del Posts [Input][0]
    return Response

#Create post lists
for Subs in DictSubs:
    Picture(Subs)
    