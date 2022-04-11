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
handler.setLevel(logging.INFO)
logging.basicConfig(filename="CommentsStream.log", format='INFO %(asctime)s %(message)s', filemode='a')
for logger_name in ("praw", "prawcore"):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

# Global variables
comment_count=0
comment_dict=OrderedDict()
comment_per_file = 1000

class CommentsStream:
    def __init__(self, reddit):
        self.reddit = reddit

    def get_comment_stream(self, subreddits=[]):
        """
        Stream comments
        """
        logger.info("Comments Streaming Started")
        try:
            subreddit = reddit.subreddit('+'.join(subreddits))
            for comment in subreddit.stream.comments(skip_existing=True):
                # print(comment.body)
                self.write_comment_stream(comment)
        except Exception as e:
            logger.info("Error in get_comment_stream()......")
            logger.error(e)

    def write_comment_stream(self, comment):
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
                        logger.info("Comment saved : " + filename)
                    
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
                com_dict.pop('_replies')

                if com_dict['_submission']:
                    com_dict['_submission'] = {'id':com_dict['_submission'].id}
                if com_dict['author']:
                    com_dict['author'] = {'name':com_dict['author'].name}
                if com_dict['subreddit']:
                    com_dict['subreddit'] = {'display_name': com_dict['subreddit'].display_name} 
                
                com_json = json.dumps(com_dict, ensure_ascii=False)
                return com_json
        except Exception as e:
            logger.info("Error in parse_comment() method......")
            logger.error(e)
    
def txt_file_to_list(file=""):
        """
            Return the content of text file in form of list
            inputs:
                    file: file name
            output:
                    a list        
        """
        list = []
        try:
            with open(file, 'r') as file:
                for line in file:
                    list.append(line.strip("\n"))
            return list
        except Exception as e:
            logger.info("Error in txt_file_to_list()......")
            logger.info(e)    

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
        # datetime1 = datetime.datetime.utcnow()
        datetime1 = datetime.datetime.now()
        d1 = str(datetime1).split(".")[0].replace("-", "-").replace(":", "-").replace(" ", "_")
        filename =str(d1)+"_"+type+"."+extension # 2022-03-14_20-03-02_s.json
        return filename
    except Exception as e:
        logger.info("Inside get_file_name method.....")
        logger.info(e)

def exit_handler():
    """
        Before exiting save the comments
    """
    global comment_count, comment_dict
    if comment_count >= 10:
        filename = get_file_name(type='ct', extension='json')
        if filename:
            filename = 'comments/stream/' + filename
            with open(filename, 'w+', encoding = 'utf-8') as file:
                json.dump(comment_dict, file, ensure_ascii=False)
                logger.info("Comment saved successfully: " + filename)
            # comment_count = 0 # Reset count to zero
            # comment_dict = OrderedDict()
    logger.info("Exit handler end")

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
    rd = CommentsStream(reddit)

    atexit.register(exit_handler)

    subreddit_list = txt_file_to_list("subreddits_list.txt")
    rd.get_comment_stream(subreddits=subreddit_list)

    # for comment in rd.get_comment_by_submission_id('tdu0l9'):
    #     print(comment.body)
