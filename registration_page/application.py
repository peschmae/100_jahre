# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import Flask, render_template, request
from .config import configure_app
import pymysql.cursors


app = Flask(__name__)

configure_app(app)

@app.route("/")
def index():
    # Connect to the database
    connection = pymysql.connect(host=app.config['DATABASE_SERVER'],
                                 user=app.config['DATABASE_USER'],
                                 password=app.config['DATABASE_PASSWORD'],
                                 db=app.config['DATABASE_NAME'],
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    app.logger.debug('index called')
    # todo: fetch list of already commited meals
    try:
        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT `buffet` FROM `registrations` WHERE `buffet`<>''"
            cursor.execute(sql)
            meals = cursor.fetchall()
    finally:
        connection.close()
    return render_template('index.html',
                           meals=meals
                           )


@app.route("/registration-complete", methods=['POST'])
def registration():
    # Connect to the database
    connection = pymysql.connect(host=app.config['DATABASE_SERVER'],
                                 user=app.config['DATABASE_USER'],
                                 password=app.config['DATABASE_PASSWORD'],
                                 db=app.config['DATABASE_NAME'],
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    app.logger.debug('form posted')
    # todo: write all that shit into the database & maybe send an email
    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `registrations` (`name`, `companions`, `buffet`, `vegetarian`) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (
                                 request.form.get('name'),
                                 request.form.get('companions', default=0),
                                 request.form.get('buffet'),
                                 request.form.get('vegetarian', default=0),
                                )
                           )

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()
    finally:
        connection.close()
    return render_template('registration.html')


@app.route("/list")
def list():
    # Connect to the database
    connection = pymysql.connect(host=app.config['DATABASE_SERVER'],
                                 user=app.config['DATABASE_USER'],
                                 password=app.config['DATABASE_PASSWORD'],
                                 db=app.config['DATABASE_NAME'],
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    app.logger.debug('list called')
    # todo: fetch list of already commited meals
    try:
        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT * FROM `registrations`"
            cursor.execute(sql)
            registrations = cursor.fetchall()

            sql = "SELECT COUNT(name)+SUM(companions) as count FROM `registrations`"
            cursor.execute(sql)
            total = cursor.fetchone()
    finally:
        connection.close()
    return render_template('list.html',
                           registrations=registrations,
                           total=total
                           )