#! /usr/bin/env python3
# coding: utf-8


from flask import Flask, render_template
import logging
from .models_afficher_communards import *
from .modele_analyse_df_communards import *

app = Flask(__name__)

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


@app.route('/presentation_methodologie/')
def presentation_methodologie():
    """Page presentation_methodologie"""
    logging.info("affiche la page de presentation_methodologie")
    return render_template('presentation_methodologie.html')

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


@app.route('/personnages/repartition_par_genre/')
def repartition_par_genre():
    titre, contexte, nombre, tableau, full_filename = analyse_repartition_par_genre()
    return render_template('analyse_personne.html', titre=titre, contexte=contexte, nombre=nombre, tableau=tableau, graph_genre=full_filename)


@app.route('/personnages/repartion_par_age/')
def repartition_par_age():
    analyse_repartition_par_date_de_naissance()
    return render_template('analyse_personne.html')


@app.route('/trouver_des_personnes/')
def trouver_des_personnes():
    """Page sur la méthodologie pour trouver les communard-e-s"""
    logging.info("affiche la page trouver des communard-e-s")
    return render_template('trouver_des_personnes.html')


@app.route('/cimetieres/')
def cimetieres():
    """Page sur les cimetieres"""
    logging.info("affiche la page cimetieres")
    return render_template('cimetieres.html')
    

if __name__ == "__main__":
    app.run()
