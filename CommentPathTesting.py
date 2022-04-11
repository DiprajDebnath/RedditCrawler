"""
Automate the comment extraction method from the submission_id text file. 
"""
import Comments
import os
import sys
import signal
import atexit

current_file = None

def sigint_handler(signum, frame):
	global current_file
	logger.info('Stop pressing the CTRL+C!')
	if current_file:
		## if 'ctrl+c' button pressed, delete the current (.start) file created by this process..............
		try:
			os.remove(current_file)
		except OSError as e:
			pass		
		logger.info('My application connection broken1')
		sys.exit()



def exit_handler():
	global current_file
	if current_file:
		## if unexpected kill occur, delete the current (.start) file created by this process..............
		try:
			os.remove(current_file)
		except OSError as e:
			pass		
		logger.info('My application connection broken2')
		sys.exit()

def collect_comments(filename, filepath):

    client_id="IlAaIMNtV8ClGY3cRhhpYw"
    client_secret="ZITbTKXqn_kfhQcPmgm_iRi46YgIlg" 
    user_agent="crawler for reddit"
    
    rd = Comments.RedditComments(client_id, client_secret, user_agent)

    filepath1 = filepath+"/"+filename  
    filename_without_start = filename.split(".")[0]		
    ## read the file and insert......................................
    print(filename_without_start)
    with open(filepath1, "r") as file:
        for sub_id in file:
            rd.get_comment_by_submission_id(sub_id=sub_id)

def get_comments(submission_id_dir):
    global current_file

    # list_of_files_with_json = list()
    # list_of_files_with_cas = list()
    list_of_files_with_start = list()
    ## take all file name and sort by their name and store in a list	
    temp_l = os.listdir(submission_id_dir)
    temp_l.sort()
    # print(temp_l)
    ## take all .cas file name and store in a list
    # for file1 in temp_l:
    #     if file1.endswith(".cas"):
    #         list_of_files_with_cas.append(file1.split(".")[0])
    ## take all .start file name and store in a list
    for file1 in temp_l:
        if file1.endswith(".start"):
            list_of_files_with_start.append(file1.split(".")[0])
    ## take all .neo file name which does not have a .start file name and thn store in a list

    # print(list_of_files_with_cas)
    # print(list_of_files_with_start)
    for file1 in temp_l:
        if file1.endswith(".txt"):
            fn = file1.split(".")[0]
            # if fn not in list_of_files_with_cas and fn not in list_of_files_with_start:
                # list_of_files_with_json.append(fn)				
            if fn not in list_of_files_with_start:    
                ## take the file for insertion ...........................(.start)........empty file
                f=os.open(submission_id_dir+"/"+fn+".start", os.O_CREAT | os.O_EXCL)
                current_file = submission_id_dir+"/"+fn+".start"
                os.close(f)

                collect_comments(fn+".txt", submission_id_dir)



if __name__ == "__main__":

    signal.signal(signal.SIGINT, sigint_handler)

    file_dir ="/home/dipraj/Documents/Dipraj_Testing/Reddit/RedditCrawler/submissions/non_stream/txt/new"
    
    get_comments(submission_id_dir=file_dir)

    atexit.register(exit_handler)