import pandas as pd
import numpy as np
import json
import csv
import os
import re
"""import nltk
from nltk import RegexpTokenizer
import string
from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import CountVectorizer
from numpy import linspace, loadtxt, ones, convolve
import matplotlib.pyplot as plt
import matplotlib.lines as ln
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter, drange , date2num"""
from datetime import datetime
import time

def random_corpus_sampling(iterable, filelist):
    iterable = int(iterable)
    maximum = len(filelist)
    rng = np.random.default_rng()  # iterable
    rints = rng.integers(low=0, high=maximum, size=iterable)
    print(rints)
    rints = np.ndarray.tolist(rints)
    return rints


def para_clean(para):
    para = "".join(para)
    para = para.replace("	", "").replace("Follow on Facebook:", '').replace("\n", ' ')
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


def space_time_to_df(pubtime_i):
    pubtime_i = single_line_clean(pubtime_i)
    pubtime_i = pubtime_i.lower()
    pubtime = datetime(*time.strptime(pubtime_i, "%e %b %y"))  # []%Y-%m-%dT%H:%M:%S
    return pubtime
    # frieze : "pubtime": "31 OCT 18"


def dashes_time_to_df(pubtime_i):
    pubtime_i = single_line_clean(pubtime_i)
    pubtime_i = pubtime_i.lower()
    pubtime = datetime(*time.strptime(pubtime_i, "%e %b %y"))  # []%Y-%m-%dT%H:%M:%S
    return pubtime
    # artforum : "2018-04-27"


def pubtime_to_df(pubtime_i, source):
    if source == "Nytimes_Arts" or "artnet" or "Hyperallergic":
        pubtime = iso_time_to_df(pubtime_i)
    elif source == "Frieze":
        pubtime = space_time_to_df(pubtime_i)
    pubtime = pubtime.strftime("%m/%d/%Y")
    return pubtime

def file_prep_and_export(final, name, text_dict):
    newname = filename_clean(name)
    output_filepath = os.path.join(os.path.expanduser('~'),'Desktop/Datasets/art/art_writing/text_cleaned_all', newname)
    #try:
    with open(output_filepath, "w") as write_file:
        json.dump(text_dict, write_file )
        print(f"written at: {newname} ")
    write_file.close()
    csv_logger(newname, text_dict)
    final += 1
    #except FileNotFoundError:
    #    print("error:   " + name)
    return final


def csv_logger(newname, text_dict, bool=False):
    log_file = f"{os.path.expanduser('~')}/Desktop/Datasets/art/art_writing/articles_ids_index.csv"
    labels = ["title", "unique_id", "source", "author", "url", "tags", "pubtime", "filename"]
    with open(log_file, 'a') as record_file:
        writer = csv.DictWriter(record_file, fieldnames=labels, quoting=csv.QUOTE_NONNUMERIC)
        #csv.QUOTE_NONNUMERIC
        if bool:
            writer.writeheader()
        else:
            log_entry = {"title": text_dict['title'], "unique_id": text_dict['unique_id'],
                         "author": text_dict['author'], "url": text_dict['url'],
                         "tags": text_dict['tags'], "pubtime": text_dict['pubtime'],
                         "source": text_dict['source'], "filename": newname}
            writer.writerow(log_entry)
            print(f"logged {text_dict['unique_id']}as : {newname} ")
    return


def article_text_id_assigner(folder_path, iterable, begin):
    """imports all textonly fields of the article and then reassigns them a unique ID
    done as one step in order to limit corpus risk"""
    filelist = os.listdir(folder_path)
    data = {}
    data = pd.DataFrame(data)
    jsonerror, keyerror, final = 0, 0, 0
    csv_logger(None, None, True)
    # begin = 0
    u_id = begin
    if iterable == "all":
        iterable = len(filelist)
        ints = list(range(begin, iterable))
    else:
        ints = list(range(begin, int(begin + iterable)))
    for i in ints:
        u_id += 1
        file = filelist[i]
        filepath = os.path.join(folder_path, file)
        f = open(filepath)  # , encoding='ascii', errors='ignore')
        try:
            j_import = json.load(f)
            j_import = j_import[0]
            #print(j_import)
            try:
                para = j_import['para']
                para = para_clean(para)
            except KeyError:
                para = None
                keyerror += 1
                pass

            try:
                title = j_import['title']
                title = single_line_clean(title)
            except KeyError:
                title = None
                keyerror += 1
                pass

            try:
                author = j_import['author']
                author = single_line_clean(author)
            except KeyError:
                author = None
                keyerror += 1
                pass

            try:
                source = j_import['source']  # change for artnet
            except KeyError:
                source = "error" # None  = "artnet"
                keyerror += 1
                pass
            try:
                url = j_import['url']
            except KeyError:
                url = None
                keyerror += 1
                pass

            try:
                captions = j_import['captions']
                if isinstance(captions, str):
                    captions = single_line_clean(captions)
                elif isinstance(captions, list):
                    new_captions = []
                    for caption in captions:
                        caption = single_line_clean(caption)
                        new_captions.append(caption)
                    captions = new_captions
            except KeyError:
                captions = None
                keyerror += 1
                pass

            try:
                tags = j_import['tag']
                new_tags = []
                for tag in tags:
                    tag = single_line_clean(tag)
                    new_tags.append(tag)
                tags = new_tags
            except KeyError:
                tags = None
                keyerror += 1
                pass

            try:
                pubtime_i = j_import['pubtime']
                pubtime = pubtime_to_df(pubtime_i, source)
            except KeyError:
                pubtime_i = None  # "2005-06-15T06:06:06"
                keyerror += 1
                pass
            f.close()
        except json.decoder.JSONDecodeError:
            f.close()
            jsonerror += 1
            pass

        text_dict = {"title": title, "unique_id": u_id,
                     "para": para, "author": author, "url": url,
                     "tags": tags, "captions": captions,
                     "pubtime": pubtime, "source": source}
        print(text_dict)
        print(f"unique ID int : {u_id}  source: {source} title : {title[10:25]}  iterator {i}")
        final = file_prep_and_export(final, file, text_dict)
    print(f"Keyerrors: {keyerror} \t Json import errors: {jsonerror}  \t  final import count: {final}")
    return


def article_loader_to_df(folder_path, iterable, israndom=False):
    """imports a certain number of articles from the database"""
    filelist = os.listdir(folder_path)
    data = {}
    data = pd.DataFrame(data)
    jsonerror, keyerror = 0, 0
    if israndom:
        ints = random_corpus_sampling(iterable, filelist)
    else:
        ints = list(range(0, iterable))
    for i in ints:
        file = filelist[i]
        filepath = os.path.join(folder_path, file)
        f = open(filepath)  # , encoding='ascii', errors='ignore')
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
                pubtime_i = None  # "2005-06-15T06:06:06"
                keyerror += 1
                pass

            new_row = {"title": title, "para": para, "author": author,
                       "pubtime": pubtime}
            data = data.append(new_row, ignore_index=True)
            f.close()
        except json.decoder.JSONDecodeError:
            f.close()
            jsonerror += 1
            pass
    # data = data.set_index('title')
    print(f"Keyerrors: {keyerror} \t Json import errors: {jsonerror}  \t  final import count: {data.shape}")
    return data


def filename_clean(filename):
    newname = filename.replace(".json", "")
    newname = newname.replace("-", "_").replace(":", "_").replace(";", "")
    newname = newname.replace("  ", "_").replace(" ", "_")

    # funny business
    newname = newname.replace('#', '').replace('%', '').replace('*', '')
    newname = newname.replace('<', '').replace('>', '').replace('@', '_AT_')
    newname = newname.replace('?', '')

    # things that look like bananas
    newname = newname.replace("(", "").replace(")", "").replace("[", "")
    newname = newname.replace("]", "").replace("{", "").replace("}", "")
    newname = newname.replace("/", "").replace("\\", "").replace("|", "")

    # things that look like whiskers
    newname = newname.replace("`", "").replace("'", "").replace('"', "")
    newname = newname.replace(".", "_").replace(",", "_").replace("+", "_")
    newname = newname.replace("__", "_")
    newname = re.sub(r'[T][\d][\d][_][\d][\d][_][\d][\d][_][\d][\d][_][\d][\d][_]','_', newname) #{2}[\d][_]{2}[\d][_]{2}[\d][_]'T00_00_00_05_00_
    newfilename = str(newname + ".json")
    return newfilename

# print(para)"""para = para[0]
#     tokenizer = RegexpTokenizer(r'\w+')
#     tokens = tokenizer.tokenize(para)
#     #print(tokens)
#     count = len(tokens)
#     if count > 1000 and brought_in < 3000:
#     brought_in += 1"""
#     """else:
#                     pass"""
#                     """folderpath = '~/Desktop/artnet_articles/'
# path = os.path.expanduser(folderpath)
#
# filelist = os.listdir(path)"""
