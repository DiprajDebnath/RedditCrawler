# Comments Stream
Parse and stores the incoming Comments stream from Reddit into json file.
# Class : CommentsStream
## Methods
- ***get_submission_stream***\
  Gets stream of Submisisons for given list of Subreddits.\
  **Input**: Subreddits
- ***write_comment_stream***\
  For storing the parsed Comment objects into a file.\
  **Input**: Comment  
- ***parse_submission***
  To parse the Comment object into json.\
  **Input**: Comment 

# Global Variables
- ***comment_count*** \
  Keeps a count of number of submission received.
- ***comment_dict***\
  Buffer to store the Comments before dumping it to json file.
- ***limit_per_file***\
  Number of Comments you want to store in each json file.

# Global Methods
- ***txt_file_to_list***\
  Return the items in a text file as list.\
  **Input**: file_name
- ***exit_handler*** 
  Stored the parsed Submisisons when the program is terminated.
- ***get_file_name***
  Returns filename as current time.