import pandas as pd
import matplotlib.pyplot as plt
import json
import os
import nltk
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

from article_loader_parser import article_loader_to_df
from sentiment_analysis_functions import *
from word_cleaning_functions import *
from topic_modeling_functions import *

global_path = 'C:/Users/17742/Desktop/win_art_writing/art_writing/'
path = 'nytimes'
#path = 'artnet_articles'
#path = 'artforum'

folder_path = global_path + path #os.path.expanduser(os.path.join(global_path, path))

data = article_loader_to_df(folder_path=folder_path, iterable=50000, israndom=True)
print(data)
#plot = timeplot_sentiment(data, "polarity", path)
