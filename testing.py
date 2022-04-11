import praw
import json
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

# """Submission"""
# # id tg9fzj, 39zje0
# # assume you have a praw.Reddit instance bound to variable `reddit`
# submission = reddit.submission("39zje0")
# print(submission.title)  # to make it non-lazy
# sub_dict = vars(submission)
# # pprint(sub_dict)

# # if sub_dict['_comments_by_id']:
# #     for key, value in sub_dict['_comments_by_id'].items():
# #         # pprint(value.id)
# #         comment_id = {'id' : value.id}
# #         sub_dict['_comments_by_id'].update({key : comment_id})

# # pprint(sub_dict['_comments_by_id'])
# if sub_dict['_comments_by_id']:
#     comment_id_list = []
#     for key, value in sub_dict['_comments_by_id'].items():
#         comment_id_list.append(value.id)
#     sub_dict.update({'_comments_by_id':comment_id_list})

# sub_dict.pop('_reddit')
# sub_dict.pop('_comments')
# # remove 'poll_data' from submission dictionary if present
# if 'poll_data' in sub_dict:
#     sub_dict.pop('poll_data')

# # Remove Redditor and Subreddit method of praw from the dictionary
# sub_dict['author'] = {'name':sub_dict['author'].name}
# sub_dict['subreddit'] = {'display_name': sub_dict['subreddit'].display_name}


# # Convert the python dictionary into a json
# sub_json = json.dumps(sub_dict, ensure_ascii=False)
# print(sub_json)


"""Comment"""
# i10iibv cs81xp8
comment = reddit.comment("i0jw0ff")
pprint(comment.body)
# pprint(vars(comment))
com_dict = vars(comment)
# print(com_dict)
com_dict.pop('_reddit')
# com_dict.pop('_replies')
if com_dict['_submission']:
    com_dict['_submission'] = {'id':com_dict['_submission'].id}
if com_dict['author']:
    com_dict['author'] = {'name':com_dict['author'].name}
if com_dict['subreddit']:
    com_dict['subreddit'] = {'display_name': com_dict['subreddit'].display_name} 
com_json = json.dumps(com_dict, ensure_ascii=False)
print(com_json)