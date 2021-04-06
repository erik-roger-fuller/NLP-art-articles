import pandas as pd
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
from scipy.signal import savgol_filter

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

def article_loader_to_df(filelist, iterable):
    """imports a certain number of articles from the database"""
    data = {}
    data = pd.DataFrame(data)
    cleaned_titles , cleaned_paras = [], []
    for file in filelist[:iterable]:
        folderpath = 'C:/Users/17742/Desktop/win_art_writing/nytimes_articles/articles_dump'
        filepath = os.path.join(folderpath, file)
        f = open(filepath) #, encoding='ascii', errors='ignore')
        try:
            j_import = json.load(f)
            j_import = j_import[0]
            try:
                para = j_import['para']
                para = para_clean(para)
                title = j_import['title']
                title = single_line_clean(title)
                author = j_import['author']
                author = single_line_clean(author)
                pubtime_i = j_import['pubtime']
                pubtime = iso_time_to_df(pubtime_i)

                new_row = {"title" : title , "para" : para , "author": author ,
                           "pubtime" : pubtime }
                data = data.append(new_row, ignore_index=True)
                f.close()
            except KeyError:
                f.close()
                pass
        except json.decoder.JSONDecodeError:
            f.close()
            pass
    #data = data.set_index('title')
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