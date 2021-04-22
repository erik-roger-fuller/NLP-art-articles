import pandas as pd
import numpy as np
import json
import os
import nltk
from nltk import RegexpTokenizer
import re
import string
from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import CountVectorizer
from numpy import linspace, loadtxt, ones, convolve
import matplotlib.pyplot as plt
import matplotlib.lines as ln
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter, drange , date2num
from datetime import datetime
import time

def random_corpus_sampling(iterable, filelist):
    iterable = int(iterable)
    maximum = len(filelist)
    rng = np.random.default_rng()#iterable
    rints = rng.integers(low=0, high=maximum, size=iterable)
    print(rints)
    rints = np.ndarray.tolist(rints)
    return rints

def para_clean(para):
    para = "".join(para)
    para = para.replace("	", "").replace("Follow  on Facebook:", '').replace("\n", ' ')
    para = para.replace("\r", " ")
    para = para.strip()
    return para

def single_line_clean(line):
    line = "".join(line)
    line = line.replace("	", "").replace("\n", ' ')
    line = line.replace("\r", " ")
    line = line.strip()
    return line

def iso_time_to_df(pubtime_i):
    pubtime_i = pubtime_i[:19]
    pubtime = datetime(*time.strptime(pubtime_i, "%Y-%m-%dT%H:%M:%S")[:6])
    return pubtime

def article_loader_to_df(folder_path, iterable, israndom=False):
    """imports a certain number of articles from the database"""
    filelist = os.listdir(folder_path)
    data = {}
    data = pd.DataFrame(data)
    jsonerror , keyerror = 0 , 0
    if israndom:
        ints = random_corpus_sampling(iterable, filelist)
    else:
        ints = list(range(0, iterable))
    for i in ints:
        file = filelist[i]
        filepath = os.path.join(folder_path, file)
        f = open(filepath) #, encoding='ascii', errors='ignore')
        try:
            j_import = json.load(f)
            j_import = j_import[0]
            try:
                para = j_import['para']
                para = para_clean(para)
            except KeyError:
                para = " "
                keyerror += 1
                pass
            try:
                title = j_import['title']
                title = single_line_clean(title)
            except KeyError:
                title = " "
                keyerror += 1
                pass
            try:
                author = j_import['author']
                author = single_line_clean(author)
            except KeyError:
                author = " "
                keyerror += 1
                pass
            try:
                pubtime_i = j_import['pubtime']
                pubtime = iso_time_to_df(pubtime_i)
            except KeyError:
                pubtime_i = None #"2005-06-15T06:06:06"
                keyerror += 1
                pass

            new_row = {"title" : title , "para" : para , "author": author ,
                       "pubtime" : pubtime }
            data = data.append(new_row, ignore_index=True)
            f.close()
        except json.decoder.JSONDecodeError:
            f.close()
            jsonerror += 1
            pass
    #data = data.set_index('title')
    print(f"Keyerrors: {keyerror} \t Json import errors: {jsonerror}  \t  final import count: {data.shape}")
    return data

# print(para)"""para = para[0]
#     tokenizer = RegexpTokenizer(r'\w+')
#     tokens = tokenizer.tokenize(para)
#     #print(tokens)
#     count = len(tokens)
#     if count > 1000 and brought_in < 3000:
#     brought_in += 1"""
#     """else:
#                     pass"""