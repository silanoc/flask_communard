#! /usr/bin/env python3
# coding: utf-8

from encodings import utf_8
from os
import sys
import pandas as pd
from SPARQLWrapper import SPARQLWrapper, JSON
import logging
import typing


class Extraction():
    def __init__(self, chemin: str) -> None:
        self.endpoint_url: str = "https://query.wikidata.org/sparql"
        self.query: str = self.ouvrir_requete(chemin)
        logging.debug("initialisation class Extraction ok")
        
    def ouvrir_requete(self, chemin: str) -> str:
        """écrit le contenu du fichier texte, 
        contenant une requete à faire dans queryservice,
        dans une chaine de caractère"""
        try:
            fichier = open(chemin, "r", encoding = "utf8")
            logging.debug("ouverture du fichier de requete")
        except:
            logging.error("echec d'ouverture du fichier de requete")
        try:
            requete: str = fichier.read()
            logging.debug("lecture du fichier de requete, le mettre dans une variable")
        except:
            logging.error("echec de la lecture du fichier de requete")
        return requete

    def get_results(self, endpoint_url, query) -> JSON:
        """code issus de queryservice https://query.wikidata.org > code > Python
        """
        user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
        sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        logging.debug("conversion du résultat de la requete en JSON - ok")
        return sparql.query().convert()

    def creation_data_frame(self, results) -> pd.DataFrame:
        try:
            df: pd.DataFrame =  pd.json_normalize(results["results"]["bindings"])
            #print("df : ",df.dtypes)
            #print(df.size)
            #print(df.columns)
            #print(df)
            logging.debug("conversion du résultat du JSON en data frame - ok")
        except:
            logging.error("echec de la convertion du Json en dataFrame")
        return df
    
    def enchainer(self):
        results = self.get_results(self.endpoint_url, self.query)
        df = self.creation_data_frame(results)
        return df
        
    def get_dataframe(self):
        logging.debug("get_dataframe - ok")
        return self.enchainer()

def obtenir_les_items_communards(df) -> list:
    """mettre dans un set pour récuper les uniques, dans une liste pour ranger par ordre alpha"""
    serie_personne: pd.Series = df['communardLabel.value'].sort_values()
    set_personne = set()
    for item in serie_personne:
        set_personne.add(item)
    list_personnage = list(set_personne)
    list_personnage.sort()
    return list_personnage

if __name__ == "__main__":

    extract = Extraction("app_communard/requetes/requete_nom_prenom_image_maiton.txt")
    df = extract.get_dataframe()
    
    qui = obtenir_les_items_communards(df)
    print(qui)
    print(len(qui))