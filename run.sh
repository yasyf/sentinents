#!/bin/bash

if [ "$DEV" == "true" ]
then
  python app.py
else
  gunicorn --worker-class socketio.sgunicorn.GeventSocketIOWorker -b "0.0.0.0:$PORT" app:app
fi
