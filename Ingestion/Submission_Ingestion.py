import json
from operator import sub
import time
import datetime
import sys
import logging
logging.basicConfig(level=logging.INFO)

from cassandra.cluster import Cluster
from cassandra.policies import RoundRobinPolicy
from cassandra.query import UNSET_VALUE
from cassandra import ConsistencyLevel
from cassandra.query import ValueSequence

class CassandraHandler:
    def __init__(self, keyspace):
        self.cluster = Cluster(['172.16.117.160'], port=9042, load_balancing_policy=RoundRobinPolicy())
        self.keyspace = keyspace
        self.session = self.cluster.connect(keyspace)
    
    def write_to_submissions(self, submission):
        try:
            author_name = submission['author']['name']
            author_id = submission['author_fullname']
            created_utc  = datetime.datetime.fromtimestamp(submission['created_utc'])
            edited  = submission['edited'] # Fix this edit return time if edited otherwise false
            if edited is not False:
                edited = True
            submission_id = submission['id'] 
            is_original_content = submission['is_original_content']
            is_self = submission['is_self']
            link_flair_text = submission['link_flair_text']
            locked = submission['locked']
            num_comments = submission['num_comments']
            over_18  = submission['over_18']
            permalink = submission['permalink']
            saved = submission['saved']
            score = submission['score']
            selftext = submission['selftext']
            spoiler = submission['spoiler']
            stickied = submission['stickied']
            subreddit = submission['subreddit']['display_name']
            subreddit_id = submission['subreddit_id']
            title = submission['title']
            upvote_ratio = submission['upvote_ratio']
            url = submission['url']
        except Exception as e:
            logging.info("Exception in write_to_submissions().........")
            logging.error(e)
        try:
            query = 'INSERT INTO ' + 'test_keyspace_dipraj.submissions2' + ' (author_name, author_id, created_utc, edited, submission_id,is_original_content, is_self, link_flair_text,locked,num_comments,over_18, permalink, saved, score, selftext, spoiler, stickied, subreddit, subreddit_id, title, upvote_ratio, url) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
            prepared_query = self.session.prepare(query)
            prepared_query.consistency_level = ConsistencyLevel.ONE
            bound = prepared_query.bind((author_name, author_id, created_utc, edited, submission_id,is_original_content, is_self, link_flair_text,locked,num_comments,over_18, permalink, saved, score, selftext, spoiler, stickied, subreddit, subreddit_id, title, upvote_ratio, url))
            self.session.execute(bound)
        except Exception as e:
            logging.info("Exception in write_to_submissions()....query handling")
            logging.error(e)
            sys.exit()

class JsonHandler:
    def read_json_file(self):
        cas = CassandraHandler('test_keyspace_dipraj')
        with open('../submissions/non_stream/json/india2022-03-16_09-45-02_s.json', 'r') as file:
            submissions = json.load(file)
            for index in submissions:
                # logging.info(submission[index])
                if submissions[index] is None:
                    continue
                cas.write_to_submissions(json.loads(submissions[index]))


if __name__ == "__main__":
    jh = JsonHandler()
    jh.read_json_file()