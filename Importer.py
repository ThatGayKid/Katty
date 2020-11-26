import praw
import random

from dotenv import load_dotenv
import os
load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    user_agent=os.getenv("USER_AGENT")
)

#Cats - CatGirls - Anime Girls
SubReddits=['animecatgirls','Nekomimi','AnimeGirls','AverageAnimeTiddies']
def Picture(Type):
    Sub = reddit.subreddit(SubReddits[(random.randint(0,1))+(Type*2)])
    Submissions = reddit.get_subreddit(Sub).get_hot(limit=100)
    for Posts in Submissions:
        if random.randint(0,99) == 0:
            return Posts
    return Submissions[99]
    
    
