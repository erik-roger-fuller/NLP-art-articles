import numpy as np
from numpy import linspace, loadtxt, ones, convolve
import pandas as pd
import json
import os
import nltk
from nltk import RegexpTokenizer
import re
from datetime import datetime
import time
import string
import spacy
nlp = spacy.load("en_core_web_sm")
from spacy.kb import KnowledgeBase
from gensim import matutils, models
import scipy.sparse
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer



import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


from gensim.utils import simple_preprocess
# Build the bigram and trigram models
bigram = gensim.models.Phrases(data_clean, min_count=5, threshold=100) # higher threshold fewer phrases.
trigram = gensim.models.Phrases(bigram[data_clean], threshold=100)

# Faster way to get a sentence clubbed as a trigram/bigram
bigram_mod = gensim.models.phrases.Phraser(bigram)
trigram_mod = gensim.models.phrases.Phraser(trigram)

# Apply a third round of cleaning
def clean_text_round3(text):
    '''build and apply gensim bigram trigram'''
    text = make_bigrams(text)
    text = make_trigrams(text)
    text = lemmatization(text)
    text = re.sub('[‘’“”…]', '', text)
    #text = text.replace(r'[^\u0020-\u007E]', '')
    return text

round3 =  clean_text_round3

data_clean = pd.DataFrame(data_clean.para.apply(round3))


nlp = spacy.load("en_core_web_sm", disable=['parser', 'ner'])

def make_bigrams(texts):
    return [bigram_mod[doc] for doc in texts]

def make_trigrams(texts):
    return [trigram_mod[bigram_mod[doc]] for doc in texts]

def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    """https://spacy.io/api/annotation"""
    for sent in texts:
        doc = nlp(" ".join(sent))
        text_out = [token.lemma_ for token in doc if token.pos_ in allowed_postags]
    return texts_out

# Remove Stop Words
#data_clean_nostops = remove_stopwords(data_clean)# Form Bigrams

# Initialize spacy 'en' model, keeping only tagger component (for efficiency)
data_clean_bigrams = make_bigrams(data_clean)

# Do lemmatization keeping only noun, adj, vb, adv
nlp = spacy.load("en_core_web_sm", disable=['parser', 'ner'])

data_clean_lemmatized = lemmatization(data_clean_bigrams, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])

print(data_clean_lemmatized[:1])

def return_nouns(data_clean):
    # Apply the nouns function to the transcripts to filter only on nouns
    data_nouns = pd.DataFrame(data_clean.para.apply(nouns))
    return data_nouns

def return_nouns_and_adj(data_clean):
    # Apply the nouns function to the transcripts to filter only on nouns
    data_nouns_adj = pd.DataFrame(data_clean.para.apply(nouns_adj))
    return data_nouns_adj

def docterm_to_termdoc(data_docterm):
    # One of the required inputs is a term-document matrix
    tdm = data_docterm.transpose()
    return tdm

#put the term-document matrix into a new gensim format, from df --> sparse matrix --> gensim corpus
sparse_counts = scipy.sparse.csr_matrix(tdm)
corpus = matutils.Sparse2Corpus(sparse_counts)
# Gensim also requires dictionary of the all terms and their respective location in the term-document matrix
id2word = dict((v, k) for k, v in cv.vocabulary_.items())
# Now that we have the corpus (term-document matrix) and id2word (dictionary of location: term),
# we need to specify two other parameters as well - the number of topics and the number of passes
lda = models.LdaModel(corpus=corpus, id2word=id2word, num_topics=10, random_state=100,
                      chunksize=100, passes=50, per_word_topics=True)
lda.print_topics()

import gensim.corpora as corpora# Create Dictionary
id2word = corpora.Dictionary(data_clean['para'])

"""
#print(lda.print_topics())
dictlda = lda[corpus]
dictlda

#!/usr/bin/python3 -m pip install pyldavis
import pyLDAvis.gensim 
import pyLDAvis# Visualize the topics
import pyLDAvis.sklearn
import gensim
#???
#

pyLDAvis.enable_notebook()

num_topics = 10
LDAvis_data_filepath = os.path.join('./results/ldavis_prepared_'+str(num_topics))

# # this is a bit time consuming - make the if statement True
# # if you want to execute visualization prep yourself
if 1 == 1:
    LDAvis_prepared = pyLDAvis.gensim.prepare(lda, corpus, id2word)
    #pyLDAvis.sklearn.prepare(lda, corpus, cv)

    with open(LDAvis_data_filepath, 'wb') as f:
        pickle.dump(LDAvis_prepared, f)# load the pre-prepared pyLDAvis data from disk

#with open(LDAvis_data_filepath, 'rb') as f:
    #LDAvis_prepared = pickle.load(f)
pyLDAvis.save_html(LDAvis_prepared, './results/ldavis_prepared_'+ str(num_topics) +'.html')
LDAvis_prepared
print(corpus)"""