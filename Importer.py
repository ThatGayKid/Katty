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
    "anime"        : "AnimeGirl",
    "girl"        : "AnimeGirl",
    "egirl"        : "AnimeGirl",
    "animegirl"    : "AnimeGirl"
    },
    {
    "kitty"        : "CatGirl",
    "katty"        : "CatGirl",
    "catty"        : "CatGirl",
    "catgirl"      : "CatGirl",
    "catgirl"      : "CatGirl"
    }
    ]

# ------------ Subreddits ------------ #
DictSubs = {
    "AnimeGirl" : ['AnimeGirls','AverageAnimeTiddies'],
    "CatGirl"   : ['animecatgirls','Nekomimi']
}

# ------------------------------------ #
#               Functions              #
# ------------------------------------ #

#Creates a dictonary of posts

Posts = {
    "AnimeGirl": [],
    "CatGirl"  : []
}
Limit = 200
def GeneratePosts(Input):
    bar = Bar(('Importing Image - '+Input), fill='V',suffix='ETA:%(eta)ds', max=(99))
    bar.next()
    TMPPosts = []
    
    #While there are less thann 200 posts stored
    while len(Posts[Input]) <= 200 :
        #For all the subreddits for the input
        #Define the sub
        #Generate the posts form the sub
        TMP = ""
        for Sub in DictSubs[Input]:
            TMP = TMP + (Sub+"+")
        Import = reddit.subreddit(TMP).hot(limit=(Limit*1.2))
        #Take each posts and dispose of the non image posts
        for Post in Import:
            if Post.url[-4:-3] == ".":
                TMPPosts.append(Post.url)
        bar.next(49)
        random.shuffle(TMPPosts)
        #Trim Posts to 200
        Posts[Input] = TMPPosts[Limit:]
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
        #If a non-space character append it
        if Chr not in Spaces:
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


    for x in Posts:
        if len(Posts[Input]) < 1:
            GeneratePosts(Input)
    
            
    Response = Posts[Input][0]
    del Posts [Input][0]
    return Response

#Create post lists
for Subs in DictSubs:
    Picture(Subs)
    