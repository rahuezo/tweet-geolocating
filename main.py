from utils.pickers import generate_randoms
from utils.readers import load_pickle, check_pickle_integrity
from random import shuffle

import tkFileDialog as fd
import unicodecsv as csv
import glob, os
import sqlite3

# Results path 
RESULTS_PATH = "results"

# File and tweets fraction
FILE_FRACTION = 0.40
TWEET_FRACTION = 0.03

# Choose directory with pickle files
pickles_directory = fd.askdirectory(title="Choose directory with pickles")

# Choose only files that end with .pkl
pickle_files = list(glob.glob(os.path.join(pickles_directory, "*.pkl")))

# Get 30% of all pickle files
grab = int(len(pickle_files) * FILE_FRACTION)

# Generate random indeces and grab those files
random_pickle_files = [pickle_files[i] for i in generate_randoms(0, len(pickle_files) - 1, n=grab)]

# Create results folder if not exists 
if not os.path.exists(RESULTS_PATH): 
    os.makedirs(RESULTS_PATH)

# Using database

db = sqlite3.connect(os.path.join(RESULTS_PATH, "tweet_geo.db"))
cursor = db.cursor()

with db: 
    cursor.execute("""CREATE TABLE IF NOT EXISTS
        tweets(latitude REAL, longitude REAL, place_id NVARCHAR(50))
    """)

    for index, pickle_file in enumerate(random_pickle_files): 
        print "{} out of {} pickle files".format(index + 1, len(random_pickle_files))

        try: 
            loaded_pickle = [obj for obj in load_pickle(pickle_file)]
        except Exception as e: 
            print "Error loading pickle"
            print "\n{}".format(e)
            continue

        if check_pickle_integrity(loaded_pickle): 
            # Grab all the objects within the loaded pickle
            loaded_pickle = loaded_pickle[0]
            
            # Load tweets from pickle file (tweet_id, lat, lon, place_id)
            tweets = [[eval(tweet[7])[0], eval(tweet[7])[1], tweet[10][:3]] for tweet in loaded_pickle]

            # Grab 1% of all tweets
            tgrab = int(len(tweets) * TWEET_FRACTION)

            # Generate random indeces and grab those tweets
            random_tweets = [tweets[i] for i in generate_randoms(0, len(tweets) - 1, n=tgrab)]
        
            # Insert tweets into db

            cursor.executemany("""INSERT INTO tweets VALUES(?,?,?)""", random_tweets)

            print "\tWrote {} tweets to file".format(len(random_tweets))



# with open("random_tweets.csv", "ab") as out_csv:
#     writer = csv.writer(out_csv, delimiter=",")

#     for index, pickle_file in enumerate(random_pickle_files): 
#         print "{} out of {} pickle files".format(index + 1, len(random_pickle_files))

#         try: 
#             loaded_pickle = [obj for obj in load_pickle(pickle_file)]
#         except Exception as e: 
#             print "Error loading pickle"
#             print "\n{}".format(e)
#             continue

#         if check_pickle_integrity(loaded_pickle): 
#             # Grab all the objects within the loaded pickle
#             loaded_pickle = loaded_pickle[0]
            
#             # Load tweets from pickle file
#             tweets = [tweet for tweet in loaded_pickle]

#             # Grab 3% of all tweets
#             tgrab = 1000 # int(len(tweets)*0.01)

#             # Generate random indeces and grab those tweets
#             random_tweets = [tweets[i] for i in generate_randoms(0, len(tweets) - 1, n=tgrab)]
        
#             writer.writerows(random_tweets)

#             print "\tWrote {} tweets to file".format(len(random_tweets))