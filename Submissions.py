"""
Crawl submissions(posts) from subreddit.
Date : 2022-03-11
"""
import json
import praw
import logging
from pprint import pprint

# Logging in PRAW
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
for logger_name in ("praw", "prawcore"):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

class Reddit:
    def __init__(self, reddit):
        self.reddit = reddit

    def get_submission(self, subreddits=[], option="hot"):
        """
        subreddit : list of subreddit in string format
        option :hot — order by the posts getting the most traffic
                new — order by the newest posts in the thread
                top — order by the most up-voted posts
                rising —order by the posts gaining popularity
        """

        if option == "hot":
            return reddit.subreddit('+'.join(subreddits)).hot(limit=None)
        if option == "new":
            return reddit.subreddit('+'.join(subreddits)).new(limit=None)
        if option == "top":
            return reddit.subreddit('+'.join(subreddits)).top(limit=None)
        if option == "rising":
            return reddit.subreddit('+'.join(subreddits)).rising(limit=None)

    def get_submission_stream(self, subreddits=[]):

        for submission in reddit.subreddit('+'.join(subreddits)).stream.submissions(skip_existing=True):
            print(submission.title)
        

if __name__ == "__main__":
    client_id="QmYcE5AJDFFR0_OeG__I-Q"
    client_secret="3UjqFoW1yfpE_Tj9YXyx5Ri0U9NFEw" 
    user_agent="crawler for reddit"
    
    # Reddit instance
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent,
    )
    rd = Reddit(reddit)
    # for submission in rd.get_submission(subreddits=["all"],option="hot"):
    #     print(submission.title)
    rd.get_submission_stream(subreddits=["all"])