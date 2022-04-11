"""
Crawl submissions(posts) from subreddit.
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
logging.basicConfig(filename="Submissions.log", format='INFO %(asctime)s %(message)s', filemode='a')
for logger_name in ("praw", "prawcore"):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

# golobal variables
submission_count = 0                # Will be used as index of submission_dict
submission_dict = OrderedDict()     # To store the submissions in a dictionary
submissions_per_file = 1000         # Number of submission per file


        

class MyReddit:
    def __init__(self, reddit):
        self.reddit = reddit # Reddit instance of PRAW

    def get_submission(self, subreddits=[], option="hot", limit=None):
        """
        subreddit : list of subreddit in string format
        option :hot — order by the posts getting the most traffic
                new — order by the newest posts in the thread
                top — order by the most up-voted posts
                rising —order by the posts gaining popularity
        """

        """ 
            Add '+' inbetween subreddit name 
            reddit.subreddit("redditdev+learnpython+botwatch")
        """
        try:
            subreddit = self.reddit.subreddit('+'.join(subreddits))

            if option == "hot":
                # Return hot posts of the subreddits
                return subreddit.hot(limit=limit)

            if option == "new":
                # Return new posts of the subreddits
                return subreddit.new(limit=limit)

            if option == "top":
                # Return top posts of the subreddits
                return subreddit.top(limit=limit)

            if option == "rising":
                # Return rising posts of the subreddits
                return subreddit.rising(limit=limit)
        except praw.exceptions.PRAWException as e:
            logger.error(e)


    def get_top_submission(self, subreddits=[], time_filter="all"):
        """
        input:
            subreddit : list of subreddit in string format
            time_filter: "all", "day", "hour", "month", "week", or "year"
        """

        """ 
            Add '+' inbetween subreddit name 
            reddit.subreddit("redditdev+learnpython+botwatch")
        """
        try:
            subreddit = self.reddit.subreddit('+'.join(subreddits))
            # Return top posts of the subreddits filtered by time
            return subreddit.top(time_filter)
        except praw.exceptions.PRAWException as e:
            logger.error(e)

    def get_submission_stream(self, subreddits=[]):
        """
            Stream Subreddit Submission
            subreddits : list of subreddit
        """
        try:
            """ 
                Add '+' inbetween subreddit name 
                reddit.subreddit("redditdev+learnpython+botwatch")
            """
            subreddit = self.reddit.subreddit('+'.join(subreddits))

            for submission in subreddit.stream.submissions(skip_existing=True):
                # print(submission.title)
                self.process_submission_stream(submission=submission)
        # except praw.exceptions.PRAWException as e:
        #     logger.info("Error in get_submission_stream().....")
        #     logger.error(e)
        except Exception as e:
            logger.info("Error in get_submission_stream().....")
            logger.error(e)
    

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

                # Remove Redditor and Subreddit method of praw from the dictionary
                sub_dict['author'] = {'name':sub_dict['author'].name}
                sub_dict['subreddit'] = {'display_name': sub_dict['subreddit'].display_name}

                # Convert the python dictionary into a json
                # sub_json = json.dumps(sub_dict)
                # sub_json = json.dumps(sub_dict, ensure_ascii=False, indent=4)
                sub_json = json.dumps(sub_dict, ensure_ascii=False)
                return sub_json
        except Exception as e:
            logger.debug("Inside parse_submission method.....")
            logger.debug(e)
            


    def save_submission_id(self, submission_id="", submission_id_list=[], subreddit=""):
        """
            Write the submission ids to a text file for comment extraction
            input : a submission id or list of submission ids
        """
        filename = get_file_name('sid', 'txt')
        filename = 'submissions/non_stream/' + filename

        if submission_id:
            with open(filename, 'a') as file:
                file.write(str(submission_id) + '\n')
        
        if submission_id_list:
            if subreddit:
                filename = get_file_name('sid', 'txt')
                path = 'submissions/non_stream/'
                full_filename = path + subreddit + "_" + filename
                with open(full_filename, 'w') as file:
                    for id in submission_id_list:
                        file.write(str(id) + '\n')
            else:
                with open(filename, 'a') as file:
                    for id in submission_id_list:
                        file.write(str(id) + '\n')
                    


    def save_submission_json(self, submission_dict={}, subreddit=""):
        """
            Writes the submission dictionary into an json file
        """
        try:
            if subreddit:
                filename = get_file_name(type='s', extension='json')
                filename = 'submissions/non_stream/' + subreddit + "_" + filename

                with open(filename, 'w', encoding = 'utf-8') as file:
                    json.dump(submission_dict, file, ensure_ascii=False, indent=4)

            else:
                filename = get_file_name(type='s', extension='json')
                filename = 'submissions/non_stream/' + filename
                if filename:
                    with open(filename, 'w', encoding = 'utf-8') as file:
                        json.dump(submission_dict, file, ensure_ascii=False, indent=4)

        except Exception as e:
            logger.info("Error in save_submission_json().....")
            logger.info(e)

    def write_to_file(self, submissions, subreddit=""):
        """
            Writes the submission into file.
            First store the submissions into a dictionary 
            then dump it into a json file.
        """
        submission_dict = OrderedDict()     # to store the submissions togeter
        submission_count = 0                # index of submission
        submission_id_list = []             # submission id list to write to text file
        try:
            for submission in submissions:
                # Parse the submission to json
                submission = self.parse_submission(submission=submission)
                if submission: # skips if null is returned
                    submission_id_list.append(json.loads(submission)["id"]) # store submission ids
                    # append submission one by one to the submission_dict
                    # and incremetn submission_count
                    submission_dict.update({submission_count: submission}) 
                    submission_count += 1

            if submission_dict: # if dictionary is not empty save it
                self.save_submission_id(submission_id_list=submission_id_list, subreddit=subreddit)
                self.save_submission_json(submission_dict=submission_dict, subreddit=subreddit)

        except Exception as e:
            logger.debug("Inside write_to_file() method.....")
            logger.debug(e)

    # def write_submission_id_to_text(self, submissions):
    #     """
    #         Writes submission ids to a text life for comment extraction
    #         submissions : praw listing object
    #     """

    #     try:
    #         filename = self.get_file_name(type='sid',extension='txt')
    #         if filename:
    #             with open(filename, 'a') as file:
    #                 for submission in submissions:
    #                     file.write(str(submission.id)+"\n")
    #     except Exception as e:
    #         logger.debug("Error in write_submission_id_to_text()............")
    #         logger.debug(e)

    def txt_file_to_list(self, file=""):
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

class MyRedditStream(MyReddit):
    def __init__(self, reddit):
        self.reddit = reddit
        MyReddit.__init__(self, reddit)
    
    def get_submission_stream(self, subreddits=[]):
        """
            Stream Subreddit Submission
            subreddits : list of subreddit
        """
        try:
            """ 
                Add '+' inbetween subreddit name 
                reddit.subreddit("redditdev+learnpython+botwatch")
            """
            subreddit = self.reddit.subreddit('+'.join(subreddits))

            for submission in subreddit.stream.submissions(skip_existing=True):
                self.process_submission_stream(submission=submission)
                # print(submission)
        except Exception as e:
            logger.info("Error in get_submission_stream().....")
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
    """
        Before exiting save the comments
    """
    global submission_count, submission_dict
    if submission_count >= 100:
        filename = get_file_name(type='ct', extension='json')
        if filename:
            filename = 'submission/stream/' + filename
            with open(filename, 'w', encoding = 'utf-8') as file:
                json.dump(submission_dict, file, ensure_ascii=False, indent=4)
            # comment_count = 0 # Reset count to zero
            # comment_dict = OrderedDict()

if __name__ == "__main__":
    # Reddit Credential
    client_id="IlAaIMNtV8ClGY3cRhhpYw"
    client_secret="ZITbTKXqn_kfhQcPmgm_iRi46YgIlg" 
    user_agent="crawler for reddit"
    
    
    # Reddit instance
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent,
    )

    # MyReddit class object
    rd = MyReddit(reddit)

    subreddit_list = rd.txt_file_to_list("subreddits_list.txt")

    for subreddit in subreddit_list:
        submissions = rd.get_submission(subreddits=[subreddit], option="hot", limit=None)
        rd.write_to_file(submissions=submissions, subreddit=subreddit)


    # # submissions = rd.get_submission(subreddits=subreddit_list,option="hot", limit=None)
    # # rd.write_to_file(submissions=submissions)
    
    # # subreddit_list = ["test"]
    # # subreddit_list = rd.txt_file_to_list("subreddits_list.txt")
    # # print(subreddit_list)
    # # rd.get_submission_stream(subreddits=subreddit_list) #streaming

    # # print(submissions)

    # atexit.register(exit_handler)
    