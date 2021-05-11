import matplotlib.pyplot as plt
import pandas as pd
import numpy as np



backgnd = "~/home/erik/Desktop/Datasets/art/art_writing/text_cleaned/"

def entity_cross_suba(artist):
    for file in artist.filename:
        filename = backgnd + file
        with open(filename, "r") as parse:
            data = pd.read_json(parse)
            pol = lambda x: TextBlob(x).sentiment.polarity
            sub = lambda x: TextBlob(x).sentiment.subjectivity
            artist.loc(file, artist['filename'])['polarity'] = data['para'].apply(pol)
            artist.loc(file, artist['filename'])['subjectivity'] = data['para'].apply(sub)


concated = pd.DataFrame({'entity': [], 'unique_id': [],
                'title': [],  'source': [], 'author'  :[], 'url': [],
                 'tags': [], 'pubtime': [], 'filename':[]})
for row in ref1.itertuples(index=True):
    findings = record[record["unique_id"] == int(row[0])]
    # print(row, found)
    if findings.shape[0] != 0:
        for found in findings['entity']:
            # print(found[1])
            addfound = {
                'entity': found, 'unique_id': row[0],
                'title': row[1], 'source': row[2], 'author': row[3], 'url': row[4],
                'tags': row[5], 'pubtime': row[6], 'filename': row[7]
            }
            print(addfound)
            concated = concated.append(addfound, ignore_index=True)

