from flask import Flask, render_template, request, session, request, jsonify, make_response, redirect
from flask.ext.sqlalchemy import SQLAlchemy
from gevent.wsgi import WSGIServer
import os, random, datetime, requests
from support import *


app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = 'SECRET YO'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql:///mindpalacedb')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
db.session.autoflush = False

import db_api

@app.route('/')
def app_index_page():
	if not session.get('username'):
		return redirect('/login')
	return render_template('index.html')

@app.route('/login', methods=['GET'])
def app_login():
	if session.get('username'):
		return redirect('/')
	return render_template('login.html')

@app.route('/login/submit', methods=['POST'])
def app_login_submit():
	username = request.form.get('username')
	password = request.form.get('password')
	return jsonify(success=db_api.handle_user_login(username, password, session))

@app.route('/logout', methods=['GET'])
def app_logout():
	session.clear()
	return redirect('/login')

@app.route('/add', methods=['POST'])
def app_add_url():
	url = request.form.get('url')
	owner_id = session.get('user_id')
	if not owner_id:
		return jsonify(success=False)
	return jsonify(db_api.add_url(owner_id, url))

@app.route('/fetch/urls', methods=['GET'])
def app_fetch_urls():
	owner_id = session.get('user_id')
	if not owner_id:
		return get_json_response([])
	return get_json_response(db_api.fetch_urls(owner_id))

@app.route('/fetch/cors', methods=['GET'])
def app_fetch_cors():
	url = request.args.get('url')
	return requests.get(url).content

@app.route('/pop', methods=['POST'])
def app_pop_url():
	url_id = request.form.get('url_id')
	return jsonify(success=db_api.pop_url(url_id))