#! /usr/bin/env python3
# coding: utf-8

from encodings import utf_8
import logging
import os
import sys
import pathlib
import pandas as pd
from SPARQLWrapper import SPARQLWrapper, JSON
from typing import NewType

struct_json = NewType('struct_json', dict)


class Extraction():
    """Objet pour récupérer sur wikidata des données via query service, via une requete en SPARQL.
    Les requêtes sont écrites dans un fichier texte dans la dossier requêtes.
    La première chose faite est de vérifier que le chemin existe.
    C'est un fichier json qui est généré.
    Il est transformé en un dataframe.
    Seul ce dataframe est communiqué en dehors de la classe, tout le reste est privé/interne.
    Attention : La requête étant écrite à la base dans query service, elle est réputé être bonne.

    :param pathlib.Path chemin: le chemin où est le fichier texte à traiter.
    """

    def __init__(self, chemin: pathlib.Path) -> None:
        if os.path.exists("app_communard/requetes/requete_nom_prenom_image_maiton.txt"):
            self.query: str = self._ouvrir_fichier_requete(chemin)
        else:
            logging.error("le chemin du fichier de requete n'existe pas")
        logging.info("initialisation class Extraction ok")

    def _ouvrir_fichier_requete(self, chemin: pathlib.Path) -> str:
        """transforme le contenu du fichier texte, 
        contenant une requete à faire dans queryservice,
        dans une chaine de caractère

        :param pathlib.Path chemin: le chemin du fichier à ouvrir.
        :return requete: le texte du fichier qui correspond à la requête SPARQL
        :rtype: str
        """
        try:
            fichier = open(chemin, "r", encoding="utf8")
            logging.info("ouverture du fichier de requete")
        except:
            logging.error("echec d'ouverture du fichier de requete")
        try:
            requete: str = fichier.read()
            logging.info(
                "lecture du fichier de requete, le mettre dans une variable")
        except:
            logging.error("echec de la lecture du fichier de requete")
        return requete

    def _get_results(self, query) -> struct_json:
        """code copier/coller de queryservice https://query.wikidata.org > code > Python"""
        endpoint_url: str = "https://query.wikidata.org/sparql"
        user_agent = "WDQS-example Python/%s.%s" % (
            sys.version_info[0], sys.version_info[1])
        sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        logging.debug("conversion du résultat de la requete en JSON - ok")
        return sparql.query().convert()

    def _convertion_json_en_data_frame(self, resultat_enjson: struct_json) -> pd.DataFrame:
        """convertie la structure json en dataframe

        :param struct_json resultat_enjson: la structure json issus de la requete
        :return df: le data frame contenant les informations souhaitées
        :rtype: pd.DataFrame
        """
        try:
            df: pd.DataFrame = pd.json_normalize(
                resultat_enjson["results"]["bindings"])
            logging.debug("les colonnes du df", df.columns)
            logging.debug(df)
            logging.info("conversion du résultat du JSON en data frame - ok")
        except:
            logging.error("echec de la convertion du Json en dataFrame")
        return df

    def _de_la_requete_au_df(self) -> pd.DataFrame:
        """enchaine les méthodes get_results et convertion_json_en_data_frame

        :return df: le df complet, pret à etre utilisé
        :rtype: pd.DataFrame
        """
        results = self._get_results(self.query)
        df: pd.DataFrame = self._convertion_json_en_data_frame(results)
        return df

    def get_dataframe(self) -> pd.DataFrame:
        """méthode publique pour transmettre le df ayant toutes les données de la requête

        :return df: le df complet, pret à etre utilisé
        :rtype: pd.DataFrame
        """
        logging.info("get_dataframe - ok")
        return self._de_la_requete_au_df()


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


if __name__ == "__main__":

    extract = Extraction(
        "app_communard/requetes/requete_nom_prenom_image_maiton.txt")
    df = extract.get_dataframe()

    qui = obtenir_les_labels_communards(df)
    logging.debug(qui)
    logging.debug(len(qui))