from flask import session, request, render_template, jsonify, g, redirect
from helpers.twitter import open_stream, close_stream
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

@socketio.on('openStream')
def handle_open_stream(data):
  room = data['track'] or '!sample!'
  open_stream(socketio, data['track'])
