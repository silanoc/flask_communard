#! /usr/bin/env python3
# coding: utf-8

import logging
import pandas as pd

logging.basicConfig(level=logging.DEBUG,
                    filename="./app_communard/logs/app.log",
                    filemode="w",
                    format='%(asctime)s - %(levelname)s - %(message)s')

class Analyse_df():
    def __init__(self, df: pd.DataFrame) -> None:
        self.df: pd.DataFrame = df
        
    def recuperer_colonnes_voulues(self, df: pd.DataFrame, *args) -> pd.DataFrame:
        """faire un data frame avec les colonnes voulues"""
        colonnes_voules: list = []
        for arg in args:
            colonnes_voules.append(arg)
        df_reduit: pd.DataFrame = df[colonnes_voules]
        return df_reduit
    
    def df_vers_serie(self, df: pd.DataFrame, colonne) -> pd.Series:
        """simple convertion"""
        return df[colonne]
    
    def serie_vers_dict(self, serie: pd.Series) -> dict:
        """simple convertion"""
        return serie.to_dict()
    

        