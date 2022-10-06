#! /usr/bin/env python3
# coding: utf-8

import pytest
import pandas as pd
from app_communard.modele_analyse_df_communards import *

class Test_analyse_df_communards():
    @pytest.fixture()
    def df_de_test(self):
        data = {'communardLabel.value':['Louise Michel', 'Eugène Varlin', 'Valles'],
                    'occupation.value':['communard', 'communard', 'communard'],
                    'communard.type':['uri', 'uri', 'uri'],
                    'sexe_ou_genreLabel':['féminin', 'masculin', 'Na']
                    }
        df = pd.DataFrame(data)
        return df
    
    def test_recuperer_colonnes_voulues(self):
        df_test_reduit: pd.DataFrame = recuper_colonnes_voulues(df_de_test,'occupation')
        assert df_test_reduit.shape == (3,1)