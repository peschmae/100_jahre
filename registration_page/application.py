# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import Flask, render_template, request, redirect, url_for
from registration_page.config import configure_app
import pymysql.cursors


app = Flask(__name__)

configure_app(app)

@app.route("/")
def index():
    app.logger.debug('index called')
    # Connect to the database
    connection = pymysql.connect(host=app.config['DATABASE_SERVER'],
                                 user=app.config['DATABASE_USER'],
                                 password=app.config['DATABASE_PASSWORD'],
                                 db=app.config['DATABASE_NAME'],
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            # Read all records for people contributing to the buffet
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
    app.logger.debug('form posted')
    if request.form.get('captcha') != '0':
        app.logger.warning('welcome to my honeypot: {}'.format(request.form.get('name')))
        return redirect(url_for('index'))

    connection = pymysql.connect(host=app.config['DATABASE_SERVER'],
                                 user=app.config['DATABASE_USER'],
                                 password=app.config['DATABASE_PASSWORD'],
                                 db=app.config['DATABASE_NAME'],
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

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

        # connection is not autocommit by default. So you must commit to save your changes
        connection.commit()
    finally:
        connection.close()
    return render_template('registration.html')


@app.route("/list")
def list():
    app.logger.debug('list called')

    connection = pymysql.connect(host=app.config['DATABASE_SERVER'],
                                 user=app.config['DATABASE_USER'],
                                 password=app.config['DATABASE_PASSWORD'],
                                 db=app.config['DATABASE_NAME'],
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            # Read all records
            sql = "SELECT * FROM `registrations`"
            cursor.execute(sql)
            registrations = cursor.fetchall()

            # Calculate total number of registrations
            sql = "SELECT COUNT(name)+SUM(companions) as count FROM `registrations`"
            cursor.execute(sql)
            total = cursor.fetchone()
    finally:
        connection.close()
    return render_template('list.html',
                           registrations=registrations,
                           total=total
                           )
