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
        
    def recuperer_colonnes_voulues(self, df: pd.DataFrame, *args):
        """faire un data frame avec les colonnes voulues"""
        colonnes_voules: list = []
        for arg in args:
            colonnes_voules.append(arg)
        df_reduit: pd.DataFrame = df[colonnes_voules]
        return df_reduit