#! /usr/bin/env python3
# coding: utf-8

import logging
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

logging.basicConfig(level=logging.DEBUG,
                    filename="./app_communard/logs/app.log",
                    filemode="w",
                    format='%(asctime)s - %(levelname)s - %(message)s')

class Analyse_df():
    def __init__(self, df: pd.DataFrame, *args) -> None:
        self.df: pd.DataFrame = df
        self.df_reduit = self._recuperer_colonnes_voulues(self.df, *args)
        
    def _recuperer_colonnes_voulues(self, df: pd.DataFrame, *args) -> pd.DataFrame:
        """faire un data frame avec les colonnes voulues"""
        colonnes_voules: list = []
        for arg in args:
            colonnes_voules.append(arg)
        df_reduit: pd.DataFrame = df[colonnes_voules]
        return df_reduit
    
    def _df_vers_compte_de_serie(self, df: pd.DataFrame, colonne) -> pd.Series:
        """double convertion. df vers series, puis compter les valeurs de series"""
        sortie = df[colonne].value_counts()
        return sortie
    
    def _serie_vers_dict(self, serie: pd.Series) -> dict:
        """simple convertion"""
        return serie.to_dict()
    
    def _serie_vers_df_renome(self, serie: pd.Series, colonne_index: str, colonne_valeur:str) -> pd.DataFrame:
        df_sortie:pd.DataFrame = serie.to_frame()
        df_sortie.reset_index(inplace = True)
        df_sortie.columns = [colonne_index,colonne_valeur]
        return df_sortie
    
    def get_dictionnaire_stat(self, colonne) -> dict:
        """dans le df, pour une colonne donnée, sort un dictionnaire avec le nombre de valeur par entrée"""
        dict_sortie: dict = self._serie_vers_dict(self._df_vers_compte_de_serie(self.df_reduit, colonne))
        return dict_sortie
    
    def get_df_pour_graph(self, colonne, colonne_index: str, colonne_valeur:str) -> pd.DataFrame:
        serie_int = self._df_vers_compte_de_serie(self.df_reduit, colonne)
        df_sortie = self._serie_vers_df_renome(serie_int, colonne_index, colonne_valeur)
        return df_sortie
    
    def get_pie(self, df, colonne_index, colonne_valeur, nom_graphique) -> str:
        colors = sns.color_palette('deep')[0:4:3]
        labels = df[colonne_index].values   #["masculin", "féminin"]
        plt.pie(data = df, x = df[colonne_valeur], labels = labels, colors = colors, autopct='%.0f%%')
        nom_graphique = f"{nom_graphique}.jpg"
        chemin_graphique = "/home/gabriel-le/Documents/flask_communard/app_communard/static/image/" + nom_graphique
        plt.savefig(chemin_graphique)
        #plt.show()
        plt.close()
        return nom_graphique
        
                                            
        

    

        