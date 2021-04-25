import pandas as pd
import re
import json


#identity = {"qid": qid, "name": name, "city": city1, "loc": loc, "desc": desc1}
with open('wikidata_art_galleries.json', 'r') as read:


    encyc = pd.read_json(read)

    print(encyc.shape, encyc.head)

    encyc_c = encyc.groupby()