import logging
import json
from pprint import pprint
import praw
import sys
import os
import math
import atexit
import datetime
from collections import OrderedDict
from timeit import default_timer as timer

# Logging in PRAW
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
logging.basicConfig(filename="SubmissionsStream.log", format='INFO %(asctime)s %(message)s', filemode='w')
for logger_name in ("praw", "prawcore"):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)


# golobal variables
submission_count = 0                # Will be used as index of submission_dict
submission_dict = OrderedDict()     # To store the submissions in a dictionary
limit_per_file = 100                # Number of submission per file


class SubmissionsStream():
    def __init__(self, reddit):
        self.reddit = reddit
    
    def get_submission_stream(self, subreddits=[]):
        """
            Stream Subreddit Submission
            subreddits : list of subreddit
        """
        logger.info("streaming started")
        try:
            """ 
                Add '+' inbetween subreddit name 
                reddit.subreddit("redditdev+learnpython+botwatch")
            """
            subreddit = self.reddit.subreddit('+'.join(subreddits))

            for submission in subreddit.stream.submissions(skip_existing=True):
                self.write_submission_stream(submission=submission)
                # print(submission)
        except Exception as e:
            logger.info("Error in get_submission_stream().....")
            logger.info(e)

    
    def write_submission_stream(self, submission):
        """
            Processes the incoming submission id from stream 
            and store it to a json file
            Input : submission object
        """
        global submission_count, submission_dict, limit_per_file, start_time
        # diff_time = math.ceil(timer()-start_time)
        try:
            # """
            #     Save Sumbission every 10 sec
            # """
            # # print("Submission arived")
            # # print("Time : " + str(diff_time))
            # if diff_time>=11:
            """
                If submission count is equal to 1000 save to json file and
                reset the count and dictionary 
            """
            if submission_count >= limit_per_file:
                filename = get_file_name(type='st', extension='json')
                if filename:
                    filename = 'submissions/stream/' + filename
                    with open(filename, 'w', encoding = 'utf-8') as file:
                        json.dump(submission_dict, file, ensure_ascii=False, indent=4)
                    submission_count = 0 # Reset count to zero
                    submission_dict = OrderedDict()
                    start_time = timer()
                    logger.info("Submissions saved : " + filename)
            else:        
                # Parse the submission object into json
                submission_json = self.parse_submission(submission=submission)
                # Just for debug purpose remove it afterwads
                # logger.info(json.loads(submission_json)["title"])
                submission_dict.update({submission_count: submission_json}) 
                submission_count += 1
        except Exception as e:
            logger.info("Error in process_submission_stream()......")
            logger.info(str(e))

    def parse_submission(self, submission=None):
        """
            submission : Submission object of PRAW
            Parse and returns the submission object into json format 
        """
        try:
            if submission:
                # Converst praw submission object into an python dictionary
                sub_dict = vars(submission)

                # remove '_reddit' from the submission dictionary 
                sub_dict.pop('_reddit')

                # remove '_comments' 
                if '_comments' in sub_dict:
                    sub_dict.pop('_comments')

                # remove 'poll_data' from submission dictionary if present
                if 'poll_data' in sub_dict:
                    sub_dict.pop('poll_data')

                # Remove Redditor and Subreddit method of praw from the dictionary
                sub_dict['author'] = {'name':sub_dict['author'].name}
                sub_dict['subreddit'] = {'display_name': sub_dict['subreddit'].display_name}

                if sub_dict['_comments_by_id']:
                    comment_id_list = []
                    for key, value in sub_dict['_comments_by_id'].items():
                        comment_id_list.append(value.id)
                    sub_dict.update({'_comments_by_id':comment_id_list})

                # Convert the python dictionary into a json
                # sub_json = json.dumps(sub_dict, ensure_ascii=False, indent=4)
                sub_json = json.dumps(sub_dict, ensure_ascii=False)
                return sub_json
        except Exception as e:
            logger.info("Inside parse_submission method.....")
            logger.info(e)
            pprint(vars(submission))
            sys.exit()
            
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
    global submission_count, submission_dict
    if submission_count >= 1:
        filename = get_file_name(type='st', extension='json')
        if filename:
            filename = 'submissions/stream/' + filename
            with open(filename, 'w', encoding = 'utf-8') as file:
                # json.dump(submission_dict, file, ensure_ascii=False, indent=4)
                json.dump(submission_dict, file, ensure_ascii=False)
                logger.info("Submission saved : " + filename)
    logger.info("exit_handler end")
            # comment_count = 0 # Reset count to zero
            # comment_dict = OrderedDict()

def main():
    client_id="QmYcE5AJDFFR0_OeG__I-Q"
    client_secret="3UjqFoW1yfpE_Tj9YXyx5Ri0U9NFEw" 
    user_agent="crawler for reddit"
    
    
    # Reddit instance
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent,
    )

    rs = SubmissionsStream(reddit)

    subreddit_list = txt_file_to_list("subreddits_list.txt")
    # subreddit_list = ['all']
    rs.get_submission_stream(subreddits=subreddit_list)

if __name__ == "__main__":
    logger.info("streaming submission main()")
    atexit.register(exit_handler)
    start_time = timer()
    main()