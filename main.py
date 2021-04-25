import pandas as pd
import json
import os
import csv

from encyclopedia_builder import ents_encyc_builder

#windows: 'C:/Users/17742/Desktop/win_art_writing/art_writing/'
global_path = '/home/erik/Desktop/Datasets/art/art_writing/text_cleaned'

path = 'text_cleaned_all'
folder_path = os.path.join(global_path, path)
# os.path.expanduser()


encyc = pd.DataFrame()
encyc0 = ents_encyc_builder("museum_datasets/MuseumFile2018_File1_Nulls.csv", 917)
print(encyc0.head)

begin = encyc0.shape[0]
encyc1 = ents_encyc_builder("museum_datasets/MuseumFile2018_File2_Nulls.csv", begin, "GMU")
print(encyc1.head)
frames = [encyc0, encyc1]

encyc = pd.concat(frames, sort=False)
begin = encyc.shape[0]

encyc2 = ents_encyc_builder("museum_datasets/MuseumFile2018_File3_Nulls.csv", begin, "HSC")
print(encyc2.head)
frames = [encyc, encyc2]
encyc = pd.concat(frames, sort=False)

print(encyc)
encyc.to_csv("museums_usa.csv", sep=",", quoting= csv.QUOTE_NONNUMERIC )

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