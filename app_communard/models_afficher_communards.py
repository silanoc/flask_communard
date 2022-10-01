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
df_communard: pd.DataFrame = extract.get_dataframe()


def obtenir_les_labels_communards(df: pd.DataFrame) -> list[str]:
    """labels = prénom/nom ou pseudo par lequel la personne est décrite dans wikidata.
    Mettre les labels dans un set pour récuper les labels uniques (doublons existants par exemple en cas de double prénom...), 
    puis dans une liste pour les ranger par ordre alphabétique

    :param pd.DataFrame df: le df avec tous les communard-e-s.
    :return list_personnage: liste de labels de communard-e-s unique par ordre alphabétique
    :rtype: list[str]
    """
    set_personne = set()
    serie_personne: pd.Series = df['communardLabel.value'].sort_values()
    for item in serie_personne:
        set_personne.add(item)
    list_personnage = list(set_personne)
    list_personnage.sort()
    logging.info("liste de labels prêtes")
    return list_personnage


def extraire_du_df_un_dict_pour_une_personne(individu: str, df: pd.DataFrame = df_communard) -> dict():
    """individu correspond à la personne recharché dans le df_communard.
    On extrait la ligne de la personne dans df2, puis on transforme ce df2 en dictionnaire.
    Il peut y avoir plusieurs ligne dans le df2, même pour une personne.

    :param str individu: le communard demandé
    :param pd.DataFrame df: le df d'où est extrait le personnage. Par défaut df_communard
    :return info_communard: dictionnaire avec totes les informations de la personne
    :rtype: dict
    """
    info_communard: dict[dict] = {}
    logging.debug(individu)
    df2: pd.DataFrame = df[df['communardLabel.value'].isin([individu])]
    logging.debug(df2)
    info_communard = df2.to_dict()
    logging.debug(info_communard)
    return info_communard


def trouver_id_communard(individu: str, dictionnaire) -> int:
    """chaque personne dans le dictionnaire posséde 1 ou plusieurs id. Il s'agit d'en extraire un.

    :param str individu: le communard demandé
    :param dict dictionnaire: le dictionnaire avec les informations du communard
    :return i_comm: l'identifiant de la personne
    :rtype str:
    """
    communard2 = dictionnaire['communard.type']
    logging.debug(communard2)
    id_comm = int(list(communard2.keys())[0])
    logging.debug(id_comm)
    return id_comm


# avoir une liste de communard-e-s, servant à afficher tous les noms sur la page personnages
liste_des_communards = obtenir_les_labels_communards(df_communard)