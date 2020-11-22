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
SubReddits=['cat','cats','animecatgirls','Nekomimi','AnimeGirls','AverageAnimeTiddies']
def Picture(Type):
    SubReddit = SubReddits[(int(random.randint(0,1)))+(Type*2)]
    Posts=[]
    for submission in reddit.subreddit(SubReddit).hot(limit=20):
        Posts.append(submission.url)
    return Posts[int(random.randint(0,19))]