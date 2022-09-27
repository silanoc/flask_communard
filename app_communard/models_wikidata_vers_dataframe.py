#! /usr/bin/env python3
# coding: utf-8

import sys
from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd

endpoint_url = "https://query.wikidata.org/sparql"

query = """SELECT ?communard ?communardLabel ?prénom ?prénomLabel  ?nom_de_famille ?nom_de_familleLabel ?image ?identifiant_Maitron WHERE {
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
  ?communard wdt:P106 wd:Q1780490.
  OPTIONAL { ?communard wdt:P735 ?prénom. }
  OPTIONAL { ?communard wdt:P4724 ?identifiant_Maitron. }
  OPTIONAL { ?communard wdt:P734 ?nom_de_famille. }
  OPTIONAL { ?communard wdt:P18 ?image. }
}
"""

def get_results(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

def creation_data_frame(results):
    df =  pd.json_normalize(results["results"]["bindings"])
    #print("df : ",df.dtypes)
    #print(df.size)
    #print(df.columns)
    #print(df)
    return df

def obtenir_les_communards(df) -> list:
    """mettre dans un set pour récuper les uniques, dans une liste pour ranger par ordre alpha"""
    serie_personne = df['communardLabel.value'].sort_values()
    set_personne = set()
    for item in serie_personne:
        set_personne.add(item)
    list_personnage = list(set_personne)
    list_personnage.sort()
    return list_personnage

if __name__ == "__main__":
    results = get_results(endpoint_url, query)
    df = creation_data_frame(results)

    qui = obtenir_les_communards(df)
    print(qui)
    print(len(qui))