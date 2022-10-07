#! /usr/bin/env python3
# coding: utf-8

import os
from flask import Flask, render_template, Blueprint
import logging
from .models_afficher_communards import df_communard, liste_des_communards, extraire_du_df_un_dict_pour_une_personne, trouver_id_communard
from .modele_analyse_df_communards import Analyse_df

#FICHIER_IMAGE = os.path.join('.','app_communard','static', 'image')
#print(FICHIER_IMAGE)

UPLOAD_FOLDER = '/home/gabriel-le/Documents/flask_communard/app_communard/static/image/'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

logging.basicConfig(level=logging.DEBUG,
                    filename="./app_communard/logs/app.log",
                    filemode="w",
                    format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/')
@app.route('/index/')
@app.route('/accueil/')
def index():
    """Page d'accueil"""
    logging.info("affiche la page d'accueil")
    return render_template('index.html')


@app.route('/personnages/')
def personnages():
    """Page avec la liste de tou-te-s les communard-e-s"""
    logging.info("affiche la page avec le label de tous les communard-e-s")
    return render_template('personnages.html', qui=liste_des_communards)


@app.route('/personnages/<communard>/')
def fiche(communard):
    """page affichant les informations pour al communard-e-s entrée en paramètre"""
    info = extraire_du_df_un_dict_pour_une_personne(communard)
    id_comm = trouver_id_communard(communard, info)
    logging.info("affiche la fiche d'un personnage")
    logging.debug(communard)
    logging.debug(info)
    logging.debug(id_comm)
    return render_template('fiche.html', communard=communard, info=info, id_comm=id_comm)


@app.route('/personnages/repartition par genre/')
def repartion_par_genre():
    analyse_genre = Analyse_df(df_communard, 'sexe_ou_genreLabel.value')
    logging.debug(df_communard)
    logging.debug(analyse_genre.df_reduit)
    #logging.debug(df_communard.columns)
    dico_genre = analyse_genre.get_dictionnaire_stat('sexe_ou_genreLabel.value')
    df_genre = analyse_genre.get_df_pour_graph('sexe_ou_genreLabel.value', 'Genre', 'Nombre')
    graph_genre = analyse_genre.get_pie(df_genre, 'Genre', 'Nombre', 'Camemberg_genre')
    logging.debug(graph_genre)
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], graph_genre)
    #full_filename = '/home/gabriel-le/Documents/flask_communard/app_communard/static/image/' + graph_genre
    logging.error(full_filename)
    titre = ("Répartition par genre")
    contexte = ("""Dans wikidata, on peut remplir le 'sexe ou genre' (P21) pour les personnes. Certaines personnes peuvent ne pas avoir ce champs renseigné.
                    Voyons comment se répartissent selon leur genre les communard·e·s ayant une fiche dans wikidata.""")
    nombre = (f"Il y a {dico_genre['féminin']} femmes, {dico_genre['masculin']} hommes")
    tableau = df_genre.to_html()
    return render_template('analyse_personne.html', titre=titre, contexte=contexte, nombre=nombre, tableau=tableau, graph_genre=full_filename)

    


@app.route('/cimetieres/')
def cimetieres():
    """Page sur les cimetieres"""
    logging.info("affiche la page cimetieres")
    return render_template('cimetieres.html')
    

if __name__ == "__main__":
    app.run()
