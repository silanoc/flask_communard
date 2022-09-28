#! /usr/bin/env python3
# coding: utf-8

import os
import logging
from flask import Flask, render_template, Blueprint

from .models import qui, obtenir_information

app = Flask(__name__)

@app.route('/')
@app.route('/index/')
@app.route('/accueil/')
def index():
    """Page d'accueil"""
    logging.debug("affiche la page d'accueil")
    return render_template('index.html')

@app.route('/personnages/')
def personnages():
    """Page avec la liste de tou-te-s les communard-e-s"""
    logging.debug("affiche la page avec tous les personnages")
    return render_template('personnages.html', qui = qui)

@app.route('/personnages/<communard>/')
def fiche(communard):
    """page affichant les informations pour al communard-e-s entrée en paramètre"""
    logging.debug("affiche la fiche d'un personnage")
    info = obtenir_information(communard)
    print("info", info)
    communard2 = info['communard.type']
    id_comm = int(list(communard2.keys())[0])
    print(id_comm)
    return render_template('fiche.html', communard = communard, info = info, id_comm = id_comm)

if __name__ == "__main__":
    app.run()