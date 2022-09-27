#! /usr/bin/env python3
# coding: utf-8
import os
from flask import Flask, render_template, Blueprint

from models import qui



app = Flask(__name__)

@app.route('/')
@app.route('/index/')
@app.route('/acceuil/')
def index() ->None:
    return render_template('index.html')

@app.route('/personnages/')
def personnages() ->None:
    return render_template('personnages.html', qui = qui)

@app.route('/personnages/<communard>/')
def fiche(communard) ->None:
    return render_template('fiche.html', communard = communard)

if __name__ == "__main__":
    app.run()