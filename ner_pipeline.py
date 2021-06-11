import pandas as pd
import numpy as np
import re
import json
import os
import textblob
from textblob import TextBlob
import pickle
import feather
import spacy
import time
from datetime import datetime

#from nltk.sentiment.vader import SentimentIntensityAnalyzer
#import flair
#import nltk
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
    #s = flair.data.Sentence(sentence)
    #flair_sentiment.predict(s)
    #total_sentiment = s.labels
    sent = TextBlob(para).sentiment
    #sid = SentimentIntensityAnalyzer()
    #sent = sid.polarity_scores(para)
    print(sent)
    return sent#pol, sub

def single_line_clean(line):
    line = "".join(line) if type(line) is list else line

    if type(line) != None:
        try:
            line = line.replace("\r", " ").replace("\n", ' ')
            line = re.sub('[ ]+', ' ', line)
            return line
        except AttributeError:
            pass
    else:
        return None

def article_processor(folder_path, chunksize, begin, u_id_begin):
    """here opens articles in chunksize chunks"""
    filelist = os.listdir(folder_path)
    jsonerror, keyerror, attribute_error,final = 0, 0, 0, 0
    # begin = 0
    u_id = u_id_begin
    highest = min(begin+chunksize, len(filelist))

    df_all = pd.DataFrame()

    for i in range(begin, highest):
        u_id += 1
        file = filelist[i]
        filepath = os.path.join(folder_path, file)

        f = open(filepath)  # , encoding='ascii', errors='ignore')
        try:
            j_import = json.load(f)

            j_import = j_import[0] if type(j_import) is list else j_import
            try:
                para = j_import['para']
                if para is None:
                    continue
                para = "".join(para) if type(para) is list else para
                if len(para) <= 5:
                    continue
            except KeyError:
                para = np.NAN
                keyerror += 1
                continue
            except TypeError:
                print(j_import)
                break

            try:
                title = j_import['title']
                title = single_line_clean(title) if title else np.NAN

            except KeyError:
                title = np.NAN
                keyerror += 1
                pass

            try:
                author = j_import['author']
                author = single_line_clean(author) if author else np.NAN
                if type(author) == str: #duplicate check for name words
                    if len(author.split(" ")) >= 4:
                        author = " ".join(dict.fromkeys(author.split(" ")))

            except KeyError:
                author = np.NAN
                keyerror += 1
                pass

            try:
                tags = j_import['tag']
                tags = filter(None, tags) if type(tags) == list else np.NAN
            except KeyError:
                tags = np.NAN
                keyerror += 1
                pass
            # second if date not a datetime obj, covert it (most are now)
            try:
                pubtime = j_import['pubtime']
                if type(pubtime) == str:
                    try:
                        pubtime = datetime.strptime(pubtime, "%m/%d/%Y")
                    except ValueError:
                        pass
            except KeyError:
                pubtime = np.NAN
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

        if df.empty == False:
            '''adding the metadata to all ents'''

            df['title']= title
            df['article_uid'] = u_id
            df['author'] = author
            df["url"] = str(j_import['url'])
            df["tags"] = str(tags)
            df["pubtime"] = pubtime
            df["source"] = j_import['source']
            df["filename"] = str(file)

            if j_import['source'] == 'artagenda' and title == "art-agenda":
                name = str(j_import['url'])
                name = name[0] if type(name) is list else name
                name = name.split("/")[-1]
                name = name.replace("-"," ").replace("]"," ").replace("'","")
                df['title']= name.title()

            if pd.notna(author) == True:
                df['is_author'] = df['ent_string'].where(df['ent_string'] == author.lower(), False)
                df['is_author'] = df['is_author'].where(df['is_author'] == False, True)
                df['is_author'] = df['is_author'].where(df['ent_type'] == "PERSON", np.NAN)

            else:
                df['is_author'] = np.NAN

            if pd.notna(title) == True:
                df['in_title'] = df.apply(lambda x: (x['title'].lower()).find(x["ent_string"]) != -1 , axis=1)
            else:
                df['in_title'] = np.NAN

            sent = sentiment_inline(para)
            df["polarity"] = sent[0]
            df["subjectivity"] = sent[1]

            #df['sentiment'] = sent

            print(df.head())
            frames = [df_all, df]
            df_all = pd.concat(frames, sort=False)

    print(df_all.info())

    print(f"Keyerrors: {keyerror}\tAttribute errors: {attribute_error} "
          f"\t Json import errors: {jsonerror}  \t  final import count: {final}")
    return df_all


global_path ='C:/Users/17742/Desktop/win_art_writing/art_writing' #text_cleaned  #windows:
#ubuntu  : global_path = '/home/erik/Desktop/Datasets/art/art_writing/text_cleaned', nlp=nlp
chunksize = 1500

path = 'artagenda' #'text_cleaned_all'
#path = 'artnews_artinamerica'
folder_path = os.path.join(global_path, path)

nlp = spacy.load('en_core_web_md')


filelist = os.listdir(folder_path)
allshape = 0
start = time.time()
pd.set_option('mode.chained_assignment', None)

for begin in range(0, len(filelist), chunksize): # 5 len(filelist)
    per = time.time()
    df_all = article_processor(folder_path, chunksize, begin, 250240 )

    #df_all.to_pickle(f"pkl_backups/second_pass/new_pass_first_corpus_{begin}_to_{begin+chunksize}.pkl")
    df_all = df_all.reset_index()
    df_all.to_feather(f"pkl_backups/second_pass/pass_art_agenda_{begin}_to_{begin+chunksize}.feather")

    end = time.time()
    shape = df_all.shape[0]
    allshape += shape
    with open('pkl_backups/second_pass/logger.txt', "a") as f:
        log = [f"\n now {time.ctime()}, \n",
               f"articles {begin} to {(begin + chunksize)} of {len(filelist)}",
            f" with {int((end - start) // 60)}:{(end - start) % 60} elapsed and {int((end - per) // 60)}:{(end - per) % 60} since last save\n"
            f"{chunksize} articles, last dataframe was {shape} lines long and so far {allshape} ents have been written\n"]
        print(log)
        f.writelines(log)
        f.close()

"""        text_dict = {"title": title, "article_uid": u_id, "author": author,
                     "url": j_import['url'], "tags": tags, "pubtime": pubtime,
                     "source": j_import['source'], "filename": file }
                     
final {'ent_string':text, 'ent_type':label, "ent_id":ent_id,  "article_uid": u_id, "author": author, "url": j_import['url'], "tags": tags,
 "pubtime": pubtime, "source": j_import['source'], "filename": file, 'is_author':is_author,  'in_title':in_title,"polarity": sent[0] ,
  "subjectivity": sent[1]  }         
                     
                     """
