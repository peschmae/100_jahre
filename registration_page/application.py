# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import Flask, render_template
from .config import configure_app


app = Flask(__name__)

configure_app(app)

@app.route("/")
def index():
    app.logger.debug('index called')
    # todo: fetch list of already commited meals
    return render_template('index.html')


@app.route("/registration-complete", methods=['POST'])
def registration():
    app.logger.debug('form posted')
    # todo: write all that shit into the database & maybe send an email
    return render_template('form.html')

