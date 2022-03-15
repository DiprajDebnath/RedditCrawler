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

# Logging in PRAW
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
for logger_name in ("praw", "prawcore"):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

# Global variables
comment_count=0
comment_dict=OrderedDict()
comment_per_file = 1000

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
                # print(comment.body)
                self.process_comment(comment)
        except Exception as e:
            logger.info("Error in get_comment_stream()......")
            logger.error(e)

    def process_comment(self, comment):
        """
            Parse and strore comment in json file of 1000 comments each
            input:
                    comment object of praw
        """
        global comment_count, comment_dict, comment_per_file
        try:
            if comment:
                if comment_count >= comment_per_file:
                    filename = get_file_name(type='ct', extension='json')
                    if filename:
                        filename = 'comments/stream/' + filename
                        with open(filename, 'w', encoding = 'utf-8') as file:
                            json.dump(comment_dict, file, ensure_ascii=False, indent=4)
                        comment_count = 0 # Reset count to zero
                        comment_dict = OrderedDict()
                    
                comment_json = self.parse_comment(comment=comment)
                comment_dict.update({comment_count: comment_json}) 
                comment_count += 1
        except Exception as e:
            logger.info("Error in process_comment().....")
            logger.info(e)
    
    def parse_comment(self, comment):
        try:
            if comment:
                com_dict = vars(comment)
                com_dict.pop('_reddit')
                com_dict['author'] = {'name':com_dict['author'].name}
                com_dict['subreddit'] = {'display_name': com_dict['subreddit'].display_name} 
                com_json = json.dumps(com_dict, ensure_ascii=False)
                return com_json
        except Exception as e:
            logger.info("Error in parse_comment() method......")
            logger.error(e)

def get_file_name(type, extension):
    """
        Return a file name as current time
        type:
            s=submission, 
            c=comment,
            sid=submission_id, 
            st=sunmission stream
        extension: 
            json or txt
    """
    try:
        datetime1 = datetime.datetime.utcnow()
        d1 = str(datetime1).split(".")[0].replace("-", "-").replace(":", "-").replace(" ", "_")
        filename =str(d1)+"_"+type+"."+extension # 2022-03-14_20-03-02_s.json
        return filename
    except Exception as e:
        logger.debug("Inside get_file_name method.....")
        logger.debug(e)

def exit_handler():
    global comment_count, comment_dict
    if comment_count >= 1:
        filename = get_file_name(type='ct', extension='json')
        if filename:
            filename = 'comments/stream/' + filename
            with open(filename, 'w', encoding = 'utf-8') as file:
                json.dump(comment_dict, file, ensure_ascii=False, indent=4)
            comment_count = 0 # Reset count to zero
            comment_dict = OrderedDict()

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

    rd.get_comment_stream(subreddits=["test"])

    # for comment in rd.get_comment_by_submission_id('tdu0l9'):
    #     print(comment.body)

    atexit.register(exit_handler)