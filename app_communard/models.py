#! /usr/bin/env python3
# coding: utf-8

import logging
from .models_wikidata_vers_dataframe import *

logging.basicConfig(level=logging.DEBUG,
                    filename="./app_communard/logs/app.log",
                    filemode="w",
                    format='%(asctime)s - %(levelname)s - %(message)s')

# extraction de la requete
extract = Extraction("app_communard/requetes/requete_nom_prenom_image_maiton.txt")
df: pd.DataFrame = extract.get_dataframe()
# avoir une liste de communard-e-s, servant à afficher tous les noms sur la page personnages
qui = obtenir_les_items_communards(df)
