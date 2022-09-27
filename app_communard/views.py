#! /usr/bin/env python3
# coding: utf-8
import os
from flask import Flask, render_template, Blueprint



app = Flask(__name__)

@app.route('/')
@app.route('/index/')
@app.route('/acceuil/')
def index() ->None:
    return render_template('index.html')

@app.route('/personnages/')
def personnages() ->None:
    return render_template('personnages.html')

if __name__ == "__main__":
    app.run()