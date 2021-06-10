import nltk
import re
from spacy.kb import KnowledgeBase
import pandas as pd
import spacy
import numpy as np


def ent_text_clean(text):
    text = text.replace("’s", "").replace("’s", "")
    text = text.replace("s’", "s").replace("s’", "s")
    return text

def first_name_last(names):
    tests = {}
    for name in names:
        name = name.replace("'s","").replace("`s","").replace("’s","")
        s_name = name.split(" ")
        last = s_name[-1]
        if len(s_name)>1:
            tests[last] = name
    print("name input: ",names.values)
    print("name tests: ",tests)
    for last in tests.keys():
        names = [tests[last] if i == last else i for i in names]
    print("name output: ",names)
    return names

def abbreviation_parser(orgs_found):
    abbrevs, tests = [], [],
    # print("orgs: ", len(orgs_found))
    for org in orgs_found:
        org = org.replace(".", "")
        #org = ent_text_clean(org)
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
    #tests = [test.upper() for test in tests]
    return tests

nlp = spacy.load('en_core_web_trf')  # lg')

def ent_sorter(text, label, unique_id, ent_types):
    if label in ent_types:
        text = ent_text_clean(text)
        if text != None:
            return {'ent_string':text, 'ent_type':label, 'article_uid':unique_id}
    else:
        pass

def ner_grabber(para, unique_id, nlp, prev):
    #ent_types = ['PERSON','ORG','GPE', 'DATE','CARDINAL', 'NORP','MONEY',
    #              'WOR', 'FAC', 'LOC', 'WORK_OF_ART', 'EVENT']
    ent_types = ['PERSON', 'ORG', 'GPE',  'DATE','NORP', 'MONEY',
                  'WOR', 'FAC', 'LOC', 'WORK_OF_ART', 'EVENT']
    document_mentions = []

    if para and unique_id:
        try:
            doc = nlp(para)
            for ent in doc.ents:
                #print(ent.text, ent.label_)
                try:
                    mention = ent_sorter(ent.text, ent.label_, unique_id, ent_types)
                    #print(mention)
                    if mention != None :
                        document_mentions.append(mention)
                except ValueError:
                    print("value error")
                    pass

        except IndexError:
            pass
    else:
        pass
    df = pd.DataFrame(document_mentions)

    """here the amount of entities are finally specified"""
    ent_ids = [i for i in range(prev, prev + df.shape[0])]
    df['ent_id'] = ent_ids
    df['ent_string'] = df['ent_string'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').str.lower()

    orgs_found = df[(df['ent_type'] == "ORG") | (df['ent_type'] == "GPE")]
    #print(orgs_found["ent_string"])
    orgs_found["ent_string"] = abbreviation_parser(orgs_found["ent_string"])

    df[(df['ent_type'] == "ORG") | (df['ent_type'] == "GPE")] = orgs_found

    names_found = df[df['ent_type'] == "PERSON"]
    names_found["ent_string"] = first_name_last(names_found["ent_string"])
    #print(names_found)
    df[df['ent_type'] == "PERSON"] = names_found
    return df #, document_person_mentions.loc.loc[,:]#print(df.loc[["ORG","GPE"], ["ent_type"]])

def spacy_importer_prepper(data, model):
    nlp = spacy.load(model)
    try:
        all_docs_mentions = np.vectorize(ner_grabber)(data['para'] , data["unique_id"], nlp)
        #convert to pandas seriers here
    except ValueError:
        all_docs_mentions = []
        pass
    return all_docs_mentions



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
    for key in fdist:
         print(key + ':', fdist[key], end='; ')
    return lower_words_list, fdist"""
""" 


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
                
            print("persons: ", people_text)
            for person in people_text:
                try:
                    document_person_mentions.append({"unique_id":unique_id, "entity": person})
                except ValueError:
                    pass
              
              
              
              # except TypeError:
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