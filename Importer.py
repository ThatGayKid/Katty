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
    Sub = (SubReddits[(random.randint(0,1))+(Type*2)])
    while True:
        Post = ImportImage(Sub,50)
        if Post[-4:-3] == ".":
            return Post
        
#Import a random url t
def ImportImage(Sub,Total):
    Import = reddit.subreddit(Sub).hot(limit=Total)
    Posts = []
    for Submission in Import:
        Posts.append(Submission.url)
    return random.choice(Posts)

