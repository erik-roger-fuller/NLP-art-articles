import nltk
import re
from spacy.kb import KnowledgeBase
import pandas as pd
import spacy

def spacy_importer_prepper(data):
    data = pd.DataFrame(data)
    nlp = spacy.load('en_core_web_sm')
    entities = []
    for i in range(1000):
        #print(i)
        #index, article in data.iterrows()
        article = data.iloc[int(i)]
        #article = article[0]
        #para = article["para"]
        meta_dict = dict([ ( "title" , article["title"] ), ("author", article["author"] ),
                 ("pubtime" , article["pubtime"]) ])
        print(meta_dict)
        #doc = nlp(para)
        #for ent in doc.ents:
            #ent_dict = dict([ ("entity", ent.text) , ("label", ent.label_) ])
            #ents_found.append(ent_dict)
        #for found_ent in ents_found:
        # #
        #ents_found =
        #    all_dict = found_ent.update(meta_dict)
        #    entities.append(all_dict)
        return meta_dict

def tokenize_corpus(joined):
    tokens = nltk.wordpunct_tokenize(joined)
    text = nltk.Text(tokens)
    words = [w.lower for w in joined]
    words_list = re.split(r'\W+', joined)
    lower_words_list = []
    for word in words_list:
        word = word.lower()
        watch = ["the", 'of', 'and', 'a', 'to', 'in', 's', 'that', "this", 'is',
                 'for','at', 'on', 'it', 'as', 'by', 'with', 'i', 'was', 'from', 'an', 'be',
                 'are', 'has', 'which', 'but', 'also', 'been', 'its', 'so',
                '1', '2' , '3', '4', '5','6','7','8','9']
        if word not in watch:
            lower_words_list.append(word)
        else:
            pass
    fdist = nltk.FreqDist(lower_words_list)
    """for key in fdist:
         print(key + ':', fdist[key], end='; ')"""
    return lower_words_list , fdist

def longest_words(lower_words_list):
    longest = ''
    for word in lower_words_list:
        if len(word) > len(longest):
            longest = word

def permutations(seq):
    if len(seq) <= 1:
         yield seq
    else:
        for perm in permutations(seq[1:]):
            for i in range(len(perm)+1):
                yield perm[:i] + seq[0:1] + perm[i:]

def named_entity_parser(data):
    lemmatizer = nlp.get_pipe("lemmatizer")
    print(lemmatizer.mode)  # 'rule'
    vocab = nlp.vocab
    kb = KnowledgeBase(vocab=vocab, entity_vector_length=64)
    orgs = []
    for article in data['para'][:1]:
        doc = nlp(article)
        for e in doc.ents:
        # ents = [(e.text, e.label_, e.kb_id_)
            if e.label_ != 'ORG':
                pass
            else:
                orgs.append(e.text)
                print(orgs)
    return orgs
