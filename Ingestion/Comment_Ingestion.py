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
    
    def write_to_comments(self, comment):
        # try:
        if comment['author'] is None:
            return
        author = comment['author']['name']
        author_id = comment['author_fullname']
        body = comment['body']
        body_html  = comment['body_html']
        created_utc = datetime.datetime.fromtimestamp(comment['created_utc'])
        edited = comment['edited']
        if edited is not False:
            edited = True
        gilded  = comment['gilded']
        likes  = comment['likes']
        comment_id = "t1_" + comment['id']
        is_submitter = comment['is_submitter']
        link_id = comment['link_id']
        parent_id = comment['parent_id']
        permalink = comment['permalink']
        saved = comment['saved']
        score  = comment['score']
        stickied = comment['stickied']
        submission_id = comment['_submission']['id']
        subreddit = comment['subreddit']['display_name']
        subreddit_id = comment['subreddit_id']
        # except Exception as e:
        #     logging.info("Exception in write_to_comments().........")
        #     logging.error(e)
        # try:
        query = 'INSERT INTO ' + 'test_keyspace_dipraj.comments2' + ' (author, author_id, body, body_html, created_utc, edited, gilded, likes, comment_id, is_submitter, link_id, parent_id, permalink, saved, score, stickied, submission_id, subreddit, subreddit_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
        prepared_query = self.session.prepare(query)
        prepared_query.consistency_level = ConsistencyLevel.ONE
        bound = prepared_query.bind((author, author_id, body, body_html, created_utc, edited, gilded, likes, comment_id, is_submitter, link_id, parent_id, permalink, saved, score, stickied, submission_id, subreddit, subreddit_id))
        self.session.execute(bound)
        # except Exception as e:
        #     logging.info("Exception in write_to_comments()....query handling")
        #     logging.error(e)
        #     sys.exit()

class JsonHandler:
    def read_json_file(self):
        cas = CassandraHandler('test_keyspace_dipraj')
        with open('../comments/non_stream/2022-03-26_03-58-19_ct.json', 'r') as file:
            comments = json.load(file)
            for index in comments:
                # logging.info(submission[index])
                if comments[index] is None:
                    continue
                cas.write_to_comments(json.loads(comments[index]))


if __name__ == "__main__":
    jh = JsonHandler()
    jh.read_json_file()