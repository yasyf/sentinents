from flask import session, request, render_template, jsonify, g, redirect
from app import app, socketio

@app.before_request
def preprocess_request():
  pass

@app.after_request
def postprocess_request(response):
  return response

@app.route('/')
def index_view():
  return render_template('index.html')

@socketio.on('request')
def handle_request(json):
  print json
