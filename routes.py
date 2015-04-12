from flask import render_template
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
  join_room(data['track'])
  open_stream(socketio, data['track'])

@socketio.on('closeStream')
def handle_close_stream(data):
  leave_room(data['track'])
  close_stream(data['track'])
