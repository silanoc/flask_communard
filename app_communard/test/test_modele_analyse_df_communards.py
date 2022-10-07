#! /usr/bin/env python3
# coding: utf-8

import pytest
import pandas as pd
from app_communard.modele_analyse_df_communards import *

class Test_analyse_df_communards():
    @pytest.fixture()
    def df_de_test(self):
        """un df pour faire les tests"""
        data = {'communardLabel.value':['Louise Michel', 'Eugène Varlin', 'Valles', 'Nathalie Lemel'],
                'occupation.value':['communard', 'communard', 'communard', 'communard'],
                'communard.type':['uri', 'uri', 'uri', 'uri'],
                'sexe_ou_genreLabel':['féminin', 'masculin', 'Na', 'féminin']}
        df = pd.DataFrame(data)
        return df
    
    @pytest.fixture()
    def serie_de_test(self):
        data = {'féminin': 2, 'masculin': 1, 'Na': 1}
        serie = pd.Series(data=data, index=['féminin', 'masculin', 'Na'])
        return serie

    def test_recuperer_colonnes_voulues(self, df_de_test):
        """on fait deux dataFrame avec des sélection de colonens différents. 
        On vérifie le type et shape"""
        analyse = Analyse_df(df_de_test)
        #--
        df_test_reduit: pd.DataFrame = analyse.recuperer_colonnes_voulues(df_de_test, 'communardLabel.value','occupation.value')
        assert type(df_test_reduit) == pd.DataFrame
        assert df_test_reduit.shape == (4, 2)
        #--
        df_test_reduit: pd.DataFrame = analyse.recuperer_colonnes_voulues(df_de_test, 'communardLabel.value')
        assert type(df_test_reduit) == pd.DataFrame
        assert df_test_reduit.shape == (4, 1)
    
    def test_df_vers_serie(self, df_de_test):
        analyse = Analyse_df(df_de_test)
        serie: pd.Series = analyse.df_vers_serie(df_de_test, 'sexe_ou_genreLabel')
        assert type(serie) == pd.Series
        assert serie.shape == (4,)
        
    def test_serie_vers_dict(self, df_de_test, serie_de_test):
        analyse = Analyse_df(df_de_test)
        sortie = analyse.serie_vers_dict(serie_de_test)
        assert type(sortie) == dict
        assert sortie == {'féminin': 2, 'masculin': 1, 'Na': 1}
        
    def test_serie_vers_df(self, df_de_test, serie_de_test: pd.Series):
        analyse = Analyse_df(df_de_test)
        df_sortie: pd.DataFrame = analyse.serie_vers_df(serie_de_test, 'sexe_ou_genreLabel', 'nombre')
        assert df_sortie.shape[0] == serie_de_test.shape[0]
        assert type(df_sortie) == pd.DataFrame
        
        