
import cPickle
import os


def load_pickle(f): 
    with open(f, "rb") as pickle_file:
        while True: 
            try: 
                yield cPickle.load(pickle_file)
            except EOFError: 
                break

def check_pickle_integrity(loaded_pickle, typeof=list, length=1): 
    return type(loaded_pickle) == typeof and len(loaded_pickle) == length
        
