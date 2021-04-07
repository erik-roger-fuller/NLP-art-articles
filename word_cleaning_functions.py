import pandas as pd
import pickle
import wordcloud
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import json
import os
import nltk
import re
import string
from collections import Counter
from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import CountVectorizer

def combine_text(list_of_text):
    '''Takes a list of text and combines them into one large chunk of text.'''
    combined_text = ' '.join(list_of_text)
    return combined_text

round1 = lambda x: clean_text_for_token_round1(x)
round2 = lambda x: clean_text_for_token_round2(x)

def clean_text_for_token_round1(text):
    '''Make text lowercase, remove text in square brackets, remove punctuation and remove words containing numbers.'''
    text = text.lower()
    text = text.replace('-', ' ')
    text = text.replace("’s ", " ").replace("' ", " ")
    text = text.replace("s’ ", " ").replace("s' ", " ")#remove proper possesives
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\w*\d\w*', '', text)
    return text

def clean_text_for_token_round2(text):
    '''Get rid of some additional punctuation and non-sensical text that was missed the first time around.'''
    text = re.sub('[‘’“”…]', '', text)
    text = re.sub('\n', '', text)
    text = re.sub('new york', 'newyork', text)
    text = re.sub('new year', 'newyear', text)
    text = re.sub('the new museum', 'newmuseum', text)
    #text = text.replace(r'[^\u0020-\u007E]', '')
    return text

def data_to_data_docterm(data):
    data_clean = pd.DataFrame(data.para.apply(round1))
    data_clean = pd.DataFrame(data_clean.para.apply(round2))
    cv = CountVectorizer(stop_words='english')
    data_cv = cv.fit_transform(data_clean.para)
    data_docterm = pd.DataFrame(data_cv.toarray(), columns=cv.get_feature_names())
    data_docterm.index = data_clean.index
    data_docterm = data_docterm.transpose()
    return data_docterm

def docterm_get_stopwords(data_docterm):
    """get the stop words for a particular corpus based on use"""
    top_dict = {}
    for ind, column in enumerate(data_docterm.columns):
        col = data_docterm.iloc[:, [ind]]
        top = col[column].sort_values(ascending=False)
        top = top.head(30)
        top.set_index = data_dtm.iloc[0, ind]
        top_dict[column] = list(zip(top.index, top.values))
    # Print the top 15 words in each article
    for title, top_words in top_dict.items():
        print(title)
        print(', '.join([word for word, count in top_words[0:14]]))
        print('---')
    # Look at the most common top words --> add them to the stop word list
    words = []
    for article in data_docterm.columns:
        top = [word for (word, count) in top_dict[article]]
        for t in top:
            words.append(t)
    # If more than half of the comedians have it as a top word, exclude it from the list
    cutoff = data_dtm.shape[1] * (1 / 3)
    new_stop_words = [word for word, count in Counter(words).most_common() if count > cutoff]
    #new_stop_words# Add new stop words
    stop_words = text.ENGLISH_STOP_WORDS.union(new_stop_words)
    return stop_words

def rewrite_docterm_w_stop_words(data_clean, stop_words):
    # Add new stop words
    cv = CountVectorizer(stop_words=stop_words)
    data_cv = cv.fit_transform(data_clean.para)
    data_stop = pd.DataFrame(data_cv.toarray(), columns=cv.get_feature_names())
    data_stop.index = data_clean.index
    return data_stop

def graph_wordcloud(data_clean):
    prep = " ".join(data_clean['para'])
    wc = WordCloud(stopwords=stop_words, background_color="white", colormap="Dark3",
                   max_font_size=200, random_state=42)
    plt.rcParams['figure.figsize'] = [300, 150]
    # Create subplots for each comedian
    # for index, comedian in enumerate(data.columns):
    wc.generate(prep)
    # plt.subplot(3, 4, index+1)
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    # plt.title(full_names[index])
    plt.show()