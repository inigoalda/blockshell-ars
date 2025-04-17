# -*- coding: utf-8 -*-
# ==================================================
# ==================== META DATA ===================
# ==================================================
__author__ = "Daxeel Soni"
__url__ = "https://daxeel.github.io"
__email__ = "daxeelsoni44@gmail.com"
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Daxeel Soni"

# ==================================================
# ================= IMPORT MODULES =================
# ==================================================
from flask import Flask, render_template, jsonify
import json

# Init flask app
app = Flask(__name__)

@app.route('/')
def mined_blocks():
    """
        Endpoint to list all mined blocks.
    """
    f = open("chain.txt", "r")
    data = json.loads(f.read())
    f.close()
    return render_template('blocks.html', data=data)

import os
import base64
import requests

@app.route('/block/<hash>')
def block(hash):
    """
        Endpoint which shows all the data for given block hash.
    """
    f = open("chain.txt", "r")
    data = json.loads(f.read())
    f.close()
    for eachBlock in data:
        if eachBlock['hash'] == hash:

            data_json = eachBlock['data']
            uid_epita = data_json['uid_epita']
            email_epita = data_json['email_epita']
            nom = data_json['nom']
            prenom = data_json['prenom']
            image = data_json['image']
            if (image != ""):
                image_path = './static/' + uid_epita + '.png'
                with open(image_path, 'wb') as f:
                    f.write(base64.b64decode(image))
                image_path = "../static/" + uid_epita + ".png"
            else:
                image_path = 'https://upload.wikimedia.org/wikipedia/fr/d/d8/Epita.png'
                image = base64.b64encode(requests.get(image_path).content).decode('utf-8')

            return render_template('blockdata.html', rawdata=eachBlock, uid_epita=uid_epita, email_epita=email_epita, nom=nom, prenom=prenom, image=image, image_path=image_path)

# Run flask app
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
