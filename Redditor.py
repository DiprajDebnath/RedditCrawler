"""
Crawl Comments and Submissions from subreddit.
Date : 2022-03-11
"""
import json
import praw
import logging
import datetime
import atexit
from collections import OrderedDict
from pprint import pprint

client_id="QmYcE5AJDFFR0_OeG__I-Q"
client_secret="3UjqFoW1yfpE_Tj9YXyx5Ri0U9NFEw" 
user_agent="crawler for reddit"


# Reddit instance
reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent,
)

redditor = reddit.redditor("high_roller_dude")
print(redditor.id)
pprint(vars(redditor))