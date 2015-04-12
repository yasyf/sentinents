from flask import session, request, render_template, jsonify, g, redirect
from helpers.twitter import open_stream, close_stream
from flask.ext.socketio import join_room, leave_room
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
  join_room(room)
  open_stream(socketio, data['track'])
