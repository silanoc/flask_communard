#! /usr/bin/env python3
# coding: utf-8

from models_wikidata_vers_dataframe import *

results = get_results(endpoint_url, query)
df = creation_data_frame(results)

qui = obtenir_les_communards(df)
