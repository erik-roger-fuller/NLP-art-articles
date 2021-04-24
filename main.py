import pandas as pd
import json
import os
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
import time"""

from article_loader_parser import article_text_id_assigner, article_loader_to_df, load_entities
#from sentiment_analysis_functions import *
#from word_cleaning_functions import *
#from topic_modeling_functions import *

#windows: 'C:/Users/17742/Desktop/win_art_writing/art_writing/'
global_path = '/home/erik/Desktop/Datasets/art/art_writing/text_cleaned'
#path = 'nytimes' # 122660 logged #122791 130 before error
#then 27979 . hyperallergic finished. therfore new begin = 150770 {then plus 500
#artforumen then logged 62414 frieze logged 14818 brings to 228002
#artnet then 24546 bringing grand total to 252548
#path = 'artnet_articles'
#path = 'frieze'
#path = 'artforum'
#path = 'hyperallergic'
path = 'text_cleaned_all'
folder_path = os.path.join(global_path, path)
# os.path.expanduser()

#article_text_id_assigner(folder_path=folder_path, iterable="all", begin=228002 )
#data = article_loader_to_df(folder_path=folder_path, iterable=5000, israndom=True)
#print(data)
#plot = timeplot_sentiment(data, "polarity", path)
name_dict, desc_dict, loc_dict = load_entities()
for QID in name_dict.keys():
    print(f"{QID}, name={name_dict[QID]}, desc={desc_dict[QID]} located={loc_dict[QID]}")