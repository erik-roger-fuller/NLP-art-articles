import nltk
import re
from spacy.kb import KnowledgeBase
import pandas as pd
import spacy
import numpy as np


def ent_text_clean(text):
    text = text.replace("'s", "")
    return text

def abbreviation_parser(orgs_found):
    abbrevs, tests = [], [],
    # print("orgs: ", len(orgs_found))
    for org in orgs_found:
        org = org.replace(".", "")
        org = ent_text_clean(org)
        try:
            if len(re.findall("[A-Z]", org)) / len(org.replace(" ", "")) > .65:
                abbrevs.append(org)
            else:
                tests.append(org)
        except ZeroDivisionError:
            tests.append(org)

    print("orgs:", len(abbrevs) + len(tests))
    if len(abbrevs) > 0:
        for test in tests:
            test_first = re.sub("^[Tt][h][e][\s]", "", test)  # elim "T/the"
            test_first = re.findall("([A-Za-z])\w+", test_first)
            test_first = "".join(test_first)

            if len(test_first) > 2:
                abbrevs = [test if i == test_first else i for i in abbrevs]

                test_first_noof = test_first.replace("o", "").replace("f", "").replace("t", "")
                # print(test_first_noof)
                abbrevs = [test if i == test_first_noof else i for i in abbrevs]

                test_first_upper = test_first.upper()
                abbrevs = [test if i.upper() == test_first_upper else i for i in abbrevs]

                # abbrevs = ["Museum of Contemporary Art" if i=="MOCA" else i for i in abbrevs]
                # abbrevs = ["Museum of Contemporary Art" if i=="MOCA" else i for i in abbrevs]

        tests.extend(abbrevs)
    print("replaced or remaining: ", len(abbrevs), abbrevs)
    print("unabbreved: ", len(tests), tests)
        #tests = np.array(tests, dtype=np.str_)

    return tests

nlp = spacy.load('en_core_web_trf')  # lg')

def ner_grabber(para, unique_id, nlp):
    document_mentions, document_person_mentions = [] , []
    orgs_text = []
    people_text = []
    orgs_found = {}#np.array()
    people_found = {}
    if para and unique_id:
        try:
            doc = nlp(para)
            for ent in doc.ents:
                # ent_dict = dict([("entity", str(ent.text)), ("label", str(ent.label_))])
                if ent.label_ == 'ORG':
                    # print(ent.text, ent.label_)
                    text = ent_text_clean(ent.text)
                    orgs_text.append(text)  # , ent.label_}
                elif ent.label_ == 'PERSON':
                    # print(ent.text, ent.label_)
                    text = ent_text_clean(ent.text)
                    people_text.append(text)  # , ent.label_}
            orgs_text = abbreviation_parser(orgs_text)
            for org in orgs_text:
                try:
                    document_mentions.append({"unique_id":unique_id, "entity": org})
                except ValueError:
                    pass
            print("persons: ", people_text)
            for person in people_text:
                try:
                    document_person_mentions.append({"unique_id":unique_id, "entity": person})
                except ValueError:
                    pass

        except IndexError:
            pass
    #print("  \n")
    else:
        pass

    return document_mentions, document_person_mentions

#orgs_found[unique_id] = org
def spacy_importer_prepper(data, model):
    nlp = spacy.load(model)
    try:
        all_docs_mentions = np.vectorize(ner_grabber)(data['para'] , data["unique_id"], nlp)
    except ValueError:
        all_docs_mentions = []
        pass
    return all_docs_mentions



"""               # except TypeError:
            #    print("didnt work" , article['unique_id'])
            #    pass
            #document_mentions
            #orgs_found[unique_id] = orgs_text
            #orgs_found = np.array([unique_id, orgs_text]) for i in range(sample):
        
        article = data.iloc[int(i)]
        # article = article[0]
        para = article["para"]
        unique_id = int(article["unique_id"])
    """






def tokenize_corpus(joined):
    tokens = nltk.wordpunct_tokenize(joined)
    text = nltk.Text(tokens)
    words = [w.lower for w in joined]
    words_list = re.split(r'\W+', joined)
    lower_words_list = []
    for word in words_list:
        word = word.lower()
        watch = ["the", 'of', 'and', 'a', 'to', 'in', 's', 'that', "this", 'is',
                 'for', 'at', 'on', 'it', 'as', 'by', 'with', 'i', 'was', 'from', 'an', 'be',
                 'are', 'has', 'which', 'but', 'also', 'been', 'its', 'so',
                 '1', '2', '3', '4', '5', '6', '7', '8', '9']
        if word not in watch:
            lower_words_list.append(word)
        else:
            pass
    fdist = nltk.FreqDist(lower_words_list)
    """for key in fdist:
         print(key + ':', fdist[key], end='; ')"""
    return lower_words_list, fdist


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
            for i in range(len(perm) + 1):
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
