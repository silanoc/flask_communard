#! /usr/bin/env python3
# coding: utf-8

import pandas as pd
from unittest.mock import patch, mock_open

from app_communard.models_wikidata_vers_dataframe import *

"""
https://stackoverflow.com/questions/1289894/how-do-i-mock-an-open-used-in-a-with-statement-using-the-mock-framework-in-pyth
@patch("builtins.open", new_callable=mock_open, read_data="data")
def test_patch(mock_file):
    assert open("path/to/open").read() == "data"
    mock_file.assert_called_with("path/to/open")
"""

def test_get_dataframe():
    """test approximatif"""
    extr_test = Extraction("app_communard/requetes/requete_nom_prenom_image_maiton.txt")
    retour = extr_test.get_dataframe()
    assert type(retour) == pd.DataFrame
