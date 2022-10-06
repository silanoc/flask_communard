#! /usr/bin/env python3
# coding: utf-8

import pandas as pd
import pytest
from app_communard.models_afficher_communards import *

class Test:
    @pytest.fixture()
    def df_de_test(self):
        data = {'communardLabel.value':['Louise Michel', 'Eugène Varlin', 'Valles'],
                    'occupation.value':['communard', 'communard', 'communard'],
                    'communard.type':['uri', 'uri', 'uri']}
        df = pd.DataFrame(data)
        return df
        
    def test_obtenir_les_labels_communards(self, df_de_test):
        """création d'un dataframe simple. 
        Comme le dictionnaire renvoie dans un ordre aléatoire, mettre dans un set pour vérifier."""    
        liste_sortie = obtenir_les_labels_communards(df_de_test)
        assert set(liste_sortie) == set(['Louise Michel', 'Eugène Varlin', 'Valles'])
        
    def test_extraire_du_df_un_dict_pour_une_personne(self, df_de_test):
        dict_varlin = extraire_du_df_un_dict_pour_une_personne('Eugène Varlin', df_de_test)
        assert dict_varlin == {'communardLabel.value': {1: 'Eugène Varlin'}, 'occupation.value': {1: 'communard'}, 'communard.type': {1: 'uri'}}

    def test_trouver_id_communard(self, df_de_test):
        id_varlin = trouver_id_communard('Eugène Varlin', df_de_test)
        assert type(id_varlin) == int 
