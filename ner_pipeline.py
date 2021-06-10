import pandas as pd
import numpy as np
import re
import json
import os
import textblob
from textblob import TextBlob
import csv
import pickle
import spacy
import time
'''
#rewrite into single pipeline for ner and everyuthing else

#first open article from raw storage

#second if date not a datetime obj, covert it (most are now)

#third assign a unique id to the article

#fourth run NER on the article

#fifth save every ner to an all/master and a seperate pkl file

#new NER SCHEME: each named entity gets a new field named ent_id and then an int id

'ent_string', 'ent_id', 'ent_type', 'article_uid', 'title', 'source', 'author', 'url', 'tags',
'pubtime', 'filename'

'GPE', 'DATE','CARDINAL','PERSON','ORG', 'DATE','NORP','MONEY', 'WOR', 'FAC', 'LOC', 'WORK_OF_ART', 'EVENT'
'''

#from article_loader_parser import article_loader_to_df
from named_entity_recognition_articles import ner_grabber

def sentiment_inline(para):
    pol = TextBlob(para).sentiment.polarity
    sub = TextBlob(para).sentiment.subjectivity
    return pol, sub

def single_line_clean(line):
    line = "".join(line) if type(line) is list else line

    line = line.replace("\r", " ").replace("\n", ' ')
    line = re.sub('[ ]+', ' ', line)
    return line

def article_processor(folder_path, iterable, begin):
    """here opens articles in chunksize chunks"""
    filelist = os.listdir(folder_path)
    jsonerror, keyerror, final = 0, 0, 0
    # begin = 0
    u_id = begin
    df_all = pd.DataFrame()
    if iterable == "all":
        iterable = len(filelist)
        ints = list(range(0, iterable))#overwrites old files but does not overwrite old logs
    else:
        ints = list(range(0, int(0 + iterable)))

    for i in ints:
        u_id += 1
        file = filelist[i]
        filepath = os.path.join(folder_path, file)

        f = open(filepath)  # , encoding='ascii', errors='ignore')
        try:
            j_import = json.load(f)
            j_import = j_import[0]
            try:
                para = j_import['para']
                if para == None:
                    continue
                para = "".join(para) if type(para) is list else para
            except KeyError:
                para = None
                keyerror += 1
                continue

            try:
                title = j_import['title']
                title = single_line_clean(title)#.lower()
            except KeyError:
                title = None
                keyerror += 1
                pass

            try:
                author = j_import['author']
                author = single_line_clean(author)#.lower()
                if len(author.split(" ")) >= 4:
                    author = " ".join(dict.fromkeys(author.split(" ")))
            except KeyError:
                author = None
                keyerror += 1
                pass

            try:
                tags = j_import['tag']
                tags = filter(None, tags)
            except KeyError:
                tags = None
                keyerror += 1
                pass
            # second if date not a datetime obj, covert it (most are now)
            try:
                pubtime = j_import['pubtime']
                #pubtime = pubtime_to_df(pubtime_i, source)
            except KeyError:
                pubtime_i = None
                keyerror += 1
                pass
            f.close()
        except json.decoder.JSONDecodeError:
            f.close()
            jsonerror += 1
            pass

        print(f"unique ID int : {u_id}  source: {j_import['source']} title : {title} \n iterator {i} date: {pubtime}")#[10:25]
        #print(text_dict)
        #print(para)
        """ here is where the nlp stuff begins"""
        df = ner_grabber(para, u_id, nlp)

        #adding the metadata to all ents
        df['title']= title
        df['article_uid'] = u_id
        df['author'] = author
        df["url"] = str(j_import['url'])
        df["tags"] = str(tags)
        df["pubtime"] = pubtime
        df["source"] = j_import['source']
        df["filename"] = str(file)

        df['is_author'] = df['ent_string'].where(df['ent_string'] == author.lower(), False)
        df['is_author'] = df['is_author'].where(df['is_author'] == False, True)
        df['is_author'] = df['is_author'].where(df['ent_type'] == "PERSON", None)

        df['in_title'] = df.apply(lambda x:  (x['title'].lower()).find(x["ent_string"]) != -1 , axis=1)

        pol, sub = sentiment_inline(para)
        df["polarity"] = pol
        df["subjectivity"] = sub


        print(df.head())
        frames = [df_all, df]
        df_all = pd.concat(frames, sort=False)

    print(df_all.info())

    print(f"Keyerrors: {keyerror} \t Json import errors: {jsonerror}  \t  final import count: {final}")
    return df_all


global_path ='C:/Users/17742/Desktop/win_art_writing/'  #windows:art_writing/
#ubuntu  : global_path = '/home/erik/Desktop/Datasets/art/art_writing/text_cleaned', nlp=nlp
chunksize = 15#00
path = 'artnews_artinamerica'
folder_path = os.path.join(global_path, path)

nlp = spacy.load('en_core_web_md')

filelist = os.listdir(folder_path)
allshape = 0
start = time.time()
for chunkbegin in range(13500, 30, chunksize): # 5 len(filelist)
    per = time.time()
    df_all = article_processor(folder_path, chunksize, chunkbegin)
    df_all.to_pickle(f"pkl_backups/second_pass/new_pass_sp_articles_{chunkbegin}_to_{chunkbegin+chunksize}.pkl")

    end = time.time()
    shape = df_all.shape[0]
    allshape += shape
    with open('pkl_backups/second_pass/logger.txt', "a") as f:
        log = [f"\n now {time.ctime()}, \n",
               f"articles {chunkbegin} to {(chunkbegin + chunksize)} of {len(filelist)}",
            f" with {int((end - start) // 60)}:{(end - start) % 60} elapsed and {int((end - per) // 60)}:{(end - per) % 60} since last save\n"
            f"{chunksize} articles, last dataframe was {shape} lines long and so far {allshape} ents have been written\n"]
        print(log)
        f.writelines(log)
        f.close()

"""        text_dict = {"title": title, "article_uid": u_id, "author": author,
                     "url": j_import['url'], "tags": tags, "pubtime": pubtime,
                     "source": j_import['source'], "filename": file }
                     """
