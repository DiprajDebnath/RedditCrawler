import json
import praw
import logging
import datetime
import atexit
from collections import OrderedDict
from pprint import pprint



client_id="IlAaIMNtV8ClGY3cRhhpYw"
client_secret="ZITbTKXqn_kfhQcPmgm_iRi46YgIlg" 
user_agent="crawler for reddit"

# Reddit instance
reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent,
)

# assume you have a reddit instance bound to variable `reddit`
subreddit = reddit.subreddit("python")
print(subreddit.title)
pprint(vars(subreddit))