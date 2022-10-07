#! /usr/bin/env python3
# coding: utf-8

import logging
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

from .models_afficher_communards import df_communard

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
        
                                            
def analyse_repartition_par_genre():
    analyse_genre = Analyse_df(df_communard, 'sexe_ou_genreLabel.value')
    dico_genre = analyse_genre.get_dictionnaire_stat('sexe_ou_genreLabel.value')
    df_genre = analyse_genre.get_df_pour_graph('sexe_ou_genreLabel.value', 'Genre', 'Nombre')
    graph_genre = analyse_genre.get_pie(df_genre, 'Genre', 'Nombre', 'Camemberg_genre')
    #logging.debug(graph_genre)
    #full_filename = os.path.join(app.config['UPLOAD_FOLDER'], graph_genre)
    full_filename = '/home/gabriel-le/Documents/flask_communard/app_communard/static/image/' + graph_genre
    #logging.error(full_filename)
    titre = ("Répartition par genre")
    contexte = ("""Dans wikidata, on peut remplir le 'sexe ou genre' (P21) pour les personnes. Certaines personnes peuvent ne pas avoir ce champs renseigné.
                    Voyons comment se répartissent selon leur genre les communard·e·s ayant une fiche dans wikidata.""")
    nombre = (f"Il y a {dico_genre['féminin']} femmes, {dico_genre['masculin']} hommes")
    tableau = df_genre.to_html()
    return titre, contexte, nombre, tableau, full_filename    


def compter_liste_dans_dict(liste: list) -> dict:
    dictionnaire = {}
    for item in liste:
        if item in dictionnaire :
            dictionnaire[item] += 1
        else:
            dictionnaire[item] = 1
    return dictionnaire


def analyse_repartition_par_date_de_naissance():
    analyse_date = Analyse_df(df_communard, 'date_de_naissance.value')
    #--
    liste_date_entiere = analyse_date.df_reduit['date_de_naissance.value'].values
    logging.debug(liste_date_entiere)    
    #--
    liste_annee = []
    liste_age = []
    debut_commune = datetime(1871, 3, 18)
    for date_naissance in liste_date_entiere:
        try:
            liste_annee.append(datetime.fromisoformat(date_naissance[:-1]).year)
            age = debut_commune - datetime.fromisoformat(date_naissance[:-1])
            liste_age.append(int(age.days // 365.25))
        except:
            logging.warning("format de date non exploitable")
    logging.debug(liste_annee)
    logging.debug(liste_age)
    dico_annee = compter_liste_dans_dict(liste_annee)
    dico_age = compter_liste_dans_dict(liste_age)
    logging.debug(dico_annee)
    logging.debug(dico_age)
    #--
    plt.hist(liste_annee)
    plt.show()
    #sns.histplot(data=dico_annee, x=dico_annee.keys, y = dico_annee.values)
    sns.histplot(data=liste_annee)
    plt.show()
    sns.boxplot(data=liste_age)
    plt.show()        