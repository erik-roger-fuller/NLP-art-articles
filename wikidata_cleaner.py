import pandas as pd
import numpy as np
import re
import csv
import json
import json
from fuzzywuzzy import fuzz


def no_duplicates(xs):
    ys = []
    for x in xs:
        re_output = re.sub(r'\b(\w+)( \1\b)+', r'\1', x)
        ys.append(re_output)
    #y = set(ys)
    return ys

def no_list_dupes(x):
    x = set(x)
    return x

def make_list(xs):
    ys = []
    for x in xs:
        ys.append(x)#x = [x]
    return ys


#identity = {"qid": qid, "name": name, "city": city1, "loc": loc, "desc": desc1}


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

    #print(matches)800
def convert_set(set):
    if len(list(set))>1:
        return [*set, ]
    else:
        return set[0]

def str_change(set):
    new = []
    for val in set:
        val = val.replace('[',"").replace(']',"").replace("'","")
        val = val.title()
        new.append(val)
    return new


def add_and_compare(i, outside, flag, encyc_m):
    add = encyc.iloc[i][flag]
    add = add.replace('{',"").replace('}',"").replace("'","")
    add = add.title()
    #outside = "".join(add)
    add = [add]
    new = str_change(outside[flag])
    add.extend(new)
    add = set(add)
    add = ", ".join(add)
    add = re.sub(r'\b(\w+)( \1\b)+', r'\1', add)
    encyc.iloc[i][flag] = add
    encyc_m.drop(encyc_m.index[i], inplace=True)

def matchy_matchy(file, encyc):
    with open(file, 'r') as read2:
        encyc_m = pd.read_csv(read2)


        for i in range(0, encyc.shape[0]):
            matches = compare_lev(encyc['name'][i], encyc_m)

            if matches:
                outside = encyc_m.iloc[matches[0]]
                flags = ['loc', 'desc', 'city' ]
                for flag in flags:
                    add_and_compare(i, outside, flag, encyc_m)
                print(encyc.iloc[i])
                print("at: ", i , "out of " , encyc.shape[0])

            if i % 9999 == 0:
                frames = [encyc, encyc_m]

                encyc_bkp = pd.concat(frames, sort=False)
                encyc_bkp.to_csv(f"art_compared_waypoint{i}.csv", sep=",", quoting=csv.QUOTE_NONNUMERIC)
                encyc_bkp = None


        frames = [encyc, encyc_m]

        encyc_f = pd.concat(frames, sort=False)
        encyc_f.to_csv("art_insts_compared.csv", sep=",", quoting= csv.QUOTE_NONNUMERIC )
        return encyc_f

with open('results/wikidata_concatenated.csv', 'r') as read:

    encyc = pd.read_csv(read)
    file = "museums_usa.csv"

    encyc = matchy_matchy(file, encyc)
    file3='art_galleries.csv'
    encyc_3 = matchy_matchy(file3, encyc_2)


'''allmatch.append
    row1 = encyc.iloc[i]
    name1 = row1['name']    #[:10000]:[:10000]:
    for j in range(0, top):
        row2 = encyc_m.iloc[j]
        name2 = row2['name']
        distance = fuzz.ratio(name1, name2)
        #print(name1, name2, distance)partial_
        if distance > 88:

            print(name1, name2, distance, i, j)
            print(row1)
            print(row2)
'''


"""


#encyc['city'] = encyc['city'].apply(make_list)
#encyc['name'] = encyc['name'].apply(make_list)
#encyc['loc'] = encyc['loc'].apply(make_list)
#'loc', 'name'], 'loc', 'name']
#encyc_c = encyc.groupby("qid").sum()

#encyc_c['city'] = encyc_c['city'].apply(no_duplicates)
#encyc_c['name'] = encyc_c['name'].apply(no_duplicates)
#encyc_c['loc'] = encyc_c['loc'].apply(no_duplicates)
#encyc_c['desc'] = encyc_c['desc'].apply(no_duplicates)


with open('results/wikidata_museums_cleaned.csv', 'r') as read1:
        encyc1 = pd.read_csv(read1)
        frames = [encyc0, encyc1]

        encyc = pd.concat(frames, sort=False)

        with open('results/wikidata_art_schools_cleaned.csv', 'r') as read2:
            encyc2 = pd.read_csv(read2)
            frames = [encyc, encyc2]

            encyc = pd.concat(frames, sort=False)
            print(encyc.shape, encyc.head)



encyc = pd.DataFrame()
encyc0 = ents_encyc_builder("museum_datasets/MuseumFile2018_File1_Nulls.csv", 917)
print(encyc0.head)

begin = encyc0.shape[0]
encyc1 = ents_encyc_builder("museum_datasets/MuseumFile2018_File2_Nulls.csv", begin, "GMU")
print(encyc1.head)
frames = [encyc0, encyc1]

encyc = pd.concat(frames, sort=False)
begin = encyc.shape[0]

encyc2 = ents_encyc_builder("museum_datasets/MuseumFile2018_File3_Nulls.csv", begin, "HSC")
print(encyc2.head)
frames = [encyc, encyc2]
encyc = pd.concat(frames, sort=False)

print(encyc)
encyc.to_csv("museums_usa.csv", sep=",", quoting= csv.QUOTE_NONNUMERIC )
"""

