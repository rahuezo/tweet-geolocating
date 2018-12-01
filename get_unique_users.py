from utils.readers import load_pickle, check_pickle_integrity

import tkFileDialog as fd
import glob, os
import sqlite3

# Results path 
RESULTS_PATH = "results"

# Choose directory with pickle files
pickles_directory = fd.askdirectory(title="Choose directory with pickles")

# Choose only files that end with .pkl
pickle_files = list(glob.glob(os.path.join(pickles_directory, "*.pkl")))[:100]

# Create results folder if not exists 
if not os.path.exists(RESULTS_PATH): 
    os.makedirs(RESULTS_PATH)

# Using database

db = sqlite3.connect(os.path.join(RESULTS_PATH, "twitter.db"))
cursor = db.cursor()

with db: 
    cursor.execute("""CREATE TABLE IF NOT EXISTS
        users(user_id INTEGER, UNIQUE(user_id))
    """)

    for index, pickle_file in enumerate(pickle_files): 
        print "{} out of {} pickle files".format(index + 1, len(pickle_files))

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
            tweets = ((tweet[1], ) for tweet in loaded_pickle)

            cursor.executemany("""INSERT OR IGNORE INTO users(user_id) VALUES(?)""", tweets)