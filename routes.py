from flask import render_template
from helpers.twitter import open_stream, close_stream, get_random_trending
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
  return render_template('index.html', random_trending=get_random_trending())

def translate_track(track):
  if track:
    return track.lower().replace('#', '')
  else:
    return 'everything'

@socketio.on('openStream')
def handle_open_stream(data):
  track = translate_track(data['track'])
  join_room(track)
  open_stream(socketio, track)

@socketio.on('closeStream')
def handle_close_stream(data):
  track = translate_track(data['track'])
  leave_room(track)
  close_stream(track)
