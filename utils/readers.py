import tkFileDialog as fd
from random import randint
import cPickle
import csv
import os


def load_pickle(f): 
    with open(f, "rb") as pickle_file:
        while True: 
            try: 
                yield cPickle.load(pickle_file)
            except EOFError: 
                break

def generate_randoms(start, end, n=100, distinct=True): 
    randoms = []

    while len(randoms) < n: 
        print len(randoms)
        random = randint(start, end)

        if distinct: 
            if end < n: 
                raise Exception("End parameter must be greater than n")

            if random not in randoms: 
                randoms.append(random)
                continue
        else: 
            randoms.append(random)
    return randoms


f = fd.askopenfilename(title="Choose pickle file")

tweets = [line for line in load_pickle(f)]
random_indeces = [randint()]

with open("random_tweets.csv", "wb") as out_csv:
    writer = csv.writer(out_csv, delimiter=",")