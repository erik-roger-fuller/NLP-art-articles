import pandas as pd
from qwikidata.entity import WikidataItem
from qwikidata.json_dump import WikidataJsonDump
from qwikidata.utils import dump_entities_to_json

from qwikidata.sparql import (get_subclasses_of_item,
                              return_sparql_query_results)

def get_text_from(entry):
    value = ""
    try:
        value = entry["value"]
    except KeyError :
        entry = None
    except TypeError:
        entry = None
    return value


# send any sparql query to the wikidata query service and get full result back
# here we use an example that counts the number of humans
sparql_query = """
SELECT ?museum ?country ?countryLabel ?located_in_the_administrative_territorial_entity ?located_in_the_administrative_territorial_entityLabel ?location ?locationLabel ?instance_of ?instance_ofLabel ?museumLabel WHERE {
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
  ?museum wdt:P31 wd:Q33506.
  OPTIONAL { ?museum wdt:P17 ?country. }
  OPTIONAL { ?museum wdt:P131 ?located_in_the_administrative_territorial_entity. }
  OPTIONAL {  }
  OPTIONAL {  }
  OPTIONAL {  }
  OPTIONAL { ?museum wdt:P276 ?location. }
  OPTIONAL {  }
  OPTIONAL {  }
  OPTIONAL { ?museum wdt:P31 ?instance_of. }
}

"""

res = return_sparql_query_results(sparql_query)
#print(res)LIMIT 100

results = res["results"]
results = results["bindings"]
#soup = BeautifulSoup(res, 'lxml')
#print(soup)
#print(results)
results = pd.DataFrame(results)
results = results[['museumLabel', 'museum', 'instance_ofLabel', 'locationLabel',
                   'located_in_the_administrative_territorial_entityLabel', 'countryLabel' ]]


#results.to_json('wikidata_museums_raw.json')
encyc = pd.DataFrame()

for i in range(results.shape[0]):
    try:
        row = results.iloc[i]
        name = row['museumLabel']
        name = get_text_from(name)
        print(name)

        desc1 = row['instance_ofLabel']
        desc1 = get_text_from(desc1)


        school = ["school", "college", "university", "academy"]

        desc1 = [desc1]
        #if any(x in desc1.lower() for x in school):
        #    desc1 = [desc1]
        desc1.append("academic institution")
        #else:
        #    desc1 =[desc1]

        city = row['locationLabel']
        city = get_text_from(city)

        state = row['located_in_the_administrative_territorial_entityLabel']
        state = get_text_from(state)

        if city not in state:
            city1 = f"{city}, {state}"
        else:
            city1 = f"{city} {state}"

        loc = row['countryLabel']
        loc = get_text_from(loc)

        qid = row['museum']
        qid = get_text_from(qid)
        qid = qid.split('entity/')
        qid = qid[-1]
        identity = {"qid": qid, "name": name, "city": city1, "loc": loc, "desc": desc1}
        encyc = encyc.append(identity, ignore_index=True)

        if i % 9999 == 0:
            encyc.to_json(f'wikidata_museums_test{i}.json')
            print(i)
    except KeyError:
        pass

encyc.to_json('wikidata_museums.json')




#item = WikidataItem(item)
 #print(item.get_label())
#results['museumLabel'].iterrows()
#print(results)
# use convenience function to get subclasses of an item as a list of item ids
#Q_RIVER = "Q4022"
#subclasses_of_river = get_subclasses_of_item(Q_RIVER)