# Submissions Stream
Parse and stores the incoming Submission stream from Reddit into json file.
# Class : SubmissionsStream
## Methods
- ***get_submission_stream***\
  Gets stream of Submisisons for given list of Subreddits.\
  **Input**: Subreddits
- ***write_submission_stream***\
  For storing the parsed Submission objects into a file.\
  **Input**: Submission  
- ***parse_submission***
  To parse the Submission object into json.\
  **Input**: Submission 

# Global Variables
- ***submission_count*** \
  Keeps a count of number of submission received.
- ***submission_dict***\
  Buffer to store the Submissions before dumping it to json file.
- ***limit_per_file***\
  Number of Submissions you want to store in each json file.

# Global Methods
- ***txt_file_to_list***\
  Return the items in a text file as list.\
  **Input**: file_name
- ***exit_handler*** 
  Stored the parsed Submisisons when the program is terminated.
- ***get_file_name***
  Returns filename as current time.