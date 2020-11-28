import random
from array import *

import praw

from dotenv import load_dotenv
import os
load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    user_agent=os.getenv("USER_AGENT")
)

#Cats - CatGirls - Anime Girls
SubReddits=[['animecatgirls','Nekomimi'],['AnimeGirls','AverageAnimeTiddies']]
Posts = [[],[]]

def GeneratePosts(Type):
    TmpPosts=[]
    Posts[Type]
    
    while len(Posts[Type]) <= 50 :
        for x in range(len(SubReddits[Type])):
            Sub = SubReddits [Type][x]
            Import = reddit.subreddit(Sub).hot(limit=200)
            del Sub
            
            for Post in Import:
                if Post.url[-4:-3] == ".":
                    TmpPosts.append(Post.url)
        random.shuffle(TmpPosts)
        Posts[Type] = TmpPosts[50:]


def Picture(Type):
    for Types in range(len(SubReddits)):
        if len(Posts[Types]) < 1:
            GeneratePosts(Types)
    Response = Posts[Type][0]
    del Posts [Type][0]
    return Response

print(Picture(0))