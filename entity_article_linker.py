import pandas as pd
import numpy as np
import json
import os
import csv
import spacy
import time
from fuzzywuzzy import fuzz

def levenshtien_distance(x,y):
    return fuzz.ratio(x, y)


def compare_lev(name1, encyc_m):
    matches = []
    results = np.vectorize(levenshtien_distance)(name1, encyc_m['name'])
    out = np.where(results > 85)
    #print(len(out))
    if out[0].size > 0:
        match = encyc_m['name'].iloc[out]
        #print(name1, match)
        #print(out.shape[0]).shape[0]
        matches.append(out)

    if len(matches)>0:
        return matches

#ref_file = "C:\\Users\\17742\\Desktop\\win_art_writing\\art_writing\\text_cleaned\\articles_ids_index.csv" ##win
ref_file = "/home/erik/Desktop/Datasets/art/art_writing/text_cleaned/articles_ids_index.csv" ##linux
#folder_path = "entities_backups"#os.path.join(global_path, path)


with open(ref_file, "r", encoding='utf-8') as read:
    reference = pd.read_csv(read, low_memory=False)
    reference.set_index("unique_id")

with open("person_entities_cleaned.csv", "r", encoding='utf-8') as read2:
    record = pd.read_csv(read2, low_memory=False)
    record.set_index("unique_id")

    #for i in range(reference.shape[0]):
    #    name1 = reference['entity']
    #    entry = record[record.index == i]
    #    if entry.shape[0] > 1:
lower = record['entity'].str.lower()
record['entity'] = lower

record.set_index('entity')

names = pd.unique(record['entity'])
#names = names.astype('category')
allnames = pd.DataFrame()


for name in names:
    name_r = record.loc[name]
    occurences = name_r['unique_id']
    name_dict = {"entity":name, "occurs":occurences}
    allnames.append(name_dict, ignore_index=True)




        #    record.loc[i, "entity"] = first_name_last(entry["entity"])
        #print(entry)


    ##del record['Unnamed: 0']
    #record.replace([], np.nan, inplace=True)
    #record.dropna(subset=['entity'], inplace=True)



"""
def first_name_last(names):
    tests = {}
    for name in names:
        name = name.replace("'s","").replace("`s","").replace("’s","")
        s_name = name.split(" ")
        last = s_name[-1]
        #first = s_name[0]
        if len(s_name)>1:
            tests[last] = name
    print("input: ",names.values)
    print("tests: ",tests)
    for last in tests.keys():
        names = [tests[last] if i == last else i for i in names]
    print("output: ",names)
    return names

    #reference = pd.DataFrame(reference){"unique_id": None, "entity": None}
        #article_ent_linker(file, entry, doc_ent_matrix_orgs, doc_ent_matrix_pers)
#print(doc_ent_matrix_orgs)

filelist = os.listdir(folder_path)
#def article_ent_linker(file, entry, doc_ent_matrix_orgs, doc_ent_matrix_pers ):
    #print(entry.dtype)


file = "all_art_persons_entities.csv"

with open(file, 'r', encoding='utf-8') as read2:
    record = pd.read_csv(read2, low_memory=False)
    record = record.set_index("unique_id")
    del record['Unnamed: 0.1']
    del record['Unnamed: 0']
    record.replace([], np.nan, inplace=True)
    record.dropna(subset=['entity'], inplace=True)




def export_to_matrix(unique_id, entity, flag):
    entry_s = {"unique_id": unique_id, "entity": entity}
    print(entry_s)

    #unique_ids = entry["unique_id"]
    entities = entry["entity"]
    #doc_ent_matrix_pers

    #np.vectorize
    #entry['unique_id'] =
    #export_to_matrix(unique_ids, entities, flag)
    #fentry.apply(lambda row: , unique_ids, entities, flag)
    #if flag == "org":

#doc_ent_matrix_orgs = pd.DataFrame(columns=["unique_id", "entity"])#.set_index("unique_id")
#doc_ent_matrix_pers = pd.DataFrame(columns=["unique_id", "entity"])#.set_index("unique_id")


for file in filelist:  #[13:18]

    file_p = f"entities_backups/{file}"
    with open(file_p, 'r', encoding='utf-8') as read2:
        entry = pd.read_csv(read2, low_memory=False)
        #entry = entry.set_index("unique_id")

        if file[:7] == "persons":
            print(file[:7])
            doc_ent_matrix_pers = pd.concat([doc_ent_matrix_pers, entry], sort=False)

        elif file[:7] == "organiz":
            print(file[:7])
            doc_ent_matrix_orgs = pd.concat([doc_ent_matrix_orgs, entry], sort=False)

doc_ent_matrix_orgs.to_csv("all_art_organiz_entities.csv", sep=",", quoting=csv.QUOTE_NONNUMERIC)
doc_ent_matrix_pers.to_csv("all_art_persons_entities.csv", sep=",", quoting=csv.QUOTE_NONNUMERIC)

"""