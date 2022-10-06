#! /usr/bin/env python3
# coding: utf-8

from flask import Flask, render_template, Blueprint
import logging
from .models_afficher_communards import liste_des_communards, extraire_du_df_un_dict_pour_une_personne, trouver_id_communard
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


@app.route('/cimetieres/')
def cimetieres():
    """Page sur les cimetieres"""
    logging.info("affiche la page cimetieres")
    return render_template('cimetieres.html')
    

if __name__ == "__main__":
    app.run()
