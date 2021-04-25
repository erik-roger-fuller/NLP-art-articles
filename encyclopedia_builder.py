import pandas as pd
import numpy as np
import json
import csv
import os
import re
from spacy.kb import KnowledgeBase
import spacy

def museum_classify(desc1, desc2, name):
    if   desc1 == "ART":
        desc1= ["Art Museum"]
    elif desc1 == "BOT":
        desc1= ["Arboretum", "Botanical Garden", "Nature Center"]
    elif desc1 == "CMU":
        desc1= ["Children Museum"]
    elif desc1 == "HST":
        desc1= ["History Museum"]
    elif desc1 == "NAT":
        desc1= ["Natural History Museum","Natural Science Museum"]
    elif desc1 == "SCI":
        desc1= ["Science Museum", " Technology Museum" ,"Planetariums"]
    elif desc1 == "ZAW":
        desc1= ["Zoo", "Aquarium", "Wildlife Conservation"]
    elif desc1 == "GMU":
        desc1= ["Museum", "Uncategorized General Museums"]
    elif desc1 == "HSC":
        desc1= ["Historical Society", "Historic Preservation"]
    else:
        desc1 = [desc1]
    school = ["school", "college", "university", "univ"]

    if any(x in desc2.lower() for x in school):
        desc1.append("academic institution")
        if name != desc2.title():
            name = (name + " at " + desc2.title())

    return desc1, name

def ents_encyc_builder(path, begin, spec=None):
    entities_loc =  os.path.join('/home/erik/Desktop/Datasets/art/art_writing/entity resources', path)
    #os.path.join('C:/Users/17742/Desktop/win_art_writing/art_galleries_nyc' , "ART_GALLERY.csv")'art_galleries_nyc/ART_GALLERY.csv'
    encyc = pd.DataFrame()

    intid = begin
    with open(entities_loc, "r", encoding='unicode_escape') as csvfile: #, encoding="utf8"
        csvreader = csv.DictReader(csvfile, delimiter=",")

        for row in csvreader:
            try:
                #print(row['NAME'])
                name = row['COMMONNAME'].title()
                try:
                    desc1 = row['DISCIPL']
                except KeyError:
                    desc1 = spec
                desc2 = row['LEGALNAME']
                desc, name = museum_classify(desc1, desc2, name)
                city = row['ADCITY'].title()
                state = row['ADSTATE']
                city = f"{city}, {state}"
                loc = "usa"

                qid = intid
                identity = {"qid":qid, "name": name, "city":city, "loc":loc, "desc":desc }
                print(identity)
                encyc = encyc.append(identity, ignore_index=True)
                intid +=1
            except UnicodeDecodeError:
                pass
    encyc.set_index("qid")
    return encyc

"""

school = ["school" , "college" ,"university"]
            if any(x in name.lower() for x in school):
                desc = "academic institution"
            else:
                desc = "art gallery"

def spacy_importer_prepper(data):
    entities = []
    for i in range(data.shape[0]):
        ents_found = []
        # print(i)
        # index, article in data.iterrows()
        article = data.iloc[int(i)]
        # article = article[0]
        para = article["para"]
        meta_dict = dict([("unique_id", article["unique_id"]), ("title", article["title"]), ("author", article["author"]),
                          ("pubtime", article["pubtime"])])
        #print(meta_dict)
        try:
            doc = nlp(para)
            for ent in doc.ents:
                #ent_dict = dict([("entity", str(ent.text)), ("label", str(ent.label_))])
                text = ent.text
                label = ent.label_
                print((text, label), end=', ')
                ent_dict = {"txt": str(text), "label": str(text)}
                ents_found.append(ent_dict)
                #print(ent_dict)
        except TypeError:
            print(article['unique_id'])
            pass
        for found_ent in ents_found:
            all_dict = found_ent.update(meta_dict)
            #print(all_dict, end=', ')
            entities.append(all_dict)
        print("  \n")
    return entities
    
    """