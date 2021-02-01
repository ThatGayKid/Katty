#Python Included Imports
import random,json,os
#Pip included Imports

from dotenv import load_dotenv
load_dotenv()

import praw
reddit = praw.Reddit(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    user_agent=os.getenv("USER_AGENT")
)

JSON = json.load(open('Text/Text.json'))
Limit = int(os.getenv("LIMIT"))

def Check(Sub:str) -> bool:
    TMP = []
    #try:
    for x in reddit.subreddit(Sub).top(limit=(1)):
        TMP.append(x)
        if len(TMP) == 1:
            return True
        return False
    # except:
    #     return False


def Generate(Sub:str)->str:
    if not(Check(Sub)):
        return JSON['Reddit']['BadSub']
    Import = reddit.subreddit(Sub).hot(limit=Limit)
    Result = []
    for Post in Import:
        if Post.url[-4:-3] == ".":
            Result.append(Post.url)
    return random.choice(Result)