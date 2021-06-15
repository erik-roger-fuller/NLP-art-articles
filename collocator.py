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

global_path ='C:/Users/17742/PycharmProjects/NLP-art-articles/pkl_backups/'

path = 'feather' #'pickle'
folder_path = os.path.join(global_path, path)
filelist = os.listdir(folder_path)

df_all = pd.DataFrame()
for i in range(0, len(filelist)):    ### #50):
    file = filelist[i]
    filepath = os.path.join(folder_path, file)
    #df = pd.read_pickle(filepath)

    df = pd.read_feather(filepath)
    del df['index']
    df['article_uid'] = df['article_uid'].astype(int)
    frames = [df_all, df]
    df_all = pd.concat(frames, sort=False)
    print(i, df_all.shape[0])
    #f = open(filepath)

#df_all.reset_index(inplace=True)
#df_all.to_feather('C:/Users/17742/PycharmProjects/NLP-art-articles/pkl_backups/feather_final_all.feather')#
df_all.to_pickle('C:/Users/17742/PycharmProjects/NLP-art-articles/pkl_backups/feather_final_all.pkl')
print("success!", df_all.shape[0])

