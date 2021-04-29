import pandas as pd
import numpy as np
import json
import os
import csv
import spacy
import time
#from encyclopedia_builder import ents_encyc_builder
from named_entity_recognition_articles import spacy_importer_prepper
from article_loader_parser import article_loader_to_df, random_corpus_sampling


def doc_opener(document_mentions, content, i , c):
    docs = document_mentions.tolist()
    rows = []
    for doc in docs:
        for entity in doc:
            # documents_all.append(entity, ignore_index=True)
            unique_id = entity["unique_id"]
            ent = entity["entity"]

            rows.append({"unique_id": unique_id, "entity": ent})

            # if len(rows) % 9999 == 0:
            #    df = pd.DataFrame(rows)
            #    df.to_csv(f"entities_test_{len(rows)}.csv", sep=",", quoting=csv.QUOTE_NONNUMERIC)

    df = pd.DataFrame(rows)
    df.to_csv(f"entities_backups/{content}_random_sample_{i}_to_{(i + c)}_entities.csv", sep=",", quoting=csv.QUOTE_NONNUMERIC)


global_path ='C:/Users/17742/Desktop/win_art_writing/art_writing/text_cleaned'  #windows:
#ubuntu  : global_path = '/home/erik/Desktop/Datasets/art/art_writing/text_cleaned', nlp=nlp

path = 'text_cleaned_all'
folder_path = os.path.join(global_path, path)
# os.path.expanduser()
filelist = os.listdir(folder_path)
total = len(filelist)
#rints = random_corpus_sampling(total, filelist)


with open("random_integers_master.json", "r") as fp:
    loadit = json.load(fp)
    #json.dump(rints, fp)

c = 1000

nlp = spacy.load('en_core_web_md')#trf'
start = time.time()

for i in range(175000,total, c):
    data = article_loader_to_df(folder_path=folder_path, iterable=c, begin=i, fileguide=loadit)#, israndom=True
    end = time.time()
    print(f" now articles {i}to {(i+c)} of {total} with {int((end - start)//60)}:{(end - start)%60} elapsed")
    #data1 = data[:a]
    try:
        document_mentions, document_person_mentions = spacy_importer_prepper(data=data, model='en_core_web_md')

        doc_opener(document_mentions, "organizations", i, c)
        doc_opener(document_person_mentions, "persons", i, c)
    except ValueError:
        pass

#article_text_id_assigner(folder_path=folder_path, iterable="all", begin=228002 )
#data = article_loader_to_df(folder_path=folder_path, iterable=5000, israndom=True)
#print(data)
#plot = timeplot_sentiment(data, "polarity", path)
#path = 'nytimes' # 122660 logged #122791 130 before error
#then 27979 . hyperallergic finished. therfore new begin = 150770 {then plus 500
#artforumen then logged 62414 frieze logged 14818 brings to 228002
#artnet then 24546 bringing grand total to 252548
#path = 'artnet_articles'
#path = 'frieze'
#path = 'artforum'
#path = 'hyperallergic'
"""import nltk
from nltk import RegexpTokenizer
import re
import string
from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import CountVectorizer
from numpy import linspace, loadtxt, ones, convolve
#from textblob import TextBlob
import matplotlib.pyplot as plt
import matplotlib.lines as ln
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter, drange , date2num
#from collections import Counter
from datetime import datetime
import time

#from article_loader_parser import article_text_id_assigner, article_loader_to_df
#from sentiment_analysis_functions import *
#from word_cleaning_functions import *
#from topic_modeling_functions import *

"""