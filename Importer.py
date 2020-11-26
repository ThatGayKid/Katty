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


def Picture(SubReddit):
	Posts=[]
	for submission in reddit.subreddit(SubReddit).hot(limit=100):
		if int(random.randint(0,100)) == 1:
			Posts.append(submission.url)
	return Posts[int(random.randint(0,100))]