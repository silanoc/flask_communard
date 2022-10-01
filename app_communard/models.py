#! /usr/bin/env python3
# coding: utf-8

from cmath import isinf
from .models_wikidata_vers_dataframe import *


logging.basicConfig(level=logging.DEBUG,
                    filename="./app_communard/logs/app.log",
                    filemode="w",
                    format='%(asctime)s - %(levelname)s - %(message)s')

def obtenir_information(individu)-> dict():
    info_communard = {}
    print(individu)
    df2 = df[df['communardLabel.value'].isin([individu])]
    #print(df2)
    info_communard = df2.to_dict()
    #print(info_communard)
    return info_communard

# extraction de la requete
extract = Extraction("app_communard/requetes/requete_nom_prenom_image_maiton.txt")
df: pd.DataFrame = extract.get_dataframe()
# avoir une liste de communard-e-s, servant à afficher tous les noms sur la page personnages
qui = obtenir_les_labels_communards(df)