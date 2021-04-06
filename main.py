import pandas as pd
import wordcloud
from wordcloud import WordCloud
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
from scipy.signal import savgol_filter
from article_loader_parser import article_loader_to_df

global_path = 'C:/Users/17742/Desktop/win_art_writing/nytimes_articles/articles_dump'
path = 'artnet_articles'
#path = 'artnet_articles'
#path = 'artnet_articles'
#folderpath = os.path.expanduser(os.path.join(global_path, path))

filelist = os.listdir(global_path)
data = article_loader_to_df(filelist, 200)
print(data)