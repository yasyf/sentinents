#!/bin/bash

if [ "$DEV" == "true" ]
then
  python app.py
else
  gunicorn --worker-class eventlet -w 1 -b "0.0.0.0:$PORT" app:app
fi
