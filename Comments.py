"""
Crawl Comments and Submissions from subreddit.
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

    def get_comment_by_submission_id(self, sub_id):
        """
            gets all the comments of a submission(post)
        """
        try:
            submission = reddit.submission(id=sub_id)
            submission.comments.replace_more(limit=None)
            for comment in submission.comments.list():
                print(comment.body)
        except praw.exceptions.PRAWException as e:
            logger.error(e)

    def get_comment_stream(self, subreddits=[]):
        """
        Stream comments
        """
        try:
            subreddit = reddit.subreddit('+'.join(subreddits))
            for comment in subreddit.stream.comments(skip_existing=True):
                print(comment.body)
        except praw.exceptions.PRAWException as e:
            logger.error(e)
        

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
    # for comment in rd.get_comment_by_subreddit(subreddits=["all"]):
    #     print(submission.title)
    # rd.get_submission_stream(subreddits=["all"])
    for comment in rd.get_comment_by_submission_id('tdu0l9'):
        print(comment.body)